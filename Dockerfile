# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create data directory for SQLite database
RUN mkdir -p data

# Set environment variables
ENV FLASK_APP=src.app
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Initialize database and run the application
CMD python seed_db.py && gunicorn --bind 0.0.0.0:5000 "src.app:app"