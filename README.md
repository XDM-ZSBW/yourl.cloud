# URL API Server with Visual Inspection

**Simple Python Flask API that returns the request URL with visual inspection capabilities**

A self-executing Python Flask application that responds with the request URL and metadata, featuring visual inspection capabilities for PC and phone devices while following Friends and Family Guard ruleset settings.

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

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the API**: http://localhost:80

### Production Deployment

```bash
# Run on port 80 (requires sudo/root)
sudo python app.py

# Or use a process manager like systemd
sudo systemctl start url-api
```

## 🔄 How it works

* The `app.py` serves as a self-executing Flask application
* Responds to all HTTP methods (GET, POST, PUT, DELETE, PATCH, OPTIONS)
* Returns JSON with the request URL and metadata
* **Visual inspection interface** for PC, phone, and tablet devices
* **Friends and Family Guard** ruleset compliance
* **Watch devices blocked** for visual inspection per security rules
* Includes health check and status endpoints
* Runs on port 80 for public access

## 📁 Project Structure

```
yourl.cloud/
├── app.py              # Main Flask application with visual inspection
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .git/              # Version control
```

## 🛠️ API Endpoints

### Main Endpoint
- **URL**: `/`
- **Methods**: GET, POST, PUT, DELETE, PATCH, OPTIONS
- **Response**: JSON with request URL and metadata, or HTML visual inspection interface

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Response**: Service health status

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
- `FLASK_DEBUG`: Set to 'true' for debug mode (default: 'false')

### Port Configuration
- Default port: 80 (HTTP)
- Configurable in `app.py`

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

## 📊 Example Response

### JSON Response
```json
{
  "url": "http://localhost:80/api/test",
  "base_url": "http://localhost:80/api/test",
  "full_path": "/api/test",
  "method": "GET",
  "remote_addr": "127.0.0.1",
  "user_agent": "Mozilla/5.0...",
  "device_type": "pc",
  "visual_inspection_allowed": true,
  "hostname": "server-hostname",
  "timestamp": "2025-08-06T12:00:00.000000",
  "headers": {
    "Host": "localhost:80",
    "User-Agent": "Mozilla/5.0..."
  },
  "session_id": "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49",
  "organization": "Yourl-Cloud Inc.",
  "friends_family_guard": true
}
```

### Visual Inspection Interface
When accessing from a browser on allowed devices, you'll see:
- **Real-time URL display** in a modern, glassmorphic interface
- **Device type badge** (PC/Phone/Tablet)
- **Timestamp and session information**
- **Friends and Family Guard status**
- **Auto-refresh functionality**

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

## 🤝 Contributing

1. Fork the repository
2. Make your changes
3. Test the API functionality and visual inspection
4. Ensure Friends and Family Guard compliance
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Note**: This project is designed to provide a simple, fast API that returns request URLs with visual inspection capabilities, following Friends and Family Guard security rules.

## About

**Organization**: Yourl-Cloud Inc.  
**Session ID**: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49  
**Repository**: https://github.com/XDM-ZSBW/yourl.cloud  
**Friends and Family Guard**: Enabled
