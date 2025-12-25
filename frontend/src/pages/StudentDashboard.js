import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Container, Row, Col, Card, Button, ProgressBar, Alert, Spinner } from 'react-bootstrap';
import { FaBook, FaCheckCircle, FaClock, FaStar } from 'react-icons/fa';

const StudentDashboard = () => {
  const [enrollments, setEnrollments] = useState([]);
  const [availableCourses, setAvailableCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      // Fetch enrolled courses
      const enrolledResponse = await axios.get('/api/courses?enrolled_only=true');
      setEnrollments(enrolledResponse.data.courses || []);

      // Fetch available courses (limit to 6 for dashboard)
      const availableResponse = await axios.get('/api/courses');
      setAvailableCourses(availableResponse.data.courses?.slice(0, 6) || []);

    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getProgressColor = (percentage) => {
    if (percentage >= 80) return 'success';
    if (percentage >= 60) return 'info';
    if (percentage >= 40) return 'warning';
    return 'danger';
  };

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <Spinner animation="border" size="lg" />
        <p className="mt-3">Loading your dashboard...</p>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      <Row className="mb-4">
        <Col>
          <h1 className="mb-3">Student Dashboard</h1>
          <p className="text-muted">Track your learning progress and discover new courses</p>
        </Col>
      </Row>

      {error && <Alert variant="danger">{error}</Alert>}

      {/* Enrolled Courses Section */}
      <Row className="mb-5">
        <Col>
          <h2 className="mb-3">
            <FaBook className="me-2" />
            My Courses ({enrollments.length})
          </h2>

          {enrollments.length === 0 ? (
            <Card className="text-center p-4">
              <Card.Body>
                <FaBook size={48} className="text-muted mb-3" />
                <h5>You haven't enrolled in any courses yet</h5>
                <p className="text-muted">Browse available courses below to start learning</p>
                <Button as={Link} to="/courses" variant="primary">
                  Browse Courses
                </Button>
              </Card.Body>
            </Card>
          ) : (
            <Row>
              {enrollments.map((enrollment) => (
                <Col md={6} lg={4} key={enrollment.id} className="mb-4">
                  <Card className="h-100">
                    <Card.Body className="d-flex flex-column">
                      <Card.Title className="mb-2">
                        {enrollment.course.title}
                      </Card.Title>

                      <div className="mb-3">
                        <small className="text-muted d-block">
                          Instructor: {enrollment.course.mentor.first_name} {enrollment.course.mentor.last_name}
                        </small>
                        <small className="text-muted d-block">
                          Category: {enrollment.course.category}
                        </small>
                      </div>

                      <div className="mb-3">
                        <div className="d-flex justify-content-between align-items-center mb-2">
                          <small>Progress</small>
                          <small>{enrollment.enrollment.completion_percentage || 0}%</small>
                        </div>
                        <ProgressBar
                          now={enrollment.enrollment.completion_percentage || 0}
                          variant={getProgressColor(enrollment.enrollment.completion_percentage || 0)}
                          className="mb-2"
                        />
                      </div>

                      <div className="mt-auto">
                        <Button
                          as={Link}
                          to={`/courses/${enrollment.course.id}`}
                          variant="primary"
                          className="w-100"
                        >
                          Continue Learning
                        </Button>
                      </div>
                    </Card.Body>
                  </Card>
                </Col>
              ))}
            </Row>
          )}
        </Col>
      </Row>

      {/* Available Courses Section */}
      <Row className="mb-4">
        <Col>
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h2>
              <FaStar className="me-2" />
              Recommended Courses
            </h2>
            <Button as={Link} to="/courses" variant="outline-primary">
              View All Courses
            </Button>
          </div>

          <Row>
            {availableCourses
              .filter(course => !enrollments.some(e => e.id === course.id))
              .slice(0, 3)
              .map((course) => (
              <Col md={6} lg={4} key={course.id} className="mb-4">
                <Card className="h-100">
                  <Card.Body className="d-flex flex-column">
                    <Card.Title className="mb-2">{course.title}</Card.Title>

                    <div className="mb-3">
                      <small className="text-muted d-block">
                        Instructor: {course.mentor.first_name} {course.mentor.last_name}
                      </small>
                      <small className="text-muted d-block">
                        Category: {course.category}
                      </small>
                      <small className="text-muted d-block">
                        Level: {course.difficulty_level}
                      </small>
                    </div>

                    <div className="mb-3">
                      <small className="text-muted d-block">
                        Duration: {course.duration_hours} hours
                      </small>
                      <small className="text-muted d-block">
                        Enrolled: {course.stats.enrolled_students} students
                      </small>
                    </div>

                    <div className="mt-auto">
                      <Button
                        as={Link}
                        to={`/courses/${course.id}`}
                        variant="outline-primary"
                        className="w-100 mb-2"
                      >
                        View Details
                      </Button>
                    </div>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Col>
      </Row>

      {/* Quick Stats */}
      <Row>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaBook size={32} className="text-primary mb-2" />
              <h4>{enrollments.length}</h4>
              <small className="text-muted">Enrolled Courses</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaCheckCircle size={32} className="text-success mb-2" />
              <h4>
                {enrollments.filter(e => e.enrollment.is_completed).length}
              </h4>
              <small className="text-muted">Completed Courses</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaClock size={32} className="text-warning mb-2" />
              <h4>
                {enrollments.filter(e => !e.enrollment.is_completed).length}
              </h4>
              <small className="text-muted">In Progress</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaStar size={32} className="text-info mb-2" />
              <h4>
                {Math.round(
                  enrollments.reduce((acc, e) =>
                    acc + (e.enrollment.completion_percentage || 0), 0
                  ) / Math.max(enrollments.length, 1)
                )}%
              </h4>
              <small className="text-muted">Avg Progress</small>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default StudentDashboard;
