from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity

from app.models import GeneratedText
from app.resources.schemas import GeneratedTextSchema
from app.services.openai_service import generate_openai_response
from app.services.auth import login_required
from app import db
    

generated_text_blue_print = Blueprint('Generated Text', 'Routes for Generated Text', url_prefix='/api')

# Generated Text Resource
@generated_text_blue_print.route('/generated-text')
class GeneratedTextResource(MethodView):
    
    @generated_text_blue_print.response(200, GeneratedTextSchema(many=True))
    @login_required
    def get(self):
        """Fetch all generated texts for the current user"""
        user_id = get_jwt_identity()
        return GeneratedText.query.filter_by(user_id=user_id).all()

    
    @generated_text_blue_print.response(201, GeneratedTextSchema)
    @generated_text_blue_print.arguments(GeneratedTextSchema)
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
@generated_text_blue_print.route('/generated-text/<int:id>')
class GeneratedTextItemResource(MethodView):
    
    @generated_text_blue_print.response(200, GeneratedTextSchema)
    @login_required
    def get(self, id):
        """Fetch a generated text by ID"""
        user_id = get_jwt_identity()
        text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()

        if not text:
            abort(404, "Not found")
        return text

    @generated_text_blue_print.arguments(GeneratedTextSchema)
    @generated_text_blue_print.response(200, GeneratedTextSchema)
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

    @generated_text_blue_print.response(204)
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
