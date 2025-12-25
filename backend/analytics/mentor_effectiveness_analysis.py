"""
Mentor Effectiveness Analysis Script
Evaluates mentor performance based on student outcomes and course metrics
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

def get_mentor_effectiveness_data():
    """Fetch mentor effectiveness data from database"""
    query = """
    SELECT
        m.id as mentor_id,
        m.first_name || ' ' || m.last_name as mentor_name,
        m.expertise,
        m.created_at as mentor_joined,
        c.id as course_id,
        c.title as course_title,
        c.category,
        c.difficulty_level,
        c.created_at as course_created,
        c.price,
        COUNT(DISTINCT e.student_id) as enrolled_students,
        COUNT(CASE WHEN e.is_completed = true THEN 1 END) as completed_students,
        ROUND(
            COUNT(CASE WHEN e.is_completed = true THEN 1 END)::decimal /
            NULLIF(COUNT(DISTINCT e.student_id), 0) * 100, 2
        ) as completion_rate,
        ROUND(AVG(r.rating), 2) as avg_course_rating,
        COUNT(r.id) as total_reviews,
        COUNT(a.id) as assignments_created,
        COUNT(s.id) as total_submissions,
        COUNT(CASE WHEN s.grade IS NOT NULL THEN 1 END) as graded_submissions,
        ROUND(AVG(s.grade), 2) as avg_assignment_score,
        COUNT(mod.id) as modules_created,
        ROUND(AVG(mod.duration_minutes), 2) as avg_module_duration
    FROM users m
    JOIN courses c ON m.id = c.mentor_id
    LEFT JOIN enrollments e ON c.id = e.course_id
    LEFT JOIN course_reviews r ON c.id = r.course_id
    LEFT JOIN assignments a ON c.id = a.course_id
    LEFT JOIN submissions s ON a.id = s.assignment_id
    LEFT JOIN modules mod ON c.id = mod.course_id
    WHERE m.role = 'mentor'
      AND m.is_approved = true
      AND m.is_active = true
      AND c.is_active = true
    GROUP BY m.id, m.first_name, m.last_name, m.expertise, m.created_at,
             c.id, c.title, c.category, c.difficulty_level, c.created_at, c.price
    ORDER BY m.id, c.created_at DESC
    """

    return pd.read_sql(query, engine)

def calculate_mentor_metrics(df):
    """Calculate comprehensive mentor effectiveness metrics"""
    print("=== MENTOR EFFECTIVENESS METRICS ===\n")

    # Aggregate by mentor
    mentor_summary = df.groupby(['mentor_id', 'mentor_name', 'expertise']).agg({
        'course_id': 'count',
        'enrolled_students': 'sum',
        'completed_students': 'sum',
        'completion_rate': 'mean',
        'avg_course_rating': 'mean',
        'total_reviews': 'sum',
        'assignments_created': 'sum',
        'graded_submissions': 'sum',
        'avg_assignment_score': 'mean',
        'modules_created': 'sum'
    }).round(2)

    mentor_summary = mentor_summary.reset_index()

    # Calculate weighted effectiveness score
    mentor_summary['effectiveness_score'] = (
        mentor_summary['completion_rate'] * 0.4 +  # 40% weight on completion
        mentor_summary['avg_course_rating'] * 10 * 0.3 +  # 30% weight on ratings (scaled)
        mentor_summary['avg_assignment_score'] * 0.3  # 30% weight on assignment scores
    ).round(2)

    print(f"Total mentors analyzed: {len(mentor_summary)}")
    print(f"Courses created: {mentor_summary['course_id'].sum()}")
    print(f"Total student enrollments: {mentor_summary['enrolled_students'].sum()}")
    print(".2f")

    return mentor_summary

def rank_mentors(mentor_summary):
    """Rank mentors by various metrics"""
    print("\n=== MENTOR RANKINGS ===\n")

    # Top mentors by effectiveness score
    print("--- Top Mentors by Overall Effectiveness ---")
    top_effective = mentor_summary.sort_values('effectiveness_score', ascending=False).head(10)
    for idx, row in top_effective.iterrows():
        print(".2f"
              ".1f"
              ".1f")

    # Top mentors by completion rate
    print("\n--- Top Mentors by Completion Rate ---")
    top_completion = mentor_summary[mentor_summary['enrolled_students'] >= 5].sort_values('completion_rate', ascending=False).head(5)
    for idx, row in top_completion.iterrows():
        print(".2f"
              ".0f")

    # Top mentors by student satisfaction
    print("\n--- Top Mentors by Student Satisfaction ---")
    top_rated = mentor_summary[mentor_summary['total_reviews'] >= 3].sort_values('avg_course_rating', ascending=False).head(5)
    for idx, row in top_rated.iterrows():
        print(".2f"
              ".0f")

    # Most productive mentors
    print("\n--- Most Productive Mentors ---")
    most_productive = mentor_summary.sort_values(['course_id', 'enrolled_students'], ascending=False).head(5)
    for idx, row in most_productive.iterrows():
        print(f"{row['mentor_name']}: {row['course_id']} courses, {row['enrolled_students']} students")

    return top_effective, top_completion, top_rated, most_productive

def analyze_course_performance_by_mentor(df):
    """Analyze course performance patterns by mentor"""
    print("\n=== COURSE PERFORMANCE BY MENTOR ===\n")

    # Course success metrics
    course_success = df.groupby(['mentor_name', 'course_title']).agg({
        'enrolled_students': 'first',
        'completion_rate': 'first',
        'avg_course_rating': 'first',
        'total_reviews': 'first'
    }).round(2)

    # Best performing courses
    print("--- Highest Rated Courses ---")
    best_courses = course_success[course_success['total_reviews'] >= 3].sort_values('avg_course_rating', ascending=False).head(10)
    for idx, row in best_courses.iterrows():
        print(".2f"
              ".1f")

    # Most successful courses (high completion + good ratings)
    course_success['success_score'] = (
        course_success['completion_rate'] * 0.6 +
        course_success['avg_course_rating'] * 20 * 0.4
    ).round(2)

    print("\n--- Most Successful Courses ---")
    successful_courses = course_success[course_success['enrolled_students'] >= 5].sort_values('success_score', ascending=False).head(10)
    for idx, row in successful_courses.iterrows():
        print(".2f"
              ".1f")

    return course_success

def analyze_mentor_workload_efficiency(df):
    """Analyze mentor workload and efficiency"""
    print("\n=== MENTOR WORKLOAD ANALYSIS ===\n")

    workload_df = df.groupby(['mentor_id', 'mentor_name']).agg({
        'course_id': 'count',
        'enrolled_students': 'sum',
        'graded_submissions': 'sum',
        'modules_created': 'sum',
        'assignments_created': 'sum'
    }).reset_index()

    # Calculate efficiency metrics
    workload_df['avg_students_per_course'] = (workload_df['enrolled_students'] / workload_df['course_id']).round(1)
    workload_df['grading_load'] = (workload_df['graded_submissions'] / workload_df['enrolled_students']).round(2)
    workload_df['content_density'] = (workload_df['modules_created'] / workload_df['course_id']).round(1)

    print("--- Workload Distribution ---")
    print(workload_df[['mentor_name', 'course_id', 'enrolled_students', 'avg_students_per_course']].sort_values('enrolled_students', ascending=False).head(10))

    print("\n--- Content Creation Efficiency ---")
    content_efficient = workload_df.sort_values('content_density', ascending=False).head(5)
    for idx, row in content_efficient.iterrows():
        print(".1f"
              ".1f")

    return workload_df

def create_mentor_visualizations(df, mentor_summary):
    """Create visualizations for mentor effectiveness"""
    sns.set_style("whitegrid")

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # Effectiveness score distribution
    axes[0, 0].hist(mentor_summary['effectiveness_score'], bins=15, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Distribution of Mentor Effectiveness Scores')
    axes[0, 0].set_xlabel('Effectiveness Score')
    axes[0, 0].set_ylabel('Number of Mentors')
    axes[0, 0].axvline(mentor_summary['effectiveness_score'].mean(), color='red', linestyle='--',
                       label='.1f')
    axes[0, 0].legend()

    # Completion rate vs Course rating scatter
    valid_data = mentor_summary.dropna(subset=['completion_rate', 'avg_course_rating'])
    if len(valid_data) > 0:
        axes[0, 1].scatter(valid_data['completion_rate'], valid_data['avg_course_rating'],
                          alpha=0.6, s=valid_data['enrolled_students']/10)
        axes[0, 1].set_title('Completion Rate vs Course Rating')
        axes[0, 1].set_xlabel('Completion Rate (%)')
        axes[0, 1].set_ylabel('Average Course Rating')

    # Top mentors by effectiveness
    top_mentors = mentor_summary.sort_values('effectiveness_score', ascending=False).head(10)
    top_mentors.plot(x='mentor_name', y='effectiveness_score', kind='barh', ax=axes[1, 0])
    axes[1, 0].set_title('Top 10 Mentors by Effectiveness Score')
    axes[1, 0].set_xlabel('Effectiveness Score')

    # Workload analysis
    workload_data = df.groupby('mentor_name')['enrolled_students'].sum().sort_values(ascending=False).head(10)
    workload_data.plot(kind='bar', ax=axes[1, 1], rot=45)
    axes[1, 1].set_title('Top 10 Mentors by Student Load')
    axes[1, 1].set_ylabel('Total Students')

    plt.tight_layout()
    plt.savefig('mentor_effectiveness_analysis.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved as 'mentor_effectiveness_analysis.png'")

def generate_mentor_report(df, mentor_summary):
    """Generate comprehensive mentor effectiveness report"""
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_mentors': len(mentor_summary),
        'total_courses': mentor_summary['course_id'].sum(),
        'total_students': mentor_summary['enrolled_students'].sum(),
        'average_effectiveness_score': mentor_summary['effectiveness_score'].mean(),
        'mentor_performance_distribution': {
            'high_performers': len(mentor_summary[mentor_summary['effectiveness_score'] >= 80]),
            'average_performers': len(mentor_summary[(mentor_summary['effectiveness_score'] >= 60) & (mentor_summary['effectiveness_score'] < 80)]),
            'needs_improvement': len(mentor_summary[mentor_summary['effectiveness_score'] < 60])
        },
        'top_mentors': mentor_summary.sort_values('effectiveness_score', ascending=False).head(5)[['mentor_name', 'effectiveness_score', 'enrolled_students']].to_dict('records'),
        'key_insights': {
            'avg_completion_rate': df['completion_rate'].mean(),
            'avg_course_rating': df['avg_course_rating'].mean(),
            'most_common_expertise': df['expertise'].mode().iloc[0] if len(df) > 0 else None,
            'avg_courses_per_mentor': mentor_summary['course_id'].mean()
        }
    }

    # Save report
    import json
    with open('mentor_effectiveness_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print("
Mentor effectiveness report saved as 'mentor_effectiveness_report.json'")
    return report

def main():
    """Main analysis function"""
    print("Fetching mentor effectiveness data...")
    df = get_mentor_effectiveness_data()

    if df.empty:
        print("No data found. Please check database connection and data.")
        return

    print(f"Loaded {len(df)} course records for {df['mentor_id'].nunique()} mentors")

    # Perform analyses
    mentor_summary = calculate_mentor_metrics(df)
    rank_mentors(mentor_summary)
    analyze_course_performance_by_mentor(df)
    analyze_mentor_workload_efficiency(df)

    # Create visualizations
    create_mentor_visualizations(df, mentor_summary)

    # Generate report
    generate_mentor_report(df, mentor_summary)

    print("\n=== ANALYSIS COMPLETE ===")
    print("Files generated:")
    print("- mentor_effectiveness_analysis.png (visualizations)")
    print("- mentor_effectiveness_report.json (summary report)")

if __name__ == "__main__":
    main()
