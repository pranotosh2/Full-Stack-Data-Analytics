"""
Course Completion Analysis Script
Uses Pandas and SQLAlchemy to analyze course completion trends
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/damp_db')
engine = create_engine(DATABASE_URL)

def get_completion_data():
    """Fetch course completion data from database"""
    query = """
    SELECT
        c.id as course_id,
        c.title as course_title,
        c.category,
        c.difficulty_level,
        c.created_at as course_created,
        u.first_name || ' ' || u.last_name as mentor_name,
        e.student_id,
        e.enrollment_date,
        e.completion_percentage,
        e.is_completed,
        e.completion_date,
        COUNT(m.id) as total_modules
    FROM courses c
    JOIN users u ON c.mentor_id = u.id
    LEFT JOIN enrollments e ON c.id = e.course_id
    LEFT JOIN modules m ON c.id = m.course_id
    WHERE c.is_active = true
    GROUP BY c.id, c.title, c.category, c.difficulty_level, c.created_at,
             u.first_name, u.last_name, e.student_id, e.enrollment_date,
             e.completion_percentage, e.is_completed, e.completion_date
    ORDER BY c.created_at DESC, e.enrollment_date DESC
    """

    return pd.read_sql(query, engine)

def analyze_completion_rates(df):
    """Analyze course completion rates"""
    print("=== COURSE COMPLETION ANALYSIS ===\n")

    # Overall completion rate
    total_enrollments = len(df)
    completed_enrollments = len(df[df['is_completed'] == True])
    completion_rate = (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0

    print(".2f")
    print(f"Total Enrollments: {total_enrollments}")
    print(f"Completed Enrollments: {completed_enrollments}")
    print(".2f")

    # Completion rate by category
    print("\n--- Completion Rate by Category ---")
    category_completion = df.groupby('category').agg({
        'student_id': 'count',
        'is_completed': lambda x: (x.sum() / len(x) * 100)
    }).round(2)
    category_completion.columns = ['enrollments', 'completion_rate']
    print(category_completion.sort_values('completion_rate', ascending=False))

    # Completion rate by difficulty
    print("\n--- Completion Rate by Difficulty Level ---")
    difficulty_completion = df.groupby('difficulty_level').agg({
        'student_id': 'count',
        'is_completed': lambda x: (x.sum() / len(x) * 100)
    }).round(2)
    difficulty_completion.columns = ['enrollments', 'completion_rate']
    print(difficulty_completion.sort_values('completion_rate', ascending=False))

    return completion_rate, category_completion, difficulty_completion

def analyze_time_to_completion(df):
    """Analyze time taken to complete courses"""
    print("\n=== TIME TO COMPLETION ANALYSIS ===\n")

    # Filter completed enrollments
    completed_df = df[df['is_completed'] == True].copy()

    if len(completed_df) == 0:
        print("No completed enrollments found.")
        return

    # Calculate completion time in days
    completed_df['completion_time_days'] = (
        pd.to_datetime(completed_df['completion_date']) -
        pd.to_datetime(completed_df['enrollment_date'])
    ).dt.days

    # Remove outliers (negative days or extremely long times)
    completed_df = completed_df[
        (completed_df['completion_time_days'] >= 0) &
        (completed_df['completion_time_days'] <= 365)
    ]

    print(f"Average completion time: {completed_df['completion_time_days'].mean():.1f} days")
    print(f"Median completion time: {completed_df['completion_time_days'].median():.1f} days")
    print(f"Fastest completion: {completed_df['completion_time_days'].min()} days")
    print(f"Slowest completion: {completed_df['completion_time_days'].max()} days")

    # Completion time by category
    print("\n--- Average Completion Time by Category ---")
    category_time = completed_df.groupby('category')['completion_time_days'].agg([
        'mean', 'median', 'count'
    ]).round(1)
    print(category_time.sort_values('mean'))

    return completed_df['completion_time_days']

def create_completion_visualizations(df):
    """Create visualizations for completion analysis"""
    # Set style
    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 10))

    # Completion rate by category
    plt.subplot(2, 2, 1)
    category_completion = df.groupby('category')['is_completed'].mean() * 100
    category_completion.sort_values().plot(kind='barh')
    plt.title('Completion Rate by Category (%)')
    plt.xlabel('Completion Rate (%)')

    # Completion rate by difficulty
    plt.subplot(2, 2, 2)
    difficulty_completion = df.groupby('difficulty_level')['is_completed'].mean() * 100
    difficulty_completion.plot(kind='bar')
    plt.title('Completion Rate by Difficulty Level (%)')
    plt.ylabel('Completion Rate (%)')
    plt.xticks(rotation=45)

    # Enrollment distribution
    plt.subplot(2, 2, 3)
    course_enrollments = df.groupby('course_title')['student_id'].count().sort_values(ascending=False).head(10)
    course_enrollments.plot(kind='barh')
    plt.title('Top 10 Courses by Enrollment')
    plt.xlabel('Number of Enrollments')

    # Completion percentage distribution
    plt.subplot(2, 2, 4)
    plt.hist(df['completion_percentage'], bins=20, edgecolor='black')
    plt.title('Distribution of Completion Percentages')
    plt.xlabel('Completion Percentage')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.savefig('course_completion_analysis.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved as 'course_completion_analysis.png'")

def generate_completion_report(df):
    """Generate a comprehensive completion report"""
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_courses': df['course_id'].nunique(),
        'total_enrollments': len(df),
        'total_students': df['student_id'].nunique(),
        'overall_completion_rate': (df['is_completed'].sum() / len(df) * 100) if len(df) > 0 else 0,
        'top_performing_categories': df.groupby('category')['is_completed'].mean().sort_values(ascending=False).head(3).to_dict(),
        'completion_by_difficulty': df.groupby('difficulty_level')['is_completed'].mean().sort_values(ascending=False).to_dict(),
        'most_popular_courses': df.groupby('course_title')['student_id'].count().sort_values(ascending=False).head(5).to_dict()
    }

    # Save report to JSON
    import json
    with open('completion_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print("
Completion report saved as 'completion_report.json'")
    return report

def main():
    """Main analysis function"""
    print("Fetching course completion data...")
    df = get_completion_data()

    if df.empty:
        print("No data found. Please check database connection and data.")
        return

    print(f"Loaded {len(df)} enrollment records from {df['course_id'].nunique()} courses")

    # Perform analyses
    analyze_completion_rates(df)
    analyze_time_to_completion(df)

    # Create visualizations
    create_completion_visualizations(df)

    # Generate report
    generate_completion_report(df)

    print("\n=== ANALYSIS COMPLETE ===")
    print("Files generated:")
    print("- course_completion_analysis.png (visualizations)")
    print("- completion_report.json (summary report)")

if __name__ == "__main__":
    main()
