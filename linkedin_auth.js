/**
 * yourl.cloud - LinkedIn Social Authentication
 * ===========================================
 * 
 * LinkedIn OAuth 2.0 integration for yourl.cloud
 * Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
 * 
 * References:
 * - LinkedIn OAuth 2.0 Documentation
 * - Web Crypto API for secure token storage
 * - 3FA integration with social proximity scoring
 */

class LinkedInAuth {
    constructor() {
        this.sessionId = "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49";
        this.clientId = null; // Set your LinkedIn App Client ID
        this.redirectUri = window.location.origin + '/auth/linkedin/callback';
        this.scope = 'r_liteprofile r_emailaddress';
        this.state = this.generateState();
        
        // LinkedIn OAuth endpoints
        this.authUrl = 'https://www.linkedin.com/oauth/v2/authorization';
        this.tokenUrl = 'https://www.linkedin.com/oauth/v2/accessToken';
        this.profileUrl = 'https://api.linkedin.com/v2/me';
        this.emailUrl = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))';
    }

    /**
     * Generate secure state parameter for OAuth
     */
    generateState() {
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Initialize LinkedIn authentication
     * @param {string} clientId - LinkedIn App Client ID
     */
    init(clientId) {
        this.clientId = clientId;
        console.log('LinkedIn Auth initialized for yourl.cloud');
    }

    /**
     * Start LinkedIn OAuth flow
     */
    login() {
        if (!this.clientId) {
            throw new Error('LinkedIn Client ID not configured. Call init() first.');
        }

        const params = new URLSearchParams({
            response_type: 'code',
            client_id: this.clientId,
            redirect_uri: this.redirectUri,
            state: this.state,
            scope: this.scope
        });

        const authUrl = `${this.authUrl}?${params.toString()}`;
        
        // Store state for verification
        sessionStorage.setItem('linkedin_state', this.state);
        
        // Redirect to LinkedIn
        window.location.href = authUrl;
    }

    /**
     * Handle OAuth callback
     * @param {string} code - Authorization code from LinkedIn
     * @param {string} state - State parameter for verification
     */
    async handleCallback(code, state) {
        // Verify state parameter
        const storedState = sessionStorage.getItem('linkedin_state');
        if (state !== storedState) {
            throw new Error('Invalid state parameter');
        }

        try {
            // Exchange code for access token
            const tokenData = await this.exchangeCodeForToken(code);
            
            // Get user profile
            const profile = await this.getProfile(tokenData.access_token);
            
            // Get user email
            const email = await this.getEmail(tokenData.access_token);
            
            // Store user data securely
            await this.storeUserData({
                profile: profile,
                email: email,
                accessToken: tokenData.access_token,
                expiresAt: Date.now() + (tokenData.expires_in * 1000)
            });

            return {
                profile: profile,
                email: email,
                accessToken: tokenData.access_token
            };

        } catch (error) {
            console.error('LinkedIn callback failed:', error);
            throw error;
        }
    }

    /**
     * Exchange authorization code for access token
     * @param {string} code - Authorization code
     */
    async exchangeCodeForToken(code) {
        const response = await fetch(this.tokenUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                grant_type: 'authorization_code',
                code: code,
                client_id: this.clientId,
                client_secret: this.clientSecret, // In production, handle this server-side
                redirect_uri: this.redirectUri
            })
        });

        if (!response.ok) {
            throw new Error('Failed to exchange code for token');
        }

        return await response.json();
    }

    /**
     * Get LinkedIn user profile
     * @param {string} accessToken - LinkedIn access token
     */
    async getProfile(accessToken) {
        const response = await fetch(this.profileUrl, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'X-Restli-Protocol-Version': '2.0.0'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to get LinkedIn profile');
        }

        return await response.json();
    }

    /**
     * Get LinkedIn user email
     * @param {string} accessToken - LinkedIn access token
     */
    async getEmail(accessToken) {
        const response = await fetch(this.emailUrl, {
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'X-Restli-Protocol-Version': '2.0.0'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to get LinkedIn email');
        }

        const data = await response.json();
        return data.elements?.[0]?.['handle~']?.emailAddress || null;
    }

    /**
     * Store user data securely using Web Crypto API
     * @param {Object} userData - User profile and token data
     */
    async storeUserData(userData) {
        try {
            // Encrypt user data before storing
            const key = await this.generateStorageKey();
            const encryptedData = await this.encryptData(JSON.stringify(userData), key);
            
            // Store encrypted data
            localStorage.setItem('linkedin_user_data', encryptedData);
            
            console.log('LinkedIn user data stored securely');
        } catch (error) {
            console.error('Failed to store user data:', error);
            throw error;
        }
    }

    /**
     * Retrieve stored user data
     */
    async getUserData() {
        try {
            const encryptedData = localStorage.getItem('linkedin_user_data');
            if (!encryptedData) return null;

            const key = await this.generateStorageKey();
            const decryptedData = await this.decryptData(encryptedData, key);
            
            const userData = JSON.parse(decryptedData);
            
            // Check if token is expired
            if (userData.expiresAt && Date.now() > userData.expiresAt) {
                this.logout();
                return null;
            }

            return userData;
        } catch (error) {
            console.error('Failed to retrieve user data:', error);
            return null;
        }
    }

    /**
     * Generate encryption key for local storage
     */
    async generateStorageKey() {
        const password = this.sessionId + 'linkedin_storage';
        const salt = new TextEncoder().encode('yourl_cloud_linkedin_salt');
        
        const keyMaterial = await crypto.subtle.importKey(
            'raw',
            new TextEncoder().encode(password),
            'PBKDF2',
            false,
            ['deriveBits', 'deriveKey']
        );

        return await crypto.subtle.deriveKey(
            {
                name: 'PBKDF2',
                salt: salt,
                iterations: 100000,
                hash: 'SHA-256'
            },
            keyMaterial,
            { name: 'AES-GCM', length: 256 },
            true,
            ['encrypt', 'decrypt']
        );
    }

    /**
     * Encrypt data for storage
     */
    async encryptData(data, key) {
        const iv = crypto.getRandomValues(new Uint8Array(12));
        const encodedData = new TextEncoder().encode(data);
        
        const encryptedData = await crypto.subtle.encrypt(
            { name: 'AES-GCM', iv: iv },
            key,
            encodedData
        );

        const encryptedArray = new Uint8Array(encryptedData);
        const combined = new Uint8Array(iv.length + encryptedArray.length);
        combined.set(iv);
        combined.set(encryptedArray, iv.length);

        return btoa(String.fromCharCode(...combined));
    }

    /**
     * Decrypt stored data
     */
    async decryptData(encryptedData, key) {
        const combined = new Uint8Array(
            atob(encryptedData).split('').map(char => char.charCodeAt(0))
        );
        
        const iv = combined.slice(0, 12);
        const data = combined.slice(12);

        const decryptedData = await crypto.subtle.decrypt(
            { name: 'AES-GCM', iv: iv },
            key,
            data
        );

        return new TextDecoder().decode(decryptedData);
    }

    /**
     * Logout user and clear stored data
     */
    logout() {
        localStorage.removeItem('linkedin_user_data');
        sessionStorage.removeItem('linkedin_state');
        console.log('LinkedIn user logged out');
    }

    /**
     * Check if user is authenticated
     */
    async isAuthenticated() {
        const userData = await this.getUserData();
        return userData !== null;
    }

    /**
     * Get current user profile
     */
    async getCurrentUser() {
        return await this.getUserData();
    }
}

// LinkedIn Auth UI Component
class LinkedInAuthUI {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.auth = new LinkedInAuth();
        this.init();
    }

    async init() {
        if (!this.container) {
            console.error('LinkedIn Auth container not found');
            return;
        }

        // Check if user is already authenticated
        const isAuthenticated = await this.auth.isAuthenticated();
        
        if (isAuthenticated) {
            this.showAuthenticatedUI();
        } else {
            this.showLoginUI();
        }
    }

    showLoginUI() {
        this.container.innerHTML = `
            <div class="linkedin-auth-section">
                <h5 class="text-center mb-3">
                    <i class="fab fa-linkedin me-2"></i>LinkedIn Authentication
                </h5>
                <div class="d-grid">
                    <button class="btn btn-linkedin btn-lg" onclick="linkedInAuthUI.login()">
                        <i class="fab fa-linkedin me-2"></i>Sign in with LinkedIn
                    </button>
                </div>
                <div class="text-center mt-2">
                    <small class="text-muted">
                        <i class="fas fa-shield-alt me-1"></i>Secure OAuth 2.0 authentication
                    </small>
                </div>
            </div>
        `;
    }

    showAuthenticatedUI() {
        this.auth.getCurrentUser().then(userData => {
            if (userData) {
                this.container.innerHTML = `
                    <div class="linkedin-auth-section">
                        <h5 class="text-center mb-3">
                            <i class="fab fa-linkedin me-2"></i>LinkedIn Profile
                        </h5>
                        <div class="text-center">
                            <div class="mb-2">
                                <strong>${userData.profile.localizedFirstName} ${userData.profile.localizedLastName}</strong>
                            </div>
                            <div class="text-muted small">
                                ${userData.email || 'Email not available'}
                            </div>
                        </div>
                        <div class="d-grid gap-2 mt-3">
                            <button class="btn btn-outline-secondary btn-sm" onclick="linkedInAuthUI.logout()">
                                <i class="fas fa-sign-out-alt me-2"></i>Sign Out
                            </button>
                        </div>
                    </div>
                `;
            }
        });
    }

    async login() {
        try {
            // Initialize with your LinkedIn App Client ID
            this.auth.init('YOUR_LINKEDIN_CLIENT_ID');
            this.auth.login();
        } catch (error) {
            console.error('LinkedIn login failed:', error);
            alert('LinkedIn login failed. Please try again.');
        }
    }

    async logout() {
        this.auth.logout();
        this.showLoginUI();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        LinkedInAuth,
        LinkedInAuthUI
    };
} else {
    // Browser environment - attach to window
    window.LinkedInAuth = LinkedInAuth;
    window.LinkedInAuthUI = LinkedInAuthUI;
}
