# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (for mysqlclient, psycopg2, etc.)
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install pip & dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files for whitenoise
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run with Gunicorn (WSGI server)
CMD ["gunicorn", "yourproject.wsgi:application", "--bind", "0.0.0.0:8000"]
