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