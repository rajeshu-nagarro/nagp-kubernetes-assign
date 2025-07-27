#!/usr/bin/env python3
"""
Application entry point for the Employee Management System.
This file can be used to run the application in different environments.
"""

import os
from src import create_app, initialize_database

def main():
    """Main function to run the application"""
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create app using factory method
    app = create_app(config_name)
    
    # Initialize database
    initialize_database(app)
    
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = config_name == 'development'
    
    print(f"Starting Employee Management System...")
    print(f"Environment: {config_name}")
    print(f"Running on: http://{host}:{port}")
    
    if config_name == 'production':
        print("WARNING: Running Flask development server in production!")
        print("For production, use a WSGI server like Gunicorn:")
        print("gunicorn --config gunicorn.conf.py wsgi:application")
    
    # Run the application
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
