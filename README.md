# Yourl-Cloud Inc. - AI-Friendly Service Hub

> **An ethical, AI-friendly service hub following myl.zip standards and practices**

**Organization**: Yourl-Cloud Inc.  
**Repository**: [https://github.com/XDM-ZSBW/yourl.cloud](https://github.com/XDM-ZSBW/yourl.cloud)  
**Session ID**: `f1d78acb-de07-46e0-bfa7-f5b75e3c0c49`

## 🎯 Project Overview

Yourl-Cloud Inc. is a simplified, ethical service hub built with modern web standards. The service prioritizes AI-friendly design, ethical standards, and accessibility for all users and AI agents. Deployed on Google Cloud with HTTPS support and enterprise-grade security.

## 📁 Project Structure

```
yourl-cloud/
├── public/              # Static files for web server
│   ├── index.html       # Main service interface
│   ├── *.js            # JavaScript modules
│   └── nginx.conf      # Nginx configuration
├── app.yaml            # Google App Engine configuration
├── cloudbuild.yaml     # Google Cloud Build CI/CD
├── server.js           # Express.js server
├── package.json        # Node.js dependencies
├── deploy.sh           # Linux/macOS deployment script
├── deploy.bat          # Windows deployment script
├── README.md           # This documentation
└── docker-compose.yml  # Docker development setup
```

## ✨ Key Features

- **🤖 AI-Friendly Design**: Structured meta tags and ethical AI compliance
- **🔒 Security-First**: HTTPS-only, 256-bit encryption, IPv6 networking
- **🎨 Modern UI**: Bootstrap 5 responsive design with Font Awesome icons
- **📱 Accessibility**: WCAG compliant with full keyboard navigation
- **⚡ Lightweight**: Simplified structure with essential files only
- **☁️ Cloud-Native**: Google Cloud deployment with auto-scaling
- **🏢 Enterprise-Ready**: Yourl-Cloud Inc. branding and compliance

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/XDM-ZSBW/yourl.cloud.git
   cd yourl.cloud
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Access the application**: http://localhost:8080

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
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Deploy to App Engine
gcloud app deploy app.yaml

# Open the application
gcloud app browse
```

#### Deployment Features

- **🔒 HTTPS by Default**: Automatic SSL certificate management
- **⚡ Auto-scaling**: Handles traffic spikes automatically
- **🌍 Global CDN**: Fast loading worldwide
- **📊 Monitoring**: Built-in logging and metrics
- **🔄 CI/CD**: Automated deployment pipeline
- **💰 Cost-Effective**: Pay only for what you use

## 🐳 Docker Development

### Quick Docker Setup

1. **Build and run with Docker**:
   ```bash
   # Unix/Linux/macOS
   ./docker-build.sh run
   
   # Windows
   docker-build.bat run
   ```

2. **Access the application**:
   - **Main Application**: http://localhost:8080
   - **Health Check**: http://localhost:8080/health
   - **Status**: http://localhost:8080/status

### Docker Commands

```bash
# Build image only
./docker-build.sh build

# Run container
./docker-build.sh run

# Start container (if not running)
./docker-build.sh start

# Stop container
./docker-build.sh stop

# View logs
./docker-build.sh logs

# Check status
./docker-build.sh status

# Clean up
./docker-build.sh clean

# Show help
./docker-build.sh help
```

### Docker Compose

For more advanced deployments, use Docker Compose:

```bash
# Start with Docker Compose
docker-compose up -d

# Start with production profile
docker-compose --profile production up -d

# Stop services
docker-compose down
```

### Docker Features

- **🔒 Security**: Non-root user, security headers, rate limiting
- **⚡ Performance**: Nginx optimization, gzip compression, caching
- **🏥 Health Checks**: Automatic health monitoring
- **📊 Monitoring**: Built-in status and health endpoints
- **🔄 Auto-restart**: Container restart policy
- **🌐 IPv6 Support**: Full IPv6 compatibility

## 🔧 Security Requirements

- **HTTPS-only**: Secure connections required
- **256-bit encryption**: Minimum TLS encryption standard
- **IPv6 networking**: Next-generation IP protocol only
- **myl.zip compliance**: Ethical AI standards
- **Enterprise security**: SOC2, ISO27001 compliance ready

## 🤖 AI Agent Integration

### Meta Tags for AI Recognition
```html
<meta name="ai-service-entry-points" content="myl.zip">
<meta name="ai-ethics-framework" content="myl.zip-standards">
<meta name="session-id" content="f1d78acb-de07-46e0-bfa7-f5b75e3c0c49">
<meta name="organization" content="Yourl-Cloud Inc.">
```

## 🔐 3FA Encryption System

### Three-Factor Authentication (3FA)
Yourl-Cloud Inc. implements a **public, authorized solution for encrypting social proximity influence scores** with Three-Factor Authentication:

1. **Factor 1**: Password/Passphrase (something you know)
2. **Factor 2**: OTP/Hardware Token (something you have)  
3. **Factor 3**: 256-bit Random Key (something you possess)

### Key Features
- **256-bit AES-GCM encryption** for influence scores
- **PKI-based authorization** for public/private key management
- **Social proximity scoring** algorithm with customizable metrics
- **Browser-native cryptography** using Web Crypto API
- **Zero-knowledge architecture** - keys never leave client

### Usage Example
```javascript
// Initialize 3FA system
const auth = new ThreeFactorAuth();
const scoring = new SocialProximityScoring();
const pki = new PKIAuthorization();

// Generate 256-bit key (Factor 3)
const secretKey = await auth.generate256bitKey();

// Derive master key from three factors
const { masterKey, salt } = await auth.deriveMasterKey(password, otp, secretKey);

// Calculate and encrypt influence score
const score = scoring.calculateInfluenceScore(userData);
const encryption = new InfluenceScoreEncryption(masterKey);
const encryptedScore = await encryption.encryptScore(score, userData);

// PKI signing for authorization
const { privateKey, publicKey } = await pki.generateKeyPair();
const signature = await pki.signScore(privateKey, encryptedScore);
```

### Security Standards
- **HTTPS-only**: All connections encrypted in transit
- **256-bit minimum**: AES-256-GCM encryption standard
- **IPv6-only**: Next-generation networking protocol
- **myl.zip compliance**: Ethical AI standards
- **Zero-trust architecture**: Continuous verification

## 🔗 LinkedIn Social Authentication

### OAuth 2.0 Integration
Yourl-Cloud Inc. supports **LinkedIn social logon** with secure OAuth 2.0 authentication:

- **Secure OAuth 2.0 flow** with state parameter verification
- **Encrypted token storage** using Web Crypto API
- **Profile data access** (name, email, professional info)
- **Automatic token refresh** and session management
- **3FA integration** for enhanced security

### Setup Instructions
1. **Create LinkedIn App**:
   - Visit [LinkedIn Developers](https://www.linkedin.com/developers/)
   - Create a new app
   - Get your Client ID and Client Secret

2. **Configure OAuth**:
   ```javascript
   // Initialize LinkedIn Auth
   const linkedInAuth = new LinkedInAuth();
   linkedInAuth.init('YOUR_LINKEDIN_CLIENT_ID');
   ```

3. **Add to Yourl-Cloud Inc.**:
   - LinkedIn authentication is already integrated
   - Configure your Client ID in `linkedin_auth.js`
   - Set up redirect URI: `https://yourl.cloud/auth/linkedin/callback`

### Security Features
- **256-bit AES-GCM encryption** for token storage
- **State parameter verification** prevents CSRF attacks
- **Secure session management** with automatic expiration
- **Zero-knowledge architecture** - sensitive data encrypted locally

## 🔄 myl.zip Fallback System

### Offline-First Architecture
Yourl-Cloud Inc. implements a **robust fallback system** for myl.zip connections that ensures continuous access to ethical standards:

- **Local Cache**: Uses `localStorage` with keys `myl.zip` and `myl.zip-standards`
- **GitHub Cache**: Falls back to GitHub API when myl.zip is unreachable
- **Offline Content**: Provides offline fallback with last known good state
- **Connection Monitoring**: Real-time connection status checking

### Fallback Strategy
1. **Primary**: Direct connection to `https://myl.zip`
2. **Secondary**: Local cache (24-hour expiry)
3. **Tertiary**: GitHub cache (`https://api.github.com/repos/myl-zip/standards/contents`)
4. **Final**: Offline fallback content

### Features
- **Automatic Detection**: Monitors myl.zip connectivity in real-time
- **Smart Caching**: Stores content with SHA-256 checksums
- **User Notifications**: Shows connection status and fallback warnings
- **Healthcare Integration**: Includes healthcare trust level standards
- **Session Persistence**: Maintains state across browser sessions

### Usage Example
```javascript
// Initialize fallback system
const mylZipFallback = new MylZipFallback();
const status = await mylZipFallback.initialize();

if (status.status === 'CACHED') {
    mylZipFallback.showFallbackNotification();
}
```

## 🌐 Transition from Offline to Online: myl.zip Becomes a Connected Service

**Background:**  
Originally, the `myl.zip` project was developed as a local tool for managing secure downloads and handling thread-based context for agents and users, with a focus on privacy-first, *offline* workflows.

**Evolution:**  
With advancements in secure web development and user demand for *online collaboration* and *short-term encrypted memory sharing* with AI agents, the codebase at this repository now forms the basis for the transition to a **cloud-based, privacy-centric journaling and context-sharing platform**.

### 🔐 Inspiration: Secure AI Memory Sharing

Drawing from the architectural design (`download.html`, `thread-downloader.html`) and local-first ethos:

- **Short-term AI memory (ephemeral storage)** is now supported online with browser-based encryption.  
- User notes, prompt experiments, or session context can be shared *temporarily* between devices or AI agents.
- **Everything is encrypted client-side:** The server only relays encrypted blobs; all secrets/keys stay with the user.
- Optional *"erase on unfocus"* or *timer-based* destruction enhances privacy, inspired by the original download-and-forget model.

### 🚀 How It Works:  
- Use the online journaling tool at [yourl.cloud] for 3-minute, privacy-preserving writing sessions.
- Each session encrypts content in-browser before any upload or sharing; only those with the session key can decrypt.
- Data is auto-erased after session expiry or tab unfocus unless *explicitly* shared or saved by the user.
- No permanent log or server-side learning—preserving the spirit of ephemeral, user-controlled offline tools.

### 📁 Project Structure Enhancements

The core files (`download.html`, `thread-downloader.html`) now serve as templates for:
- Browser-based encryption/decryption utilities
- Secure, short-lived session sharing between users/agents
- Transparent, open-source logic so users can verify privacy guarantees

### 🤝 Contributing to the Future

We welcome PRs that:
- Refactor utilities for better cryptographic hygiene
- Extend the API for additional cipher support or federated AI agent memory integrations
- Improve in-browser UX for secure journaling or ephemeral context exchange

**Note:**  
This project is dedicated to maintaining the highest standards for user privacy—both on disk and in the cloud. All encryption logic is open-source and auditable, and no plaintext user data is ever stored server-side by default.

## 🌐 Trust Mesh Network

### CA NONPROFIT Trust Architecture
Yourl-Cloud Inc. implements a **conceptual Trust Mesh Network** for ethical service access:

- **CA NONPROFIT Status**: Filing under review (Operating: August 4, 2025)
- **Trust Levels**: Bank, Utility, Healthcare, and Mesh security standards
- **Mesh Nodes**: Core, Gateway, and Distribution nodes
- **Service Providers**: Integration with myl.zip, Perplexity AI, and Healthcare Gateway

### Security Levels

#### 🏦 BANK_LEVEL
- **Encryption**: AES-256-GCM
- **Authentication**: 3FA (Three-Factor Authentication)
- **Audit**: REAL_TIME monitoring
- **Compliance**: SOC2 Type 2
- **Trust Score**: 0.95+ required

#### 🏥 HEALTHCARE_LEVEL (NEW)
- **Encryption**: AES-256-GCM
- **Authentication**: 3FA with role-based access
- **Audit**: REAL_TIME monitoring
- **Compliance**: HIPAA, SOC2 Type 2, ISO27001
- **Features**: Patient privacy, end-to-end encryption, role-based access
- **Trust Score**: 0.98+ required

#### ⚡ UTILITY_LEVEL
- **Encryption**: AES-256-GCM
- **Authentication**: 2FA
- **Audit**: HOURLY monitoring
- **Compliance**: ISO27001
- **Trust Score**: 0.85+ required

#### 🌐 MESH_LEVEL
- **Encryption**: AES-256-GCM
- **Authentication**: 1FA
- **Audit**: DAILY monitoring
- **Compliance**: GDPR
- **Trust Score**: 0.75+ required

### Healthcare Integration
- **HIPAA Compliance**: Full healthcare data protection standards
- **Patient Privacy**: End-to-end encryption for patient data
- **Audit Trail**: Comprehensive logging for healthcare access
- **Access Control**: Role-based access with 3FA authentication
- **Healthcare Gateway**: Dedicated service provider for healthcare services

## 🌐 Access Points

1. **Primary Service**: [https://yourl.cloud](https://yourl.cloud)
2. **Ethics Framework**: [https://myl.zip](https://myl.zip)
3. **AI Research**: [https://perplexity.ai](https://perplexity.ai)
4. **Repository**: [https://github.com/XDM-ZSBW/yourl.cloud](https://github.com/XDM-ZSBW/yourl.cloud)

## 🛠️ Technology Stack

- **HTML5**: Modern web standards
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icon library
- **Vanilla JavaScript**: No frameworks, lightweight
- **Progressive Enhancement**: Works without JavaScript
- **3FA Encryption**: Three-Factor Authentication with 256-bit keys
- **AES-256-GCM**: Military-grade encryption for influence scores
- **PKI**: Public Key Infrastructure for authorization
- **Web Crypto API**: Browser-native cryptographic operations
- **myl.zip Fallback**: Offline-first architecture with GitHub cache
- **Trust Mesh Network**: CA NONPROFIT trust architecture
- **Healthcare Integration**: HIPAA-compliant healthcare trust level
- **LinkedIn OAuth 2.0**: Social authentication integration
- **Local Storage**: Client-side caching with dual-key strategy
- **Google Cloud**: App Engine, Cloud Build, Container Registry
- **Express.js**: Node.js web framework
- **HTTPS**: Automatic SSL certificate management

## 📚 References and Attribution

### Official Documentation
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Font Awesome Icons](https://fontawesome.com/)
- [MDN Web Docs](https://developer.mozilla.org/) - Web standards
- [Google Cloud Documentation](https://cloud.google.com/docs/)

### AI and Research Sources
- **Perplexity.ai** - AI research and best practices
- **myl.zip** - Ethical AI standards framework
- **GitHub Copilot** - Development assistance

### Development Tools
- **Cursor IDE** - AI-powered development environment
- **Git/GitHub** - Version control and collaboration
- **Google Cloud SDK** - Cloud deployment and management

## 🤝 Contributing

1. **Fork the repository**
2. **Follow myl.zip ethical standards**
3. **Keep structure simple** (essential files only)
4. **Test accessibility** and responsive design
5. **Submit a Pull Request**

## 📄 License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/XDM-ZSBW/yourl.cloud/issues)
- **Documentation**: Check the `status` file for current project state
- **Reset Utilities**: Use provided reset scripts for clean state
- **Deployment**: Use `deploy.sh` or `deploy.bat` for Google Cloud deployment

---

**Built with ❤️ by Yourl-Cloud Inc. following ethical AI standards • Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49**

## 🧪 Beta Journaling Tool

### Privacy-First Secure Journaling
Yourl-Cloud Inc. offers a **closed beta journaling tool** with privacy-first design and automatic content erasure:

- **🔒 Privacy-First**: Content never leaves your browser unless you explicitly save it
- **⏰ 3-Minute Timer**: Automatic content erasure when timer expires or page loses focus
- **💾 Local Download**: Save journal entries as text files to your device
- **🛡️ Secure Sessions**: Encrypted sessions with automatic logout and content clearing

### Beta Access
- **Invite Codes**: `YOURL2024`, `BETA2024`, `JOURNAL2024`
- **Access URL**: `https://yourl.cloud/beta/access`
- **Journal URL**: `https://yourl.cloud/beta/journal`
- **Session Duration**: 3 minutes per session
- **Max Users**: 100 concurrent beta users

### Security Features
- **No server storage**: Journal content never stored on servers
- **Local processing**: All journaling functionality runs in browser
- **Automatic erasure**: Content cleared on timer expiry or page blur
- **Session management**: Temporary access with automatic expiration

### Quick Start
1. Visit `https://yourl.cloud/beta/access`
2. Enter invite code (e.g., `YOURL2024`)
3. Access journaling tool at `https://yourl.cloud/beta/journal`
4. Start writing with 3-minute timer
5. Save content to device before timer expires

For detailed documentation, see [BETA_JOURNALING.md](BETA_JOURNALING.md).