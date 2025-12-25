"""
Main application entry point for the Data Analytics Mentorship Platform
"""
import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )
