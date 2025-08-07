# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create templates directory if it doesn't exist
RUN mkdir -p templates

# Expose port (Cloud Run will override this)
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

# Run the application with Gunicorn in production
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]
