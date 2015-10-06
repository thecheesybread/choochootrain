import sqlite3
import traceback
from application_config import app, db
from models.user_models import roles_users, Role, User, user_datastore
from flask import render_template, redirect, request
from flask.ext.security import Security, login_required, roles_required, current_user
from flask.ext.security.signals import user_registered
from flask.ext.login import logout_user
from flask_security.forms import LoginForm, RegisterForm, TextField, Required
import json

# Let's try to only keep routes and coniguration within application.py to keep the code clean.

# Todo(Lu Cheng) consider moving registration and signin logic inside of config.
class ExtendedRegisterForm(RegisterForm):
  firstname = TextField('First Name', [Required()])
  lastname = TextField('Last Name', [Required()])

security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
  default_role = user_datastore.find_role("user")
  user_datastore.add_role_to_user(user, default_role)
  db.session.commit()

# Makes Login From and Registration Form show up on every page
# so we can load it on the modal of every page.
@app.context_processor
def inject_login_forms():
    return dict(login_user_form=LoginForm(), register_user_form=ExtendedRegisterForm() )

@app.route('/register', methods=['GET'])
def register():
  return render_template('authentication/register.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
  return 'success'

if __name__ == '__main__':
  app.run()
