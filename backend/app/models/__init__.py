# Models package initialization
from .user import User
from .course import Course
from .enrollment import Enrollment
from .module import Module
from .assignment import Assignment
from .submission import Submission
from .analytics_event import AnalyticsEvent
from .course_review import CourseReview

__all__ = [
    'User', 'Course', 'Enrollment', 'Module', 'Assignment',
    'Submission', 'AnalyticsEvent', 'CourseReview'
]
