from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from .config import Config

class Base(DeclarativeBase):
    pass

load_dotenv()

db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(testing=False):
    app = Flask(__name__, static_folder='static')

    # Configuração para testes
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória
        app.config['JWT_SECRET_KEY'] = "1fj301jfio12jlkml1mfjn4gfu3iofdikd3"
        app.config['TESTING'] = True
    else:
        app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.route('/')
    def serve_frontend():
        return send_from_directory('static', 'index.html') 
    
    from app.routes import api 
    app.register_blueprint(api, url_prefix='/v1')
    
    from app import models

    with app.app_context():
        db.create_all()  
        create_default_user()  

    return app

def create_default_user():
    from app.models import User  
    if not User.query.filter_by(name='admin').first():
        hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
        new_user = User(name='admin', password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
