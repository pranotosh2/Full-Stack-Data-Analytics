"""
Module model for course content organization
"""
from datetime import datetime
from .. import db

class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(20), default='text')
    content_url = db.Column(db.String(500))
    duration_minutes = db.Column(db.Integer)
    is_free = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('course_id', 'order_index', name='unique_course_order'),
    )

    def __init__(self, course_id, title, order_index, description=None,
                 content_type='text', content_url=None, duration_minutes=None, is_free=False):
        self.course_id = course_id
        self.title = title
        self.order_index = order_index
        self.description = description
        self.content_type = content_type
        self.content_url = content_url
        self.duration_minutes = duration_minutes
        self.is_free = is_free

    def to_dict(self):
        """Convert module object to dictionary for API responses"""
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'order_index': self.order_index,
            'content_type': self.content_type,
            'content_url': self.content_url,
            'duration_minutes': self.duration_minutes,
            'is_free': self.is_free,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Module {self.title} (Course {self.course_id}, Order {self.order_index})>'
