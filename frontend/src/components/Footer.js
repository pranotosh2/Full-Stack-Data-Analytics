import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-dark text-light mt-auto py-4">
      <Container>
        <Row>
          <Col md={6}>
            <h5>Data Analytics Mentorship Platform</h5>
            <p className="mb-0">
              Empowering the next generation of data analytics professionals
              through mentorship and hands-on learning.
            </p>
          </Col>
          <Col md={3}>
            <h6>Quick Links</h6>
            <ul className="list-unstyled">
              <li><a href="/courses" className="text-light text-decoration-none">Browse Courses</a></li>
              <li><a href="/dashboard" className="text-light text-decoration-none">Dashboard</a></li>
              <li><a href="/profile" className="text-light text-decoration-none">Profile</a></li>
            </ul>
          </Col>
          <Col md={3}>
            <h6>Contact</h6>
            <ul className="list-unstyled">
              <li>support@damp-platform.com</li>
              <li>+1 (555) 123-4567</li>
            </ul>
          </Col>
        </Row>
        <hr />
        <Row>
          <Col className="text-center">
            <p className="mb-0">
              &copy; {currentYear} Data Analytics Mentorship Platform.
              All rights reserved.
            </p>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
