"""
Assignment model for course assessments
"""
from datetime import datetime
from .. import db

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    assignment_type = db.Column(db.String(20), default='homework')
    max_points = db.Column(db.Integer, default=100)
    due_date = db.Column(db.DateTime)
    submission_instructions = db.Column(db.Text)
    grading_rubric = db.Column(db.Text)
    is_required = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    submissions = db.relationship('Submission', backref='assignment', lazy=True, cascade='all, delete-orphan')

    def __init__(self, course_id, title, description, assignment_type='homework',
                 max_points=100, due_date=None, submission_instructions=None,
                 grading_rubric=None, is_required=True, module_id=None):
        self.course_id = course_id
        self.module_id = module_id
        self.title = title
        self.description = description
        self.assignment_type = assignment_type
        self.max_points = max_points
        self.due_date = due_date
        self.submission_instructions = submission_instructions
        self.grading_rubric = grading_rubric
        self.is_required = is_required

    def get_submissions_count(self):
        """Get total number of submissions"""
        return len(self.submissions)

    def get_graded_submissions_count(self):
        """Get number of graded submissions"""
        return len([s for s in self.submissions if s.grade is not None])

    def get_average_grade(self):
        """Calculate average grade for the assignment"""
        graded_submissions = [s for s in self.submissions if s.grade is not None]
        if not graded_submissions:
            return 0.0

        total_points = sum(s.grade for s in graded_submissions)
        return round(total_points / len(graded_submissions), 2)

    def is_past_due(self):
        """Check if assignment is past due date"""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date

    def to_dict(self, include_stats=False):
        """Convert assignment object to dictionary for API responses"""
        assignment_dict = {
            'id': self.id,
            'course_id': self.course_id,
            'module_id': self.module_id,
            'title': self.title,
            'description': self.description,
            'assignment_type': self.assignment_type,
            'max_points': self.max_points,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'submission_instructions': self.submission_instructions,
            'grading_rubric': self.grading_rubric,
            'is_required': self.is_required,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        if include_stats:
            assignment_dict['stats'] = {
                'submissions_count': self.get_submissions_count(),
                'graded_count': self.get_graded_submissions_count(),
                'average_grade': self.get_average_grade()
            }

        return assignment_dict

    def __repr__(self):
        return f'<Assignment {self.title} (Course {self.course_id})>'
