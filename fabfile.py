from fabric.api import local, task, settings
from termcolor import colored
from application import app, db, user_datastore
from utils.password_utils import encrypt_password
import json

@task
def clean():
  with settings(warn_only=True):
    local('rm choochootrain.db')

@task
def build():
  clean()
  db.create_all()
  initialize_users()
  seed_worksheet_questions()

@task(default=True)
def run():
  app.run()


def initialize_users():
  user_role = user_datastore.create_role(name='user')
  admin_role = user_datastore.create_role(name='admin')

  admin_user = user_datastore.create_user(email='thecheesybread@gmail.com', firstname='Lu', lastname='Cheng', password=encrypt_password('p@ssw0rd'))
  user_datastore.add_role_to_user(admin_user, admin_role)

  test_user1 = user_datastore.create_user(email='hpatel516@gmail.com', firstname='Hurshal', lastname='Patel', password=encrypt_password('p@ssw0rd'))

  user_datastore.add_role_to_user(test_user1, user_role)

  db.session.add(user_role)
  db.session.add(admin_role)
  db.session.add(admin_user)
  db.session.add(test_user1)
  db.session.commit()

  print colored('Roles, admin user, and test user are created.', 'blue')
