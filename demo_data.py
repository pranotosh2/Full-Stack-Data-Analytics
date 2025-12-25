#!/usr/bin/env python3
"""
Generate demo data for the DAMP platform analytics dashboard
"""
import random
from datetime import datetime, timedelta
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def generate_demo_data():
    """Generate sample data for demonstration"""
    # Set up environment for testing with SQLite first
    os.environ['DATABASE_URL'] = 'sqlite:///test_damp.db'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret'

    # Change to backend directory for imports
    os.chdir(backend_path)

    from app import create_app, db
    from app.models.user import User
    from app.models.course import Course
    from app.models.enrollment import Enrollment
    from app.models.module import Module
    from app.models.assignment import Assignment
    from app.models.submission import Submission
    from app.models.course_review import CourseReview
    from app.models.analytics_event import AnalyticsEvent

    app = create_app('testing')

    with app.app_context():
        # Clear existing data
        db.session.query(Submission).delete()
        db.session.query(Assignment).delete()
        db.session.query(CourseReview).delete()
        db.session.query(Enrollment).delete()
        db.session.query(Module).delete()
        db.session.query(Course).delete()
        db.session.query(AnalyticsEvent).delete()
        db.session.query(User).delete()
        db.session.commit()

        print("🧹 Cleared existing data")

        # Create admin
        admin = User(
            username='admin1',
            email='admin@damp.com',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        admin.set_password('password123')
        admin.is_approved = True
        db.session.add(admin)

        # Create mentors
        mentors_data = [
            ('mentor1', 'John', 'Smith', 'Data Science'),
            ('mentor2', 'Sarah', 'Johnson', 'Machine Learning'),
            ('mentor3', 'Mike', 'Brown', 'Statistics'),
            ('mentor4', 'Emily', 'Davis', 'Data Visualization'),
            ('mentor5', 'Alex', 'Wilson', 'AI & Deep Learning')
        ]

        mentors = []
        for username, fname, lname, expertise in mentors_data:
            mentor = User(
                username=username,
                email=f'{username}@damp.com',
                first_name=fname,
                last_name=lname,
                role='mentor',
                expertise=expertise
            )
            mentor.set_password('password123')
            mentor.is_approved = True
            db.session.add(mentor)
            mentors.append(mentor)

        # Create students
        students_data = [
            ('alice', 'Alice', 'Thompson'),
            ('bob', 'Bob', 'Garcia'),
            ('carol', 'Carol', 'Martinez'),
            ('david', 'David', 'Lee'),
            ('emma', 'Emma', 'Taylor'),
            ('frank', 'Frank', 'Anderson'),
            ('grace', 'Grace', 'White'),
            ('henry', 'Henry', 'Clark'),
            ('iris', 'Iris', 'Rodriguez'),
            ('jack', 'Jack', 'Lewis')
        ]

        students = []
        for username, fname, lname in students_data:
            student = User(
                username=username,
                email=f'{username}@damp.com',
                first_name=fname,
                last_name=lname,
                role='student'
            )
            student.set_password('password123')
            db.session.add(student)
            students.append(student)

        db.session.commit()
        print("👥 Created users")

        # Create courses
        courses_data = [
            ('Introduction to Data Analytics', 'Python, SQL', 'beginner', 20, 49.99, 0),
            ('Advanced Machine Learning', 'Python, TensorFlow', 'advanced', 40, 99.99, 1),
            ('Data Visualization with Python', 'Matplotlib, Seaborn', 'intermediate', 15, 39.99, 3),
            ('Statistics for Data Science', 'R, Python', 'intermediate', 25, 59.99, 2),
            ('Deep Learning Fundamentals', 'PyTorch, Neural Networks', 'advanced', 35, 89.99, 4),
            ('SQL for Data Analysis', 'PostgreSQL, MySQL', 'beginner', 12, 29.99, 0),
            ('Big Data with Hadoop', 'Hadoop, Spark', 'advanced', 30, 79.99, 1),
            ('Time Series Analysis', 'Python, Forecasting', 'intermediate', 20, 49.99, 2)
        ]

        courses = []
        for title, desc, level, hours, price, mentor_idx in courses_data:
            course = Course(
                title=title,
                description=f'Comprehensive course on {desc}',
                mentor_id=mentors[mentor_idx].id,
                category=random.choice(['Data Analytics', 'Machine Learning', 'Database', 'Statistics']),
                difficulty_level=level,
                duration_hours=hours,
                price=price,
                enrollment_limit=random.randint(20, 50)
            )
            db.session.add(course)
            courses.append(course)

        db.session.commit()
        print("📚 Created courses")

        # Create enrollments with varying completion rates
        for student in students:
            # Each student enrolls in 2-5 random courses
            enrolled_courses = random.sample(courses, random.randint(2, 5))

            for course in enrolled_courses:
                enrollment = Enrollment(
                    student_id=student.id,
                    course_id=course.id,
                    enrollment_date=datetime.utcnow() - timedelta(days=random.randint(1, 180))
                )

                # Random completion based on course difficulty
                difficulty_multiplier = {'beginner': 0.8, 'intermediate': 0.6, 'advanced': 0.4}
                completion_chance = difficulty_multiplier.get(course.difficulty_level, 0.5)

                if random.random() < completion_chance:
                    enrollment.is_completed = True
                    enrollment.completion_percentage = 100.0
                    enrollment.completion_date = enrollment.enrollment_date + timedelta(days=random.randint(7, 90))
                else:
                    enrollment.completion_percentage = random.uniform(10, 90)

                db.session.add(enrollment)

        db.session.commit()
        print("📝 Created enrollments")

        # Create modules for each course
        for course in courses:
            num_modules = random.randint(3, 8)
            for i in range(num_modules):
                module = Module(
                    course_id=course.id,
                    title=f'Module {i+1}: {random.choice(["Fundamentals", "Advanced Concepts", "Practical Applications", "Case Studies", "Projects"])}',
                    description=f'Detailed content for module {i+1}',
                    order_index=i+1,
                    content_type=random.choice(['video', 'notebook', 'pdf', 'text']),
                    duration_minutes=random.randint(30, 120),
                    is_free=(i == 0)  # First module is free
                )
                db.session.add(module)

        db.session.commit()
        print("📖 Created modules")

        # Create assignments
        for course in courses:
            num_assignments = random.randint(2, 5)
            modules = Module.query.filter_by(course_id=course.id).all()

            for i in range(num_assignments):
                assignment = Assignment(
                    course_id=course.id,
                    module_id=random.choice(modules).id if modules else None,
                    title=f'Assignment {i+1}: {random.choice(["Data Analysis", "Model Building", "Visualization", "Report Writing"])}',
                    description=f'Complete this assignment to practice {course.category} concepts',
                    assignment_type=random.choice(['homework', 'project', 'quiz']),
                    max_points=random.randint(50, 100),
                    due_date=datetime.utcnow() + timedelta(days=random.randint(7, 30))
                )
                db.session.add(assignment)

                # Create submissions for enrolled students
                enrollments = Enrollment.query.filter_by(course_id=course.id).all()
                for enrollment in enrollments:
                    if random.random() < 0.8:  # 80% submission rate
                        submission = Submission(
                            assignment_id=assignment.id,
                            student_id=enrollment.student_id,
                            submission_content=f'Sample submission for {assignment.title}',
                            submitted_at=datetime.utcnow() - timedelta(days=random.randint(0, 7))
                        )

                        # Assign grades to some submissions
                        if random.random() < 0.7:  # 70% grading rate
                            submission.grade = random.uniform(60, 100)
                            submission.feedback = random.choice([
                                'Excellent work! Well done.',
                                'Good effort, but could use more detail.',
                                'Solid understanding of concepts.',
                                'Needs improvement in analysis.',
                                'Outstanding performance!'
                            ])

                        db.session.add(submission)

        db.session.commit()
        print("📝 Created assignments and submissions")

        # Create course reviews
        for course in courses:
            # 30-70% of enrolled students leave reviews
            enrollments = Enrollment.query.filter_by(course_id=course.id, is_completed=True).all()
            reviewers = random.sample(enrollments, max(1, int(len(enrollments) * random.uniform(0.3, 0.7))))

            for enrollment in reviewers:
                review = CourseReview(
                    course_id=course.id,
                    student_id=enrollment.student_id,
                    rating=random.randint(3, 5),  # Mostly positive reviews
                    review_text=random.choice([
                        'Great course! Learned a lot.',
                        'Excellent instructor and content.',
                        'Very comprehensive and well-structured.',
                        'Helpful assignments and clear explanations.',
                        'Highly recommended for beginners.'
                    ])
                )
                db.session.add(review)

        db.session.commit()
        print("⭐ Created course reviews")

        # Create analytics events
        events = ['course_viewed', 'assignment_submitted', 'module_completed', 'login', 'profile_updated']
        for _ in range(500):  # Generate 500 random events
            user = random.choice(students + mentors)
            event = AnalyticsEvent(
                user_id=user.id,
                event_type=random.choice(events),
                event_data={'source': 'demo_generation'},
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(event)

        db.session.commit()
        print("📊 Created analytics events")

        print("\n✅ Demo data generation complete!")
        print(f"   📊 {len(students)} students")
        print(f"   👨‍🏫 {len(mentors)} mentors")
        print(f"   📚 {len(courses)} courses")
        print(f"   📝 {Enrollment.query.count()} enrollments")
        print(f"   📖 {Module.query.count()} modules")
        print(f"   📋 {Assignment.query.count()} assignments")
        print(f"   📤 {Submission.query.count()} submissions")
        print(f"   ⭐ {CourseReview.query.count()} reviews")

        print("\n🚀 You can now run the analytics dashboard:")
        print("   python run_analytics.py")

if __name__ == '__main__':
    print("🎭 Generating demo data for DAMP Analytics Dashboard...")
    try:
        generate_demo_data()
    except Exception as e:
        print(f"❌ Error generating demo data: {e}")
        sys.exit(1)
