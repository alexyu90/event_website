import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Connect to the database
# Databse URI here:
DATABASE_NAME = "fyyur"
username = 'alex'
password = ''
url = 'localhost:5432'
SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format(
    username, password, url, DATABASE_NAME)

#SQLALCHEMY_DATABASE_URI = 'postgres://alex@localhost:5432/fyyur'
