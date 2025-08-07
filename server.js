/**
 * yourl.cloud - Express.js Server for Google Cloud
 * ===============================================
 * 
 * Yourl-Cloud Inc. - AI-Friendly Service Hub
 * Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
 * 
 * HTTPS-enabled server for Google Cloud deployment with beta journaling tool
 */

const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const compression = require('compression');
const morgan = require('morgan');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 8080;
const SESSION_ID = process.env.SESSION_ID || 'f1d78acb-de07-46e0-bfa7-f5b75e3c0c49';
const ORGANIZATION = process.env.ORGANIZATION || 'Yourl-Cloud Inc.';

// Beta authorization configuration
const BETA_CONFIG = {
    enabled: true,
    inviteCodes: ['YOURL2024', 'BETA2024', 'JOURNAL2024'], // Add your invite codes here
    maxUsers: 100,
    sessionDuration: 180000, // 3 minutes in milliseconds
    requireAuth: true
};

// In-memory beta user storage (replace with database in production)
const betaUsers = new Map();
const betaSessions = new Map();

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
      fontSrc: ["'self'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://myl.zip", "https://perplexity.ai", "https://api.github.com"],
      frameSrc: ["'none'"],
      objectSrc: ["'none'"]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));

// CORS configuration
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? ['https://yourl.cloud', 'https://www.yourl.cloud']
    : true,
  credentials: true
}));

// Compression middleware
app.use(compression());

// Logging middleware
app.use(morgan('combined'));

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static file serving
app.use(express.static(path.join(__dirname, 'public'), {
  maxAge: '1d',
  etag: true,
  lastModified: true
}));

// Beta authorization middleware
function requireBetaAuth(req, res, next) {
    if (!BETA_CONFIG.enabled) {
        return res.status(404).json({ error: 'Beta feature not available' });
    }

    const sessionId = req.cookies?.betaSession || req.headers['x-beta-session'];
    const inviteCode = req.query.invite || req.body.invite;

    // Check if user has valid session
    if (sessionId && betaSessions.has(sessionId)) {
        const session = betaSessions.get(sessionId);
        if (Date.now() - session.timestamp < BETA_CONFIG.sessionDuration) {
            req.betaUser = session.user;
            return next();
        } else {
            // Session expired
            betaSessions.delete(sessionId);
            res.clearCookie('betaSession');
        }
    }

    // Check invite code
    if (inviteCode && BETA_CONFIG.inviteCodes.includes(inviteCode)) {
        const userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        const user = {
            id: userId,
            inviteCode: inviteCode,
            joinedAt: new Date().toISOString(),
            sessionId: sessionId
        };

        const session = {
            user: user,
            timestamp: Date.now()
        };

        betaUsers.set(userId, user);
        betaSessions.set(sessionId, session);

        // Set session cookie
        res.cookie('betaSession', sessionId, {
            httpOnly: true,
            secure: process.env.NODE_ENV === 'production',
            maxAge: BETA_CONFIG.sessionDuration,
            sameSite: 'strict'
        });

        req.betaUser = user;
        return next();
    }

    // No valid session or invite code
    return res.status(401).json({ 
        error: 'Beta access required',
        message: 'Please provide a valid invite code to access the beta journaling tool',
        inviteRequired: true
    });
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    sessionId: SESSION_ID,
    organization: ORGANIZATION,
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    betaEnabled: BETA_CONFIG.enabled
  });
});

// Status endpoint
app.get('/status', (req, res) => {
  res.status(200).json({
    service: 'yourl-cloud',
    organization: ORGANIZATION,
    sessionId: SESSION_ID,
    status: 'operational',
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    betaUsers: betaUsers.size,
    betaSessions: betaSessions.size
  });
});

// API endpoints for 3FA system
app.get('/api/3fa/status', (req, res) => {
  res.json({
    status: 'active',
    sessionId: SESSION_ID,
    features: ['encryption', 'authentication', 'scoring'],
    timestamp: new Date().toISOString()
  });
});

// Trust mesh network status
app.get('/api/trust-mesh/status', (req, res) => {
  res.json({
    network: 'active',
    sessionId: SESSION_ID,
    providers: ['myl.zip', 'perplexity.ai', 'healthcare-gateway'],
    trustLevel: 'UTILITY_LEVEL',
    timestamp: new Date().toISOString()
  });
});

// Beta journaling endpoints
app.get('/beta/journal', requireBetaAuth, (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'beta', 'journal.html'));
});

app.get('/beta/access', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'beta', 'access.html'));
});

app.post('/api/beta/auth', (req, res) => {
    const { inviteCode } = req.body;
    
    if (!inviteCode) {
        return res.status(400).json({ 
            error: 'Invite code required',
            message: 'Please provide an invite code to access the beta'
        });
    }

    if (!BETA_CONFIG.inviteCodes.includes(inviteCode)) {
        return res.status(401).json({ 
            error: 'Invalid invite code',
            message: 'The provided invite code is not valid'
        });
    }

    // Generate user and session
    const userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const user = {
        id: userId,
        inviteCode: inviteCode,
        joinedAt: new Date().toISOString(),
        sessionId: sessionId
    };

    const session = {
        user: user,
        timestamp: Date.now()
    };

    betaUsers.set(userId, user);
    betaSessions.set(sessionId, session);

    // Set session cookie
    res.cookie('betaSession', sessionId, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        maxAge: BETA_CONFIG.sessionDuration,
        sameSite: 'strict'
    });

    res.json({
        success: true,
        message: 'Beta access granted',
        sessionId: sessionId,
        user: {
            id: user.id,
            joinedAt: user.joinedAt
        },
        expiresAt: new Date(Date.now() + BETA_CONFIG.sessionDuration).toISOString()
    });
});

app.get('/api/beta/status', requireBetaAuth, (req, res) => {
    res.json({
        status: 'active',
        user: req.betaUser,
        sessionValid: true,
        expiresAt: new Date(Date.now() + BETA_CONFIG.sessionDuration).toISOString(),
        features: ['secure-journaling', 'privacy-first', 'auto-erase']
    });
});

app.post('/api/beta/logout', (req, res) => {
    const sessionId = req.cookies?.betaSession || req.headers['x-beta-session'];
    
    if (sessionId && betaSessions.has(sessionId)) {
        const session = betaSessions.get(sessionId);
        betaUsers.delete(session.user.id);
        betaSessions.delete(sessionId);
    }

    res.clearCookie('betaSession');
    res.json({ success: true, message: 'Logged out successfully' });
});

// Beta info endpoint (public)
app.get('/api/beta/info', (req, res) => {
    res.json({
        enabled: BETA_CONFIG.enabled,
        maxUsers: BETA_CONFIG.maxUsers,
        currentUsers: betaUsers.size,
        sessionDuration: BETA_CONFIG.sessionDuration,
        features: ['secure-journaling', 'privacy-first', 'auto-erase'],
        organization: ORGANIZATION,
        sessionId: SESSION_ID
    });
});

// Serve index.html for all other routes (SPA support)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong',
    sessionId: SESSION_ID,
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Yourl-Cloud Inc. server running on port ${PORT}`);
  console.log(`📊 Session ID: ${SESSION_ID}`);
  console.log(`🏢 Organization: ${ORGANIZATION}`);
  console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔒 HTTPS: ${process.env.NODE_ENV === 'production' ? 'Enabled' : 'Development'}`);
  console.log(`🧪 Beta Journaling: ${BETA_CONFIG.enabled ? 'Enabled' : 'Disabled'}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});

module.exports = app;
