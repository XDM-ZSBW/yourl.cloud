# Yourl-Cloud Inc. - Beta Journaling Tool

> **Privacy-first, secure journaling tool for closed beta users**

**Organization**: Yourl-Cloud Inc.  
**Session ID**: `f1d78acb-de07-46e0-bfa7-f5b75e3c0c49`  
**Status**: Closed Beta

## 🎯 Overview

The Beta Journaling Tool is a privacy-first journaling experience that runs entirely in your browser. Your content never leaves your device unless you explicitly save it, ensuring maximum privacy and security.

## 🔒 Security Features

### Privacy-First Design
- **No server storage**: Your journal content never leaves your browser
- **Local processing**: All journaling happens in your browser using JavaScript
- **Automatic erasure**: Content is cleared when timer expires or page loses focus
- **Secure sessions**: Encrypted sessions with automatic logout

### Timer System
- **3-minute timer**: Automatic countdown with visual indicators
- **Warning states**: Color-coded warnings at 60s and 30s remaining
- **Auto-erase**: Content automatically cleared when timer expires
- **Page blur detection**: Content cleared when page loses focus

### Content Management
- **Local download**: Save journal entries as text files to your device
- **Session persistence**: Content persists during active session (localStorage)
- **Clear functionality**: Manual content clearing option
- **Auto-save**: Content automatically saved during active session

## 🚀 Access

### Beta Access Requirements
- **Invite code required**: Access is restricted to invited users only
- **Session-based**: Temporary access with automatic expiration
- **Limited users**: Maximum 100 concurrent beta users

### Available Invite Codes
- `YOURL2024` - Primary beta access code
- `BETA2024` - Secondary beta access code  
- `JOURNAL2024` - Journal-specific beta access code

### Access Process
1. Visit `/beta/access` to enter invite code
2. Enter valid invite code (e.g., `YOURL2024`)
3. Gain access to `/beta/journal` for 3 minutes
4. Journal content automatically cleared on session expiry

## 📁 File Structure

```
public/beta/
├── journal.html          # Main journaling interface
├── access.html           # Beta access page
└── README.md            # This documentation

server.js                 # Express server with beta endpoints
```

## 🔧 Technical Implementation

### Frontend (JavaScript)
- **SecureJournal class**: Main journaling functionality
- **Timer management**: 3-minute countdown with visual feedback
- **Event handling**: Page blur, visibility change, beforeunload
- **Local storage**: Session persistence during active session
- **File download**: Blob-based local file saving

### Backend (Node.js/Express)
- **Beta authorization**: Invite code validation and session management
- **Route protection**: Middleware for beta access control
- **Session management**: In-memory session storage (replace with database in production)
- **API endpoints**: Authentication, status, and logout endpoints

### Security Measures
- **HTTPS-only**: All connections encrypted in transit
- **Session cookies**: HttpOnly, secure, sameSite cookies
- **Content Security Policy**: Strict CSP headers
- **CORS configuration**: Restricted origins in production

## 🎨 User Interface

### Journal Interface (`/beta/journal`)
- **Clean design**: Modern, responsive Bootstrap 5 interface
- **Timer display**: Large countdown timer with color-coded warnings
- **Text area**: Full-featured textarea with auto-focus
- **Control buttons**: Save to device and clear content options
- **Status indicators**: Real-time session status and timer state

### Access Interface (`/beta/access`)
- **Invite code form**: Simple form for entering beta access codes
- **Feature showcase**: Overview of beta features and security measures
- **Privacy notice**: Clear information about data handling
- **Status indicators**: System status and availability

## 🔄 API Endpoints

### Beta Authentication
- `POST /api/beta/auth` - Authenticate with invite code
- `GET /api/beta/status` - Check beta session status
- `POST /api/beta/logout` - Logout from beta session
- `GET /api/beta/info` - Public beta information

### Response Examples

#### Successful Authentication
```json
{
  "success": true,
  "message": "Beta access granted",
  "sessionId": "session_1234567890_abc123",
  "user": {
    "id": "user_1234567890_xyz789",
    "joinedAt": "2024-01-01T12:00:00.000Z"
  },
  "expiresAt": "2024-01-01T12:03:00.000Z"
}
```

#### Beta Status
```json
{
  "status": "active",
  "user": {
    "id": "user_1234567890_xyz789",
    "inviteCode": "YOURL2024",
    "joinedAt": "2024-01-01T12:00:00.000Z"
  },
  "sessionValid": true,
  "expiresAt": "2024-01-01T12:03:00.000Z",
  "features": ["secure-journaling", "privacy-first", "auto-erase"]
}
```

## 🚀 Deployment

### Prerequisites
- Node.js 18+ installed
- Google Cloud project configured
- HTTPS enabled (required for production)

### Local Development
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Access beta tool
# http://localhost:8080/beta/access
```

### Production Deployment
```bash
# Deploy to Google Cloud
./deploy.sh

# Access beta tool
# https://yourl.cloud/beta/access
```

## 🔍 Monitoring

### Health Checks
- `GET /health` - Overall system health including beta status
- `GET /status` - Detailed status including beta user count
- `GET /api/beta/info` - Beta-specific information

### Logging
- **Access logs**: Beta access attempts and session creation
- **Error logs**: Invalid invite codes and session failures
- **Performance logs**: Response times and system metrics

## 🛡️ Privacy & Compliance

### Data Handling
- **No content storage**: Journal content never stored on servers
- **Session data only**: Only session metadata stored (user ID, timestamp)
- **Automatic cleanup**: Session data automatically cleared on expiry
- **Local processing**: All journaling functionality runs in browser

### Compliance
- **GDPR compliant**: No personal data collection or storage
- **Privacy by design**: Privacy-first architecture
- **Transparent**: Clear privacy notices and data handling policies
- **User control**: Users have full control over their content

## 🔮 Future Enhancements

### Planned Features
- **Database integration**: Persistent user management
- **Advanced encryption**: End-to-end encryption for saved content
- **Cloud sync**: Optional cloud storage for saved entries
- **Mobile app**: Native mobile application
- **Social features**: Sharing and collaboration options

### Technical Improvements
- **Performance optimization**: Faster loading and response times
- **Offline support**: PWA capabilities for offline journaling
- **Advanced security**: Multi-factor authentication
- **Analytics**: Usage analytics (privacy-preserving)

## 📞 Support

### Beta Support
- **Issues**: Report bugs via GitHub Issues
- **Feedback**: Share feedback via beta feedback form
- **Documentation**: Check this README for technical details
- **Status**: Monitor system status at `/status`

### Contact
- **Organization**: Yourl-Cloud Inc.
- **Session ID**: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
- **Repository**: https://github.com/XDM-ZSBW/yourl.cloud

---

**Built with ❤️ by Yourl-Cloud Inc. following ethical AI standards • Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49**
