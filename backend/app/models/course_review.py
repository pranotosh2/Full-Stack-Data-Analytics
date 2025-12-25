"""
Course review model for student feedback
"""
from datetime import datetime
from .. import db

class CourseReview(db.Model):
    __tablename__ = 'course_reviews'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('course_id', 'student_id', name='unique_course_student_review'),
    )

    def __init__(self, course_id, student_id, rating, review_text=None):
        self.course_id = course_id
        self.student_id = student_id
        self.rating = rating
        self.review_text = review_text

    def to_dict(self, include_course=False, include_student=False):
        """Convert review object to dictionary for API responses"""
        review_dict = {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'rating': self.rating,
            'review_text': self.review_text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_course and self.course:
            review_dict['course'] = {
                'id': self.course.id,
                'title': self.course.title
            }

        if include_student and self.student:
            review_dict['student'] = {
                'id': self.student.id,
                'first_name': self.student.first_name,
                'last_name': self.student.last_name
            }

        return review_dict

    def __repr__(self):
        return f'<CourseReview Course {self.course_id} by Student {self.student_id} - Rating {self.rating}>'
