# Use Python 3.11 slim image for smaller size and security
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Upgrade system packages and install security updates
# This addresses CVEs in system packages like pam, tar, sqlite3, glibc, etc.
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and setuptools to latest secure versions
# This addresses CVEs like CVE-2025-47273 and CVE-2024-6345 for setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies with security updates
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create templates directory if it doesn't exist
RUN mkdir -p templates

# Set proper ownership for security
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (Cloud Run will override this)
EXPOSE 8080

# Set environment variables for production
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check for container monitoring
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application with Gunicorn in production
# Using secure configuration from gunicorn.conf.py
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]
