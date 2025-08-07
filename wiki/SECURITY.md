# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| 0.9.x   | :white_check_mark: |
| 0.8.x   | :x:                |
| < 0.8   | :x:                |

## Reporting a Vulnerability

We take the security of Yourl.Cloud seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Contact Information

**Security Team Email**: security@yourl.cloud  
**PGP Key**: [Available upon request]  
**Reference Code**: `38f26aee-4e52-484e-bbc8-d973ca0bcb10`

### Reporting Process

1. **Private Disclosure**: Send your report to security@yourl.cloud with the subject line `[SECURITY] Vulnerability Report - [Reference Code: 38f26aee-4e52-484e-bbc8-d973ca0bcb10]`

2. **Include the following information**:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Suggested fix (if available)
   - Your contact information (optional)

3. **Acknowledgement Timeline**: We commit to acknowledging receipt of your report within **48 hours** of submission.

### Disclosure Process

1. **Initial Response**: Within 48 hours of receiving your report
2. **Assessment**: Our security team will assess the vulnerability within 5 business days
3. **Updates**: You will receive regular updates on the status of your report
4. **Resolution**: We will work to resolve the issue and provide a timeline for fixes
5. **Public Disclosure**: Vulnerabilities will be publicly disclosed after fixes are available, typically within 30 days of initial report

### Anonymous Reporting

We understand that some researchers prefer to remain anonymous. You may submit reports without providing personal information, but please include the reference code for tracking purposes.

## Scope

This security policy covers:

- ✅ **Core Application Code**: All Python Flask application code in the main repository
- ✅ **Dependencies**: Python packages listed in `requirements.txt`
- ✅ **Configuration Files**: Docker, Cloud Build, and deployment configurations
- ✅ **Documentation**: Security-relevant documentation and guides
- ✅ **API Endpoints**: All HTTP endpoints and their security implications

**Not Covered**:
- ❌ Third-party services (Google Cloud, GitHub, etc.)
- ❌ User-generated content or data
- ❌ External integrations not maintained by Yourl Cloud Inc.

## Attribution and Credit

We believe in recognizing the valuable contributions of security researchers:

- **Hall of Fame**: Security researchers who report valid vulnerabilities will be listed in our Security Hall of Fame (with permission)
- **Acknowledgements**: Public acknowledgements in release notes and security advisories
- **Optional Anonymity**: Researchers may choose to remain anonymous in public disclosures

## Security Best Practices

### For Contributors

1. **Code Review**: All code changes require security review
2. **Dependency Updates**: Regularly update dependencies to patch known vulnerabilities
3. **Testing**: Security testing is required for all new features
4. **Documentation**: Security-relevant changes must be documented

### For Users

1. **Keep Updated**: Always use the latest supported version
2. **Monitor Advisories**: Subscribe to security advisories
3. **Report Issues**: Report any security concerns immediately
4. **Follow Guidelines**: Adhere to deployment and configuration best practices

## Security Features

Yourl.Cloud implements several security measures:

- **Friends and Family Guard**: Device-based access control system
- **HTTPS Enforcement**: All communications encrypted in transit
- **Input Validation**: Comprehensive input sanitization and validation
- **Error Handling**: Secure error handling without information disclosure
- **Session Management**: Secure session handling and timeout mechanisms

## Compliance

This project adheres to:

- **OWASP Guidelines**: Following OWASP security best practices
- **Industry Standards**: Compliance with relevant security standards
- **Privacy Regulations**: Respect for user privacy and data protection
- **Open Source Security**: Following open source security best practices

## Contact Information

**Yourl Cloud Inc.**  
**Security Team**: security@yourl.cloud  
**General Inquiries**: info@yourl.cloud  
**Website**: https://yourl.cloud  
**Repository**: https://github.com/XDM-ZSBW/yourl.cloud  

## Thank You

We sincerely thank all security researchers and community members who help keep Yourl.Cloud secure. Your contributions are invaluable to our mission of providing secure, reliable cloud services.

**Reference Code**: `38f26aee-4e52-484e-bbc8-d973ca0bcb10`

---

*This security policy is maintained by Yourl Cloud Inc. and is subject to updates as our security practices evolve.*
