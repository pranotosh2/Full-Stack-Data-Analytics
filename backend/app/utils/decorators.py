"""
Custom decorators for the Data Analytics Mentorship Platform
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from ..models import User

def role_required(roles):
    """
    Decorator to check if user has required role(s)

    Args:
        roles: List of allowed roles (e.g., ['admin', 'mentor'])
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)

            if not user:
                return jsonify({'error': 'User not found'}), 404

            if not user.is_active:
                return jsonify({'error': 'Account is deactivated'}), 401

            # Check mentor approval
            if user.role == 'mentor' and not user.is_approved:
                return jsonify({'error': 'Mentor account pending approval'}), 401

            if user.role not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def mentor_or_admin_required(f):
    """Decorator for routes that require mentor or admin role"""
    return role_required(['mentor', 'admin'])(f)

def admin_required(f):
    """Decorator for routes that require admin role"""
    return role_required(['admin'])(f)

def student_required(f):
    """Decorator for routes that require student role"""
    return role_required(['student'])(f)
