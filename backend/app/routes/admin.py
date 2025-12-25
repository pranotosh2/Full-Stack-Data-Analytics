"""
Admin routes for the Data Analytics Mentorship Platform
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Course, Enrollment, AnalyticsEvent, db
from ..utils.decorators import admin_required
from sqlalchemy import func, extract
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Get all users with optional filtering"""
    # Query parameters
    role = request.args.get('role')
    status = request.args.get('status')  # active, inactive, pending
    search = request.args.get('search')

    query = User.query

    # Apply filters
    if role:
        query = query.filter_by(role=role)
    if status:
        if status == 'active':
            query = query.filter_by(is_active=True)
        elif status == 'inactive':
            query = query.filter_by(is_active=False)
        elif status == 'pending' and role == 'mentor':
            query = query.filter_by(role='mentor', is_approved=False)
    if search:
        query = query.filter(
            db.or_(
                User.username.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                User.first_name.ilike(f'%{search}%'),
                User.last_name.ilike(f'%{search}%')
            )
        )

    users = query.all()

    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': len(users)
    }), 200

@admin_bp.route('/users/<int:user_id>/approve', methods=['POST'])
@jwt_required()
@admin_required
def approve_mentor(user_id):
    """Approve a mentor account"""
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role != 'mentor':
        return jsonify({'error': 'User is not a mentor'}), 400

    if user.is_approved:
        return jsonify({'error': 'Mentor is already approved'}), 400

    try:
        user.is_approved = True
        db.session.commit()

        # Log approval
        AnalyticsEvent.log_event(
            user_id=user_id,
            event_type='mentor_approved',
            event_data={'approved_by': get_jwt_identity()}
        )

        return jsonify({
            'message': 'Mentor approved successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Approval failed', 'details': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_user_status(user_id):
    """Activate/deactivate a user account"""
    user = User.query.get(user_id)
    data = request.get_json()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role == 'admin':
        return jsonify({'error': 'Cannot deactivate admin accounts'}), 400

    new_status = data.get('is_active')
    if new_status is None:
        return jsonify({'error': 'is_active field required'}), 400

    try:
        user.is_active = new_status
        db.session.commit()

        # Log status change
        AnalyticsEvent.log_event(
            user_id=user_id,
            event_type='user_status_changed',
            event_data={
                'new_status': new_status,
                'changed_by': get_jwt_identity()
            }
        )

        return jsonify({
            'message': f'User {"activated" if new_status else "deactivated"} successfully',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Status update failed', 'details': str(e)}), 500

@admin_bp.route('/courses/<int:course_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_course_status(course_id):
    """Activate/deactivate a course"""
    course = Course.query.get(course_id)
    data = request.get_json()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    new_status = data.get('is_active')
    if new_status is None:
        return jsonify({'error': 'is_active field required'}), 400

    try:
        course.is_active = new_status
        db.session.commit()

        # Log course status change
        AnalyticsEvent.log_event(
            user_id=get_jwt_identity(),
            event_type='course_status_changed',
            event_data={
                'course_id': course_id,
                'new_status': new_status
            }
        )

        return jsonify({
            'message': f'Course {"activated" if new_status else "deactivated"} successfully',
            'course': course.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Course status update failed', 'details': str(e)}), 500

@admin_bp.route('/analytics/overview', methods=['GET'])
@jwt_required()
@admin_required
def get_analytics_overview():
    """Get platform analytics overview"""
    try:
        # User statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        total_students = User.query.filter_by(role='student', is_active=True).count()
        total_mentors = User.query.filter_by(role='mentor', is_active=True, is_approved=True).count()
        pending_mentors = User.query.filter_by(role='mentor', is_approved=False).count()

        # Course statistics
        total_courses = Course.query.count()
        active_courses = Course.query.filter_by(is_active=True).count()

        # Enrollment statistics
        total_enrollments = Enrollment.query.count()
        completed_enrollments = Enrollment.query.filter_by(is_completed=True).count()

        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_registrations = User.query.filter(User.created_at >= thirty_days_ago).count()
        recent_enrollments = Enrollment.query.filter(Enrollment.enrollment_date >= thirty_days_ago).count()

        # Calculate completion rate
        completion_rate = (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0

        return jsonify({
            'overview': {
                'users': {
                    'total': total_users,
                    'active': active_users,
                    'students': total_students,
                    'mentors': total_mentors,
                    'pending_mentors': pending_mentors
                },
                'courses': {
                    'total': total_courses,
                    'active': active_courses
                },
                'enrollments': {
                    'total': total_enrollments,
                    'completed': completed_enrollments,
                    'completion_rate': round(completion_rate, 2)
                },
                'recent_activity': {
                    'registrations_last_30_days': recent_registrations,
                    'enrollments_last_30_days': recent_enrollments
                }
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Analytics retrieval failed', 'details': str(e)}), 500

@admin_bp.route('/analytics/user-growth', methods=['GET'])
@jwt_required()
@admin_required
def get_user_growth():
    """Get user registration trends over time"""
    try:
        # Get monthly user registrations for the last 12 months
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)

        monthly_registrations = db.session.query(
            extract('year', User.created_at).label('year'),
            extract('month', User.created_at).label('month'),
            func.count(User.id).label('count')
        ).filter(
            User.created_at >= twelve_months_ago
        ).group_by(
            extract('year', User.created_at),
            extract('month', User.created_at)
        ).order_by(
            extract('year', User.created_at),
            extract('month', User.created_at)
        ).all()

        # Format the data
        growth_data = []
        for row in monthly_registrations:
            growth_data.append({
                'year': int(row.year),
                'month': int(row.month),
                'registrations': row.count
            })

        return jsonify({
            'user_growth': growth_data
        }), 200

    except Exception as e:
        return jsonify({'error': 'User growth data retrieval failed', 'details': str(e)}), 500

@admin_bp.route('/analytics/course-performance', methods=['GET'])
@jwt_required()
@admin_required
def get_course_performance():
    """Get course performance analytics"""
    try:
        courses = Course.query.filter_by(is_active=True).all()

        course_performance = []
        for course in courses:
            course_performance.append({
                'course_id': course.id,
                'title': course.title,
                'mentor': course.mentor.get_full_name(),
                'enrolled_students': course.get_enrolled_students_count(),
                'completion_rate': course.get_completion_rate(),
                'average_rating': course.get_average_rating(),
                'total_modules': course.get_modules_count()
            })

        # Sort by enrollment count (most popular first)
        course_performance.sort(key=lambda x: x['enrolled_students'], reverse=True)

        return jsonify({
            'course_performance': course_performance
        }), 200

    except Exception as e:
        return jsonify({'error': 'Course performance data retrieval failed', 'details': str(e)}), 500
