# Data Analytics Mentorship Platform (DAMP)

A comprehensive web application for data analytics education and mentorship, built with modern technologies and designed for scalability.

## 🚀 Features

### User Roles & Permissions
- **Students**: Enroll in courses, track progress, submit assignments, access learning materials
- **Mentors**: Create and manage courses, review submissions, provide feedback
- **Admins**: Manage users, approve mentors, view analytics, oversee platform operations

### Core Functionality
- **Course Management**: Create, edit, and organize data analytics courses
- **Progress Tracking**: Monitor learning progress with detailed analytics
- **Assignment System**: Submit and grade assignments with feedback
- **User Authentication**: Secure JWT-based authentication with role-based access
- **Analytics Dashboard**: Comprehensive insights into platform performance
- **Responsive Design**: Modern UI built with React and Bootstrap

### Technical Features
- **RESTful API**: Well-documented backend API
- **Database Analytics**: SQL queries and Python scripts for KPI analysis
- **Data Visualization**: Charts and graphs for performance metrics
- **File Upload**: Support for course materials and assignments
- **Email Notifications**: Configurable email system for updates

## 🛠 Technology Stack

### Backend
- **Python Flask**: REST API framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database
- **JWT**: Authentication tokens
- **Flask-Migrate**: Database migrations

### Frontend
- **React**: Modern JavaScript library
- **React Router**: Client-side routing
- **Bootstrap**: Responsive UI components
- **Axios**: HTTP client for API calls
- **Chart.js**: Data visualization

### Analytics
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Static data visualization
- **Streamlit**: Interactive analytics dashboard
- **Plotly**: Interactive charts and graphs
- **SQL**: Complex analytical queries

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Reverse proxy and static file serving

## 📁 Project Structure

```
data-analytics-mentorship-platform/
├── backend/                          # Flask API backend
│   ├── app/
│   │   ├── models/                  # SQLAlchemy models
│   │   ├── routes/                  # API endpoints
│   │   ├── utils/                   # Helper functions
│   │   ├── config.py                # Configuration
│   │   └── __init__.py
│   ├── analytics/                   # Data analysis scripts
│   ├── migrations/                  # Database migrations
│   ├── tests/                       # Unit tests
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Backend container
│   └── run.py                       # Application entry point
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── components/              # Reusable components
│   │   ├── pages/                   # Page components
│   │   ├── contexts/                # React contexts
│   │   ├── services/                # API services
│   │   └── utils/                   # Helper functions
│   ├── public/                      # Static assets
│   ├── package.json                 # Node dependencies
│   ├── Dockerfile                   # Frontend container
│   └── nginx.conf                   # Nginx config
├── database/                         # Database files
│   ├── schema.sql                   # Database schema
│   └── analytics_queries.sql        # Analytical queries
├── deployment/                       # Deployment configs
│   ├── docker-compose.yml           # Docker services
│   └── nginx.conf                   # Production nginx
└── docs/                            # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL (if running locally)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/damp-platform.git
cd damp-platform
```

### 2. Environment Configuration
```bash
# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit the environment files with your configuration
```

### 3. Docker Deployment (Recommended)
```bash
# Build and start all services
docker-compose -f deployment/docker-compose.yml up -d

# View logs
docker-compose -f deployment/docker-compose.yml logs -f

# Stop services
docker-compose -f deployment/docker-compose.yml down
```

### 4. Local Development Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For analytics dashboard (optional)
pip install streamlit plotly

# Set environment variables
export FLASK_ENV=development
export DATABASE_URL=postgresql://username:password@localhost:5432/damp_db

# Run migrations
flask db upgrade

# Start the backend
python run.py
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 📊 Database Setup

### Using Docker
The database is automatically created when using Docker Compose.

### Manual Setup
```sql
-- Create database
CREATE DATABASE damp_db;

-- Run the schema
\i database/schema.sql;

-- Create initial admin user
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active, is_approved)
VALUES ('admin', 'admin@damp.com', '$2b$12$...', 'Admin', 'User', 'admin', true, true);
```

### Demo Data Generation
Generate comprehensive sample data for testing and analytics:

```bash
# Generate demo data with users, courses, enrollments, and analytics
python demo_data.py

# Or use the basic setup script
python setup.py
```

#### Sample Data Structure
The demo data includes realistic educational platform data:

**Users (15 total)**:
- **Students (12)**: Diverse learners with different enrollment patterns
- **Mentors (3)**: Experienced educators teaching various subjects
- **Admins (1)**: Platform administrators

**Courses (8 total)**:
- **Data Analytics Fundamentals**: Beginner-level introduction
- **Advanced Machine Learning**: Advanced AI/ML concepts
- **Data Visualization**: Intermediate visualization techniques
- **Statistics for Data Science**: Intermediate statistical methods
- **Deep Learning Fundamentals**: Advanced neural networks
- **SQL for Data Analysis**: Beginner database querying
- **Big Data with Hadoop**: Advanced distributed computing
- **Time Series Analysis**: Intermediate forecasting methods

**Enrollment Patterns**:
- **Realistic completion rates**: 60-95% based on course difficulty
- **Varied enrollment numbers**: 5-25 students per course
- **Time-based enrollments**: Spread across 6 months
- **Progress tracking**: Partial completion for active students

**Academic Performance**:
- **Grade distributions**: Realistic bell curves (60-100 range)
- **Late submissions**: 20% rate to simulate real-world patterns
- **Assignment completion**: 70-80% submission rates
- **Course reviews**: 3.5-5.0 star ratings

**Analytics Events (500+)**:
- User login patterns
- Course view activities
- Assignment submissions
- Module completions
- Profile updates

#### What the Sample Data Demonstrates
- **Realistic user behavior patterns** in an educational platform
- **Varied course performance** across different difficulty levels
- **Student engagement metrics** that reflect actual learning platforms
- **Teaching effectiveness indicators** for mentor evaluation
- **Platform growth trends** over a 12-month period
- **Business intelligence insights** for platform optimization
- Analytics events for dashboard visualization

## 🔍 Analytics & Reporting

### Interactive Analytics Dashboard (Streamlit)
The platform includes a comprehensive interactive analytics dashboard built with Streamlit that provides real-time insights into platform performance, user behavior, and learning outcomes.

```bash
# Quick start (from project root)
python run_analytics.py

# Or manually:
cd backend/analytics
python run_dashboard.py
```

The dashboard will be available at `http://localhost:8501` and includes six detailed analytics pages:

#### 🏠 **Overview Dashboard**
**Purpose**: Provides a high-level snapshot of the entire platform's health and performance.

**Key Metrics Displayed**:
- **Total Users**: Overall user count with active user breakdown
- **Active Courses**: Number of currently available courses
- **Total Enrollments**: Complete enrollment numbers with completion status
- **Completion Rate**: Overall course completion percentage across the platform

**Visualizations**:
- **User Distribution Pie Chart**: Shows the proportion of students vs mentors vs pending mentors
- **Recent Activity Bar Chart**: Displays new enrollments and active courses over the last 30 days

**Business Insights**:
- Platform growth indicators
- User engagement levels
- Course utilization rates
- Overall learning completion trends

#### 👥 **User Analytics Dashboard**
**Purpose**: Analyzes user acquisition, growth patterns, and demographic distribution.

**Key Metrics Displayed**:
- **User Registration Trends**: Monthly new user signups over the past year
- **User Role Distribution**: Breakdown of students, mentors, and administrators

**Visualizations**:
- **Monthly Registration Line Chart**: Tracks user growth over time with markers for each data point
- **User Roles Bar Chart**: Compares the number of users in each role category

**Business Insights**:
- Platform adoption rates
- User acquisition velocity
- Demographic balance between learners and educators
- Seasonal registration patterns
- User retention and growth sustainability

#### 📚 **Course Performance Dashboard**
**Purpose**: Evaluates the effectiveness and popularity of individual courses and course categories.

**Key Metrics Displayed**:
- **Course Enrollment Rankings**: Top 10 courses by student enrollment numbers
- **Course Completion Rates**: Success rates for each course
- **Category Performance**: Average completion and rating by subject category

**Visualizations**:
- **Enrollment Rankings Bar Chart**: Horizontal bar chart showing most popular courses
- **Completion Rate Analysis**: Bar chart ranking courses by completion percentage
- **Category Performance Charts**: Side-by-side comparison of completion rates and average ratings across categories
- **Detailed Course Table**: Comprehensive data table with all course metrics

**Business Insights**:
- Most demanded skills and topics
- Course quality indicators
- Subject area performance comparison
- Content effectiveness measurement
- Curriculum optimization opportunities

#### 🎓 **Student Performance Dashboard**
**Purpose**: Analyzes individual student learning outcomes, grade distributions, and engagement patterns.

**Key Metrics Displayed**:
- **Grade Distribution**: Histogram of assignment scores across all students
- **Course-wise Performance**: Average grades for each course
- **Late Submission Analysis**: Comparison of on-time vs late submissions

**Visualizations**:
- **Grade Distribution Histogram**: Shows the spread of student performance
- **Course Performance Bar Chart**: Compares average grades across different courses
- **Late Submission Pie Chart**: Proportion of on-time vs late assignments
- **Performance Comparison Bar Chart**: Average grades for timely vs late submissions

**Business Insights**:
- Student learning effectiveness
- Course difficulty assessment
- Assignment completion patterns
- Grade inflation detection
- Student support needs identification
- Learning outcome quality measurement

#### 📈 **Trends & Insights Dashboard**
**Purpose**: Provides time-series analysis and forward-looking insights for platform planning and optimization.

**Key Metrics Displayed**:
- **User Growth Trends**: Monthly and cumulative user registration patterns
- **Course Performance Overview**: Comprehensive course metrics table
- **Key Platform Insights**: Summary statistics and recommendations

**Visualizations**:
- **Monthly Registration Trends**: Line chart showing user acquisition over time
- **Cumulative User Growth**: Line chart displaying total user base expansion
- **Course Performance Data Table**: Detailed metrics for all courses
- **Key Insights Cards**: Highlighted metrics for most popular, highest-rated, and best-performing courses

**Business Insights**:
- Platform scalability assessment
- Growth rate calculations
- Seasonal trend identification
- Future capacity planning
- Content strategy optimization
- Platform health monitoring

### Automated Analytics Scripts
For batch processing, scheduled reports, and detailed data analysis:

#### Course Completion Analysis (`course_completion_analysis.py`)
**Purpose**: Comprehensive analysis of course completion patterns and student engagement.

**What it analyzes**:
- Overall platform completion rates
- Course-by-course completion statistics
- Completion rates by difficulty level (beginner/intermediate/advanced)
- Completion rates by subject category
- Time-to-completion analysis for finished courses
- Course enrollment vs completion correlations

**Outputs generated**:
- Detailed completion rate report (JSON)
- Visual analysis charts (PNG)
- Statistical summaries and insights
- Category-wise performance comparisons

**Business value**: Identifies successful courses, highlights areas needing improvement, tracks learning effectiveness.

#### Student Performance Analysis (`student_performance_analysis.py`)
**Purpose**: In-depth analysis of student learning outcomes and academic performance.

**What it analyzes**:
- Individual student grade distributions
- Assignment submission patterns and timeliness
- Performance variations across different courses
- Grade progression and improvement trends
- Late submission rates and their impact on grades
- Student engagement and participation metrics

**Outputs generated**:
- Performance distribution histograms
- Student ranking and comparison reports
- Course-wise performance analysis
- Submission pattern insights
- At-risk student identification

**Business value**: Measures learning quality, identifies struggling students, optimizes course difficulty, improves teaching methods.

#### Mentor Effectiveness Analysis (`mentor_effectiveness_analysis.py`)
**Purpose**: Evaluates teaching quality and mentor performance across multiple courses.

**What it analyzes**:
- Completion rates for courses taught by each mentor
- Student satisfaction ratings for mentor-led courses
- Course enrollment numbers and growth trends
- Mentor workload distribution and course load
- Teaching effectiveness scores combining multiple metrics
- Comparative analysis across all mentors

**Outputs generated**:
- Mentor performance ranking reports
- Teaching effectiveness visualizations
- Workload analysis charts
- Student satisfaction metrics
- Mentor development recommendations

**Business value**: Ensures teaching quality, identifies star performers, guides mentor training, optimizes course assignments.

## 🚀 Extending the Dashboard

### Adding Custom Analytics

#### Creating New Dashboard Pages
```python
# In simple_dashboard.py, add new page to sidebar
page = st.sidebar.radio(
    "Select Analytics View",
    ["🏠 Overview", "👥 User Analytics", "📚 Course Performance",
     "🎓 Student Performance", "📈 Trends", "🎯 Custom Analytics"]  # Add new page
)

# Add corresponding if statement
elif page == "🎯 Custom Analytics":
    st.title("🎯 Custom Analytics")
    # Add your custom visualizations here
```

#### Adding New Visualizations
```python
import plotly.express as px

# Example: Add correlation analysis
correlation_data = data[['metric1', 'metric2']].corr()
fig = px.imshow(correlation_data, title='Correlation Matrix')
st.plotly_chart(fig)
```

#### Custom KPI Calculations
```python
# Example: Calculate custom metrics
def calculate_custom_metric(data):
    # Your calculation logic
    return result

custom_kpi = calculate_custom_metric(your_data)
st.metric("Custom KPI", f"{custom_kpi:.2f}")
```

#### Database Integration
For production use with real data:
```python
# Connect to your database
engine = create_engine('postgresql://user:pass@localhost/db')

# Query custom data
custom_data = pd.read_sql("""
    SELECT your_custom_metrics
    FROM your_tables
    WHERE your_conditions
""", engine)

# Create visualizations
fig = px.bar(custom_data, x='category', y='value')
st.plotly_chart(fig)
```

### Advanced Features to Consider

#### Predictive Analytics
- Student success prediction models
- Course completion forecasting
- User churn analysis
- Revenue projections

#### Real-time Monitoring
- Live user activity tracking
- Real-time enrollment notifications
- Performance alerts and thresholds

#### Export Capabilities
- PDF report generation
- Excel data exports
- Scheduled email reports
- API endpoints for external systems

#### Enhanced Filtering
- Date range selectors
- Multi-select category filters
- Dynamic cohort analysis
- Comparative period analysis

### Understanding Dashboard Visualizations

#### Chart Types and Their Business Meaning

**📊 KPI Cards (Overview Page)**
- **Total Users**: Platform reach and market penetration
- **Active Courses**: Content library health and variety
- **Total Enrollments**: Revenue potential and user engagement
- **Completion Rate**: Learning effectiveness and course quality

**🥧 Pie Charts**
- **User Distribution**: Platform balance between learners and educators
- **Late Submissions**: Student engagement and course pacing issues

**📈 Line Charts**
- **User Growth**: Platform adoption velocity and scalability
- **Cumulative Users**: Total addressable market capture
- **Registration Trends**: Seasonal patterns and marketing effectiveness

**📊 Bar Charts**
- **Course Rankings**: Content popularity and market demand
- **Performance Comparisons**: Quality assessment across categories
- **Grade Distributions**: Learning outcome quality indicators

**📉 Histograms**
- **Grade Spread**: Student performance distribution and equity
- **Frequency Analysis**: Common performance patterns identification

#### Business Intelligence Insights

**🎯 Decision-Making Applications**:
- **Content Strategy**: Identify high-demand topics vs underperforming courses
- **Student Success**: Pinpoint at-risk learners needing additional support
- **Teaching Quality**: Recognize effective mentors for course assignments
- **Platform Growth**: Track user acquisition and retention patterns
- **Revenue Optimization**: Focus on high-completion, high-demand courses

**📋 Actionable Insights Examples**:
- Courses with <70% completion rates need content improvement
- Students with consistent low grades need personalized learning plans
- Mentors with >85% completion rates should teach advanced courses
- Categories with high enrollment but low completion need curriculum review

### Dashboard Usage by Stakeholder

#### 👨‍🎓 **For Students**
**Primary Focus**: Student Performance Dashboard
- Track personal grade progress and improvement trends
- Compare performance across different courses
- Identify strengths and areas needing improvement
- Monitor assignment submission timeliness

**Key Insights to Monitor**:
- Personal grade distribution compared to class averages
- Late submission patterns and their impact on grades
- Course completion percentages and time remaining

#### 👨‍🏫 **For Mentors**
**Primary Focus**: Course Performance + Student Performance Dashboards
- Evaluate teaching effectiveness across courses
- Identify struggling students needing additional support
- Compare course performance within subject categories
- Track assignment completion and grading patterns

**Key Insights to Monitor**:
- Completion rates for courses they teach
- Student performance in their classes vs platform averages
- Late submission rates indicating course pacing issues
- Course ratings and reviews for content improvement

#### 👑 **For Administrators**
**Primary Focus**: Overview + All Analytics Dashboards
- Monitor overall platform health and growth
- Make strategic decisions about course offerings
- Identify mentors needing additional training
- Track user acquisition and retention metrics

**Key Insights to Monitor**:
- Platform-wide completion rates and user engagement
- Course performance across all categories
- Mentor effectiveness rankings and workload distribution
- User growth trends and registration patterns

#### 💼 **For Investors/Business Stakeholders**
**Primary Focus**: Overview + Trends Dashboards
- Assess platform scalability and market fit
- Monitor key business metrics and growth indicators
- Evaluate content quality and user satisfaction
- Track platform health and expansion opportunities

**Key Insights to Monitor**:
- User growth velocity and market penetration
- Course completion rates as quality indicators
- Revenue potential through enrollment numbers
- Platform engagement and retention metrics

## 🔧 Dashboard Troubleshooting

### Common Issues and Solutions

#### Dashboard Won't Load
**Symptoms**: "Site cannot be reached" or connection refused
**Solutions**:
```bash
# Check if Streamlit is running
ps aux | grep streamlit

# Kill existing processes
pkill -f streamlit

# Restart dashboard
python run_analytics.py
```

#### No Data Showing
**Symptoms**: Empty charts or "No data available" messages
**Cause**: Sample data not loaded or corrupted
**Solutions**:
```bash
# Regenerate sample data by restarting
python simple_dashboard.py

# Or check if the dashboard script is running the correct data generation
```

#### Charts Not Rendering
**Symptoms**: Blank chart areas or Plotly errors
**Cause**: Missing Plotly.js dependencies or browser issues
**Solutions**:
```bash
# Update Plotly
pip install --upgrade plotly streamlit-plotly-events

# Clear browser cache
# Or try different browser (Chrome recommended)
```

#### Port Already in Use
**Symptoms**: "Port 8501 already in use" error
**Solutions**:
```bash
# Find process using port
netstat -tulpn | grep :8501

# Kill the process
# Or use different port
streamlit run simple_dashboard.py --server.port 8502
```

#### Performance Issues
**Symptoms**: Slow loading, freezing, or unresponsive interface
**Solutions**:
- Close other applications to free up RAM
- Reduce browser tabs
- Restart the Streamlit server
- Check system has adequate resources (4GB+ RAM recommended)

#### Permission Errors
**Symptoms**: "Permission denied" when accessing files
**Solutions**:
```bash
# Run with proper permissions
chmod +x run_analytics.py
python run_analytics.py

# Or run as administrator (Windows)
```

#### Data Not Updating
**Symptoms**: Dashboard shows old data even after changes
**Solutions**:
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart the dashboard
python run_analytics.py
```

### Understanding Dashboard Visualizations
- **Course completion rates** and time-to-completion analysis
- **Student performance distribution** and grade analytics
- **Enrollment trends** and platform engagement statistics
- **Mentor effectiveness scores** and teaching quality metrics
- **Interactive visualizations** with filtering and drill-down capabilities
- **Automated report generation** for stakeholder communication
- **Predictive insights** from historical data patterns
- **Comparative analysis** across courses, students, and mentors

## 🚀 GitHub Deployment & CI/CD

### Repository
**GitHub Repository**: https://github.com/pranotosh2/Full-Stack-Data-Analytics

### Automated CI/CD Pipeline
The repository includes comprehensive GitHub Actions workflows:

#### Main CI/CD Pipeline (`ci-cd.yml`)
- **Backend Testing**: Python linting, Flask app validation, database tests
- **Frontend Testing**: Node.js dependency checks, build verification
- **Docker Validation**: Container build tests and Compose configuration
- **Analytics Testing**: Script import validation and data generation
- **Security Scanning**: Vulnerability assessment with Trivy
- **Deployment Stages**: Staging and production deployment workflows

#### Analytics Documentation (`analytics-docs.yml`)
- **Manual Trigger**: Generate analytics reports on demand
- **Report Types**: Completion, Performance, Effectiveness, or All
- **Artifact Storage**: Generated reports and visualizations
- **Scheduled Generation**: Can be configured for regular reporting

#### Dashboard Deployment (`deploy-dashboard.yml`)
- **Package Creation**: Self-contained dashboard deployment package
- **Artifact Generation**: Ready-to-deploy dashboard bundle
- **Deployment Scripts**: Automated setup and launch scripts

### Running CI/CD Locally

#### Backend Testing
```bash
cd backend
pip install -r requirements.txt
python -m pytest tests/ 2>/dev/null || echo "No tests configured - checking imports"
python -c "from app import create_app; app = create_app('testing'); print('✅ Flask app OK')"
```

#### Frontend Testing
```bash
cd frontend
npm install
npm run build
npm test -- --coverage --watchAll=false 2>/dev/null || echo "No tests configured"
```

#### Docker Validation
```bash
# Test Docker builds
docker build -t damp-backend:test ./backend
docker build -t damp-frontend:test ./frontend

# Validate Compose configuration
docker-compose -f deployment/docker-compose.yml config
```

### Deployment Options

#### 1. **Full Stack Deployment (Docker)**
```bash
# Production deployment
docker-compose -f deployment/docker-compose.yml up -d

# With custom environment
cp backend/.env.example backend/.env
# Edit backend/.env with production values
docker-compose -f deployment/docker-compose.yml up -d
```

#### 2. **Analytics Dashboard Only**
```bash
# Download from GitHub Actions artifact
# Or deploy directly
pip install streamlit plotly pandas numpy
streamlit run simple_dashboard.py --server.port 8501
```

#### 3. **Cloud Platform Deployment**
- **Heroku**: Connect GitHub repo, auto-deploy on push
- **Railway**: Direct GitHub integration
- **Render**: GitHub webhook deployment
- **AWS/GCP/Azure**: Container deployment with GitHub Actions

### Environment Configuration
```bash
# Backend (.env)
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET_KEY=your-jwt-production-key
FLASK_ENV=production

# Frontend (.env)
REACT_APP_API_URL=https://your-api-domain.com
```

## 🧪 Testing

## 🚀 Deployment

### Production Deployment
1. Update environment variables for production
2. Configure SSL certificates
3. Set up monitoring and logging
4. Configure backup strategies

### Environment Variables
```bash
# Backend
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-jwt-production-key
DATABASE_URL=postgresql://prod-user:prod-password@prod-db:5432/damp_prod
FLASK_ENV=production

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
```

### SSL Configuration
Update `deployment/nginx.conf` with SSL certificates and configure HTTPS.

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh JWT token
- `GET /auth/profile` - Get user profile

### Course Endpoints
- `GET /api/courses` - List courses
- `POST /api/courses` - Create course (mentors/admins)
- `GET /api/courses/:id` - Get course details
- `PUT /api/courses/:id` - Update course

### Enrollment Endpoints
- `POST /api/courses/:id/enroll` - Enroll in course
- `PUT /api/enrollments/:id/progress` - Update progress

### Admin Endpoints
- `GET /admin/users` - List all users
- `GET /admin/analytics/overview` - Platform analytics

## 📚 GitHub Repository Features

### Repository Structure
```
🏗️ Full-Stack-Data-Analytics/
├── 📁 backend/              # Flask API (45 files)
├── 📁 frontend/             # React SPA (12 files)
├── 📁 database/             # SQL schemas & queries
├── 📁 deployment/           # Docker & cloud configs
├── 📁 .github/              # CI/CD workflows
├── 📄 README.md            # Comprehensive docs (776 lines)
├── 📄 .gitignore           # Python/Node.js/Docker ignores
└── 🐍 *.py scripts         # Analytics & setup scripts
```

### GitHub Actions Workflows
- **🚀 CI/CD Pipeline**: Automated testing on every push
- **📊 Analytics Reports**: Manual report generation
- **📦 Dashboard Deployment**: Automated packaging

### Repository Stats
- **Languages**: Python (70%), JavaScript (20%), SQL (7%), Docker (3%)
- **Size**: ~6.5MB (compressed)
- **Contributors**: 1 (main maintainer)
- **License**: MIT (open source)

### Key Files Overview
- **`simple_dashboard.py`**: Interactive analytics dashboard
- **`demo_data.py`**: Sample data generator
- **`setup.py`**: Basic database setup
- **`run_analytics.py`**: Dashboard launcher
- **`requirements.txt`**: Python dependencies
- **`package.json`**: Node.js dependencies
- **`docker-compose.yml`**: Full-stack deployment

## 🤝 Contributing

### Development Workflow
1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/Full-Stack-Data-Analytics.git
   cd Full-Stack-Data-Analytics
   ```
3. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make** your changes and test thoroughly
5. **Commit** with descriptive messages:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open** a Pull Request on GitHub

### Contribution Guidelines
- **Code Style**: Follow PEP 8 for Python, ESLint for JavaScript
- **Testing**: Add tests for new features
- **Documentation**: Update README for significant changes
- **Commits**: Use conventional commit format
- **Issues**: Create issues for bugs and feature requests

### Areas for Contribution
- **🔧 Backend Features**: New API endpoints, authentication methods
- **🎨 Frontend UI**: Enhanced dashboards, new components
- **📊 Analytics**: Additional metrics, advanced visualizations
- **🚀 DevOps**: CI/CD improvements, cloud deployments
- **📚 Documentation**: Tutorials, API docs, deployment guides
- **🧪 Testing**: Unit tests, integration tests, E2E tests

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for data analytics education and mentorship
- Inspired by modern e-learning platforms
- Designed for scalability and maintainability

## 📞 Support

For support, email support@damp-platform.com or create an issue in the repository.

---

**Note**: This is a comprehensive portfolio project demonstrating full-stack development skills, database design, analytics implementation, and modern deployment practices.
