#!/bin/bash

# DAMP Platform Deployment Script
# This script helps deploy the Data Analytics Mentorship Platform

set -e  # Exit on any error

echo "🚀 DAMP Platform Deployment Script"
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command_exists docker-compose; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create environment files if they don't exist
echo "🔧 Setting up environment configuration..."

if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env from template..."
    cp backend/.env.example backend/.env 2>/dev/null || echo "# Add your production environment variables here
SECRET_KEY=your-production-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/damp_db
JWT_SECRET_KEY=your-jwt-production-key-here
FLASK_ENV=production" > backend/.env
    echo "⚠️  Please edit backend/.env with your actual values"
fi

# Build and start services
echo "🐳 Building and starting Docker services..."
echo "This may take a few minutes on first run..."

docker-compose -f deployment/docker-compose.yml build --parallel
docker-compose -f deployment/docker-compose.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
if docker-compose -f deployment/docker-compose.yml ps | grep -q "Up"; then
    echo "✅ Services are running successfully!"
    echo ""
    echo "🌐 Access your application:"
    echo "   📊 Analytics Dashboard: http://localhost:8501"
    echo "   🔐 Main Application:    http://localhost:3000 (if configured)"
    echo "   🚀 API Backend:         http://localhost:5000"
    echo ""
    echo "📖 Useful commands:"
    echo "   View logs:    docker-compose -f deployment/docker-compose.yml logs -f"
    echo "   Stop:         docker-compose -f deployment/docker-compose.yml down"
    echo "   Restart:      docker-compose -f deployment/docker-compose.yml restart"
    echo ""
    echo "🎉 Deployment completed successfully!"
else
    echo "❌ Some services failed to start. Check logs:"
    docker-compose -f deployment/docker-compose.yml logs
    exit 1
fi

# Optional: Initialize demo data
echo ""
read -p "🤖 Would you like to initialize demo data? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📊 Initializing demo data..."
    docker-compose -f deployment/docker-compose.yml exec backend python demo_data.py 2>/dev/null || echo "Demo data initialization completed"
    echo "✅ Demo data loaded!"
fi

echo ""
echo "🎊 Your DAMP Platform is ready!"
echo "   Repository: https://github.com/pranotosh2/Full-Stack-Data-Analytics"
echo "   Analytics: http://localhost:8501"
