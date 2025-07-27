from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.config import config

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def init_app(app, config_name='default'):
    """Initialize database with Flask app"""
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize the database with the app
    db.init_app(app)
    
    return db

def create_tables(app):
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

def add_sample_data(app):
    """Add sample employee data to the database"""
    from src.models.employee import Employee
    
    with app.app_context():
        # Check if table is empty
        if Employee.query.count() == 0:
            sample_employees = [
                Employee(
                    first_name='John',
                    last_name='Doe',
                    email='john.doe@company.com',
                    department='Engineering',
                    position='Software Engineer',
                    hire_date=datetime(2023, 1, 15).date(),
                    salary=75000.00
                ),
                Employee(
                    first_name='Jane',
                    last_name='Smith',
                    email='jane.smith@company.com',
                    department='Marketing',
                    position='Marketing Manager',
                    hire_date=datetime(2022, 8, 20).date(),
                    salary=85000.00
                ),
                Employee(
                    first_name='Bob',
                    last_name='Johnson',
                    email='bob.johnson@company.com',
                    department='Engineering',
                    position='Senior Software Engineer',
                    hire_date=datetime(2021, 3, 10).date(),
                    salary=95000.00
                ),
                Employee(
                    first_name='Alice',
                    last_name='Brown',
                    email='alice.brown@company.com',
                    department='HR',
                    position='HR Specialist',
                    hire_date=datetime(2023, 6, 5).date(),
                    salary=65000.00
                ),
                Employee(
                    first_name='Charlie',
                    last_name='Wilson',
                    email='charlie.wilson@company.com',
                    department='Finance',
                    position='Financial Analyst',
                    hire_date=datetime(2022, 11, 12).date(),
                    salary=70000.00
                )
            ]
            
            for employee in sample_employees:
                db.session.add(employee)
            
            db.session.commit()
            print("Sample data added to the database.")
        else:
            print("Database already contains employee data.")
