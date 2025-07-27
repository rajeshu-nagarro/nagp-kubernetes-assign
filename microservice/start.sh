#!/bin/bash
# Startup script for Employee Management System

set -e

# Default values
export FLASK_ENV=${FLASK_ENV:-production}
export PORT=${PORT:-5000}
export GUNICORN_WORKERS=${GUNICORN_WORKERS:-4}

echo "Starting Employee Management System..."
echo "Environment: $FLASK_ENV"
echo "Port: $PORT"

# Wait for database to be ready if DATABASE_URL is set
if [ ! -z "$DATABASE_URL" ]; then
    echo "Waiting for database to be ready..."
    # Simple check - could be enhanced with proper health check
    sleep 5
fi

# Handle user permissions based on environment
if [ "$FLASK_ENV" = "development" ]; then
    echo "Starting in development mode with Flask dev server..."
    echo "Running as current user for development flexibility..."
    python app.py
else
    echo "Starting in production mode with Gunicorn..."
    echo "Workers: $GUNICORN_WORKERS"
    echo "Switching to non-root user for security..."
    
    # Switch to non-root user for production
    if [ "$(id -u)" = "0" ]; then
        # If running as root, switch to appuser
        exec gosu appuser gunicorn --config gunicorn.conf.py wsgi:application
    else
        # If already running as non-root user
        exec gunicorn --config gunicorn.conf.py wsgi:application
    fi
fi
