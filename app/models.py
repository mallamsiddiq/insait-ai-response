from . import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    hash_password = db.Column("password", db.String(128), nullable=False)  # Renamed to _password for encapsulation

    @property
    def password(self):
        """Prevent password from being accessed"""
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, raw_password):
        """Automatically hash password before storing"""
        self.hash_password = generate_password_hash(raw_password)

    def check_password(self, password):
        """Verify a password against the stored hash"""
        return check_password_hash(self.hash_password, password)

class GeneratedText(db.Model):
    __tablename__ = 'generated_text'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))