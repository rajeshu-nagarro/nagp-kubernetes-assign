# Employee Management System

A Flask web application that displays employee data from a MySQL database using SQLAlchemy ORM.

## Features

- Single page web application built with Flask
- Displays employee list in a responsive table
- Uses SQLAlchemy ORM for database interactions
- Real-time statistics (total employees, departments, average salary)
- Sample data included for testing

## Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)

## Setup Instructions

### 1. Clone and Navigate to Project

```bash
cd /microservice
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

First, create a MySQL database:

```sql
CREATE DATABASE employee_db;
```

### 4. Environment Configuration

Copy the example environment file and configure your database settings:

```bash
cp .env.example .env
```

Edit the `.env` file with your MySQL credentials:

```
DATABASE_URL=mysql+pymysql://your_username:your_password@localhost/employee_db
```

### 5. Run the Application

You can run the application in multiple ways:

**Option 1: Using the main app entry point (Recommended)**
```bash
python app.py
```

The application will:
- Create the database tables automatically
- Insert sample employee data
- Start the server on `http://localhost:5000`

### 6. Docker Deployment

**Single Dockerfile for All Environments** - The Docker setup automatically detects the environment and runs the appropriate server:

**How to run**
```bash
# Uses Gunicorn WSGI server with non-root user
docker-compose up
```

# Run using docker
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DATABASE_URL="mysql+pymysql://user:password@host/employee_db" \
  -e GUNICORN_WORKERS=4 \
  employee-management


## Database Schema

The application uses a single `employee` table with the following structure:

```sql
CREATE TABLE employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    hire_date DATE NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Web Routes

### Employee Routes
- `GET /` - Main page displaying employee list
- `GET /add` - Add employee form page
- `POST /add` - Handle add employee form submission
- `GET /employees` - JSON API endpoint returning all employees
- `GET /employee/<id>` - JSON API endpoint returning specific employee

### Health Check Routes
- `GET /health` - General health check endpoint
- `GET /health/db` - Database-specific health check

## Architecture

The application follows below architecture using Factory pattern:

### Factory Method Pattern (`src/__init__.py`)
- **create_app()**: Factory method that creates and configures Flask application instances
- **Environment-based Configuration**: Supports different configurations for development, production, and testing environment.
- **Blueprint Registration**: Registers all route

### Models (`src/models/`)
- **Employee Model**: Handles all employee-related database operations
- Uses SQLAlchemy ORM for database interactions
- Includes methods for CRUD operations
- Located in dedicated src/models directory

### Routes (`src/routes/`)
- **Employee Blueprint**: Handles all employee-related HTTP requests
- **Health Blueprint**: Provides health check endpoints
- Uses Flask blueprints for modular route organization
- Located in dedicated src/routes directory

### Database (`src/database.py`)
- Centralized database configuration and initialization
- Handles database connection setup with different environments
- Manages sample data insertion
- Support for multiple database configurations

### Configuration (`src/config.py`)
- Environment-specific configurations (development, production, testing)
- Centralized configuration management
- Supports environment variables for sensitive data

### Smart Startup Script (`start.sh`)
- **Environment Detection**: Automatically detects `FLASK_ENV` variable
- **Security Handling**: Uses non-root user in production, flexible in development
- **Server Selection**: Chooses Gunicorn for production, Flask dev server for development
- **Database Readiness**: Waits for database connection before starting

## Features

### Employee List Display
- Shows all employees in a responsive table
- Displays ID, name, email, department, position, hire date, and salary
- Hover effects and modern styling

### Statistics Dashboard
- Total number of employees
- Number of unique departments
- Average salary calculation

### Error Handling
- Connection error handling
- Loading states
- User-friendly error messages

## Sample Data

The application includes sample data for 5 employees across different departments:
- Engineering
- Marketing
- HR
- Finance

## Technology Stack

- **Backend**: Python Flask
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database Driver**: PyMySQL

## File Structure

```
microservice/
├── app.py                   # Development entry point
├── wsgi.py                 # WSGI entry point for production
├── start.sh                # Smart startup script (env-aware)
├── requirements.txt        # Python dependencies (includes Gunicorn)
├── gunicorn.conf.py        # Gunicorn configuration
├── .env.example           # Environment variables template
├── .dockerignore          # Docker ignore file
├── Dockerfile             # Universal Docker configuration
├── docker-compose.yml     # Production Docker Compose
├── src/                   # Source code directory
│   ├── __init__.py        # Flask app factory method
│   ├── config.py          # Application configuration settings
│   ├── database.py        # Database configuration and initialization
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   └── employee.py    # Employee model
│   ├── routes/            # Application routes/blueprints
│   │   ├── __init__.py
│   │   ├── employee.py    # Employee-related routes
│   │   └── health.py      # Health check routes
│   └── templates/         # HTML templates
│       ├── index.html     # Employee list page
│       └── add_employee.html  # Add employee form
└── README.md              # This file
```

## Troubleshooting

### Database Connection Issues
- Ensure MySQL server is running
- Check database credentials in `.env` file
- Verify the database exists

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Port Already in Use
If port 5000 is busy, modify the PORT in .env file:
