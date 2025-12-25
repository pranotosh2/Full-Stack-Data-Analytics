-- Data Analytics Mentorship Platform - Analytics Queries
-- Key Performance Indicators (KPIs) and analytical queries

-- ================================================================================
-- COURSE COMPLETION RATE ANALYSIS
-- ================================================================================

-- Overall course completion rate
SELECT
    COUNT(*) as total_enrollments,
    COUNT(CASE WHEN is_completed = true THEN 1 END) as completed_enrollments,
    ROUND(
        COUNT(CASE WHEN is_completed = true THEN 1 END)::decimal /
        NULLIF(COUNT(*), 0) * 100, 2
    ) as completion_rate_percentage
FROM enrollments;

-- Course completion rate by course
SELECT
    c.title as course_title,
    c.category,
    COUNT(e.*) as total_enrollments,
    COUNT(CASE WHEN e.is_completed = true THEN 1 END) as completed_enrollments,
    ROUND(
        COUNT(CASE WHEN e.is_completed = true THEN 1 END)::decimal /
        NULLIF(COUNT(e.*), 0) * 100, 2
    ) as completion_rate
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
WHERE c.is_active = true
GROUP BY c.id, c.title, c.category
ORDER BY completion_rate DESC;

-- ================================================================================
-- STUDENT PERFORMANCE ANALYSIS
-- ================================================================================

-- Average student performance by course
SELECT
    c.title as course_title,
    COUNT(DISTINCT e.student_id) as enrolled_students,
    COUNT(s.*) as total_submissions,
    COUNT(CASE WHEN s.grade IS NOT NULL THEN 1 END) as graded_submissions,
    ROUND(AVG(s.grade), 2) as average_grade,
    ROUND(
        COUNT(CASE WHEN s.grade IS NOT NULL THEN 1 END)::decimal /
        NULLIF(COUNT(s.*), 0) * 100, 2
    ) as grading_completion_rate
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
LEFT JOIN assignments a ON c.id = a.course_id
LEFT JOIN submissions s ON a.id = s.assignment_id
WHERE c.is_active = true
GROUP BY c.id, c.title
ORDER BY average_grade DESC;

-- Student performance distribution
SELECT
    CASE
        WHEN grade >= 90 THEN 'A (90-100)'
        WHEN grade >= 80 THEN 'B (80-89)'
        WHEN grade >= 70 THEN 'C (70-79)'
        WHEN grade >= 60 THEN 'D (60-69)'
        ELSE 'F (0-59)'
    END as grade_range,
    COUNT(*) as count,
    ROUND(COUNT(*)::decimal / SUM(COUNT(*)) OVER() * 100, 2) as percentage
FROM submissions
WHERE grade IS NOT NULL
GROUP BY
    CASE
        WHEN grade >= 90 THEN 'A (90-100)'
        WHEN grade >= 80 THEN 'B (80-89)'
        WHEN grade >= 70 THEN 'C (70-79)'
        WHEN grade >= 60 THEN 'D (60-69)'
        ELSE 'F (0-59)'
    END
ORDER BY grade_range;

-- ================================================================================
-- ENROLLMENT TRENDS ANALYSIS
-- ================================================================================

-- Monthly enrollment trends (last 12 months)
SELECT
    DATE_TRUNC('month', enrollment_date) as month,
    COUNT(*) as enrollments,
    COUNT(DISTINCT course_id) as unique_courses,
    COUNT(DISTINCT student_id) as unique_students
FROM enrollments
WHERE enrollment_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', enrollment_date)
ORDER BY month DESC;

-- Course enrollment popularity
SELECT
    c.title as course_title,
    c.category,
    c.difficulty_level,
    COUNT(e.*) as total_enrollments,
    COUNT(CASE WHEN e.is_completed = true THEN 1 END) as completed_enrollments,
    ROUND(AVG(r.rating), 2) as average_rating,
    COUNT(r.*) as total_reviews
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
LEFT JOIN course_reviews r ON c.id = r.course_id
WHERE c.is_active = true
GROUP BY c.id, c.title, c.category, c.difficulty_level
ORDER BY total_enrollments DESC
LIMIT 20;

-- ================================================================================
-- MENTOR EFFECTIVENESS ANALYSIS
-- ================================================================================

-- Mentor performance metrics
SELECT
    u.first_name || ' ' || u.last_name as mentor_name,
    u.expertise,
    COUNT(DISTINCT c.id) as courses_created,
    COUNT(DISTINCT e.student_id) as total_students_taught,
    COUNT(e.*) as total_enrollments,
    COUNT(CASE WHEN e.is_completed = true THEN 1 END) as completed_enrollments,
    ROUND(
        COUNT(CASE WHEN e.is_completed = true THEN 1 END)::decimal /
        NULLIF(COUNT(e.*), 0) * 100, 2
    ) as completion_rate,
    ROUND(AVG(r.rating), 2) as average_course_rating,
    COUNT(r.*) as total_reviews
FROM users u
LEFT JOIN courses c ON u.id = c.mentor_id
LEFT JOIN enrollments e ON c.id = e.course_id
LEFT JOIN course_reviews r ON c.id = r.course_id
WHERE u.role = 'mentor' AND u.is_approved = true AND c.is_active = true
GROUP BY u.id, u.first_name, u.last_name, u.expertise
ORDER BY completion_rate DESC;

-- Mentor course statistics
SELECT
    u.first_name || ' ' || u.last_name as mentor_name,
    c.title as course_title,
    c.category,
    COUNT(e.*) as enrollments,
    COUNT(CASE WHEN e.is_completed = true THEN 1 END) as completions,
    ROUND(AVG(r.rating), 2) as course_rating,
    COUNT(a.*) as assignments_created,
    COUNT(s.*) as total_submissions,
    COUNT(CASE WHEN s.grade IS NOT NULL THEN 1 END) as graded_submissions,
    ROUND(AVG(s.grade), 2) as average_assignment_score
FROM users u
JOIN courses c ON u.id = c.mentor_id
LEFT JOIN enrollments e ON c.id = e.course_id
LEFT JOIN course_reviews r ON c.id = r.course_id
LEFT JOIN assignments a ON c.id = a.course_id
LEFT JOIN submissions s ON a.id = s.assignment_id
WHERE u.role = 'mentor' AND u.is_approved = true AND c.is_active = true
GROUP BY u.id, u.first_name, u.last_name, c.id, c.title, c.category
ORDER BY mentor_name, course_title;

-- ================================================================================
-- PLATFORM ENGAGEMENT ANALYSIS
-- ================================================================================

-- User engagement by role (last 30 days)
SELECT
    u.role,
    COUNT(DISTINCT u.id) as active_users,
    COUNT(ae.*) as total_events,
    COUNT(DISTINCT DATE(ae.created_at)) as active_days,
    ROUND(COUNT(ae.*)::decimal / COUNT(DISTINCT u.id), 2) as avg_events_per_user
FROM users u
LEFT JOIN analytics_events ae ON u.id = ae.user_id
    AND ae.created_at >= CURRENT_DATE - INTERVAL '30 days'
WHERE u.is_active = true
GROUP BY u.role
ORDER BY role;

-- Most common events
SELECT
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users,
    DATE_TRUNC('day', created_at) as event_date
FROM analytics_events
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY event_type, DATE_TRUNC('day', created_at)
ORDER BY event_date DESC, event_count DESC;

-- ================================================================================
-- REVENUE AND BUSINESS METRICS
-- ================================================================================

-- Course revenue potential (assuming paid courses)
SELECT
    c.title as course_title,
    c.price,
    COUNT(e.*) as enrollments,
    (c.price * COUNT(e.*)) as potential_revenue,
    c.category,
    c.difficulty_level
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
WHERE c.is_active = true AND c.price > 0
GROUP BY c.id, c.title, c.price, c.category, c.difficulty_level
ORDER BY potential_revenue DESC;

-- Platform growth metrics
SELECT
    DATE_TRUNC('month', created_at) as month,
    COUNT(CASE WHEN role = 'student' THEN 1 END) as new_students,
    COUNT(CASE WHEN role = 'mentor' THEN 1 END) as new_mentors,
    COUNT(*) as total_new_users,
    SUM(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)) as cumulative_users
FROM users
WHERE created_at >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;

-- ================================================================================
-- COURSE CONTENT ANALYSIS
-- ================================================================================

-- Course content completeness
SELECT
    c.title as course_title,
    COUNT(m.*) as total_modules,
    COUNT(CASE WHEN m.content_type = 'video' THEN 1 END) as video_modules,
    COUNT(CASE WHEN m.content_type = 'pdf' THEN 1 END) as pdf_modules,
    COUNT(CASE WHEN m.content_type = 'notebook' THEN 1 END) as notebook_modules,
    COUNT(a.*) as assignments,
    ROUND(AVG(m.duration_minutes), 2) as avg_module_duration,
    c.duration_hours as expected_duration
FROM courses c
LEFT JOIN modules m ON c.id = m.course_id
LEFT JOIN assignments a ON c.id = a.course_id
WHERE c.is_active = true
GROUP BY c.id, c.title, c.duration_hours
ORDER BY total_modules DESC;

-- Assignment completion and grading analysis
SELECT
    c.title as course_title,
    a.title as assignment_title,
    a.assignment_type,
    COUNT(s.*) as submissions,
    COUNT(CASE WHEN s.grade IS NOT NULL THEN 1 END) as graded,
    ROUND(AVG(s.grade), 2) as average_score,
    COUNT(CASE WHEN s.is_late = true THEN 1 END) as late_submissions,
    ROUND(
        COUNT(CASE WHEN s.is_late = true THEN 1 END)::decimal /
        NULLIF(COUNT(s.*), 0) * 100, 2
    ) as late_submission_rate
FROM courses c
JOIN assignments a ON c.id = a.course_id
LEFT JOIN submissions s ON a.id = s.assignment_id
WHERE c.is_active = true
GROUP BY c.id, c.title, a.id, a.title, a.assignment_type
ORDER BY c.title, a.title;
