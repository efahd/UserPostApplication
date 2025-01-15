from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login' #set the login route
    login_manager.login_message_category = 'info'

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app