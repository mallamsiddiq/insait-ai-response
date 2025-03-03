# from flask_restx import Resource
# from flask import request
# from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
# from werkzeug.security import generate_password_hash, check_password_hash


# from app.models import User, GeneratedText
# from app.resources.schemas import (namespace, generated_text_schema, generated_text_response_schema,
#                                    user_schema, register_schema)
# from app.services.openai_service import generate_openai_response
# from app import db, bcrypt, api

# from app.resources.schemas import UserSchema


# # from app.services.token_services import create_access_token

# # User Resource
# @namespace.route('/users')
# class UserResource(Resource):

#     @namespace.marshal_with(UserSchema(many=True), as_list=True)
#     def get(self):
#         """Fetch all users"""
#         return User.query.all()

#     @namespace.expect(register_schema)
#     @namespace.marshal_with(user_schema)
#     def post(self):
#         """Create a new user"""
#         new_user = request.json
#         if User.query.filter_by(username=new_user['username']).first():
#             api.abort(409, "Username already exists")

#         try:
            
#             user = User(**new_user)
#             db.session.add(user)
#             db.session.commit()
#             return user, 201
#         except Exception as e:
#             db.session.rollback()
#             api.abort(500, f"Error creating user: {str(e)}")

# # Login Resource
# @namespace.route('/login')
# class LoginResource(Resource):
#     @namespace.expect(register_schema)
#     def post(self):
#         """Login a user and return JWT"""
#         login_data = request.json
#         user = User.query.filter_by(username=login_data['username']).first()

#         if not user:
#             api.abort(401, "User not found")
        
#         if not user.check_password(login_data['password']):
#             api.abort(401, "Invalid credentials")

#         # Generate JWT token
#         token = create_access_token(identity=user.id)
#         return {"access_token": token}, 200
    

# # Generated Text resource
# @namespace.route('/generated-text')
# class GeneratedTextResource(Resource):
    
#     @namespace.marshal_with(generated_text_response_schema, as_list=True)
#     @jwt_required()
#     def get(self):
#         """Fetch all generated texts for the current user"""
#         user_id = get_jwt_identity()
#         return GeneratedText.query.filter_by(user_id=user_id).all()

#     @namespace.expect(generated_text_schema)
#     @namespace.marshal_with(generated_text_response_schema)
#     @jwt_required()
#     def post(self):
#         """Generate and store new text"""
#         user_id = get_jwt_identity()
#         new_generated_text = request.json
        
#         generated_text = GeneratedText(
#             user_id=user_id, 
#             prompt=new_generated_text['prompt'], 
#             response=generate_openai_response(new_generated_text['prompt'])  # Call OpenAI
#         )
#         db.session.add(generated_text)
#         db.session.commit()
#         return generated_text, 201

# # Generated Text Item resource (for individual generated text actions)
# @namespace.route('/generated-text/<int:id>')
# class GeneratedTextItemResource(Resource):
#     @namespace.marshal_with(generated_text_response_schema)
#     @jwt_required()
#     def get(self, id):
#         """Fetch a generated text by ID"""
#         user_id = get_jwt_identity()
#         text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()
#         if not text:
#             api.abort(404, "Not found")
#         return text

#     @namespace.expect(generated_text_schema)
#     @namespace.marshal_with(generated_text_response_schema)
#     @jwt_required()
#     def put(self, id):
#         """Update a generated text by ID"""
#         user_id = get_jwt_identity()
#         text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()
#         if not text:
#             api.abort(404, "Not found")

#         print("request.json: ", request.json)
        
        
#         text.prompt = (new_prompt:= request.json['prompt'])
#         text.response = generate_openai_response(new_prompt)
#         db.session.commit()
#         return text

#     @jwt_required()
#     def delete(self, id):
#         """Delete a generated text by ID"""
#         user_id = get_jwt_identity()
#         text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()
#         if not text:
#             api.abort(404, "Not found")
#         db.session.delete(text)
#         db.session.commit()
#         return '', 204
    

# api.add_namespace(namespace)

# # Add the Namespace to the API
# # Assuming you have an `api` object in your `app.py`
# # api.add_namespace(api)

