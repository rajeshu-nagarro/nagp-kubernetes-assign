FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    gosu \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh


# Set default environment variables
ENV FLASK_APP=src:create_app
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV GUNICORN_WORKERS=4
ENV GUNICORN_LOG_LEVEL=info
ENV PORT=80

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app

# Expose port
EXPOSE $PORT
# Use startup script to determine which server to run
CMD ["./start.sh"]
