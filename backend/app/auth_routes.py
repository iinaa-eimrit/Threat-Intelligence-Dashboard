from flask import Blueprint, request, jsonify
from models.user import User, AuditLog
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime, os

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'analyst')
    )
    db.session.add(user)
    db.session.commit()
    log = AuditLog(user_id=user.id, action='register', details='User registered')
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'User registered'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = jwt.encode({
        'user_id': user.id,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, SECRET_KEY, algorithm='HS256')
    log = AuditLog(user_id=user.id, action='login', details='User logged in')
    db.session.add(log)
    db.session.commit()
    return jsonify({'token': token})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # JWT logout is stateless; client deletes token
    return jsonify({'message': 'Logged out'})
