"""
Main API routes for the Data Analytics Mentorship Platform
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_, or_, func
from ..models import (
    User, Course, Enrollment, Module, Assignment, Submission,
    CourseReview, AnalyticsEvent, db
)
from ..utils.decorators import role_required
from datetime import datetime

api_bp = Blueprint('api', __name__)

# ===== COURSE ROUTES =====

@api_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    """Get all courses with optional filtering"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Query parameters
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    mentor_id = request.args.get('mentor_id')
    search = request.args.get('search')
    enrolled_only = request.args.get('enrolled_only', 'false').lower() == 'true'

    query = Course.query.filter_by(is_active=True)

    # Apply filters
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    if mentor_id:
        query = query.filter_by(mentor_id=mentor_id)
    if search:
        query = query.filter(
            or_(
                Course.title.ilike(f'%{search}%'),
                Course.description.ilike(f'%{search}%')
            )
        )

    # If student wants only enrolled courses
    if enrolled_only and user.role == 'student':
        enrolled_course_ids = [e.course_id for e in user.enrollments]
        query = query.filter(Course.id.in_(enrolled_course_ids))

    courses = query.all()

    # Add enrollment status for current user
    courses_data = []
    for course in courses:
        course_data = course.to_dict(include_mentor=True, include_stats=True)

        # Check enrollment status
        enrollment = Enrollment.query.filter_by(
            student_id=current_user_id,
            course_id=course.id
        ).first()
        course_data['enrollment_status'] = enrollment.to_dict() if enrollment else None

        courses_data.append(course_data)

    return jsonify({
        'courses': courses_data,
        'total': len(courses_data)
    }), 200

@api_bp.route('/courses/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    """Get detailed course information"""
    current_user_id = get_jwt_identity()
    course = Course.query.get(course_id)

    if not course or not course.is_active:
        return jsonify({'error': 'Course not found'}), 404

    course_data = course.to_dict(include_mentor=True, include_stats=True)

    # Add modules if user is enrolled or is the mentor
    user = User.query.get(current_user_id)
    is_enrolled = Enrollment.query.filter_by(
        student_id=current_user_id,
        course_id=course_id
    ).first() is not None

    if is_enrolled or course.mentor_id == current_user_id or user.role == 'admin':
        course_data['modules'] = [module.to_dict() for module in course.modules]
        course_data['assignments'] = [assignment.to_dict() for assignment in course.assignments]

    # Add enrollment info for students
    if user.role == 'student':
        enrollment = Enrollment.query.filter_by(
            student_id=current_user_id,
            course_id=course_id
        ).first()
        course_data['enrollment'] = enrollment.to_dict() if enrollment else None

    return jsonify(course_data), 200

@api_bp.route('/courses', methods=['POST'])
@jwt_required()
@role_required(['mentor', 'admin'])
def create_course():
    """Create a new course (mentors and admins only)"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()

    # Validate required fields
    required_fields = ['title', 'description', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        course = Course(
            title=data['title'],
            description=data['description'],
            mentor_id=current_user_id,
            category=data['category'],
            difficulty_level=data.get('difficulty_level', 'beginner'),
            duration_hours=data.get('duration_hours'),
            price=data.get('price', 0.00),
            enrollment_limit=data.get('enrollment_limit'),
            prerequisites=data.get('prerequisites'),
            learning_objectives=data.get('learning_objectives')
        )

        db.session.add(course)
        db.session.commit()

        # Log course creation
        AnalyticsEvent.log_event(
            user_id=current_user_id,
            event_type='course_created',
            event_data={'course_id': course.id, 'title': course.title}
        )

        return jsonify({
            'message': 'Course created successfully',
            'course': course.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Course creation failed', 'details': str(e)}), 500

# ===== ENROLLMENT ROUTES =====

@api_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@jwt_required()
@role_required(['student'])
def enroll_course(course_id):
    """Enroll student in a course"""
    current_user_id = get_jwt_identity()
    course = Course.query.get(course_id)

    if not course or not course.is_active:
        return jsonify({'error': 'Course not found or inactive'}), 404

    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(
        student_id=current_user_id,
        course_id=course_id
    ).first()

    if existing_enrollment:
        return jsonify({'error': 'Already enrolled in this course'}), 409

    # Check enrollment limit
    if not course.is_enrollment_open():
        return jsonify({'error': 'Course enrollment is closed'}), 400

    try:
        enrollment = Enrollment(student_id=current_user_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()

        # Log enrollment
        AnalyticsEvent.log_event(
            user_id=current_user_id,
            event_type='course_enrolled',
            event_data={'course_id': course_id}
        )

        return jsonify({
            'message': 'Successfully enrolled in course',
            'enrollment': enrollment.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Enrollment failed', 'details': str(e)}), 500

@api_bp.route('/enrollments/<int:enrollment_id>/progress', methods=['PUT'])
@jwt_required()
def update_progress(enrollment_id):
    """Update student progress in a course"""
    current_user_id = get_jwt_identity()
    enrollment = Enrollment.query.get(enrollment_id)

    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404

    if enrollment.student_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    module_id = data.get('module_id')
    completed = data.get('completed', False)

    if not module_id:
        return jsonify({'error': 'Module ID required'}), 400

    try:
        enrollment.update_progress(module_id, completed)
        db.session.commit()

        return jsonify({
            'message': 'Progress updated successfully',
            'enrollment': enrollment.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Progress update failed', 'details': str(e)}), 500

# ===== ASSIGNMENT ROUTES =====

@api_bp.route('/assignments/<int:assignment_id>/submit', methods=['POST'])
@jwt_required()
@role_required(['student'])
def submit_assignment(assignment_id):
    """Submit an assignment"""
    current_user_id = get_jwt_identity()
    assignment = Assignment.query.get(assignment_id)

    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    # Check if student is enrolled in the course
    enrollment = Enrollment.query.filter_by(
        student_id=current_user_id,
        course_id=assignment.course_id
    ).first()

    if not enrollment:
        return jsonify({'error': 'Not enrolled in this course'}), 403

    data = request.get_json()

    try:
        submission = Submission(
            assignment_id=assignment_id,
            student_id=current_user_id,
            submission_content=data.get('submission_content'),
            submission_files=data.get('submission_files', [])
        )

        db.session.add(submission)
        db.session.commit()

        # Log submission
        AnalyticsEvent.log_event(
            user_id=current_user_id,
            event_type='assignment_submitted',
            event_data={'assignment_id': assignment_id}
        )

        return jsonify({
            'message': 'Assignment submitted successfully',
            'submission': submission.to_dict(include_assignment=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Submission failed', 'details': str(e)}), 500

@api_bp.route('/assignments/<int:assignment_id>/grade', methods=['POST'])
@jwt_required()
def grade_submission(assignment_id):
    """Grade a student submission (mentors and admins only)"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role not in ['mentor', 'admin']:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    submission_id = data.get('submission_id')
    grade = data.get('grade')
    feedback = data.get('feedback')

    if not submission_id or grade is None:
        return jsonify({'error': 'Submission ID and grade required'}), 400

    submission = Submission.query.get(submission_id)

    if not submission or submission.assignment_id != assignment_id:
        return jsonify({'error': 'Submission not found'}), 404

    # Check if mentor owns the course or is admin
    if user.role == 'mentor' and submission.assignment.course.mentor_id != current_user_id:
        return jsonify({'error': 'Unauthorized to grade this submission'}), 403

    try:
        submission.submit_grade(grade, feedback, current_user_id)
        db.session.commit()

        return jsonify({
            'message': 'Submission graded successfully',
            'submission': submission.to_dict(include_assignment=True, include_student=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Grading failed', 'details': str(e)}), 500

# ===== REVIEW ROUTES =====

@api_bp.route('/courses/<int:course_id>/review', methods=['POST'])
@jwt_required()
@role_required(['student'])
def submit_review(course_id):
    """Submit a course review"""
    current_user_id = get_jwt_identity()

    # Check if student is enrolled and completed the course
    enrollment = Enrollment.query.filter_by(
        student_id=current_user_id,
        course_id=course_id
    ).first()

    if not enrollment or not enrollment.is_completed:
        return jsonify({'error': 'Must complete the course to leave a review'}), 403

    data = request.get_json()

    if not data.get('rating') or not isinstance(data['rating'], int) or data['rating'] < 1 or data['rating'] > 5:
        return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400

    try:
        # Check if review already exists
        existing_review = CourseReview.query.filter_by(
            course_id=course_id,
            student_id=current_user_id
        ).first()

        if existing_review:
            # Update existing review
            existing_review.rating = data['rating']
            existing_review.review_text = data.get('review_text')
            db.session.commit()
            message = 'Review updated successfully'
        else:
            # Create new review
            review = CourseReview(
                course_id=course_id,
                student_id=current_user_id,
                rating=data['rating'],
                review_text=data.get('review_text')
            )
            db.session.add(review)
            db.session.commit()
            message = 'Review submitted successfully'

        return jsonify({
            'message': message
        }), 201 if not existing_review else 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Review submission failed', 'details': str(e)}), 500
