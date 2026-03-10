# Use official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port Cloud Run expects
EXPOSE 8080

# Use gunicorn for production (handles multiple requests)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
