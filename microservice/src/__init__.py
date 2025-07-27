from flask import Flask
import os
from src.database import init_app, create_tables, add_sample_data
from src.routes.employee import employee_bp
from src.routes.health import health_bp

def create_app(config_name=None):
    """Factory method to create and configure Flask application"""
    # Set template directory to src/templates
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    
    app = Flask(__name__, template_folder=template_dir)
    
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Initialize database
    init_app(app, config_name)
    
    # Register blueprints
    app.register_blueprint(employee_bp)
    app.register_blueprint(health_bp)
    
    return app

def initialize_database(app):
    """Initialize database tables and sample data"""
    create_tables(app)
    add_sample_data(app)
