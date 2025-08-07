/**
 * yourl.cloud - Express.js Server for Google Cloud
 * ===============================================
 * 
 * Yourl-Cloud Inc. - AI-Friendly Service Hub
 * Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
 * 
 * HTTPS-enabled server for Google Cloud deployment
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

// Static file serving
app.use(express.static(path.join(__dirname, 'public'), {
  maxAge: '1d',
  etag: true,
  lastModified: true
}));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    sessionId: SESSION_ID,
    organization: ORGANIZATION,
    version: '1.0.0',
    environment: process.env.NODE_ENV || 'development'
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
    environment: process.env.NODE_ENV || 'development'
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
