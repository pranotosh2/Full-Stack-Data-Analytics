#!/usr/bin/env python3
"""
Simple Streamlit Analytics Dashboard for DAMP
Shows sample data without requiring full Flask app setup
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="DAMP Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Generate sample data
def generate_sample_data():
    """Generate sample data for demonstration"""

    # Sample users
    users = pd.DataFrame({
        'user_id': range(1, 16),
        'username': [f'user{i}' for i in range(1, 16)],
        'role': ['student'] * 12 + ['mentor'] * 3,
        'is_active': [True] * 14 + [False] * 1,
        'created_at': [datetime.now() - timedelta(days=random.randint(1, 365)) for _ in range(15)]
    })

    # Sample courses
    courses = pd.DataFrame({
        'course_id': range(1, 9),
        'title': [
            'Introduction to Data Analytics',
            'Advanced Machine Learning',
            'Data Visualization with Python',
            'Statistics for Data Science',
            'Deep Learning Fundamentals',
            'SQL for Data Analysis',
            'Big Data with Hadoop',
            'Time Series Analysis'
        ],
        'category': ['Data Analytics', 'Machine Learning', 'Data Visualization',
                    'Statistics', 'Deep Learning', 'Database', 'Big Data', 'Time Series'],
        'difficulty': ['beginner', 'advanced', 'intermediate', 'intermediate',
                      'advanced', 'beginner', 'advanced', 'intermediate'],
        'enrolled_students': [random.randint(5, 25) for _ in range(8)],
        'completion_rate': [random.uniform(60, 95) for _ in range(8)],
        'avg_rating': [random.uniform(3.5, 5.0) for _ in range(8)]
    })

    # Sample enrollments
    enrollments = []
    for _, course in courses.iterrows():
        num_students = course['enrolled_students']
        for i in range(num_students):
            enrollments.append({
                'student_id': random.randint(1, 12),
                'course_id': course['course_id'],
                'enrollment_date': datetime.now() - timedelta(days=random.randint(1, 180)),
                'completion_percentage': random.uniform(0, 100),
                'is_completed': random.random() < course['completion_rate']/100
            })
    enrollments_df = pd.DataFrame(enrollments)

    # Sample assignments and grades
    assignments = []
    for _, enrollment in enrollments_df.iterrows():
        if random.random() < 0.7:  # 70% have submitted assignments
            assignments.append({
                'student_id': enrollment['student_id'],
                'course_id': enrollment['course_id'],
                'assignment_title': f'Assignment {random.randint(1, 5)}',
                'grade': random.uniform(60, 100) if random.random() < 0.8 else None,
                'is_late': random.random() < 0.2
            })
    assignments_df = pd.DataFrame(assignments)

    # User growth data
    dates = pd.date_range(start=datetime.now() - timedelta(days=365),
                         end=datetime.now(), freq='M')
    growth_data = pd.DataFrame({
        'date': dates,
        'registrations': [random.randint(5, 20) for _ in range(len(dates))]
    })
    growth_data['cumulative_users'] = growth_data['registrations'].cumsum()

    return users, courses, enrollments_df, assignments_df, growth_data

def main():
    """Main Streamlit application"""

    st.sidebar.title("📊 DAMP Analytics Dashboard")
    st.sidebar.markdown("---")

    # Load sample data
    users, courses, enrollments, assignments, growth_data = generate_sample_data()

    page = st.sidebar.radio(
        "Select Analytics View",
        ["🏠 Overview", "👥 User Analytics", "📚 Course Performance",
         "🎓 Student Performance", "📈 Trends"]
    )

    st.sidebar.markdown("---")
    st.sidebar.info("Real-time analytics for the Data Analytics Mentorship Platform")
    st.sidebar.success("✅ Sample data loaded successfully!")

    # Main content
    if page == "🏠 Overview":
        st.title("📊 Platform Overview")
        st.markdown("Real-time insights into platform performance and key metrics")

        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Users",
                len(users),
                f"{len(users[users['is_active']])} active"
            )

        with col2:
            st.metric(
                "Active Courses",
                len(courses),
                f"{len(courses)} total"
            )

        with col3:
            st.metric(
                "Total Enrollments",
                len(enrollments),
                f"{len(enrollments[enrollments['is_completed']])} completed"
            )

        with col4:
            completion_rate = (len(enrollments[enrollments['is_completed']]) / len(enrollments) * 100)
            st.metric(
                "Completion Rate",
                ".1f",
                "Sample data"
            )

        # User distribution
        st.subheader("👥 User Distribution")
        user_counts = users['role'].value_counts()
        user_data = pd.DataFrame({
            'Role': user_counts.index,
            'Count': user_counts.values
        })

        fig_users = px.pie(user_data, values='Count', names='Role',
                          title='User Distribution by Role')
        st.plotly_chart(fig_users, use_container_width=True)

        # Recent activity
        st.subheader("📈 Recent Activity (Last 30 Days)")
        recent_enrollments = len(enrollments[
            enrollments['enrollment_date'] > datetime.now() - timedelta(days=30)
        ])
        activity_data = pd.DataFrame({
            'Metric': ['New Enrollments (30d)', 'Active Courses'],
            'Count': [recent_enrollments, len(courses)]
        })

        fig_activity = px.bar(activity_data, x='Metric', y='Count',
                             title='Recent Activity Metrics')
        st.plotly_chart(fig_activity, use_container_width=True)

    elif page == "👥 User Analytics":
        st.title("👥 User Analytics")
        st.markdown("Detailed analysis of user growth and engagement")

        # User growth over time
        st.subheader("📈 User Registration Trends")
        fig_growth = px.line(growth_data, x='date', y='registrations',
                            title='Monthly User Registrations', markers=True)
        fig_growth.update_layout(xaxis_title='Month', yaxis_title='New Users')
        st.plotly_chart(fig_growth, use_container_width=True)

        # User role distribution
        st.subheader("👤 User Roles")
        role_dist = users['role'].value_counts()
        fig_roles = px.bar(x=role_dist.index, y=role_dist.values,
                          title='Users by Role')
        fig_roles.update_layout(xaxis_title='Role', yaxis_title='Count')
        st.plotly_chart(fig_roles, use_container_width=True)

    elif page == "📚 Course Performance":
        st.title("📚 Course Performance")
        st.markdown("Analytics on course effectiveness and student engagement")

        # Top courses by enrollment
        st.subheader("🎯 Top Courses by Enrollment")
        top_courses = courses.nlargest(10, 'enrolled_students')
        fig_enrollment = px.bar(top_courses, x='enrolled_students', y='title',
                              title='Course Enrollment Rankings',
                              orientation='h')
        fig_enrollment.update_layout(yaxis_title='Course', xaxis_title='Enrolled Students')
        st.plotly_chart(fig_enrollment, use_container_width=True)

        # Completion rate analysis
        st.subheader("📊 Course Completion Rates")
        completion_data = courses.sort_values('completion_rate', ascending=False)

        fig_completion = px.bar(completion_data, x='completion_rate', y='title',
                              title='Course Completion Rates',
                              orientation='h')
        fig_completion.update_layout(yaxis_title='Course', xaxis_title='Completion Rate (%)')
        st.plotly_chart(fig_completion, use_container_width=True)

        # Category performance
        st.subheader("🏷️ Performance by Category")
        category_perf = courses.groupby('category').agg({
            'enrolled_students': 'sum',
            'completion_rate': 'mean',
            'avg_rating': 'mean'
        }).round(2).reset_index()

        col1, col2 = st.columns(2)

        with col1:
            fig_cat_completion = px.bar(category_perf, x='category', y='completion_rate',
                                      title='Avg Completion Rate by Category')
            st.plotly_chart(fig_cat_completion, use_container_width=True)

        with col2:
            fig_cat_rating = px.bar(category_perf, x='category', y='avg_rating',
                                  title='Avg Rating by Category')
            st.plotly_chart(fig_cat_rating, use_container_width=True)

        # Course details table
        st.subheader("📋 Course Details")
        st.dataframe(courses)

    elif page == "🎓 Student Performance":
        st.title("🎓 Student Performance")
        st.markdown("Analysis of student grades, progress, and learning outcomes")

        # Grade distribution
        st.subheader("📊 Grade Distribution")
        graded_assignments = assignments.dropna(subset=['grade'])
        if not graded_assignments.empty:
            fig_grades = px.histogram(graded_assignments, x='grade',
                                    title='Distribution of Assignment Grades',
                                    nbins=20)
            fig_grades.update_layout(xaxis_title='Grade', yaxis_title='Frequency')
            st.plotly_chart(fig_grades, use_container_width=True)

            # Performance by course
            st.subheader("📚 Performance by Course")
            course_avg = graded_assignments.groupby('course_id')['grade'].agg(['mean', 'count']).round(2)
            course_avg = course_avg.reset_index().rename(columns={'mean': 'avg_grade', 'count': 'submissions'})

            # Add course titles
            course_avg = course_avg.merge(courses[['course_id', 'title']], on='course_id')

            fig_course_perf = px.bar(course_avg, x='title', y='avg_grade',
                                   title='Average Grade by Course')
            fig_course_perf.update_layout(xaxis_title='Course', yaxis_title='Average Grade')
            st.plotly_chart(fig_course_perf, use_container_width=True)

            # Late submission analysis
            st.subheader("⏰ Late Submission Analysis")
            late_stats = graded_assignments.groupby('is_late')['grade'].agg(['count', 'mean']).round(2)
            late_stats = late_stats.reset_index()

            col1, col2 = st.columns(2)

            with col1:
                fig_late_count = px.pie(late_stats, values='count', names='is_late',
                                      title='Late vs On-time Submissions')
                st.plotly_chart(fig_late_count, use_container_width=True)

            with col2:
                fig_late_perf = px.bar(late_stats, x='is_late', y='mean',
                                     title='Average Grade: Late vs On-time')
                fig_late_perf.update_layout(xaxis_title='Late Submission', yaxis_title='Average Grade')
                st.plotly_chart(fig_late_perf, use_container_width=True)

        else:
            st.info("No graded assignments available in sample data")

    elif page == "📈 Trends":
        st.title("📈 Trends & Insights")
        st.markdown("Time-based analysis and trend identification")

        # User growth trends
        st.subheader("📊 User Growth Trends")

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

        # Course performance trends
        st.subheader("📚 Course Performance Overview")
        perf_metrics = courses[['title', 'enrolled_students', 'completion_rate', 'avg_rating']]
        st.dataframe(perf_metrics.sort_values('enrolled_students', ascending=False))

        # Key insights
        st.subheader("💡 Key Insights")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Most Popular Course",
                     courses.loc[courses['enrolled_students'].idxmax(), 'title'][:20] + "...")

        with col2:
            st.metric("Highest Rated Course",
                     courses.loc[courses['avg_rating'].idxmax(), 'title'][:20] + "...")

        with col3:
            st.metric("Best Completion Rate",
                     ".1f")

if __name__ == "__main__":
    main()
