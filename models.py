from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
class User(UserMixin, db.Model):
    """User model """

    __tablename__ = "users"
    id = db.Column('id',db.Integer,primary_key=True)
    username = db.Column('username',db.String(25), unique=True, nullable=False)
    password = db.Column('password',db.String(), nullable=False)
