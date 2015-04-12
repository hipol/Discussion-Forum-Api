# Import flask and template operators
import os
from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

auth = HTTPBasicAuth()


# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers

db = SQLAlchemy(app)

# Import a module / component using its blueprint handler variable (mod_auth)
from app.user_auth.controllers import user_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)


from app.communities.controllers import communities as communities_blueprint
app.register_blueprint(communities_blueprint)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
