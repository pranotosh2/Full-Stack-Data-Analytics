"""
Submission model for student assignment submissions
"""
from datetime import datetime
from .. import db

class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submission_content = db.Column(db.Text)
    submission_files = db.Column(db.JSON)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.Numeric(5, 2))
    feedback = db.Column(db.Text)
    graded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    graded_at = db.Column(db.DateTime)
    is_late = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.UniqueConstraint('assignment_id', 'student_id', name='unique_assignment_student'),
    )

    def __init__(self, assignment_id, student_id, submission_content=None,
                 submission_files=None):
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.submission_content = submission_content
        self.submission_files = submission_files or []

        # Check if submission is late
        if self.assignment and self.assignment.due_date:
            self.is_late = datetime.utcnow() > self.assignment.due_date

    def submit_grade(self, grade, feedback, graded_by):
        """Submit a grade for the assignment"""
        self.grade = grade
        self.feedback = feedback
        self.graded_by = graded_by
        self.graded_at = datetime.utcnow()

    def get_percentage_score(self):
        """Get percentage score based on max points"""
        if not self.grade or not self.assignment:
            return 0.0
        return round((self.grade / self.assignment.max_points) * 100, 2)

    def to_dict(self, include_assignment=False, include_student=False):
        """Convert submission object to dictionary for API responses"""
        submission_dict = {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'student_id': self.student_id,
            'submission_content': self.submission_content,
            'submission_files': self.submission_files,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'grade': float(self.grade) if self.grade else None,
            'feedback': self.feedback,
            'graded_by': self.graded_by,
            'graded_at': self.graded_at.isoformat() if self.graded_at else None,
            'is_late': self.is_late
        }

        if include_assignment and self.assignment:
            submission_dict['assignment'] = {
                'id': self.assignment.id,
                'title': self.assignment.title,
                'max_points': self.assignment.max_points
            }

        if include_student and self.student:
            submission_dict['student'] = {
                'id': self.student.id,
                'first_name': self.student.first_name,
                'last_name': self.student.last_name
            }

        return submission_dict

    def __repr__(self):
        return f'<Submission Student {self.student_id} for Assignment {self.assignment_id}>'
