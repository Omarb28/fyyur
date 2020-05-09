import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

# local database
# SQLALCHEMY_DATABASE_URI = 'postgresql://vagrant:vagrant@localhost:5432/fyyur'

# remote database
SQLALCHEMY_DATABASE_URI = 'postgres://bsogzflyygtivv:f072c96d8750ab2813eca9ef2ca3cd7438609b886cdb592bc3a2221cec29cb39@ec2-23-22-156-110.compute-1.amazonaws.com:5432/d4ibbmtunji83t'

# my heroku web app link:  https://fyyur-app-omar.herokuapp.com/
# my github profile: 

SQLALCHEMY_TRACK_MODIFICATIONS = False
