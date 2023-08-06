"""
Initialize the app
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from app import cloud_utils

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.login_message = (
    "You must be logged in to access this page.Please log in first."
)
bcrypt = Bcrypt(app)
db.init_app(app)
login_manager.init_app(app)
status, response = cloud_utils.create_s3_bucket()
if status:
    print(response)
else:
    print(response)
    exit(1)

status, response = cloud_utils.create_dynamodb_table()
if status:
    print(response)
else:
    print(response)
    exit(1)

from app import routes, models, auth
