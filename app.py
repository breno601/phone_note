from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from itsdangerous import URLSafeTimedSerializer
import os

app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'breno601@gmail.com',
    MAIL_PASSWORD = 'my_password',
))

app.secret_key = os.urandom(12)

ts = URLSafeTimedSerializer(app.secret_key)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone_note.db'
db = SQLAlchemy(app)


if __name__ == "__main__":

    # Import views here to avoid circular dependencies.
    
    from views import *

    app.run(debug=True)
