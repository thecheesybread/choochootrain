from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = 'PRODUCTION' not in os.environ
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQL_DATABASE_URI', 'sqlite:///choochootrain.db')
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
# TODO change this later.
app.config['SECURITY_PASSWORD_SALT'] = '$2a$12$skCRnkqE5L01bHEke678Ju'
# See here for all configurable options:
# /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/flask_security
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True

app.config['SECURITY_REGISTER_URL'] = '/register'
app.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'authentication/register.html'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'authentication/login.html'
app.config['SECURITY_LOGIN_URL'] = '/signin'
app.config['SECURITY_RESET_URL'] = '/reset_password'

app.config['SECURITY_POST_LOGIN_VIEW'] = 'success'
# Flask security settings: https://pythonhosted.org/Flask-Security/configuration.html
# Flask security templates that we could copy from if we want to reimplement:
# /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/flask_security/templates/security
app.config['SECURITY_CHANGEABLE'] = True
# app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'base.html'

# Fake emails for now
class FakeMail(object):
  def send(self, message):
    pass

app.extensions = getattr(app, 'extensions', {})
app.extensions['mail'] = FakeMail()

################################################################################
# Database
################################################################################
db = SQLAlchemy(app)
