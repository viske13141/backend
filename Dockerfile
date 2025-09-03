# Use Python 3.11 (stable)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (example: mysqlclient, tesseract, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    tesseract-ocr \
    libtesseract-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv or just requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (Render looks for this)
EXPOSE 8000

# Run your app (change to match your entrypoint, e.g., Django, Flask, FastAPI)
CMD ["python", "app.py"]
