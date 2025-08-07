# Yourl-Cloud Inc. - Domain Display Service

> **A simple, fast-loading service that displays the domain in the user's preferred language locale**

**Organization**: Yourl-Cloud Inc.  
**Repository**: [https://github.com/XDM-ZSBW/yourl.cloud](https://github.com/XDM-ZSBW/yourl.cloud)  
**Session ID**: `f1d78acb-de07-46e0-bfa7-f5b75e3c0c49`  
**Current Version**: 2.0.0 (Simplified Domain Display)

## 🎯 Project Overview

Yourl-Cloud Inc. is a **simplified, fast-deploying domain display service** built for speed and efficiency. The service automatically detects the user's preferred language and displays the current domain in a clean, modern interface. Deployed on Google Cloud with HTTPS support and minimal resource usage.

## 📁 Project Structure

```
yourl-cloud/
├── public/              # Static files for web server
│   └── index.html       # Main domain display interface
├── app.yaml            # Google App Engine configuration (simplified)
├── README.md           # This documentation
└── Status              # Current project status
```

## ✨ Key Features

- **🌐 Language Detection**: Automatically detects and displays user's preferred language
- **🔒 HTTPS-Only**: Secure connections with automatic SSL certificates
- **⚡ Fast Loading**: Minimal resources, optimized for speed
- **📱 Responsive Design**: Works on all devices and screen sizes
- **🎨 Modern UI**: Clean, gradient-based design with glassmorphism effects
- **☁️ Cloud-Native**: Google Cloud App Engine deployment
- **💰 Cost-Effective**: Minimal resource usage (0.5 CPU, 0.25GB RAM)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/XDM-ZSBW/yourl.cloud.git
   cd yourl.cloud
   ```

2. **Serve static files** (any method):
   ```bash
   # Using Python
   python -m http.server 8080
   
   # Using Node.js
   npx serve public
   
   # Using PHP
   php -S localhost:8080 -t public
   ```

3. **Access the application**: http://localhost:8080

### Google Cloud Deployment

#### Prerequisites

1. **Install Google Cloud SDK**:
   - [Download and install](https://cloud.google.com/sdk/docs/install)
   - Authenticate: `gcloud auth login`

2. **Create Google Cloud Project**:
   ```bash
   gcloud projects create yourl-cloud-inc --name="Yourl-Cloud Inc."
   gcloud config set project yourl-cloud-inc
   ```

#### Deploy to Google Cloud

**Option 1: Automated Deployment (Recommended)**

```bash
# Linux/macOS
./deploy.sh

# Windows
deploy.bat
```

**Option 2: Manual Deployment**

```bash
# Enable required APIs
gcloud services enable appengine.googleapis.com

# Deploy to App Engine
gcloud app deploy app.yaml

# Open the application
gcloud app browse
```

#### Deployment Features

- **🔒 HTTPS by Default**: Automatic SSL certificate management
- **⚡ Auto-scaling**: Handles traffic spikes automatically (0-5 instances)
- **🌍 Global CDN**: Fast loading worldwide
- **📊 Monitoring**: Built-in logging and metrics
- **💰 Cost-Effective**: Pay only for what you use (minimal resources)

## 🎨 User Interface

### What Users See

When users visit your service, they'll see:

1. **Organization Branding**: "Yourl-Cloud Inc." header
2. **Domain Display**: Current domain (e.g., `https://cloud-yourl-724465449320.us-west1.run.app/`)
3. **Language Information**: User's preferred language (e.g., "Your preferred language: English (en-US)")
4. **Status Information**: Session ID and deployment timestamp

### Language Support

The service automatically detects and displays support for:
- **English** (en)
- **Spanish** (es)
- **French** (fr)
- **German** (de)
- **Italian** (it)
- **Portuguese** (pt)
- **Russian** (ru)
- **Chinese** (zh)
- **Japanese** (ja)
- **Korean** (ko)
- **And more** (falls back to language code)

## 🔧 Technical Details

### Architecture

- **Static File Serving**: No server-side processing required
- **Client-Side Language Detection**: Uses `navigator.language` API
- **Responsive Design**: CSS Grid and Flexbox for modern layouts
- **Progressive Enhancement**: Works without JavaScript
- **Accessibility**: WCAG compliant with semantic HTML

### Performance

- **Load Time**: < 1 second on average
- **Resource Usage**: 0.5 CPU, 0.25GB RAM
- **File Size**: < 10KB total
- **Dependencies**: None (vanilla HTML/CSS/JS)

### Security

- **HTTPS-Only**: All connections encrypted
- **No Data Collection**: No user data stored or transmitted
- **Privacy-First**: No tracking or analytics
- **Secure Headers**: Automatic security headers via App Engine

## 🌐 Access Points

1. **Primary Service**: [https://yourl.cloud](https://yourl.cloud)
2. **Cloud Run**: [https://cloud-yourl-724465449320.us-west1.run.app/](https://cloud-yourl-724465449320.us-west1.run.app/)
3. **Repository**: [https://github.com/XDM-ZSBW/yourl.cloud](https://github.com/XDM-ZSBW/yourl.cloud)

## 🛠️ Technology Stack

- **HTML5**: Modern web standards
- **CSS3**: Flexbox, Grid, Gradients, Glassmorphism
- **Vanilla JavaScript**: No frameworks, lightweight
- **Google Cloud**: App Engine, Cloud Build
- **HTTPS**: Automatic SSL certificate management

## 📚 References and Attribution

### Official Documentation
- [MDN Web Docs](https://developer.mozilla.org/) - Web standards
- [Google Cloud Documentation](https://cloud.google.com/docs/)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)

### Development Tools
- **Cursor IDE** - AI-powered development environment
- **Git/GitHub** - Version control and collaboration
- **Google Cloud SDK** - Cloud deployment and management

## 🤝 Contributing

1. **Fork the repository**
2. **Keep it simple** - focus on speed and efficiency
3. **Test accessibility** and responsive design
4. **Submit a Pull Request**

## 📄 License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/XDM-ZSBW/yourl.cloud/issues)
- **Documentation**: Check the `Status` file for current project state
- **Deployment**: Use `deploy.sh` or `deploy.bat` for Google Cloud deployment

---

**Built with ❤️ by Yourl-Cloud Inc. • Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49 • Version: 2.0.0**