/**
 * yourl.cloud - myl.zip Fallback System
 * =====================================
 * 
 * Fallback system for myl.zip connections with GitHub cache integration
 * Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
 * 
 * References:
 * - GitHub API for cache retrieval
 * - Local storage for last known good state
 * - Healthcare trust level integration
 * - Offline-first architecture
 */

class MylZipFallback {
    constructor() {
        this.sessionId = "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49";
        this.mylZipUrl = "https://myl.zip";
        this.githubCacheUrl = "https://api.github.com/repos/myl-zip/standards/contents";
        this.localStorageKey = "myl.zip"; // Updated to use myl.zip as requested
        this.localStorageStandardsKey = "myl.zip-standards"; // Added for standards-specific cache
        this.cacheExpiryHours = 24;
        
        // Fallback states
        this.fallbackStates = {
            ONLINE: "ONLINE",
            CACHED: "CACHED", 
            OFFLINE: "OFFLINE"
        };
        
        this.currentState = this.fallbackStates.ONLINE;
    }

    /**
     * Initialize myl.zip fallback system
     */
    async initialize() {
        console.log('myl.zip Fallback System initialized');
        
        // Check current connection status
        const connectionStatus = await this.checkConnection();
        
        if (connectionStatus.connected) {
            this.currentState = this.fallbackStates.ONLINE;
            await this.updateLastKnownGood();
        } else {
            this.currentState = this.fallbackStates.CACHED;
            await this.loadFromCache();
        }
        
        return {
            status: this.currentState,
            lastUpdated: await this.getLastKnownGoodTimestamp(),
            cacheAge: await this.getCacheAge()
        };
    }

    /**
     * Check myl.zip connection status
     */
    async checkConnection() {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
            
            const response = await fetch(this.mylZipUrl, {
                method: 'HEAD',
                signal: controller.signal,
                mode: 'no-cors'
            });
            
            clearTimeout(timeoutId);
            
            return {
                connected: true,
                timestamp: new Date().toISOString(),
                responseTime: Date.now()
            };
            
        } catch (error) {
            console.warn('myl.zip connection failed:', error.message);
            return {
                connected: false,
                timestamp: new Date().toISOString(),
                error: error.message
            };
        }
    }

    /**
     * Update last known good state from myl.zip
     */
    async updateLastKnownGood() {
        try {
            const response = await fetch(this.mylZipUrl);
            const content = await response.text();
            
            const lastKnownGood = {
                content: content,
                timestamp: new Date().toISOString(),
                source: 'myl.zip',
                checksum: await this.generateChecksum(content)
            };
            
            // Store in both main cache and standards-specific cache
            localStorage.setItem(this.localStorageKey, JSON.stringify(lastKnownGood));
            localStorage.setItem(this.localStorageStandardsKey, JSON.stringify(lastKnownGood));
            console.log('Last known good state updated from myl.zip');
            
            return lastKnownGood;
            
        } catch (error) {
            console.error('Failed to update last known good state:', error);
            throw error;
        }
    }

    /**
     * Load content from GitHub cache
     */
    async loadFromGitHubCache() {
        try {
            // Fetch from GitHub API
            const response = await fetch(this.githubCacheUrl);
            const data = await response.json();
            
            if (Array.isArray(data)) {
                // Find the main standards file
                const standardsFile = data.find(item => 
                    item.name === 'standards.md' || 
                    item.name === 'README.md' ||
                    item.name.includes('standards')
                );
                
                if (standardsFile) {
                    const contentResponse = await fetch(standardsFile.download_url);
                    const content = await contentResponse.text();
                    
                    const cachedData = {
                        content: content,
                        timestamp: new Date().toISOString(),
                        source: 'github_cache',
                        checksum: await this.generateChecksum(content),
                        githubUrl: standardsFile.html_url
                    };
                    
                    // Store in both main cache and standards-specific cache
                    localStorage.setItem(this.localStorageKey, JSON.stringify(cachedData));
                    localStorage.setItem(this.localStorageStandardsKey, JSON.stringify(cachedData));
                    console.log('Content loaded from GitHub cache');
                    
                    return cachedData;
                }
            }
            
            throw new Error('No suitable standards file found in GitHub cache');
            
        } catch (error) {
            console.error('Failed to load from GitHub cache:', error);
            throw error;
        }
    }

    /**
     * Load content from local cache
     */
    async loadFromCache() {
        try {
            // Check both main cache and standards-specific cache
            let cachedData = localStorage.getItem(this.localStorageKey) || localStorage.getItem(this.localStorageStandardsKey);
            
            if (cachedData) {
                const parsed = JSON.parse(cachedData);
                const cacheAge = await this.getCacheAge();
                
                // Check if cache is still valid (24 hours)
                if (cacheAge < this.cacheExpiryHours * 60 * 60 * 1000) {
                    console.log('Loading from local cache');
                    return parsed;
                } else {
                    console.log('Cache expired, attempting GitHub cache');
                    return await this.loadFromGitHubCache();
                }
            } else {
                console.log('No local cache found, attempting GitHub cache');
                return await this.loadFromGitHubCache();
            }
            
        } catch (error) {
            console.error('Failed to load from cache:', error);
            return this.getOfflineFallback();
        }
    }

    /**
     * Get offline fallback content
     */
    getOfflineFallback() {
        const offlineContent = {
            content: `
# myl.zip - Offline Standards

## Ethical AI Standards (Cached)

### Core Principles
- **Transparency**: All AI systems must be transparent in their operations
- **Accountability**: Clear responsibility for AI system outcomes
- **Fairness**: Unbiased and equitable AI systems
- **Privacy**: Protection of user data and privacy
- **Security**: Robust security measures for AI systems

### Trust Levels
- **BANK_LEVEL**: 3FA, REAL_TIME audit, SOC2_TYPE2 compliance
- **UTILITY_LEVEL**: 2FA, HOURLY audit, ISO27001 compliance
- **HEALTHCARE_LEVEL**: 3FA, REAL_TIME audit, HIPAA compliance
- **MESH_LEVEL**: 1FA, DAILY audit, GDPR compliance

### Healthcare Standards
- **HIPAA Compliance**: Full healthcare data protection
- **Patient Privacy**: End-to-end encryption for patient data
- **Audit Trail**: Comprehensive logging for healthcare access
- **Access Control**: Role-based access with 3FA authentication

*This content is cached from the last known good state of myl.zip*
*Last updated: ${new Date().toISOString()}*
            `,
            timestamp: new Date().toISOString(),
            source: 'offline_fallback',
            checksum: 'offline_fallback_hash'
        };
        
        return offlineContent;
    }

    /**
     * Generate checksum for content
     */
    async generateChecksum(content) {
        const encoder = new TextEncoder();
        const data = encoder.encode(content);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Get last known good timestamp
     */
    async getLastKnownGoodTimestamp() {
        // Check both main cache and standards-specific cache
        let cachedData = localStorage.getItem(this.localStorageKey) || localStorage.getItem(this.localStorageStandardsKey);
        if (cachedData) {
            const parsed = JSON.parse(cachedData);
            return parsed.timestamp;
        }
        return null;
    }

    /**
     * Get cache age in milliseconds
     */
    async getCacheAge() {
        const timestamp = await this.getLastKnownGoodTimestamp();
        if (timestamp) {
            return Date.now() - new Date(timestamp).getTime();
        }
        return Infinity;
    }

    /**
     * Get current myl.zip content
     */
    async getContent() {
        const connectionStatus = await this.checkConnection();
        
        if (connectionStatus.connected) {
            this.currentState = this.fallbackStates.ONLINE;
            return await this.updateLastKnownGood();
        } else {
            this.currentState = this.fallbackStates.CACHED;
            return await this.loadFromCache();
        }
    }

    /**
     * Display fallback notification
     */
    showFallbackNotification() {
        const notification = document.createElement('div');
        notification.className = 'alert alert-warning alert-dismissible fade show position-fixed';
        notification.style.cssText = 'top: 20px; left: 20px; z-index: 9999; min-width: 300px;';
        
        notification.innerHTML = `
            <strong><i class="fas fa-exclamation-triangle me-2"></i>myl.zip Connection Lost</strong>
            <br>
            <small>Displaying last known good state from cache. 
            <a href="#" onclick="mylZipFallback.refreshConnection()">Try to reconnect</a></small>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 10000);
    }

    /**
     * Refresh connection to myl.zip
     */
    async refreshConnection() {
        const connectionStatus = await this.checkConnection();
        
        if (connectionStatus.connected) {
            this.currentState = this.fallbackStates.ONLINE;
            await this.updateLastKnownGood();
            
            // Show success notification
            this.showSuccessNotification();
            
            return true;
        } else {
            this.currentState = this.fallbackStates.CACHED;
            this.showFallbackNotification();
            return false;
        }
    }

    /**
     * Show success notification
     */
    showSuccessNotification() {
        const notification = document.createElement('div');
        notification.className = 'alert alert-success alert-dismissible fade show position-fixed';
        notification.style.cssText = 'top: 20px; left: 20px; z-index: 9999; min-width: 300px;';
        
        notification.innerHTML = `
            <strong><i class="fas fa-check-circle me-2"></i>myl.zip Connected</strong>
            <br>
            <small>Connection restored successfully.</small>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        MylZipFallback
    };
} else {
    // Browser environment - attach to window
    window.MylZipFallback = MylZipFallback;
}
