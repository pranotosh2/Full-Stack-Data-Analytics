"""
Analytics event model for tracking user activity
"""
from datetime import datetime
from .. import db

class AnalyticsEvent(db.Model):
    __tablename__ = 'analytics_events'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_type = db.Column(db.String(50), nullable=False)
    event_data = db.Column(db.JSON)
    session_id = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))  # Support IPv6
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id=None, event_type='', event_data=None,
                 session_id=None, ip_address=None, user_agent=None):
        self.user_id = user_id
        self.event_type = event_type
        self.event_data = event_data or {}
        self.session_id = session_id
        self.ip_address = ip_address
        self.user_agent = user_agent

    @staticmethod
    def log_event(user_id, event_type, event_data=None, session_id=None,
                  ip_address=None, user_agent=None):
        """Static method to log an analytics event"""
        event = AnalyticsEvent(
            user_id=user_id,
            event_type=event_type,
            event_data=event_data,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(event)
        return event

    def to_dict(self):
        """Convert event object to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'event_data': self.event_data,
            'session_id': self.session_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<AnalyticsEvent {self.event_type} by User {self.user_id}>'
