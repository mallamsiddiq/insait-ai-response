# project_structure
# ├── app/
# │   ├── __init__.py
# │   ├── models.py
# │   ├── routes.py
# │   ├── auth.py
# │   ├── config.py
# │   ├── openai_service.py
# ├── run.py
# ├── Dockerfile
# ├── docker-compose.yml
# ├── requirements.txt

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    from .routes import main
    from .auth import auth
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    return app

# app/config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@db:5432/ai_text_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'supersecretkey'
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# app/models.py
from . import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class GeneratedText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# app/auth.py
from flask import Blueprint, request, jsonify
from .models import User
from . import db, bcrypt
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], password=bcrypt.generate_password(data['password']).decode('utf-8'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# app/openai_service.py
import openai
from .config import Config

openai.api_key = Config.OPENAI_API_KEY

def generate_openai_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100
    )
    return response['choices'][0]['text'].strip()

# app/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import GeneratedText
from . import db
from .openai_service import generate_openai_response

main = Blueprint('main', __name__)

@main.route('/generate-text', methods=['POST'])
@jwt_required()
def generate_text():
    data = request.json
    user_id = get_jwt_identity()
    text_response = generate_openai_response(data['prompt'])
    generated_text = GeneratedText(user_id=user_id, prompt=data['prompt'], response=text_response)
    db.session.add(generated_text)
    db.session.commit()
    return jsonify({'id': generated_text.id, 'response': text_response})

@main.route('/generated-text/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_generated_text(id):
    user_id = get_jwt_identity()
    text = GeneratedText.query.filter_by(id=id, user_id=user_id).first()
    if not text:
        return jsonify({'message': 'Not found'}), 404
    
    if request.method == 'GET':
        return jsonify({'id': text.id, 'prompt': text.prompt, 'response': text.response})
    elif request.method == 'PUT':
        data = request.json
        text.response = data.get('response', text.response)
        db.session.commit()
        return jsonify({'message': 'Updated successfully'})
    elif request.method == 'DELETE':
        db.session.delete(text)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'})

# run.py
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
