import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # carregar config
    app.config.from_pyfile('../config.py')

    # pasta uploads
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # importar models
    from app import models

    # importar rotas
    from app import routes

    # criar banco automaticamente
    with app.app_context():
        db.create_all()

    return app