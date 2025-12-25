"""
Course model for the Data Analytics Mentorship Platform
"""
from datetime import datetime
from .. import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty_level = db.Column(db.String(20), default='beginner')
    duration_hours = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2), default=0.00)
    is_active = db.Column(db.Boolean, default=True)
    enrollment_limit = db.Column(db.Integer)
    prerequisites = db.Column(db.Text)
    learning_objectives = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    modules = db.relationship('Module', backref='course', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='course', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('CourseReview', backref='course', lazy=True, cascade='all, delete-orphan')

    def __init__(self, title, description, mentor_id, category, difficulty_level='beginner',
                 duration_hours=None, price=0.00, enrollment_limit=None, prerequisites=None,
                 learning_objectives=None):
        self.title = title
        self.description = description
        self.mentor_id = mentor_id
        self.category = category
        self.difficulty_level = difficulty_level
        self.duration_hours = duration_hours
        self.price = price
        self.enrollment_limit = enrollment_limit
        self.prerequisites = prerequisites
        self.learning_objectives = learning_objectives

    def get_enrolled_students_count(self):
        """Get the number of enrolled students"""
        return len([e for e in self.enrollments if e.student.is_active])

    def get_completion_rate(self):
        """Calculate course completion rate"""
        total_enrollments = len(self.enrollments)
        if total_enrollments == 0:
            return 0.0

        completed_enrollments = len([e for e in self.enrollments if e.is_completed])
        return round((completed_enrollments / total_enrollments) * 100, 2)

    def get_average_rating(self):
        """Calculate average course rating"""
        if not self.reviews:
            return 0.0

        total_rating = sum(review.rating for review in self.reviews)
        return round(total_rating / len(self.reviews), 2)

    def is_enrollment_open(self):
        """Check if enrollment is still open"""
        if not self.is_active:
            return False

        if self.enrollment_limit:
            return self.get_enrolled_students_count() < self.enrollment_limit

        return True

    def get_modules_count(self):
        """Get total number of modules"""
        return len(self.modules)

    def to_dict(self, include_mentor=False, include_stats=False):
        """Convert course object to dictionary for API responses"""
        course_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'mentor_id': self.mentor_id,
            'category': self.category,
            'difficulty_level': self.difficulty_level,
            'duration_hours': self.duration_hours,
            'price': float(self.price) if self.price else 0.0,
            'is_active': self.is_active,
            'enrollment_limit': self.enrollment_limit,
            'prerequisites': self.prerequisites,
            'learning_objectives': self.learning_objectives,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        if include_mentor and self.mentor:
            course_dict['mentor'] = {
                'id': self.mentor.id,
                'first_name': self.mentor.first_name,
                'last_name': self.mentor.last_name,
                'expertise': self.mentor.expertise
            }

        if include_stats:
            course_dict['stats'] = {
                'enrolled_students': self.get_enrolled_students_count(),
                'completion_rate': self.get_completion_rate(),
                'average_rating': self.get_average_rating(),
                'modules_count': self.get_modules_count()
            }

        return course_dict

    def __repr__(self):
        return f'<Course {self.title} by Mentor {self.mentor_id}>'
