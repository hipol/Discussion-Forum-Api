# Run a test server.
from app import app, manager

from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from app import db
from app.user_auth.models import User
#from app.communities.models import Community

if __name__ == '__main__':
	app.run()

