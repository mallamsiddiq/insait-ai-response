 
import pytest, os
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models import User, GeneratedText
from .config import TestConfig



@pytest.fixture
def app():
    
    app = create_app(TestConfig)
    
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for tests
    # app.config['JWT_SECRET_KEY'] = 'secret'  # Secret for JWT token
    with app.app_context():
        db.create_all()  # Create the database tables
        yield app
        db.drop_all()  # Clean up after tests


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def new_generated_text():
    return {
        'prompt': "Hello, World!"
    }


valid_user_data = {
    "username": "testuser",
    "password": "testpassword"
}

valid_user_data_2 = {
    "username": "testuser2",
    "password": "testpassword2"
}


invalid_user_data = {
    "username": "wronguser",
    "password": "wrongpassword"
}

@pytest.fixture
def valid_user():
    return valid_user_data

@pytest.fixture
def valid_user_2():
    return valid_user_data_2


@pytest.fixture
def invalid_user():
    return invalid_user_data


@pytest.fixture
def auth_header():
    # Create a JWT token for an authenticated user
    user = db.session.query(User).filter_by(username=valid_user_data["username"]).first()
    if not user:
        user = User(**valid_user_data)
        db.session.add(user)
        db.session.commit()
        
    
    # Generate JWT token for this user
    access_token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def auth_header_2():
    # Create a JWT token for an authenticated user

    user = db.session.query(User).filter_by(username=valid_user_data_2["username"]).first()
    if not user:
        user = User(**valid_user_data_2)
        db.session.add(user)
        db.session.commit()
        
    
    # Generate JWT token for this user
    access_token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def invalid_auth_header():
    
    # Generate Random Jwt token for non user
    access_token = create_access_token(identity='invalid_user_id')
    return {'Authorization': f'Bearer {access_token}'}




@pytest.fixture
def user_with_generated_text():
    
    user = db.session.query(User).filter_by(username=valid_user_data["username"]).first()
    if not user:
        user = User(**valid_user_data)
        db.session.add(user)
        db.session.commit()
    
    generated_text = GeneratedText(
        user_id=user.id,
        prompt="Test Prompt",
        response="Generated response"
    )
    db.session.add(generated_text)
    db.session.commit()

    return user, generated_text


@pytest.fixture
def user_without_generated_text(valid_user_2):
    user = db.session.query(User).filter_by(username=valid_user_2["username"]).first()
    if not user:
        user = User(**valid_user_2)
        db.session.add(user)
        db.session.commit()
    return user, None







