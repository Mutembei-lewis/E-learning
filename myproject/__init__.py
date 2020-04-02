import os
from flask import Flask, render_template, request,redirect,session,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_mail import Mail


login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gotthekeystothecity'
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////home/walker/megaproject/30thmonday/Userdatabase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False


db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager.init_app(app)
login_manager.login_view = "login"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lewismutembei001@gmail.com'
app.config['MAIL_PASSWORD'] = 'Lewis668@'
mail = Mail(app)

