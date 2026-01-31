from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    # Ee column kachithanga undali
    is_admin = db.Column(db.Boolean, default=False) 

class Complaint(db.Model):
    complaint_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    proof_image = db.Column(db.String(200))