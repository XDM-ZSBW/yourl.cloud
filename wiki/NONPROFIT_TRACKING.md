# Yourl.Cloud Nonprofit Tracking System

## Overview
Yourl.Cloud is operated by Yourl Cloud Inc., a registered nonprofit organization dedicated to making prompt engineering and AI services accessible to anyone who can send ASCII messages, regardless of their device capabilities.

## Marketing Code System

### Purpose
The marketing code system serves multiple critical functions for our nonprofit mission:
1. **Transparency**: Every code change, build, and deployment is traceable
2. **Donor Attribution**: Features funded by donors can be tracked and reported
3. **Usage Insights**: Helps measure the impact of our services
4. **Audit Trail**: Supports nonprofit compliance and reporting requirements

### Code Types

1. **Deployment Codes** (`DEPLOY-YYYYMMDD-XXXX`)
   - Generated for each production deployment
   - Tracks which features are being deployed
   - Links to donor-funded improvements
   - Example: `DEPLOY-20250807-A1B2`

2. **Feature Codes** (`FEAT-YYYYMMDD-XXXX`)
   - Created for new feature development
   - Includes donor and partner attribution
   - Tracks feature progress and adoption
   - Example: `FEAT-20250807-C3D4`

3. **Build Codes** (`BUILD-YYYYMMDD-XXXX`)
   - Generated for each build artifact
   - Links features to deployments
   - Supports CI/CD auditing
   - Example: `BUILD-20250807-E5F6`

### Public Access
Two marketing codes are always publicly available:
1. `current_public_code`: The code for the currently deployed production version
2. `next_public_code`: The code for the upcoming deployment

These codes are displayed on the landing page and can be used to track deployment status.

## Auditing and Reporting

### Quarterly Reports
Marketing codes support our quarterly nonprofit reporting:
1. Feature adoption metrics
2. Donor impact tracking
3. Usage statistics
4. Service accessibility metrics

### Public Auditing
Any stakeholder can audit our deployment and feature history:
```bash
python scripts/marketing_code.py --project PROJECT_ID --action audit
```

### Donor Recognition
Donor-funded features are tracked and recognized:
1. Attribution in code and documentation
2. Impact metrics in quarterly reports
3. Public acknowledgment (when permitted)

## Domain Transfer Process

### Current Status
The yourl.cloud domain is being transferred to Yourl Cloud Inc. nonprofit ownership.

### Transfer Steps
1. **Pre-Transfer**
   - Document all DNS records
   - Export SSL certificates
   - Backup service configurations
   - Create transfer timeline

2. **During Transfer**
   - Maintain service continuity
   - Update DNS records
   - Verify SSL certificate validity
   - Monitor service health

3. **Post-Transfer**
   - Verify DNS propagation
   - Confirm SSL functionality
   - Update documentation
   - Notify stakeholders

4. **Security Measures**
   - Maintain SSL security
   - Preserve DNSSEC settings
   - Update security policies
   - Document changes

## Best Practices

### Code Management
1. All code changes must be linked to a marketing code
2. Document donor attribution in commit messages
3. Keep sensitive information private
4. Maintain clear audit trails

### Deployment
1. Generate new marketing codes for each deployment
2. Include feature and donor information
3. Update public codes automatically
4. Notify stakeholders of changes

### Documentation
1. Keep README.md current
2. Update wiki with feature details
3. Maintain clear deployment logs
4. Document all marketing codes

### Security
1. Never expose private marketing codes
2. Protect donor information
3. Secure deployment processes
4. Regular security audits

## Contact

For questions about our nonprofit operations or marketing code system:
- Email: bcherrman@gmail.com
- GitHub: https://github.com/XDM-ZSBW/yourl.cloud
- Documentation: https://github.com/XDM-ZSBW/yourl.cloud/wiki
