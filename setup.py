#!/usr/bin/env python3
"""
Data Analytics Mentorship Platform - Setup Script
This script helps initialize the database with sample data for development
"""
import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def create_sample_data():
    """Create sample data for development and testing"""
    from backend.app import create_app
    from backend.app.models import db, User, Course, Module, Assignment

    app = create_app('development')

    with app.app_context():
        # Create all tables
        db.create_all()

        # Create admin user
        admin = User(
            username='admin1',
            email='admin@damp.com',
            password='password123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        admin.set_password('password123')
        db.session.add(admin)

        # Create sample mentors
        mentor1 = User(
            username='mentor1',
            email='mentor1@damp.com',
            password='password123',
            first_name='John',
            last_name='Smith',
            role='mentor',
            expertise='Data Science',
            bio='Experienced data scientist with 5+ years in the field'
        )
        mentor1.set_password('password123')
        mentor1.is_approved = True
        db.session.add(mentor1)

        mentor2 = User(
            username='mentor2',
            email='mentor2@damp.com',
            password='password123',
            first_name='Sarah',
            last_name='Johnson',
            role='mentor',
            expertise='Machine Learning',
            bio='ML engineer specializing in predictive analytics'
        )
        mentor2.set_password('password123')
        mentor2.is_approved = True
        db.session.add(mentor2)

        # Create sample students
        student1 = User(
            username='student1',
            email='student1@damp.com',
            password='password123',
            first_name='Alice',
            last_name='Brown',
            role='student'
        )
        student1.set_password('password123')
        db.session.add(student1)

        student2 = User(
            username='student2',
            email='student2@damp.com',
            password='password123',
            first_name='Bob',
            last_name='Wilson',
            role='student'
        )
        student2.set_password('password123')
        db.session.add(student2)

        # Create sample courses
        course1 = Course(
            title='Introduction to Data Analytics',
            description='Learn the fundamentals of data analytics using Python and SQL',
            mentor_id=1,  # mentor1
            category='Data Analytics',
            difficulty_level='beginner',
            duration_hours=20,
            price=49.99,
            prerequisites='Basic programming knowledge',
            learning_objectives='Understand data analysis concepts, work with datasets, create visualizations'
        )
        db.session.add(course1)

        course2 = Course(
            title='Advanced Machine Learning',
            description='Deep dive into machine learning algorithms and their applications',
            mentor_id=2,  # mentor2
            category='Machine Learning',
            difficulty_level='advanced',
            duration_hours=40,
            price=99.99,
            prerequisites='Python, Statistics, Linear Algebra',
            learning_objectives='Master ML algorithms, model evaluation, deployment strategies'
        )
        db.session.add(course2)

        course3 = Course(
            title='SQL for Data Analysis',
            description='Master SQL queries for data manipulation and analysis',
            mentor_id=1,  # mentor1
            category='Database',
            difficulty_level='intermediate',
            duration_hours=15,
            price=29.99,
            prerequisites='Basic SQL knowledge',
            learning_objectives='Complex queries, data warehousing, optimization techniques'
        )
        db.session.add(course3)

        db.session.commit()

        # Create sample modules for course1
        module1 = Module(
            course_id=1,
            title='Getting Started with Python',
            description='Introduction to Python programming for data analysis',
            order_index=1,
            content_type='video',
            duration_minutes=45
        )
        db.session.add(module1)

        module2 = Module(
            course_id=1,
            title='Data Manipulation with Pandas',
            description='Learn to work with data using Pandas library',
            order_index=2,
            content_type='notebook',
            duration_minutes=60
        )
        db.session.add(module2)

        # Create sample assignments
        assignment1 = Assignment(
            course_id=1,
            module_id=2,
            title='Data Cleaning Exercise',
            description='Clean and prepare a dataset for analysis',
            assignment_type='homework',
            max_points=100,
            submission_instructions='Submit your Jupyter notebook with the cleaned dataset'
        )
        db.session.add(assignment1)

        db.session.commit()

        print("✅ Sample data created successfully!")
        print("\n📊 Created:")
        print("- 1 Admin user (admin1/password123)")
        print("- 2 Mentor users (mentor1 & mentor2)")
        print("- 2 Student users (student1 & student2)")
        print("- 3 Sample courses with modules and assignments")

        print("\n🔗 You can now:")
        print("- Start the backend: cd backend && python run.py")
        print("- Start the frontend: cd frontend && npm start")
        print("- Access the application at http://localhost:3000")
        print("- Login with any of the created users")

if __name__ == '__main__':
    print("🚀 Setting up Data Analytics Mentorship Platform...")
    print("This will create sample data for development and testing.\n")

    try:
        create_sample_data()
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\nMake sure:")
        print("- PostgreSQL is running")
        print("- Database connection is configured in backend/.env")
        print("- All dependencies are installed")
        sys.exit(1)
