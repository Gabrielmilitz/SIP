import os

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/sip_db'

SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')

# Configuração de e-mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'gabrielmarinmilitz@gmail.com'
MAIL_PASSWORD = 'exyn ieen xiao bjjz '
MAIL_DEFAULT_SENDER = 'gabrielmarinmilitz@gmail.com'
