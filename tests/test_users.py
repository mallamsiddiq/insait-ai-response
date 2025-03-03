 
import pytest
from flask_jwt_extended import decode_token
from flask import current_app


def test_get_users(client, auth_header):
    response = client.get('/api/users', headers=auth_header)
    assert response.status_code == 200
    assert len(response.json) > 0


def test_create_user(client):
    new_user = {
        'username': 'newuser',
        'password': 'newpassword'
    }
    response = client.post('/api/users', json=new_user)
    assert response.status_code == 201
    assert response.json['username'] == new_user['username']


def test_user_creation_conflict(client):
    # Creating a user with an existing username should return 409 conflict
    existing_user = {'username': 'testuser', 'password': 'password'}
    client.post('/api/users', json=existing_user)
    response = client.post('/api/users', json=existing_user)
    
    
    assert response.status_code == 409
    assert response.json['message'] == 'Username already exists'


def test_login_success(client, valid_user, user_with_generated_text):
    """Test successful login."""
    response = client.post('/api/login', json=valid_user)
    
    assert response.status_code == 200  # Expecting HTTP 200 OK
    assert 'access_token' in response.json  # Ensure that a token is returned in the response
    token = response.json['access_token']
    assert token is not None
    decoded_token = decode_token(token)
    
    identity = current_app.config['JWT_IDENTITY_CLAIM']
    assert identity in decoded_token
    assert decoded_token[identity] == user_with_generated_text[0].id


def test_login_invalid_credentials(client, valid_user, user_with_generated_text):
    """Test unsuccessful login due to wrong credentials."""
    invalid_username = {'username': 'wronguser', 'password': valid_user['password']}
    response = client.post('/api/login', json=invalid_username)
    assert response.status_code == 401  # Expecting HTTP 401 Unauthorized
    assert response.json['message'] == "User not found"
    
    invalid_password = {'username': valid_user['username'], 'password': 'wrongpassword'}
    response = client.post('/api/login', json=invalid_password)
    assert response.status_code == 401  # Expecting HTTP 401 Unauthorized
    assert response.json['message'] == "Invalid credentials"