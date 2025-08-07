# URL API Server with Visual Inspection and Google Cloud Run Support

**Simple Python Flask API that returns the request URL with visual inspection capabilities and Google Cloud Run deployment**

A self-executing Python Flask application that responds with the request URL and metadata, featuring visual inspection capabilities for PC and phone devices while following Friends and Family Guard ruleset settings. Enhanced for Google Cloud Run deployment with dual-mode endpoint support, production-ready WSGI server, and **full domain mapping compatibility**.

**All instances deploy as production instances** - the tester decides whether they're using it for personal or work purposes.

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/XDM-ZSBW/yourl.cloud.git
   cd yourl.cloud
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application** (All instances are production instances):
   ```bash
   # Using the startup script (recommended)
   python start.py
   
   # Or direct execution
   python app.py
   ```

4. **Access the API**: http://localhost:8080

### Production Deployment

**All instances deploy as production instances** - the tester decides the usage context:

```bash
# All instances use Gunicorn WSGI server
gunicorn --config gunicorn.conf.py wsgi:app

# Or using the startup script
python start.py
```

### Google Cloud Run Deployment

1. **Build and deploy using Cloud Build**:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

2. **Or deploy manually**:
   ```bash
   # Build the Docker image
   docker build -t yourl-cloud .
   
   # Deploy to Cloud Run
   gcloud run deploy yourl-cloud \
     --image yourl-cloud \
     --platform managed \
     --region us-west1 \
     --allow-unauthenticated \
     --port 8080
   ```

### 🌐 Domain Mapping Support

**Full compatibility with Google Cloud Run domain mappings** for custom domains like `yourl.cloud`:

```bash
# Map custom domain to Cloud Run service
gcloud run domain-mappings create \
  --service yourl-cloud \
  --domain yourl.cloud \
  --region us-west1 \
  --platform managed
```

**Key Domain Mapping Features:**
- ✅ **X-Forwarded Headers Support**: Proper handling of `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Proto`
- ✅ **Automatic Domain Detection**: Real-time domain and protocol detection
- ✅ **Health Check Compatibility**: `/health` endpoint for Cloud Run health checks
- ✅ **CORS Support**: Configured for domain mapping cross-origin requests
- ✅ **HTTPS Support**: Automatic HTTPS detection and protocol handling
- ✅ **Proxy Trust**: Configured to trust Cloud Run's proxy headers

For detailed domain mapping instructions, see [CLOUD_RUN_DOMAIN_MAPPING.md](CLOUD_RUN_DOMAIN_MAPPING.md).

## 🔄 How it works

* The `app.py` serves as a self-executing Flask application
* **Dual-mode endpoint**: GET shows landing page, POST handles authentication
* **Google Cloud Run support**: Reads `PORT` environment variable (default 8080)
* **Visual inspection interface** for PC, phone, and tablet devices
* **Friends and Family Guard** ruleset compliance
* **Watch devices blocked** for visual inspection per security rules
* **Demo authentication** with hardcoded password for rapid prototyping
* **Production WSGI server**: Gunicorn for all deployments
* **All instances are production instances**: Tester decides personal vs work usage
* **Domain mapping compatibility**: Full support for custom domains
* Includes health check and status endpoints
* Runs on port 8080 for Cloud Run compatibility

## 📁 Project Structure

```
yourl.cloud/
├── app.py              # Main Flask application with visual inspection and Cloud Run support
├── wsgi.py             # WSGI entry point for production deployment (domain mapping compatible)
├── gunicorn.conf.py    # Gunicorn configuration for production
├── start.py            # Startup script with auto-detection
├── requirements.txt    # Python dependencies (includes Gunicorn)
├── Dockerfile         # Docker configuration for Cloud Run (uses Gunicorn)
├── cloudbuild.yaml    # Google Cloud Build configuration
├── .dockerignore      # Docker ignore rules
├── templates/         # HTML templates
│   └── index.html     # Landing page template
├── README.md          # This file
├── CLOUD_RUN_DOMAIN_MAPPING.md  # Comprehensive domain mapping guide
└── .git/              # Version control
```

## 🛠️ API Endpoints

### Main Endpoint (Dual-mode)
- **URL**: `/`
- **Methods**: GET, POST
- **GET Response**: Landing page with input box and affiliate links
- **POST Response**: JSON with connections list (if password correct) or thanks page

### API Endpoint
- **URL**: `/api`
- **Methods**: GET, POST, PUT, DELETE, PATCH, OPTIONS
- **Response**: JSON with request URL and metadata, or HTML visual inspection interface

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Response**: Service health status with Cloud Run support info

### Status
- **URL**: `/status`
- **Method**: GET
- **Response**: Service information and configuration

### Friends and Family Guard Status
- **URL**: `/guard`
- **Method**: GET
- **Response**: Guard ruleset configuration and status

## 🔧 Configuration

### Environment Variables
- `PORT`: Port to run on (default: 8080 for Cloud Run)
- `FLASK_DEBUG`: Set to 'true' for debug mode (default: 'false')

### Demo Configuration
```python
DEMO_CONFIG = {
    "password": "yourl2024",  # Hardcoded demo password
    "connections": [
        # List of connection objects
    ]
}
```

### Friends and Family Guard Ruleset
```python
FRIENDS_FAMILY_GUARD = {
    "enabled": True,
    "visual_inspection": {
        "pc_allowed": True,      # Desktop computers
        "phone_allowed": True,   # Mobile phones
        "watch_blocked": True,   # Smartwatches (blocked)
        "tablet_allowed": True   # Tablets
    }
}
```

## 👁️ Visual Inspection

### Device Detection
The application automatically detects device types based on User-Agent strings:

- **PC**: Windows, macOS, Linux desktop browsers
- **Phone**: Mobile devices, Android, iPhone
- **Tablet**: iPad, Android tablets, Kindle
- **Watch**: Smartwatches, wearables (blocked for visual inspection)

### Visual Interface Features
- **Real-time URL display** with metadata
- **Device type identification** with color-coded badges
- **Friends and Family Guard status** indicator
- **Auto-refresh** every 30 seconds
- **Keyboard shortcuts** (Ctrl+R/Cmd+R for refresh)
- **Responsive design** for all screen sizes
- **Accessibility-friendly** interface

### Security Rules
- ✅ **PC**: Visual inspection allowed
- ✅ **Phone**: Visual inspection allowed
- ✅ **Tablet**: Visual inspection allowed
- ❌ **Watch**: Visual inspection blocked (security rule)

## 🔐 Authentication

### Demo Mode
- **Password**: `yourl2024` (hardcoded for rapid prototyping)
- **Purpose**: Replace with proper user/session authentication and database lookup before production
- **Access**: POST to `/` with password in form data

### Production Considerations
- Implement proper user authentication
- Add database integration for user management
- Replace hardcoded password with secure authentication
- Add session management and security headers

## 📊 Example Responses

### Landing Page (GET /)
Returns a modern HTML interface with:
- Input box for password authentication
- Affiliate links to related services
- Responsive design for all devices

### Authentication Success (POST /)
```json
{
  "status": "success",
  "message": "Authentication successful",
  "connections": [
    {
      "id": 1,
      "name": "GitHub Repository",
      "url": "https://github.com/XDM-ZSBW/yourl.cloud",
      "description": "Source code and documentation"
    }
  ],
  "timestamp": "2025-08-06T12:00:00.000000",
  "session_id": "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49",
  "organization": "Yourl Cloud Inc."
}
```

### API Response (GET /api)
```json
{
  "url": "http://localhost:8080/api/test",
  "base_url": "http://localhost:8080/api/test",
  "full_path": "/api/test",
  "method": "GET",
  "remote_addr": "127.0.0.1",
  "user_agent": "Mozilla/5.0...",
  "device_type": "pc",
  "visual_inspection_allowed": true,
  "hostname": "server-hostname",
  "timestamp": "2025-08-06T12:00:00.000000",
  "headers": {
    "Host": "localhost:8080",
    "User-Agent": "Mozilla/5.0..."
  },
  "session_id": "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49",
  "organization": "Yourl Cloud Inc.",
  "friends_family_guard": true
}
```

## 🛡️ Friends and Family Guard

### Purpose
The Friends and Family Guard ruleset ensures appropriate access control for visual inspection based on device capabilities and security considerations.

### Rules
1. **PC devices**: Full visual inspection access
2. **Phone devices**: Full visual inspection access
3. **Tablet devices**: Full visual inspection access
4. **Watch devices**: Visual inspection blocked (screen size and security considerations)

### Implementation
- Automatic device detection via User-Agent analysis
- Conditional HTML rendering based on device type
- Security-first approach for wearable devices
- Transparent status reporting

## ☁️ Google Cloud Run Support

### Features
- **Environment-based port configuration**: Reads `PORT` environment variable
- **Docker containerization**: Optimized Dockerfile for Cloud Run
- **Automated deployment**: Cloud Build configuration included
- **Scalability**: Automatic scaling based on demand
- **HTTPS support**: Automatic SSL/TLS termination

### Deployment Options
1. **Cloud Build**: Automated CI/CD pipeline
2. **Manual deployment**: Direct gcloud commands
3. **Local testing**: Docker container simulation

## 🤝 Contributing

1. Fork the repository
2. Make your changes
3. Test the API functionality and visual inspection
4. Ensure Friends and Family Guard compliance
5. Test Google Cloud Run deployment
6. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Note**: This project is designed to provide a simple, fast API that returns request URLs with visual inspection capabilities, following Friends and Family Guard security rules, and optimized for Google Cloud Run deployment.

## About

**Organization**: Yourl Cloud Inc.  
**Session ID**: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49  
**Repository**: https://github.com/XDM-ZSBW/yourl.cloud  
**Friends and Family Guard**: Enabled  
**Google Cloud Run**: Supported  
**Demo Mode**: Enabled (password: yourl2024)
