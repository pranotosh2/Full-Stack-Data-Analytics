"""
Student Performance Analysis Script
Analyzes student grades, progress, and learning patterns
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/damp_db')
engine = create_engine(DATABASE_URL)

def get_student_performance_data():
    """Fetch student performance data from database"""
    query = """
    SELECT
        s.id as student_id,
        s.first_name || ' ' || s.last_name as student_name,
        c.id as course_id,
        c.title as course_title,
        c.category,
        c.difficulty_level,
        e.enrollment_date,
        e.completion_percentage,
        e.is_completed,
        e.completion_date,
        a.id as assignment_id,
        a.title as assignment_title,
        a.assignment_type,
        a.max_points,
        sub.grade,
        sub.submitted_at,
        sub.is_late,
        m.id as mentor_id,
        m.first_name || ' ' || m.last_name as mentor_name
    FROM users s
    JOIN enrollments e ON s.id = e.student_id
    JOIN courses c ON e.course_id = c.id
    JOIN users m ON c.mentor_id = m.id
    LEFT JOIN assignments a ON c.id = a.course_id
    LEFT JOIN submissions sub ON a.id = sub.assignment_id AND s.id = sub.student_id
    WHERE s.role = 'student' AND s.is_active = true AND c.is_active = true
    ORDER BY s.id, c.id, a.id
    """

    return pd.read_sql(query, engine)

def calculate_performance_metrics(df):
    """Calculate various student performance metrics"""
    print("=== STUDENT PERFORMANCE METRICS ===\n")

    # Overall grade distribution
    graded_submissions = df.dropna(subset=['grade'])

    if len(graded_submissions) == 0:
        print("No graded submissions found.")
        return None

    print(f"Total submissions: {len(df)}")
    print(f"Graded submissions: {len(graded_submissions)}")
    print(".1f"
    print(f"Average grade: {graded_submissions['grade'].mean():.2f}")
    print(f"Median grade: {graded_submissions['grade'].median():.2f}")
    print(f"Highest grade: {graded_submissions['grade'].max()}")
    print(f"Lowest grade: {graded_submissions['grade'].min()}")

    # Grade distribution
    print("\n--- Grade Distribution ---")
    grade_ranges = pd.cut(graded_submissions['grade'],
                         bins=[0, 60, 70, 80, 90, 100],
                         labels=['F (0-59)', 'D (60-69)', 'C (70-79)', 'B (80-89)', 'A (90-100)'])
    grade_dist = grade_ranges.value_counts().sort_index()
    for grade_range, count in grade_dist.items():
        percentage = (count / len(graded_submissions) * 100)
        print(".1f")

    return graded_submissions

def analyze_performance_by_course(df):
    """Analyze performance variations by course"""
    print("\n=== PERFORMANCE BY COURSE ===\n")

    course_performance = df.dropna(subset=['grade']).groupby(['course_title', 'category']).agg({
        'grade': ['mean', 'median', 'std', 'count'],
        'is_late': 'sum',
        'student_id': 'nunique'
    }).round(2)

    course_performance.columns = ['avg_grade', 'median_grade', 'std_dev', 'submissions', 'late_submissions', 'unique_students']
    course_performance['late_rate'] = (course_performance['late_submissions'] / course_performance['submissions'] * 100).round(2)

    print("Top performing courses:")
    top_courses = course_performance.sort_values('avg_grade', ascending=False).head(10)
    print(top_courses[['avg_grade', 'submissions', 'late_rate']])

    print("\nCourses with highest late submission rates:")
    late_courses = course_performance[course_performance['submissions'] >= 5].sort_values('late_rate', ascending=False).head(5)
    print(late_courses[['avg_grade', 'late_rate', 'submissions']])

    return course_performance

def analyze_performance_by_student(df):
    """Analyze individual student performance patterns"""
    print("\n=== INDIVIDUAL STUDENT PERFORMANCE ===\n")

    student_performance = df.dropna(subset=['grade']).groupby('student_id').agg({
        'grade': ['mean', 'median', 'count'],
        'course_id': 'nunique',
        'is_late': ['sum', 'mean'],
        'is_completed': 'sum'
    }).round(2)

    student_performance.columns = ['avg_grade', 'median_grade', 'total_submissions',
                                 'courses_enrolled', 'late_submissions', 'late_rate',
                                 'courses_completed']

    student_performance['completion_rate'] = (
        student_performance['courses_completed'] /
        student_performance['courses_enrolled'] * 100
    ).round(2)

    print(f"Total active students: {len(student_performance)}")
    print(".2f")
    print(".2f")

    # Top performers
    print("\n--- Top Performing Students ---")
    top_students = student_performance[student_performance['total_submissions'] >= 3].sort_values('avg_grade', ascending=False).head(5)
    print(top_students[['avg_grade', 'total_submissions', 'courses_completed', 'late_rate']])

    # Students needing attention (low grades, high late submissions)
    print("\n--- Students Needing Attention ---")
    struggling_students = student_performance[
        (student_performance['avg_grade'] < 70) &
        (student_performance['total_submissions'] >= 2)
    ].sort_values('avg_grade').head(5)
    print(struggling_students[['avg_grade', 'total_submissions', 'late_rate', 'completion_rate']])

    return student_performance

def analyze_performance_trends(df):
    """Analyze performance trends over time"""
    print("\n=== PERFORMANCE TRENDS OVER TIME ===\n")

    # Convert dates and create time-based analysis
    df['enrollment_month'] = pd.to_datetime(df['enrollment_date']).dt.to_period('M')

    monthly_performance = df.dropna(subset=['grade']).groupby('enrollment_month').agg({
        'grade': ['mean', 'count'],
        'is_late': 'mean',
        'is_completed': 'mean'
    }).round(2)

    monthly_performance.columns = ['avg_grade', 'submissions', 'late_rate', 'completion_rate']
    monthly_performance['late_rate'] = (monthly_performance['late_rate'] * 100).round(2)
    monthly_performance['completion_rate'] = (monthly_performance['completion_rate'] * 100).round(2)

    print("Monthly performance trends:")
    print(monthly_performance.tail(6))  # Last 6 months

    return monthly_performance

def create_performance_visualizations(df):
    """Create visualizations for performance analysis"""
    sns.set_style("whitegrid")

    # Filter for graded submissions
    graded_df = df.dropna(subset=['grade'])

    if len(graded_df) == 0:
        print("No graded submissions available for visualization.")
        return

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # Grade distribution
    axes[0, 0].hist(graded_df['grade'], bins=20, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Distribution of Student Grades')
    axes[0, 0].set_xlabel('Grade')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].axvline(graded_df['grade'].mean(), color='red', linestyle='--', label='.2f')
    axes[0, 0].legend()

    # Performance by course category
    category_perf = graded_df.groupby('category')['grade'].mean().sort_values()
    category_perf.plot(kind='barh', ax=axes[0, 1])
    axes[0, 1].set_title('Average Grade by Course Category')
    axes[0, 1].set_xlabel('Average Grade')

    # Performance by difficulty level
    difficulty_perf = graded_df.groupby('difficulty_level')['grade'].mean()
    difficulty_perf.plot(kind='bar', ax=axes[1, 0], rot=45)
    axes[1, 0].set_title('Average Grade by Difficulty Level')
    axes[1, 0].set_ylabel('Average Grade')

    # Late submission analysis
    late_by_category = graded_df.groupby('category')['is_late'].mean() * 100
    late_by_category.sort_values().plot(kind='barh', ax=axes[1, 1])
    axes[1, 1].set_title('Late Submission Rate by Category (%)')
    axes[1, 1].set_xlabel('Late Submission Rate (%)')

    plt.tight_layout()
    plt.savefig('student_performance_analysis.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved as 'student_performance_analysis.png'")

def generate_performance_report(df):
    """Generate comprehensive performance report"""
    graded_df = df.dropna(subset=['grade'])

    report = {
        'generated_at': datetime.now().isoformat(),
        'total_students': df['student_id'].nunique(),
        'total_submissions': len(df),
        'graded_submissions': len(graded_df),
        'overall_average_grade': graded_df['grade'].mean() if len(graded_df) > 0 else 0,
        'grade_distribution': {
            'A (90-100)': len(graded_df[graded_df['grade'] >= 90]),
            'B (80-89)': len(graded_df[(graded_df['grade'] >= 80) & (graded_df['grade'] < 90)]),
            'C (70-79)': len(graded_df[(graded_df['grade'] >= 70) & (graded_df['grade'] < 80)]),
            'D (60-69)': len(graded_df[(graded_df['grade'] >= 60) & (graded_df['grade'] < 70)]),
            'F (0-59)': len(graded_df[graded_df['grade'] < 60])
        },
        'late_submission_rate': (graded_df['is_late'].sum() / len(graded_df) * 100) if len(graded_df) > 0 else 0,
        'top_performing_categories': graded_df.groupby('category')['grade'].mean().sort_values(ascending=False).head(3).to_dict(),
        'performance_insights': {
            'high_performers': len(graded_df[graded_df['grade'] >= 90]),
            'at_risk_students': len(graded_df[graded_df['grade'] < 70]),
            'consistent_late_submitters': len(graded_df[graded_df['is_late'] == True])
        }
    }

    # Save report
    import json
    with open('student_performance_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print("
Performance report saved as 'student_performance_report.json'")
    return report

def main():
    """Main analysis function"""
    print("Fetching student performance data...")
    df = get_student_performance_data()

    if df.empty:
        print("No data found. Please check database connection and data.")
        return

    print(f"Loaded {len(df)} records for {df['student_id'].nunique()} students")

    # Perform analyses
    graded_df = calculate_performance_metrics(df)
    if graded_df is None:
        return

    analyze_performance_by_course(df)
    analyze_performance_by_student(df)
    analyze_performance_trends(df)

    # Create visualizations
    create_performance_visualizations(df)

    # Generate report
    generate_performance_report(df)

    print("\n=== ANALYSIS COMPLETE ===")
    print("Files generated:")
    print("- student_performance_analysis.png (visualizations)")
    print("- student_performance_report.json (summary report)")

if __name__ == "__main__":
    main()
