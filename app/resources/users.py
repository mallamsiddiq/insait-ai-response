from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token

from app.models import User
from app.resources.schemas import UserSchema
from app.services.auth import login_required
from app import db
    

users_blue_print = Blueprint('Users', 'Routes for Users', url_prefix='/api')

# User Resource
@users_blue_print.route('/users')
class UserResource(MethodView):
    
    @users_blue_print.response(200, UserSchema(many=True))
    @login_required
    def get(self, args = None):
        """Fetch all users"""
        return User.query.all()

    @users_blue_print.response(201, UserSchema)
    @users_blue_print.arguments(UserSchema)
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
@users_blue_print.route('/login')
class LoginResource(MethodView):
    
    @users_blue_print.response(200)
    @users_blue_print.arguments(UserSchema)
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
    
