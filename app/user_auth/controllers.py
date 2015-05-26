from flask import Blueprint, abort, request, render_template, \
                  flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from app import db
from app.user_auth.models import User
from flask import Flask, jsonify
from flask.ext.httpauth import HTTPBasicAuth


#!/usr/bin/env python
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)





auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with email/password
        user = User.query.filter_by(email = email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# Define the blueprint: 'auth', set its url prefix: app.url/auth
user_auth = Blueprint('authbp', __name__, url_prefix='/auth')

# Set the route and accepted methods
@user_auth.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    postal_code = request.json.get('postal_code')
    password = request.json.get('password')
    if email is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(email = email).first() is not None:
        abort(400) # existing user
    user = User(first_name, last_name, email, postal_code)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'email': user.email }), 201

@user_auth.route('/signup/admin', methods=['POST'])
def signup_admin():
    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    postal_code = request.json.get('postal_code')
    password = request.json.get('password')
    if email is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(email = email).first() is not None:
        abort(400) # existing user
    user = User(first_name, last_name, email, postal_code)
    user.hash_password(password)
    user.is_admin = True
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'email': user.email }), 201

@user_auth.route("/users", methods=['GET'])
def userList():
    userlist = User.query.all()
    return jsonify({"users" : [user.serialize() for user in userlist]})

@user_auth.route('/user/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify(user.serialize())

@user_auth.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii'), 'id': g.user.id })



