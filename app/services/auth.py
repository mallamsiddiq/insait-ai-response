from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User

def login_required(view_func):
    @wraps(view_func)
    @jwt_required()  # Use the built-in JWT required decorator
    def decorated_function(self, *args, **kwargs):  # Accept `self` for class-based views
        user_id = get_jwt_identity()  # Get user ID from token
        user = User.query.get(user_id)  # Fetch user from DB

        if not user:
            return jsonify({"msg": "Invalid user"}), 401

        return view_func(self, *args, **kwargs)  # Pass `self` to maintain method binding

    return decorated_function
