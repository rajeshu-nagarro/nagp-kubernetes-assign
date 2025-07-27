from flask import Blueprint, jsonify
from datetime import datetime
from src.database import db

# Create health check blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'service': 'employee-management-system',
        'version': '1.0.0'
    })

@health_bp.route('/health/db')
def database_health():
    """Database-specific health check"""
    try:
        # More detailed database health check
        db.session.execute('SELECT 1')
        
        # Check if we can access the employee table
        from src.models.employee import Employee
        employee_count = Employee.query.count()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected',
            'employee_count': employee_count,
            'message': 'Database is accessible and functional'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'disconnected',
            'error': str(e)
        }), 503
