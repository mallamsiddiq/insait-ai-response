from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, create_access_token

from app.models import User, GeneratedText
from app.resources.schemas import UserSchema, GeneratedTextSchema
from app.services.openai_service import generate_openai_response
from app.services.auth import login_required
from app import db
    


blue_print = Blueprint('generated_text', 'generated_text', url_prefix='/api')

# User Resource
@blue_print.route('/users')
class UserResource(MethodView):
    
    @blue_print.response(200, UserSchema(many=True))
    @login_required
    def get(self, args = None):
        """Fetch all users"""
        return User.query.all()

    @blue_print.response(201, UserSchema)
    @blue_print.arguments(UserSchema)
    def post(self, new_user):
        """Create a new user"""
        
        if User.query.filter_by(username=new_user['username']).first():
            abort(409, message = "Username already exists")

        try:
            user = User(**new_user)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            abort(500, message = f"Error creating user: {str(e)}")


# Login Resource
@blue_print.route('/login')
class LoginResource(MethodView):
    
    @blue_print.response(200)
    @blue_print.arguments(UserSchema)
    def post(self, login_data):
        """Login a user and return JWT"""
        
        user = User.query.filter_by(username=login_data['username']).first()

        if not user:
            abort(401, message = "User not found")
        
        if not user.check_password(login_data['password']):
            abort(401, message = "Invalid credentials")

        # Generate JWT token
        token = create_access_token(identity=user.id)
        return {"access_token": token}, 200
    

# Generated Text Resource
@blue_print.route('/generated-text')
class GeneratedTextResource(MethodView):
    
    @blue_print.response(200, GeneratedTextSchema(many=True))
    @login_required
    def get(self):
        """Fetch all generated texts for the current user"""
        user_id = get_jwt_identity()
        return GeneratedText.query.filter_by(user_id=user_id).all()

    
    @blue_print.response(201, GeneratedTextSchema)
    @blue_print.arguments(GeneratedTextSchema)
    @login_required
    def post(self, new_generated_text):
        """Generate and store new text"""
        user_id = get_jwt_identity()
        
        generated_text = GeneratedText(
            user_id=user_id, 
            prompt=new_generated_text['prompt'], 
            response=generate_openai_response(new_generated_text['prompt'])  # Call OpenAI
        )
        db.session.add(generated_text)
        db.session.commit()
        return generated_text


# Generated Text Item Resource (for individual generated text actions)
@blue_print.route('/generated-text/<int:id>')
class GeneratedTextItemResource(MethodView):
    
    @blue_print.response(200, GeneratedTextSchema)
    @login_required
    def get(self, id):
        """Fetch a generated text by ID"""
        user_id = get_jwt_identity()
        text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()

        if not text:
            abort(404, "Not found")
        return text

    @blue_print.arguments(GeneratedTextSchema)
    @blue_print.response(200, GeneratedTextSchema)
    @login_required
    def put(self, new_data, id):
        """Update a generated text by ID"""
        user_id = get_jwt_identity()
        text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()
        if not text:
            abort(404, "Not found")

        new_prompt = new_data['prompt']
        
        text.prompt = new_prompt
        text.response = generate_openai_response(new_prompt)
        db.session.commit()
        return text

    @blue_print.response(204)
    @login_required
    def delete(self, id):
        """Delete a generated text by ID"""
        user_id = get_jwt_identity()
        text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()
        if not text:
            abort(404, "Not found")
        db.session.delete(text)
        db.session.commit()
        return '', 204
