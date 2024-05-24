from flask import Flask
# from pdfminer.high_level import extract_text
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
import email_validator

app  = Flask(__name__)
app.config["SECRET_KEY"] = "62913a7dac3933f87a84626fcdeaaf9e2653f0a000843efd9bf2b31ba4767402"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'galalamrewida@gmail.com'
app.config['MAIL_PASSWORD'] = 'vafdsfmhqkyndgwj'
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager =LoginManager(app)
# with app.app_context():
#     db.create_all()
# app.app_context().push()
from resume import routs
