from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify(message="Email already exists."), 409

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User created successfully."), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not check_password_hash(user.password, data.get('password')):
        return jsonify(message="Please check your login details and try again."), 401

    login_user(user)
    return jsonify(message="Login successful."), 200

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message="Successfully logged out."), 200
