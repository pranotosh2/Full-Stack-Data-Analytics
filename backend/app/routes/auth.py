"""
Authentication routes for the Data Analytics Mentorship Platform
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from ..models import User, AnalyticsEvent
from .. import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Validate role
    if data['role'] not in ['student', 'mentor']:
        return jsonify({'error': 'Invalid role. Must be student or mentor'}), 400

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    try:
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            bio=data.get('bio'),
            expertise=data.get('expertise')
        )

        db.session.add(user)
        db.session.commit()

        # Log registration event
        AnalyticsEvent.log_event(
            user_id=user.id,
            event_type='user_registered',
            event_data={'role': user.role}
        )

        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT tokens"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 401

    # Check mentor approval
    if user.role == 'mentor' and not user.is_approved:
        return jsonify({'error': 'Mentor account pending approval'}), 401

    # Create tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    # Log login event
    AnalyticsEvent.log_event(
        user_id=user.id,
        event_type='user_login',
        event_data={'role': user.role}
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh access token using refresh token"""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)

    return jsonify({
        'access_token': access_token
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user': user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        # Update allowed fields
        allowed_fields = ['first_name', 'last_name', 'bio', 'expertise', 'profile_picture']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        db.session.commit()

        # Log profile update
        AnalyticsEvent.log_event(
            user_id=user.id,
            event_type='profile_updated',
            event_data={'fields_updated': list(data.keys())}
        )

        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Profile update failed', 'details': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password required'}), 400

    if not user.check_password(data['current_password']):
        return jsonify({'error': 'Current password is incorrect'}), 400

    try:
        user.set_password(data['new_password'])
        db.session.commit()

        # Log password change
        AnalyticsEvent.log_event(
            user_id=user.id,
            event_type='password_changed'
        )

        return jsonify({
            'message': 'Password changed successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Password change failed', 'details': str(e)}), 500
