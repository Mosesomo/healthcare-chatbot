import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer


load_dotenv()


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = '1c2bd454f2ab00d3042ab99d86492999'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

serial = URLSafeTimedSerializer(app.config['SECRET_KEY'])

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from system import routes