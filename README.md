# yourl.cloud - AI-Friendly URL Shortening Service

[![Deploy to Google Cloud Run](https://github.com/XDM-ZSBW/yourl.cloud/actions/workflows/deploy-to-cloud-run.yml/badge.svg)](https://github.com/XDM-ZSBW/yourl.cloud/actions/workflows/deploy-to-cloud-run.yml)

> **An ethical, AI-friendly URL shortening service following myl.zip standards and practices**

**Live Service**: [https://app-yourl-cloud-724465449320.us-west1.run.app/](https://app-yourl-cloud-724465449320.us-west1.run.app/)

**Session ID**: `f1d78acb-de07-46e0-bfa7-f5b75e3c0c49`

## 🎯 Project Overview

yourl.cloud is a modern, ethical URL shortening service built with Python Flask and designed for seamless Google Cloud Run deployment. The service prioritizes AI-friendly design, ethical standards, and accessibility for all users and AI agents.

### ✨ Key Features

- **🤖 AI-Friendly Design**: Structured data, meta tags, and API endpoints optimized for AI agents
- **🔒 Ethical Standards**: Following [myl.zip](https://myl.zip) ethics and responsible AI practices  
- **⚡ Cloud-Native**: Optimized for Google Cloud Run with automatic scaling
- **🎨 Modern UI**: Bootstrap 5 responsive design with Font Awesome icons
- **📱 Accessibility**: WCAG compliant with screen reader support
- **🔄 CI/CD Ready**: GitHub Actions workflows for continuous deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud Account with billing enabled
- Docker (optional, for local containerized development)

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/XDM-ZSBW/yourl.cloud.git
   cd yourl.cloud
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the service**:
   - Local: [http://localhost:8080](http://localhost:8080)
   - Health check: [http://localhost:8080/health](http://localhost:8080/health)

## ☁️ Cloud Deployment

### Option 1: Automatic Deployment (Recommended)

1. **Fork this repository** to your GitHub account
2. **Set up Google Cloud secrets** in your GitHub repository:
   - `GCP_PROJECT_ID`: Your Google Cloud Project ID
   - `GCP_SA_KEY`: Service Account JSON key with Cloud Run admin permissions
3. **Push to main branch** - GitHub Actions will automatically deploy!

### Option 2: Manual Deployment

1. **Build and deploy using Cloud Build**:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

2. **Or deploy directly**:
   ```bash
   gcloud run deploy yourl-cloud \
     --source . \
     --platform managed \
     --region us-west1 \
     --allow-unauthenticated
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8080` |
| `HOST` | Server host | `0.0.0.0` |
| `SESSION_ID` | Unique session identifier | `f1d78acb-de07-46e0-bfa7-f5b75e3c0c49` |
| `SECRET_KEY` | Flask secret key | `dev-key-change-in-production` |

### Cloud Run Configuration

- **Memory**: 1 GiB
- **CPU**: 1 vCPU  
- **Max Instances**: 10
- **Timeout**: 300 seconds
- **Concurrency**: 80 requests per instance

## 🤖 AI Agent Integration

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main interface with myl.zip sidebar |
| `/health` | GET | Health check and service status |
| `/api/services` | GET | Available services information |
| `/api/ethics` | GET | Ethics framework and compliance |
| `/api/shorten` | POST | URL shortening functionality |

### Example API Usage

```python
import requests

# Shorten a URL
response = requests.post('https://yourl.cloud/api/shorten', 
                        json={'url': 'https://example.com'})
data = response.json()
print(f"Shortened URL: {data['shortened_url']}")

# Get service information
services = requests.get('https://yourl.cloud/api/services').json()
print(f"Available services: {services['services']}")
```

```javascript
// JavaScript example
fetch('https://yourl.cloud/api/shorten', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: 'https://example.com' })
})
.then(response => response.json())
.then(data => console.log('Shortened:', data.shortened_url));
```

## 🏗️ Architecture

```
yourl.cloud/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── cloudbuild.yaml       # Cloud Build configuration
├── .github/workflows/    # GitHub Actions CI/CD
├── templates/            # Jinja2 HTML templates
├── static/               # CSS, JS, and image assets
└── README.md            # This documentation
```

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask 3.0, Waitress WSGI server
- **Frontend**: Bootstrap 5, Font Awesome icons, vanilla JavaScript
- **Cloud**: Google Cloud Run, Container Registry, Cloud Build
- **CI/CD**: GitHub Actions with automated deployments
- **Monitoring**: Built-in health checks and logging

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow ethical standards** as outlined by [myl.zip](https://myl.zip)
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Submit a Pull Request** - our automated workflow will notify maintainers

### Development Workflow

1. Make your changes following our coding standards
2. Test locally with `python app.py`
3. Commit with clear, descriptive messages
4. Push to your fork and create a Pull Request
5. Automated CI/CD will test and deploy upon approval

## 📚 References and Attribution

This project was built with guidance from official documentation, AI assistance, and community best practices:

### Official Documentation
- [Flask Documentation](https://flask.palletsprojects.com/) - Python web framework
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs) - Serverless container platform
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/) - CSS framework
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - CI/CD automation

### AI and Research Sources
- **Perplexity.ai** - AI research assistant for best practices and troubleshooting
- **GitHub Copilot** - AI code completion and suggestions
- **myl.zip** - Ethical AI standards and practices framework

### Community Resources
- [Stack Overflow](https://stackoverflow.com/) - Community problem solving
- [MDN Web Docs](https://developer.mozilla.org/) - Web standards documentation
- [Font Awesome](https://fontawesome.com/) - Icon library
- [Google Cloud Community](https://cloud.google.com/community) - Cloud deployment patterns

### Development Tools
- **Cursor IDE** - AI-powered development environment
- **Docker** - Containerization technology
- **Git/GitHub** - Version control and collaboration

## 🔒 Security and Privacy

- **HTTPS Everywhere**: All traffic encrypted in transit
- **No User Tracking**: Minimal data collection following privacy-first design
- **Secure Headers**: Implementation of security best practices
- **Regular Updates**: Automated dependency updates via GitHub Actions

## 🌍 Accessibility

This project follows Web Content Accessibility Guidelines (WCAG 2.1 AA):

- **Keyboard Navigation**: Full functionality accessible via keyboard
- **Screen Reader Support**: Semantic HTML and ARIA labels
- **Color Contrast**: High contrast ratios for visual accessibility
- **Responsive Design**: Mobile-first, works across all device sizes
- **Large Text Support**: Scalable fonts and layouts

## 📄 License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/XDM-ZSBW/yourl.cloud/issues)
- **Discussions**: [GitHub Discussions](https://github.com/XDM-ZSBW/yourl.cloud/discussions)
- **Documentation**: [GitHub Wiki](https://github.com/XDM-ZSBW/yourl.cloud/wiki)

---

**Built with ❤️ following ethical AI standards • Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49**
