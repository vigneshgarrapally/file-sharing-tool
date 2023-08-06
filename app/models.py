"""
This file is used to create the database models for the application.
"""
from flask_login import UserMixin
from app import db, app, bcrypt


class User(db.Model, UserMixin):
    """
    A class representing a user in the application.

    Attributes:
    -----------
    id : int
        The unique identifier for the user.
    full_name : str
        The full name of the user.
    email : str
        The email address of the user.
    password_hash : str
        The hashed password of the user.

    Methods:
    --------
    __repr__():
        Returns a string representation of the User object.
    get_id():
        Returns the email address of the user.
    set_password(password: str):
        Sets the password_hash attribute to the hashed value of the given password.
    get(email: str):
        Returns the User object with the given email address.
    check_password(password: str):
        Returns True if the given password matches the hashed password of the user, False otherwise.
    """

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def get_id(self):
        return self.email

    @staticmethod
    def get(email):
        return User.query.filter_by(email=email).first()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()
