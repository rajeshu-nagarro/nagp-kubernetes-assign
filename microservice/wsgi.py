#!/usr/bin/env python3
"""
WSGI entry point for the Employee Management System.
This file is used by WSGI servers like Gunicorn in production.
"""

import os
from src import create_app, initialize_database

# Get configuration from environment
config_name = os.environ.get('FLASK_ENV', 'production')

# Create app using factory method
app = create_app(config_name)

# Initialize database on startup
initialize_database(app)

# This is what WSGI servers will use
application = app

if __name__ == "__main__":
    # This allows running the WSGI file directly for testing
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"Starting Employee Management System (WSGI)...")
    print(f"Environment: {config_name}")
    print(f"Running on: http://{host}:{port}")
    
    app.run(host=host, port=port, debug=False)
