import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.openai_service import generate_openai_response, random_texts


def test_generate_openai_response_with_openai_key(app):

    app.config['OPENAI_API_KEY'] = 'test_openai_api_key'
    
    response = generate_openai_response('Hello!')
    
    assert response is not None
    assert isinstance(response, str)
    assert response not in random_texts


def test_generate_openai_response_without_openai_key(app):
    
    response = generate_openai_response('Hello!')
    assert response is not None
    assert isinstance(response, str)
    assert response in random_texts
