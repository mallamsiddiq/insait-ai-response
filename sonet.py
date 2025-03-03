# app/schemas.py
from flask_marshmallow import Marshmallow
from .models import User, GeneratedText

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class GeneratedTextSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GeneratedText
        load_instance = True



# app/resources.py
from flask_smorest import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, GeneratedText
from .schemas import UserSchema, GeneratedTextSchema
from . import db

blp = Blueprint('api', __name__, url_prefix='/api')

@blp.route('/users', methods=['GET', 'POST'])
class UserResource:
    @blp.response(UserSchema(many=True))
    def get(self):
        return User.query.all()

    @blp.arguments(UserSchema)
    @blp.response(UserSchema, code=201)
    def post(self, new_user):
        user = User(username=new_user['username'], password=new_user['password'])
        db.session.add(user)
        db.session.commit()
        return user

@blp.route('/generated-text', methods=['GET', 'POST'])
class GeneratedTextResource:
    @blp.response(GeneratedTextSchema(many=True))
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return GeneratedText.query.filter_by(user_id=user_id).all()

    @blp.arguments(GeneratedTextSchema)
    @blp.response(GeneratedTextSchema, code=201)
    @jwt_required()
    def post(self, new_generated_text):
        user_id = get_jwt_identity()
        generated_text = GeneratedText(
            user_id=user_id, prompt=new_generated_text['prompt'], response=new_generated_text['response']
        )
        db.session.add(generated_text)
        db.session.commit()
        return generated_text
