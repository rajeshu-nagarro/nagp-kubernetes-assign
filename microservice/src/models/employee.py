from src.database import db
from sqlalchemy import Numeric
from datetime import datetime

class Employee(db.Model):
    """Employee model for storing employee information"""
    __tablename__ = 'employee'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    hire_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    salary = db.Column(Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'
    
    def to_dict(self):
        """Convert employee object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'department': self.department,
            'position': self.position,
            'hire_date': self.hire_date.strftime('%Y-%m-%d') if self.hire_date else None,
            'salary': float(self.salary),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    @classmethod
    def create_employee(cls, first_name, last_name, email, department, position, hire_date, salary):
        """Create a new employee instance"""
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            position=position,
            hire_date=hire_date,
            salary=salary
        )
    
    @classmethod
    def get_all_employees(cls):
        """Get all employees from the database"""
        return cls.query.all()
    
    @classmethod
    def get_employee_by_id(cls, employee_id):
        """Get employee by ID"""
        return cls.query.get(employee_id)
    
    @classmethod
    def get_employee_by_email(cls, email):
        """Get employee by email"""
        return cls.query.filter_by(email=email).first()
    
    def save(self):
        """Save employee to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete employee from database"""
        db.session.delete(self)
        db.session.commit()
