from flask import Blueprint, abort, request, render_template, \
                  flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from app import db
from app.user_auth.models import User
from flask import Flask, jsonify
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# Define the blueprint: 'auth', set its url prefix: app.url/auth
user_auth = Blueprint('authbp', __name__, url_prefix='/auth')

# Set the route and accepted methods
@user_auth.route('/signup', methods=['POST'])
def signup():
    email = request.get_json('email')
    password = request.get_json('password')
    first_name = request.get_json('first_name')
    last_name = request.get_json('last_name')
    postal_code = request.get_json('postal_code')
    password = request.get_json('password')
    if email is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(email = email).first() is not None:
        abort(400) # existing user
    user = User(first_name, last_name, email, postal_code)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'email': user.email }), 201

#@user_auth.route('/login', methods=['POST'])
#def login():
#    """Logs the user in."""
#    response = {'status':403}

#    if g.user:
#        response = {'status':300}
        
#    error = None
#    if request.method == 'POST':


#    return jsonify(**response)

#@user_auth.route('/logout')
#def logout():
#    """Logs the user out."""
#    flash('You were logged out')
#    session.pop('user_id', None)
#    response = {'status':200}
#    return jsonify(**response)

@user_auth.route("/users", methods=['GET'])
def userList():
    userlist = User.query.all()
    return jsonify({"users" : [user.serialize() for user in userlist]})

@user_auth.route('/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify(user.serialize())

@user_auth.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})



