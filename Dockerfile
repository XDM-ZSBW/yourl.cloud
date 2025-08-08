# Use Python 3.11 slim image for Cloud Run domain mapping compatibility
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

# Set environment variables for Cloud Run domain mapping
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

# Health check for Cloud Run domain mapping compatibility
# Cloud Run uses /health endpoint for health checks
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Run the application with WSGI server for production
# Use gunicorn for better performance and Cloud Run compatibility
CMD ["python", "app.py"]
