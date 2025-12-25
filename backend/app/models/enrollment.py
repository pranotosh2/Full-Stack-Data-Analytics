"""
Enrollment model for student-course relationships
"""
from datetime import datetime
from .. import db

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_percentage = db.Column(db.Numeric(5, 2), default=0.00)
    is_completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)
    progress_data = db.Column(db.JSON)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='unique_student_course'),
    )

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

    def update_progress(self, module_id, completed=False):
        """Update progress for a specific module"""
        if not self.progress_data:
            self.progress_data = {}

        self.progress_data[str(module_id)] = {
            'completed': completed,
            'completed_at': datetime.utcnow().isoformat() if completed else None
        }

        # Calculate overall completion percentage
        total_modules = len(self.course.modules) if self.course else 0
        if total_modules > 0:
            completed_modules = sum(1 for progress in self.progress_data.values()
                                  if progress.get('completed', False))
            self.completion_percentage = round((completed_modules / total_modules) * 100, 2)

            # Check if course is completed
            if completed_modules == total_modules and not self.is_completed:
                self.is_completed = True
                self.completion_date = datetime.utcnow()

    def get_module_progress(self, module_id):
        """Get progress for a specific module"""
        if not self.progress_data:
            return {'completed': False, 'completed_at': None}
        return self.progress_data.get(str(module_id), {'completed': False, 'completed_at': None})

    def to_dict(self):
        """Convert enrollment object to dictionary for API responses"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'completion_percentage': float(self.completion_percentage) if self.completion_percentage else 0.0,
            'is_completed': self.is_completed,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'progress_data': self.progress_data
        }

    def __repr__(self):
        return f'<Enrollment Student {self.student_id} in Course {self.course_id}>'
