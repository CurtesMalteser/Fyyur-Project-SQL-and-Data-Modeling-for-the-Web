import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
# TODO IMPLEMENT DATABASE URL
username = os.environ.get('USER', os.environ.get('USERNAME'))
SQLALCHEMY_DATABASE_URI = 'postgresql://{}@localhost:5432/fyyurapp'.format(username)
SQLALCHEMY_TRACK_MODIFICATIONS = False
