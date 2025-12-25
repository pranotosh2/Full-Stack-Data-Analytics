"""
User model for the Data Analytics Mentorship Platform
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .. import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(500))
    bio = db.Column(db.Text)
    expertise = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    created_courses = db.relationship('Course', backref='mentor', lazy=True,
                                     foreign_keys='Course.mentor_id')
    enrollments = db.relationship('Enrollment', backref='student', lazy=True,
                                 foreign_keys='Enrollment.student_id')
    submissions = db.relationship('Submission', backref='student', lazy=True,
                                 foreign_keys='Submission.student_id')
    graded_submissions = db.relationship('Submission', backref='grader', lazy=True,
                                       foreign_keys='Submission.graded_by')
    reviews = db.relationship('CourseReview', backref='student', lazy=True)
    analytics_events = db.relationship('AnalyticsEvent', backref='user', lazy=True)

    def __init__(self, username, email, password, first_name, last_name, role):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.set_password(password)

        # Auto-approve admins and students, mentors need approval
        if role in ['admin', 'student']:
            self.is_approved = True

    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}"

    def is_mentor_approved(self):
        """Check if user is an approved mentor"""
        return self.role == 'mentor' and self.is_approved

    def can_create_courses(self):
        """Check if user can create courses"""
        return self.role in ['mentor', 'admin'] and (self.is_approved or self.role == 'admin')

    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.role == 'admin'

    def to_dict(self):
        """Convert user object to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'is_approved': self.is_approved,
            'profile_picture': self.profile_picture,
            'bio': self.bio,
            'expertise': self.expertise,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
