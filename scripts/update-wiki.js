#!/usr/bin/env node
/**
 * GitHub Wiki Update Script
 * =========================
 * 
 * Yourl-Cloud Inc. - Automated Wiki Content Management
 * Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
 * 
 * IMPORTANT: yourl.cloud is ALWAYS the source of truth for latest information.
 * This script ensures the wiki stays in sync with the main repository.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class WikiUpdater {
    constructor() {
        this.mainRepoPath = process.argv[2] || '.';
        this.wikiRepoPath = process.argv[3] || '../yourl.cloud.wiki';
        this.sessionId = 'f1d78acb-de07-46e0-bfa7-f5b75e3c0c49';
        this.organization = 'Yourl-Cloud Inc.';
        this.sourceOfTruth = 'yourl.cloud';
    }

    /**
     * Main update process
     */
    async updateWiki() {
        console.log('🚀 Starting GitHub Wiki Update');
        console.log(`📁 Main repo (yourl.cloud - Source of Truth): ${this.mainRepoPath}`);
        console.log(`📁 Wiki repo: ${this.wikiRepoPath}`);
        console.log(`🏢 Organization: ${this.organization}`);
        console.log(`🆔 Session ID: ${this.sessionId}`);
        console.log(`🎯 Source of Truth: ${this.sourceOfTruth}`);
        console.log('');

        try {
            // Validate paths
            this.validatePaths();
            
            // Process main documentation
            await this.processMainDocs();
            
            // Process beta documentation
            await this.processBetaDocs();
            
            // Generate wiki navigation
            await this.generateNavigation();
            
            // Update wiki metadata
            await this.updateWikiMetadata();
            
            // Create source attribution
            await this.createSourceAttribution();
            
            console.log('✅ Wiki update completed successfully!');
            console.log('🎯 Remember: yourl.cloud is always the source of truth for latest information.');
            
        } catch (error) {
            console.error('❌ Wiki update failed:', error.message);
            process.exit(1);
        }
    }

    /**
     * Validate repository paths
     */
    validatePaths() {
        if (!fs.existsSync(this.mainRepoPath)) {
            throw new Error(`Main repository path not found: ${this.mainRepoPath}`);
        }
        
        if (!fs.existsSync(this.wikiRepoPath)) {
            console.log('⚠️  Wiki repository not found, creating...');
            this.createWikiRepo();
        }
    }

    /**
     * Create wiki repository if it doesn't exist
     */
    createWikiRepo() {
        try {
            fs.mkdirSync(this.wikiRepoPath, { recursive: true });
            console.log('📁 Created wiki repository directory');
        } catch (error) {
            throw new Error(`Failed to create wiki repository: ${error.message}`);
        }
    }

    /**
     * Process main documentation files
     */
    async processMainDocs() {
        console.log('📚 Processing main documentation from yourl.cloud...');
        
        // Copy and process README.md
        const readmePath = path.join(this.mainRepoPath, 'README.md');
        if (fs.existsSync(readmePath)) {
            const content = fs.readFileSync(readmePath, 'utf8');
            const processedContent = this.processContent(content, 'Home', 'README.md');
            fs.writeFileSync(path.join(this.wikiRepoPath, 'Home.md'), processedContent);
            console.log('✅ Updated Home.md from yourl.cloud README.md');
        }

        // Copy and process Status file
        const statusPath = path.join(this.mainRepoPath, 'Status');
        if (fs.existsSync(statusPath)) {
            const content = fs.readFileSync(statusPath, 'utf8');
            const processedContent = this.processContent(content, 'Status', 'Status');
            fs.writeFileSync(path.join(this.wikiRepoPath, 'Status.md'), processedContent);
            console.log('✅ Updated Status.md from yourl.cloud');
        }
    }

    /**
     * Process beta documentation
     */
    async processBetaDocs() {
        console.log('🧪 Processing beta documentation from yourl.cloud...');
        
        const betaPath = path.join(this.mainRepoPath, 'BETA_JOURNALING.md');
        if (fs.existsSync(betaPath)) {
            const content = fs.readFileSync(betaPath, 'utf8');
            const processedContent = this.processContent(content, 'Beta-Journaling', 'BETA_JOURNALING.md');
            fs.writeFileSync(path.join(this.wikiRepoPath, 'Beta-Journaling.md'), processedContent);
            console.log('✅ Updated Beta-Journaling.md from yourl.cloud');
        }
    }

    /**
     * Process content for wiki compatibility
     */
    processContent(content, pageName, sourceFile) {
        // Add wiki metadata with source attribution
        const metadata = `---
title: ${pageName}
organization: ${this.organization}
session_id: ${this.sessionId}
last_updated: ${new Date().toISOString()}
source_of_truth: ${this.sourceOfTruth}
source_file: ${sourceFile}
---

> **Source of Truth**: [yourl.cloud](https://yourl.cloud) - Always the latest information
> **Source File**: \`${sourceFile}\` from yourl.cloud repository
> **Last Synced**: ${new Date().toISOString()}

`;
        
        // Convert GitHub-specific links to wiki links
        let processedContent = content
            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, text, url) => {
                // Convert internal links to wiki format
                if (url.startsWith('./') || url.startsWith('../')) {
                    const fileName = path.basename(url, path.extname(url));
                    return `[[${text}|${fileName}]]`;
                }
                return match;
            })
            .replace(/^#\s+(.+)$/gm, (match, title) => {
                // Ensure proper heading hierarchy
                return `# ${title}`;
            });

        return metadata + processedContent;
    }

    /**
     * Generate wiki navigation
     */
    async generateNavigation() {
        console.log('🧭 Generating wiki navigation...');
        
        const sidebarContent = `# Yourl-Cloud Inc. Wiki

> **Source of Truth**: [yourl.cloud](https://yourl.cloud) - Always the latest information

## 📚 Documentation
- [[Home|Home]] - Latest from yourl.cloud README.md
- [[Beta Journaling|Beta-Journaling]] - Latest from yourl.cloud
- [[Project Status|Status]] - Latest from yourl.cloud

## 🔧 Technical
- [[API Reference|API-Reference]]
- [[Deployment Guide|Deployment-Guide]]
- [[Security Standards|Security-Standards]]

## 🤝 Contributing
- [[Contributing Guidelines|Contributing]]
- [[Code of Conduct|Code-of-Conduct]]

## 📊 Status
- [[Project Status|Status]] - Real-time from yourl.cloud
- [[Changelog|Changelog]]

## ℹ️ Information
- [[Source Information|_Source-Info]] - About this wiki
- [[Wiki Metadata|_Wiki-Metadata]] - Technical details

---
*Last synced: ${new Date().toISOString()}*
*Source: yourl.cloud - Always the latest information*
*Session ID: ${this.sessionId}*
*Organization: ${this.organization}*
`;

        fs.writeFileSync(path.join(this.wikiRepoPath, '_Sidebar.md'), sidebarContent);
        console.log('✅ Updated _Sidebar.md with source attribution');
    }

    /**
     * Update wiki metadata
     */
    async updateWikiMetadata() {
        console.log('📊 Updating wiki metadata...');
        
        const metadataContent = `# Wiki Metadata

## Repository Information
- **Organization**: ${this.organization}
- **Session ID**: ${this.sessionId}
- **Last Updated**: ${new Date().toISOString()}
- **Wiki Version**: 1.0.0
- **Source of Truth**: ${this.sourceOfTruth}

## Update Process
This wiki is automatically updated from the main repository using:
- GitHub Actions workflow: \`.github/workflows/update-wiki.yml\`
- Node.js script: \`scripts/update-wiki.js\`
- Manual trigger: \`workflow_dispatch\`

## Content Sources
- \`README.md\` → \`Home.md\` (Main source of truth)
- \`BETA_JOURNALING.md\` → \`Beta-Journaling.md\`
- \`Status\` → \`Status.md\`
- \`docs/\` → Wiki pages

## Navigation
- \`_Sidebar.md\` - Main navigation
- \`_Footer.md\` - Footer content (if exists)
- \`_Source-Info.md\` - Source attribution

## 🎯 Important Note
**yourl.cloud is ALWAYS the source of truth for the latest information.**
This wiki is automatically synchronized to ensure you have access to the most current documentation.
`;

        fs.writeFileSync(path.join(this.wikiRepoPath, '_Wiki-Metadata.md'), metadataContent);
        console.log('✅ Updated _Wiki-Metadata.md');
    }

    /**
     * Create source attribution file
     */
    async createSourceAttribution() {
        console.log('📝 Creating source attribution...');
        
        const sourceInfoContent = `# Source Information

## 🎯 Source of Truth

**yourl.cloud is ALWAYS the source of truth for the latest information.**

This wiki is automatically synchronized with the main yourl.cloud repository to ensure you always have access to the most current documentation and information.

## 🔄 Sync Process

- **Automatic**: Wiki updates automatically when main repository changes
- **Manual**: Can be triggered manually via GitHub Actions
- **Real-time**: Always reflects the latest state of yourl.cloud

## 📁 Content Sources

| Wiki Page | Source File | Description |
|-----------|-------------|-------------|
| Home.md | README.md | Main project documentation |
| Beta-Journaling.md | BETA_JOURNALING.md | Beta journaling tool docs |
| Status.md | Status | Current project status |
| _Sidebar.md | Generated | Navigation and structure |

## 🚀 Latest Information

For the absolute latest information, always check:
- **Primary**: https://yourl.cloud
- **Repository**: https://github.com/XDM-ZSBW/yourl.cloud
- **Wiki**: https://github.com/XDM-ZSBW/yourl.cloud/wiki (synced from yourl.cloud)

## 🔍 Verification

To verify you have the latest information:
1. Check the "Last Synced" timestamp on this page
2. Compare with the latest commit on yourl.cloud
3. Always refer to https://yourl.cloud for the most current information

---
*This wiki is automatically maintained and synchronized with yourl.cloud*
*Session ID: ${this.sessionId}*
*Organization: ${this.organization}*
`;

        fs.writeFileSync(path.join(this.wikiRepoPath, '_Source-Info.md'), sourceInfoContent);
        console.log('✅ Created _Source-Info.md');
    }
}

// Run the updater
if (require.main === module) {
    const updater = new WikiUpdater();
    updater.updateWiki().catch(console.error);
}

module.exports = WikiUpdater;
