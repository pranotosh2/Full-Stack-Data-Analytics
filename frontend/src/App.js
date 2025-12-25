import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import PrivateRoute from './components/PrivateRoute';

// Layout Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Auth Components
import Login from './pages/Login';
import Register from './pages/Register';

// Dashboard Components
import StudentDashboard from './pages/StudentDashboard';
import MentorDashboard from './pages/MentorDashboard';
import AdminDashboard from './pages/AdminDashboard';

// Course Components
import CourseList from './pages/CourseList';
import CourseDetail from './pages/CourseDetail';
import CourseCreate from './pages/CourseCreate';
import CourseEdit from './pages/CourseEdit';

// Other Pages
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Navbar />
          <main className="flex-shrink-0">
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              {/* Protected Routes */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />

              <Route path="/dashboard" element={
                <PrivateRoute>
                  <DashboardRouter />
                </PrivateRoute>
              } />

              <Route path="/courses" element={
                <PrivateRoute>
                  <CourseList />
                </PrivateRoute>
              } />

              <Route path="/courses/:courseId" element={
                <PrivateRoute>
                  <CourseDetail />
                </PrivateRoute>
              } />

              <Route path="/courses/create" element={
                <PrivateRoute roles={['mentor', 'admin']}>
                  <CourseCreate />
                </PrivateRoute>
              } />

              <Route path="/courses/:courseId/edit" element={
                <PrivateRoute roles={['mentor', 'admin']}>
                  <CourseEdit />
                </PrivateRoute>
              } />

              <Route path="/profile" element={
                <PrivateRoute>
                  <Profile />
                </PrivateRoute>
              } />

              {/* Admin Routes */}
              <Route path="/admin/*" element={
                <PrivateRoute roles={['admin']}>
                  <AdminDashboard />
                </PrivateRoute>
              } />

              {/* 404 Route */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

// Component to route to appropriate dashboard based on user role
function DashboardRouter() {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const role = user.role;

  switch (role) {
    case 'student':
      return <StudentDashboard />;
    case 'mentor':
      return <MentorDashboard />;
    case 'admin':
      return <AdminDashboard />;
    default:
      return <Navigate to="/login" replace />;
  }
}

export default App;
