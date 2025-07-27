from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from src.models.employee import Employee
from src.database import db
from datetime import datetime
import socket
import os

# Create employee blueprint
employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/')
def index():
    """Main page that displays employee list"""
    # Get container/hostname information
    hostname = socket.gethostname()
    container_id = os.environ.get('HOSTNAME', hostname)
    flask_env = os.environ.get('FLASK_ENV', 'unknown')
    
    return render_template('index.html', 
                         hostname=hostname,
                         container_id=container_id,
                         flask_env=flask_env)

@employee_bp.route('/add')
def add_employee_form():
    """Display add employee form"""
    # Get container/hostname information for consistency
    hostname = socket.gethostname()
    container_id = os.environ.get('HOSTNAME', hostname)
    flask_env = os.environ.get('FLASK_ENV', 'unknown')
    
    return render_template('add_employee.html',
                         hostname=hostname,
                         container_id=container_id,
                         flask_env=flask_env)

@employee_bp.route('/add', methods=['POST'])
def add_employee():
    """Handle add employee form submission"""
    try:
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        department = request.form.get('department', '').strip()
        position = request.form.get('position', '').strip()
        hire_date_str = request.form.get('hire_date', '').strip()
        salary_str = request.form.get('salary', '').strip()
        
        # Validate required fields
        if not all([first_name, last_name, email, department, position, hire_date_str, salary_str]):
            flash('All fields are required!', 'error')
            return redirect(url_for('employee.add_employee_form'))
        
        # Validate email format
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address!', 'error')
            return redirect(url_for('employee.add_employee_form'))
        
        # Parse hire date
        try:
            hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Please enter a valid hire date (YYYY-MM-DD)!', 'error')
            return redirect(url_for('employee.add_employee_form'))
        
        # Parse salary
        try:
            salary = float(salary_str)
            if salary < 0:
                flash('Salary must be a positive number!', 'error')
                return redirect(url_for('employee.add_employee_form'))
        except ValueError:
            flash('Please enter a valid salary amount!', 'error')
            return redirect(url_for('employee.add_employee_form'))
        
        # Check if email already exists
        existing_employee = Employee.get_employee_by_email(email)
        if existing_employee:
            flash('An employee with this email already exists!', 'error')
            return redirect(url_for('employee.add_employee_form'))
        
        # Create new employee
        new_employee = Employee.create_employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            position=position,
            hire_date=hire_date,
            salary=salary
        )
        
        # Save to database
        new_employee.save()
        
        flash(f'Employee {first_name} {last_name} added successfully!', 'success')
        return redirect(url_for('employee.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding employee: {str(e)}', 'error')
        return redirect(url_for('employee.add_employee_form'))

@employee_bp.route('/employees')
def get_employees():
    """API endpoint to fetch all employees"""
    try:
        employees = Employee.get_all_employees()
        employees_data = [employee.to_dict() for employee in employees]
        return jsonify({
            'success': True,
            'data': employees_data,
            'count': len(employees_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@employee_bp.route('/employee/<int:employee_id>')
def get_employee(employee_id):
    """API endpoint to fetch a specific employee"""
    try:
        employee = Employee.get_employee_by_id(employee_id)
        if employee:
            return jsonify({
                'success': True,
                'data': employee.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Employee not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
