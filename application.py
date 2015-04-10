# Run a test server.
from app import app

from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from app import db
from app.user_auth.models import User
#from app.communities.models import Community

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
    	g.user = User.query.get([session['user_id']])


app.run(host='0.0.0.0')

