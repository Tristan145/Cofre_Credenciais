from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(255), nullable=True)