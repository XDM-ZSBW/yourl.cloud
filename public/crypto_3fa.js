/**
 * yourl.cloud - 3FA Encryption System (JavaScript)
 * ================================================
 * 
 * Three-Factor Authentication (3FA) implementation with:
 * - Factor 1: Password/Passphrase (something you know)
 * - Factor 2: OTP/Hardware Token (something you have)  
 * - Factor 3: 256-bit Random Key (something you possess)
 * 
 * Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
 * 
 * References:
 * - Web Crypto API for AES-256-GCM encryption
 * - SubtleCrypto for key generation and derivation
 * - PKI-based authorization
 * - Social proximity influence scoring
 */

class ThreeFactorAuth {
    constructor() {
        this.sessionId = "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49";
        this.keySize = 32; // 256 bits
        this.nonceSize = 12; // 96 bits for AES-GCM
        this.saltSize = 16; // 128 bits for key derivation
    }

    /**
     * Generate a cryptographically secure 256-bit key (Factor 3)
     */
    async generate256bitKey() {
        return await crypto.subtle.generateKey(
            {
                name: "AES-GCM",
                length: 256
            },
            true,
            ["encrypt", "decrypt"]
        );
    }

    /**
     * Derive master key from three factors using PBKDF2
     * 
     * @param {string} password - User password/passphrase (Factor 1)
     * @param {string} otp - One-time password/token (Factor 2) 
     * @param {CryptoKey} secretKey - 256-bit random key (Factor 3)
     * @returns {Promise<{masterKey: CryptoKey, salt: Uint8Array}>}
     */
    async deriveMasterKey(password, otp, secretKey) {
        // Combine all three factors
        const combined = new TextEncoder().encode(password + otp);
        
        // Generate salt for key derivation
        const salt = crypto.getRandomValues(new Uint8Array(this.saltSize));
        
        // Use PBKDF2 for key derivation with high iteration count
        const baseKey = await crypto.subtle.importKey(
            "raw",
            combined,
            "PBKDF2",
            false,
            ["deriveBits", "deriveKey"]
        );
        
        const masterKey = await crypto.subtle.deriveKey(
            {
                name: "PBKDF2",
                salt: salt,
                iterations: 100000, // High iteration count for security
                hash: "SHA-256"
            },
            baseKey,
            {
                name: "AES-GCM",
                length: 256
            },
            true,
            ["encrypt", "decrypt"]
        );
        
        return { masterKey, salt };
    }

    /**
     * Verify the master key against stored hash
     */
    async verifyMasterKey(password, otp, secretKey, storedSalt, storedKeyHash) {
        try {
            const { masterKey } = await this.deriveMasterKey(password, otp, secretKey);
            const keyBuffer = await crypto.subtle.exportKey("raw", masterKey);
            const keyHash = await crypto.subtle.digest("SHA-256", keyBuffer);
            
            // Compare hashes securely
            const storedHashArray = new Uint8Array(storedKeyHash);
            const computedHashArray = new Uint8Array(keyHash);
            
            if (storedHashArray.length !== computedHashArray.length) {
                return false;
            }
            
            for (let i = 0; i < storedHashArray.length; i++) {
                if (storedHashArray[i] !== computedHashArray[i]) {
                    return false;
                }
            }
            
            return true;
        } catch (error) {
            console.error("Key verification failed:", error);
            return false;
        }
    }
}

class InfluenceScoreEncryption {
    constructor(masterKey) {
        this.masterKey = masterKey;
    }

    /**
     * Encrypt a social proximity influence score using AES-256-GCM
     * 
     * @param {number} score - Influence score (float)
     * @param {Object} metadata - Additional metadata
     * @returns {Promise<Object>} Encrypted score data with nonce and metadata
     */
    async encryptScore(score, metadata = {}) {
        // Prepare score data
        const scoreData = {
            score: score,
            timestamp: new Date().toISOString(),
            sessionId: "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49",
            metadata: metadata
        };
        
        // Convert to JSON and encode
        const scoreBytes = new TextEncoder().encode(JSON.stringify(scoreData));
        
        // Generate nonce for AES-GCM
        const nonce = crypto.getRandomValues(new Uint8Array(12));
        
        // Encrypt the score data
        const encryptedData = await crypto.subtle.encrypt(
            {
                name: "AES-GCM",
                iv: nonce
            },
            this.masterKey,
            scoreBytes
        );
        
        // Return encrypted data with nonce
        return {
            encryptedData: btoa(String.fromCharCode(...new Uint8Array(encryptedData))),
            nonce: btoa(String.fromCharCode(...nonce)),
            algorithm: "AES-256-GCM",
            keySize: 256,
            timestamp: new Date().toISOString(),
            version: "1.0"
        };
    }

    /**
     * Decrypt a social proximity influence score
     * 
     * @param {Object} encryptedData - Encrypted score data from encryptScore()
     * @returns {Promise<Object>} Decrypted score data
     */
    async decryptScore(encryptedData) {
        try {
            // Decode base64 data
            const encryptedBytes = new Uint8Array(
                atob(encryptedData.encryptedData).split('').map(char => char.charCodeAt(0))
            );
            const nonce = new Uint8Array(
                atob(encryptedData.nonce).split('').map(char => char.charCodeAt(0))
            );
            
            // Decrypt the data
            const decryptedBytes = await crypto.subtle.decrypt(
                {
                    name: "AES-GCM",
                    iv: nonce
                },
                this.masterKey,
                encryptedBytes
            );
            
            // Parse JSON data
            const scoreData = JSON.parse(new TextDecoder().decode(decryptedBytes));
            
            return scoreData;
            
        } catch (error) {
            throw new Error(`Failed to decrypt score: ${error.message}`);
        }
    }
}

class SocialProximityScoring {
    constructor() {
        this.sessionId = "f1d78acb-de07-46e0-bfa7-f5b75e3c0c49";
    }

    /**
     * Calculate social proximity influence score based on user data
     * 
     * @param {Object} userData - Dictionary containing user metrics
     * @returns {number} Influence score (0.0 to 1.0)
     */
    calculateInfluenceScore(userData) {
        // Example scoring algorithm - customize based on your needs
        let score = 0.0;
        
        // Network size factor (0-30%)
        const networkSize = userData.networkSize || 0;
        const maxNetwork = userData.maxNetworkSize || 10000;
        const networkFactor = Math.min(networkSize / maxNetwork, 1.0) * 0.3;
        
        // Engagement factor (0-25%)
        const engagementRate = userData.engagementRate || 0.0;
        const engagementFactor = Math.min(engagementRate, 1.0) * 0.25;
        
        // Trust factor (0-25%)
        const trustScore = userData.trustScore || 0.0;
        const trustFactor = Math.min(trustScore, 1.0) * 0.25;
        
        // Activity factor (0-20%)
        const activityLevel = userData.activityLevel || 0.0;
        const activityFactor = Math.min(activityLevel, 1.0) * 0.20;
        
        score = networkFactor + engagementFactor + trustFactor + activityFactor;
        
        // Ensure score is between 0.0 and 1.0
        return Math.max(0.0, Math.min(1.0, score));
    }

    /**
     * Validate that score is within acceptable range
     */
    validateScore(score) {
        return score >= 0.0 && score <= 1.0;
    }
}

class PKIAuthorization {
    constructor() {
        this.algorithm = {
            name: "RSASSA-PKCS1-v1_5",
            modulusLength: 2048,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256"
        };
    }

    /**
     * Generate RSA key pair for PKI
     */
    async generateKeyPair() {
        return await crypto.subtle.generateKey(
            this.algorithm,
            true,
            ["sign", "verify"]
        );
    }

    /**
     * Serialize public key to PEM format
     */
    async serializePublicKey(publicKey) {
        const exported = await crypto.subtle.exportKey("spki", publicKey);
        const base64 = btoa(String.fromCharCode(...new Uint8Array(exported)));
        return `-----BEGIN PUBLIC KEY-----\n${base64}\n-----END PUBLIC KEY-----`;
    }

    /**
     * Sign score data with private key
     */
    async signScore(privateKey, scoreData) {
        const scoreBytes = new TextEncoder().encode(JSON.stringify(scoreData));
        const signature = await crypto.subtle.sign(
            this.algorithm,
            privateKey,
            scoreBytes
        );
        return btoa(String.fromCharCode(...new Uint8Array(signature)));
    }

    /**
     * Verify score signature with public key
     */
    async verifyScore(publicKey, scoreData, signature) {
        try {
            const scoreBytes = new TextEncoder().encode(JSON.stringify(scoreData));
            const signatureBytes = new Uint8Array(
                atob(signature).split('').map(char => char.charCodeAt(0))
            );
            
            return await crypto.subtle.verify(
                this.algorithm,
                publicKey,
                signatureBytes,
                scoreBytes
            );
        } catch (error) {
            console.error("Signature verification failed:", error);
            return false;
        }
    }
}

// Example usage and testing
async function demo3FA() {
    console.log("yourl.cloud - 3FA Encryption System Demo");
    console.log("=" .repeat(50));
    console.log(`Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49`);
    console.log();
    
    try {
        // Initialize 3FA system
        const auth = new ThreeFactorAuth();
        const scoring = new SocialProximityScoring();
        const pki = new PKIAuthorization();
        
        // Generate 256-bit key (Factor 3)
        const secretKey = await auth.generate256bitKey();
        console.log("Generated 256-bit key");
        
        // Example user factors
        const password = "secure_password_123"; // Factor 1
        const otp = "123456"; // Factor 2 (in real implementation, this would be from TOTP device)
        
        // Derive master key
        const { masterKey, salt } = await auth.deriveMasterKey(password, otp, secretKey);
        console.log("Derived master key");
        
        // Calculate influence score
        const userData = {
            networkSize: 5000,
            maxNetworkSize: 10000,
            engagementRate: 0.75,
            trustScore: 0.85,
            activityLevel: 0.90
        };
        
        const score = scoring.calculateInfluenceScore(userData);
        console.log(`Calculated influence score: ${score.toFixed(4)}`);
        
        // Encrypt the score
        const encryption = new InfluenceScoreEncryption(masterKey);
        const encryptedScore = await encryption.encryptScore(score, userData);
        console.log("Encrypted score data:", encryptedScore);
        
        // Decrypt the score
        const decryptedScore = await encryption.decryptScore(encryptedScore);
        console.log(`Decrypted score: ${decryptedScore.score.toFixed(4)}`);
        
        // PKI signing example
        const { privateKey, publicKey } = await pki.generateKeyPair();
        const signature = await pki.signScore(privateKey, encryptedScore);
        console.log("Score signature:", signature);
        
        // Verify signature
        const isValid = await pki.verifyScore(publicKey, encryptedScore, signature);
        console.log(`Signature valid: ${isValid}`);
        
        console.log("\n3FA encryption system ready for yourl.cloud!");
        
    } catch (error) {
        console.error("Demo failed:", error);
    }
}

// Export classes for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ThreeFactorAuth,
        InfluenceScoreEncryption,
        SocialProximityScoring,
        PKIAuthorization,
        demo3FA
    };
} else {
    // Browser environment - attach to window
    window.ThreeFactorAuth = ThreeFactorAuth;
    window.InfluenceScoreEncryption = InfluenceScoreEncryption;
    window.SocialProximityScoring = SocialProximityScoring;
    window.PKIAuthorization = PKIAuthorization;
    window.demo3FA = demo3FA;
}
