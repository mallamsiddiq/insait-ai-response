import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_IDENTITY_CLAIM = os.environ.get('JWT_IDENTITY_CLAIM', 'supersecretkey')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    