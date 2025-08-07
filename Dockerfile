# yourl.cloud - AI-Friendly Service Hub Dockerfile
# ================================================
# 
# Multi-stage build for optimal performance and security
# Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
# 
# Production stage with nginx
FROM nginx:alpine

# Install necessary packages
RUN apk add --no-cache \
    curl \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1001 -S nginx-user && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx-user -g nginx-user nginx-user

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy all application files
COPY . /usr/share/nginx/html/

# Remove unnecessary files from the web root
RUN rm -f /usr/share/nginx/html/Dockerfile \
    && rm -f /usr/share/nginx/html/docker-compose.yml \
    && rm -f /usr/share/nginx/html/docker-build.sh \
    && rm -f /usr/share/nginx/html/docker-build.bat \
    && rm -f /usr/share/nginx/html/.dockerignore \
    && rm -f /usr/share/nginx/html/.gcloudignore \
    && rm -f /usr/share/nginx/html/README.md \
    && rm -f /usr/share/nginx/html/LICENSE \
    && rm -f /usr/share/nginx/html/reset* \
    && rm -f /usr/share/nginx/html/Status \
    && rm -f /usr/share/nginx/html/crypto_3fa.py \
    && rm -rf /usr/share/nginx/html/.git \
    && rm -rf /usr/share/nginx/html/.github

# Set proper permissions
RUN chown -R nginx-user:nginx-user /usr/share/nginx/html && \
    chown -R nginx-user:nginx-user /var/cache/nginx && \
    chown -R nginx-user:nginx-user /var/log/nginx && \
    chown -R nginx-user:nginx-user /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx-user:nginx-user /var/run/nginx.pid

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Switch to non-root user
USER nginx-user

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
