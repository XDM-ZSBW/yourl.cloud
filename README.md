# yourl.cloud - AI-Friendly Service Hub

> **An ethical, AI-friendly service hub following myl.zip standards and practices**

**Repository**: [https://github.com/XDM-ZSBW/yourl.cloud](https://github.com/XDM-ZSBW/yourl.cloud)  
**Session ID**: `f1d78acb-de07-46e0-bfa7-f5b75e3c0c49`

## 🎯 Project Overview

yourl.cloud is a simplified, ethical service hub built with modern web standards. The service prioritizes AI-friendly design, ethical standards, and accessibility for all users and AI agents.

## 📁 Project Structure

```
yourl.cloud/
├── index.html    # Main service interface
├── README.md     # This documentation
├── reset.sh      # Unix/Linux reset script
├── reset.bat     # Windows reset script  
├── reset         # Python reset utility
└── status        # Project status file
```

## ✨ Key Features

- **🤖 AI-Friendly Design**: Structured meta tags and ethical AI compliance
- **🔒 Security-First**: HTTPS-only, 256-bit encryption, IPv6 networking
- **🎨 Modern UI**: Bootstrap 5 responsive design with Font Awesome icons
- **📱 Accessibility**: WCAG compliant with full keyboard navigation
- **⚡ Lightweight**: Simplified structure with essential files only

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/XDM-ZSBW/yourl.cloud.git
   cd yourl.cloud
   ```

2. **Open index.html** in your browser or serve with any web server

3. **Reset project** (if needed):
   ```bash
   # Unix/Linux/macOS
   ./reset.sh
   
   # Windows
   reset.bat
   
   # Python utility
   python reset
   ```

## 🔧 Security Requirements

- **HTTPS-only**: Secure connections required
- **256-bit encryption**: Minimum TLS encryption standard
- **IPv6 networking**: Next-generation IP protocol only
- **myl.zip compliance**: Ethical AI standards

## 🤖 AI Agent Integration

### Meta Tags for AI Recognition
```html
<meta name="ai-service-entry-points" content="myl.zip">
<meta name="ai-ethics-framework" content="myl.zip-standards">
<meta name="session-id" content="f1d78acb-de07-46e0-bfa7-f5b75e3c0c49">
```

## 🔐 3FA Encryption System

### Three-Factor Authentication (3FA)
yourl.cloud implements a **public, authorized solution for encrypting social proximity influence scores** with Three-Factor Authentication:

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
yourl.cloud now supports **LinkedIn social logon** with secure OAuth 2.0 authentication:

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

3. **Add to yourl.cloud**:
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
yourl.cloud implements a **robust fallback system** for myl.zip connections that ensures continuous access to ethical standards:

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

## 🌐 Trust Mesh Network

### CA NONPROFIT Trust Architecture
yourl.cloud implements a **conceptual Trust Mesh Network** for ethical service access:

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

## 📚 References and Attribution

### Official Documentation
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Font Awesome Icons](https://fontawesome.com/)
- [MDN Web Docs](https://developer.mozilla.org/) - Web standards

### AI and Research Sources
- **Perplexity.ai** - AI research and best practices
- **myl.zip** - Ethical AI standards framework
- **GitHub Copilot** - Development assistance

### Development Tools
- **Cursor IDE** - AI-powered development environment
- **Git/GitHub** - Version control and collaboration

## 🤝 Contributing

1. **Fork the repository**
2. **Follow myl.zip ethical standards**
3. **Keep structure simple** (6 essential files only)
4. **Test accessibility** and responsive design
5. **Submit a Pull Request**

## 📄 License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/XDM-ZSBW/yourl.cloud/issues)
- **Documentation**: Check the `status` file for current project state
- **Reset Utilities**: Use provided reset scripts for clean state

---

**Built with ❤️ following ethical AI standards • Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49**