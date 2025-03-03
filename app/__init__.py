from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config

from flask_smorest import Api


# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

api = Api(
    spec_kwargs={
        "title": "AI Response Generator API",
        "version": "1.0",
        "description": "A simple API",
        # "doc": "/",
        "openapi_version": "3.0.2"
    },

)

def create_app(config_class:object = Config):
    # Create the Flask application  instance
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize the extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # Import and register the API blueprint from resources
    # from app.resources.main import namespace
    # api.add_namespace(namespace)
    from app.resources.main import generated_text_blue_print
    from app.resources.users import users_blue_print
    
    api.register_blueprint(generated_text_blue_print)
    api.register_blueprint(users_blue_print)
    
    return app
