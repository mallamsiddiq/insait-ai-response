import os
from app.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory DB for tests
    JWT_SECRET = 'secret'  # Secret for JWT token
    OPENAI_API_KEY = 'testkey'