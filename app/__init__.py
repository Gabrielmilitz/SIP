import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

# Instâncias globais
db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Carrega configurações
    app.config.from_pyfile('../config.py')

    # Configura pasta de upload
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicializa extensões
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # Importa modelos e rotas
    with app.app_context():
        from app import models
        from app import routes

        # CRIA AS TABELAS AUTOMATICAMENTE
        db.create_all()

    return app