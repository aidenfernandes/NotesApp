from aidenflask import db
from flask_login import UserMixin
from sqlalchemy .sql import func

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    email=db.Column(db.String(150), unique=True)
    notes=db.relationship("Note")


class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    note=db.Column(db.String(100000))
    date=db.Column(db.DateTime(timezone=True),default=func.now)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))