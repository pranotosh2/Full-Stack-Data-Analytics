"""
Interactive Analytics Dashboard using Streamlit
Provides real-time visualization of platform analytics
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
import sys

# Add backend to path for imports
backend_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, backend_path)

from app import create_app
from app.models import db, User, Course, Enrollment, Assignment, Submission, AnalyticsEvent, CourseReview

# Configure Streamlit page
st.set_page_config(
    page_title="DAMP Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Flask app for database access
app = create_app(os.getenv('FLASK_ENV') or 'development')

def get_platform_overview():
    """Get platform overview metrics"""
    with app.app_context():
        # User statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        students = User.query.filter_by(role='student', is_active=True).count()
        mentors = User.query.filter_by(role='mentor', is_active=True, is_approved=True).count()
        pending_mentors = User.query.filter_by(role='mentor', is_approved=False).count()

        # Course statistics
        total_courses = Course.query.count()
        active_courses = Course.query.filter_by(is_active=True).count()

        # Enrollment statistics
        total_enrollments = Enrollment.query.count()
        completed_enrollments = Enrollment.query.filter_by(is_completed=True).count()
        completion_rate = (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0

        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_registrations = User.query.filter(User.created_at >= thirty_days_ago).count()
        recent_enrollments = Enrollment.query.filter(Enrollment.enrollment_date >= thirty_days_ago).count()

        return {
            'users': {
                'total': total_users,
                'active': active_users,
                'students': students,
                'mentors': mentors,
                'pending_mentors': pending_mentors
            },
            'courses': {
                'total': total_courses,
                'active': active_courses
            },
            'enrollments': {
                'total': total_enrollments,
                'completed': completed_enrollments,
                'completion_rate': completion_rate
            },
            'recent_activity': {
                'registrations_30d': recent_registrations,
                'enrollments_30d': recent_enrollments
            }
        }

def get_user_growth_data():
    """Get user registration trends over time"""
    with app.app_context():
        # Get monthly user registrations for the last 12 months
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)

        monthly_registrations = db.session.query(
            db.func.extract('year', User.created_at).label('year'),
            db.func.extract('month', User.created_at).label('month'),
            db.func.count(User.id).label('count')
        ).filter(
            User.created_at >= twelve_months_ago
        ).group_by(
            db.func.extract('year', User.created_at),
            db.func.extract('month', User.created_at)
        ).order_by(
            db.func.extract('year', User.created_at),
            db.func.extract('month', User.created_at)
        ).all()

        # Format the data
        growth_data = []
        for row in monthly_registrations:
            growth_data.append({
                'year': int(row.year),
                'month': int(row.month),
                'registrations': row.count
            })

        return pd.DataFrame(growth_data)

def get_course_performance():
    """Get course performance analytics"""
    with app.app_context():
        courses = Course.query.filter_by(is_active=True).all()

        course_performance = []
        for course in courses:
            course_performance.append({
                'course_id': course.id,
                'title': course.title,
                'mentor': course.mentor.get_full_name(),
                'category': course.category,
                'difficulty': course.difficulty_level,
                'enrolled_students': course.get_enrolled_students_count(),
                'completion_rate': course.get_completion_rate(),
                'average_rating': course.get_average_rating(),
                'modules_count': course.get_modules_count()
            })

        return pd.DataFrame(course_performance)

def get_student_performance():
    """Get student performance data"""
    with app.app_context():
        # Get assignment submissions with grades
        submissions = db.session.query(
            Submission,
            User.first_name,
            User.last_name,
            Course.title.label('course_title'),
            Assignment.title.label('assignment_title'),
            Assignment.max_points
        ).join(User, Submission.student_id == User.id)\
         .join(Assignment, Submission.assignment_id == Assignment.id)\
         .join(Course, Assignment.course_id == Course.id)\
         .filter(Submission.grade.isnot(None))\
         .all()

        performance_data = []
        for sub, fname, lname, course_title, assignment_title, max_points in submissions:
            performance_data.append({
                'student_name': f"{fname} {lname}",
                'course_title': course_title,
                'assignment_title': assignment_title,
                'grade': float(sub.grade) if sub.grade else 0,
                'max_points': max_points,
                'percentage': (float(sub.grade) / max_points * 100) if sub.grade and max_points else 0,
                'is_late': sub.is_late,
                'submitted_at': sub.submitted_at
            })

        return pd.DataFrame(performance_data)

def get_mentor_effectiveness():
    """Get mentor effectiveness data"""
    with app.app_context():
        mentors = User.query.filter_by(role='mentor', is_approved=True, is_active=True).all()

        mentor_data = []
        for mentor in mentors:
            courses = Course.query.filter_by(mentor_id=mentor.id, is_active=True).all()

            total_enrollments = sum(len(course.enrollments) for course in courses)
            total_completed = sum(len([e for e in course.enrollments if e.is_completed]) for course in courses)

            completion_rate = (total_completed / total_enrollments * 100) if total_enrollments > 0 else 0
            avg_rating = np.mean([course.get_average_rating() for course in courses if course.get_average_rating() > 0]) if courses else 0

            mentor_data.append({
                'mentor_name': mentor.get_full_name(),
                'expertise': mentor.expertise,
                'courses_count': len(courses),
                'total_students': total_enrollments,
                'completion_rate': completion_rate,
                'avg_course_rating': avg_rating,
                'courses': [course.title for course in courses]
            })

        return pd.DataFrame(mentor_data)

def main():
    """Main Streamlit application"""

    # Sidebar navigation
    st.sidebar.title("📊 DAMP Analytics Dashboard")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Select Analytics View",
        ["🏠 Overview", "👥 User Analytics", "📚 Course Performance",
         "🎓 Student Performance", "👨‍🏫 Mentor Effectiveness", "📈 Trends"]
    )

    st.sidebar.markdown("---")
    st.sidebar.info("Real-time analytics for the Data Analytics Mentorship Platform")

    # Main content
    if page == "🏠 Overview":
        st.title("📊 Platform Overview")
        st.markdown("Real-time insights into platform performance and key metrics")

        # Get data
        overview = get_platform_overview()

        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Users",
                overview['users']['total'],
                f"{overview['users']['active']} active"
            )

        with col2:
            st.metric(
                "Active Courses",
                overview['courses']['active'],
                f"{overview['courses']['total']} total"
            )

        with col3:
            st.metric(
                "Total Enrollments",
                overview['enrollments']['total'],
                f"{overview['enrollments']['completed']} completed"
            )

        with col4:
            st.metric(
                "Completion Rate",
                ".1f",
                f"{overview['recent_activity']['enrollments_30d']} this month"
            )

        # User distribution
        st.subheader("👥 User Distribution")
        user_data = pd.DataFrame({
            'Role': ['Students', 'Mentors', 'Pending Mentors'],
            'Count': [
                overview['users']['students'],
                overview['users']['mentors'],
                overview['users']['pending_mentors']
            ]
        })

        fig_users = px.pie(user_data, values='Count', names='Role',
                          title='User Distribution by Role')
        st.plotly_chart(fig_users, use_container_width=True)

        # Recent activity
        st.subheader("📈 Recent Activity (Last 30 Days)")
        activity_data = pd.DataFrame({
            'Metric': ['New Registrations', 'New Enrollments'],
            'Count': [
                overview['recent_activity']['registrations_30d'],
                overview['recent_activity']['enrollments_30d']
            ]
        })

        fig_activity = px.bar(activity_data, x='Metric', y='Count',
                             title='Recent Activity Metrics')
        st.plotly_chart(fig_activity, use_container_width=True)

    elif page == "👥 User Analytics":
        st.title("👥 User Analytics")
        st.markdown("Detailed analysis of user growth and engagement")

        # User growth over time
        st.subheader("📈 User Registration Trends")
        growth_data = get_user_growth_data()

        if not growth_data.empty:
            # Create date column for plotting
            growth_data['date'] = pd.to_datetime(growth_data[['year', 'month']].assign(day=1))
            growth_data = growth_data.sort_values('date')

            fig_growth = px.line(growth_data, x='date', y='registrations',
                               title='Monthly User Registrations',
                               markers=True)
            fig_growth.update_layout(xaxis_title='Month', yaxis_title='New Users')
            st.plotly_chart(fig_growth, use_container_width=True)

            # Growth metrics
            total_registrations = growth_data['registrations'].sum()
            avg_monthly = growth_data['registrations'].mean()
            max_month = growth_data.loc[growth_data['registrations'].idxmax()]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Registrations", total_registrations)
            with col2:
                st.metric("Avg Monthly", ".1f")
            with col3:
                st.metric("Peak Month",
                         ".0f")
        else:
            st.info("No user registration data available")

    elif page == "📚 Course Performance":
        st.title("📚 Course Performance")
        st.markdown("Analytics on course effectiveness and student engagement")

        course_data = get_course_performance()

        if not course_data.empty:
            # Top courses by enrollment
            st.subheader("🎯 Top Courses by Enrollment")
            top_courses = course_data.nlargest(10, 'enrolled_students')
            fig_enrollment = px.bar(top_courses, x='enrolled_students', y='title',
                                  title='Course Enrollment Rankings',
                                  orientation='h')
            fig_enrollment.update_layout(yaxis_title='Course', xaxis_title='Enrolled Students')
            st.plotly_chart(fig_enrollment, use_container_width=True)

            # Completion rate analysis
            st.subheader("📊 Course Completion Rates")
            completion_data = course_data[course_data['enrolled_students'] > 0].copy()
            completion_data = completion_data.sort_values('completion_rate', ascending=False)

            fig_completion = px.bar(completion_data.head(10), x='completion_rate', y='title',
                                  title='Top Courses by Completion Rate',
                                  orientation='h')
            fig_completion.update_layout(yaxis_title='Course', xaxis_title='Completion Rate (%)')
            st.plotly_chart(fig_completion, use_container_width=True)

            # Category performance
            st.subheader("🏷️ Performance by Category")
            category_perf = course_data.groupby('category').agg({
                'enrolled_students': 'sum',
                'completion_rate': 'mean',
                'average_rating': 'mean'
            }).round(2).reset_index()

            col1, col2 = st.columns(2)

            with col1:
                fig_cat_completion = px.bar(category_perf, x='category', y='completion_rate',
                                          title='Avg Completion Rate by Category')
                st.plotly_chart(fig_cat_completion, use_container_width=True)

            with col2:
                fig_cat_rating = px.bar(category_perf, x='category', y='average_rating',
                                      title='Avg Rating by Category')
                st.plotly_chart(fig_cat_rating, use_container_width=True)

            # Detailed course table
            st.subheader("📋 Detailed Course Performance")
            st.dataframe(course_data.sort_values('enrolled_students', ascending=False))
        else:
            st.info("No course performance data available")

    elif page == "🎓 Student Performance":
        st.title("🎓 Student Performance")
        st.markdown("Analysis of student grades, progress, and learning outcomes")

        performance_data = get_student_performance()

        if not performance_data.empty:
            # Grade distribution
            st.subheader("📊 Grade Distribution")
            fig_grades = px.histogram(performance_data, x='percentage',
                                    title='Distribution of Assignment Grades',
                                    nbins=20)
            fig_grades.update_layout(xaxis_title='Grade Percentage', yaxis_title='Frequency')
            st.plotly_chart(fig_grades, use_container_width=True)

            # Performance by course
            st.subheader("📚 Performance by Course")
            course_avg = performance_data.groupby('course_title')['percentage'].agg(['mean', 'count']).round(2)
            course_avg = course_avg.reset_index().rename(columns={'mean': 'avg_grade', 'count': 'submissions'})

            fig_course_perf = px.bar(course_avg, x='course_title', y='avg_grade',
                                   title='Average Grade by Course')
            fig_course_perf.update_layout(xaxis_title='Course', yaxis_title='Average Grade (%)')
            st.plotly_chart(fig_course_perf, use_container_width=True)

            # Late submission analysis
            st.subheader("⏰ Late Submission Analysis")
            late_stats = performance_data.groupby('is_late')['percentage'].agg(['count', 'mean']).round(2)
            late_stats = late_stats.reset_index()

            col1, col2 = st.columns(2)

            with col1:
                fig_late_count = px.pie(late_stats, values='count', names='is_late',
                                      title='Late vs On-time Submissions')
                st.plotly_chart(fig_late_count, use_container_width=True)

            with col2:
                fig_late_perf = px.bar(late_stats, x='is_late', y='mean',
                                     title='Average Grade: Late vs On-time')
                fig_late_perf.update_layout(xaxis_title='Late Submission', yaxis_title='Average Grade (%)')
                st.plotly_chart(fig_late_perf, use_container_width=True)

            # Top performers
            st.subheader("🏆 Top Performing Students")
            student_avg = performance_data.groupby('student_name')['percentage'].agg(['mean', 'count']).round(2)
            student_avg = student_avg[student_avg['count'] >= 2]  # At least 2 submissions
            top_students = student_avg.nlargest(10, 'mean').reset_index()

            fig_top_students = px.bar(top_students, x='mean', y='student_name',
                                    title='Top Performing Students',
                                    orientation='h')
            fig_top_students.update_layout(xaxis_title='Average Grade (%)', yaxis_title='Student')
            st.plotly_chart(fig_top_students, use_container_width=True)
        else:
            st.info("No student performance data available")

    elif page == "👨‍🏫 Mentor Effectiveness":
        st.title("👨‍🏫 Mentor Effectiveness")
        st.markdown("Analysis of mentor performance and teaching effectiveness")

        mentor_data = get_mentor_effectiveness()

        if not mentor_data.empty:
            # Mentor effectiveness overview
            st.subheader("📊 Mentor Effectiveness Overview")

            # Create effectiveness score
            mentor_data['effectiveness_score'] = (
                mentor_data['completion_rate'] * 0.5 +
                mentor_data['avg_course_rating'] * 20 * 0.3 +
                (mentor_data['courses_count'] / mentor_data['courses_count'].max()) * 100 * 0.2
            ).round(2)

            # Effectiveness rankings
            top_mentors = mentor_data.nlargest(10, 'effectiveness_score')

            fig_mentor_effective = px.bar(top_mentors, x='effectiveness_score', y='mentor_name',
                                        title='Top Mentors by Effectiveness Score',
                                        orientation='h')
            fig_mentor_effective.update_layout(xaxis_title='Effectiveness Score', yaxis_title='Mentor')
            st.plotly_chart(fig_mentor_effective, use_container_width=True)

            # Completion rate analysis
            st.subheader("🎯 Completion Rates by Mentor")
            fig_completion = px.bar(mentor_data.sort_values('completion_rate', ascending=False),
                                  x='completion_rate', y='mentor_name',
                                  title='Mentor Completion Rates',
                                  orientation='h')
            fig_completion.update_layout(xaxis_title='Completion Rate (%)', yaxis_title='Mentor')
            st.plotly_chart(fig_completion, use_container_width=True)

            # Student load vs effectiveness
            st.subheader("👥 Student Load vs Effectiveness")
            fig_load = px.scatter(mentor_data, x='total_students', y='effectiveness_score',
                                text='mentor_name', size='courses_count',
                                title='Mentor Workload vs Effectiveness')
            fig_load.update_layout(xaxis_title='Total Students', yaxis_title='Effectiveness Score')
            st.plotly_chart(fig_load, use_container_width=True)

            # Detailed mentor table
            st.subheader("📋 Detailed Mentor Performance")
            display_cols = ['mentor_name', 'expertise', 'courses_count', 'total_students',
                          'completion_rate', 'avg_course_rating', 'effectiveness_score']
            st.dataframe(mentor_data[display_cols].sort_values('effectiveness_score', ascending=False))
        else:
            st.info("No mentor effectiveness data available")

    elif page == "📈 Trends":
        st.title("📈 Trends & Insights")
        st.markdown("Time-based analysis and trend identification")

        # Get time-series data
        growth_data = get_user_growth_data()

        if not growth_data.empty:
            st.subheader("📊 User Growth Trends")

            # Cumulative growth
            growth_data['date'] = pd.to_datetime(growth_data[['year', 'month']].assign(day=1))
            growth_data = growth_data.sort_values('date')
            growth_data['cumulative_users'] = growth_data['registrations'].cumsum()

            col1, col2 = st.columns(2)

            with col1:
                fig_monthly = px.line(growth_data, x='date', y='registrations',
                                    title='Monthly Registrations', markers=True)
                fig_monthly.update_layout(xaxis_title='Month', yaxis_title='New Users')
                st.plotly_chart(fig_monthly, use_container_width=True)

            with col2:
                fig_cumulative = px.line(growth_data, x='date', y='cumulative_users',
                                       title='Cumulative User Growth', markers=True)
                fig_cumulative.update_layout(xaxis_title='Month', yaxis_title='Total Users')
                st.plotly_chart(fig_cumulative, use_container_width=True)

        # Platform health indicators
        st.subheader("🏥 Platform Health Indicators")
        overview = get_platform_overview()

        health_metrics = pd.DataFrame({
            'Metric': ['User Retention Rate', 'Course Utilization', 'Mentor Approval Rate', 'Completion Rate'],
            'Value': [
                (overview['users']['active'] / overview['users']['total'] * 100) if overview['users']['total'] > 0 else 0,
                (overview['enrollments']['total'] / overview['courses']['active']) if overview['courses']['active'] > 0 else 0,
                (overview['users']['mentors'] / (overview['users']['mentors'] + overview['users']['pending_mentors']) * 100) if (overview['users']['mentors'] + overview['users']['pending_mentors']) > 0 else 0,
                overview['enrollments']['completion_rate']
            ],
            'Status': ['Good', 'Good', 'Good', 'Good']  # Could be dynamic based on thresholds
        })

        fig_health = px.bar(health_metrics, x='Metric', y='Value',
                           title='Platform Health Indicators',
                           color='Status')
        fig_health.update_layout(xaxis_title='Metric', yaxis_title='Value (%)')
        st.plotly_chart(fig_health, use_container_width=True)

if __name__ == "__main__":
    main()
