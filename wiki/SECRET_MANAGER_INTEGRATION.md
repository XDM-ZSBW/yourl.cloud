# Google Secret Manager & Cloud SQL Integration

## Overview

Yourl.Cloud now uses Google Secret Manager as the system of record for marketing codes and Google Cloud SQL for persistent, encrypted audit logs and authorization records.

## Architecture

### Component Storage

| Component | Storage | Purpose | Rotation/Audit |
|-----------|---------|---------|----------------|
| Current/Next Code | Google Secret Manager | Fast access by app, secure, rotates | On deploy/build, version |
| Code History/Usage | Google Cloud SQL (encrypted) | Auditable, queryable, partner records | Ongoing, SQL logging |
| Authorizations/Onboard | Google Cloud SQL | E2E new user/service onboarding | API/manual, logged |

### Security Features

- **Principle of Least Privilege**: All cloud resources restricted to required accounts/roles only
- **Encrypted at Rest**: All data encrypted in Secret Manager and Cloud SQL
- **Audit Trails**: Complete logging of all code access and usage
- **Parameterized Queries**: All database operations use parameterized queries
- **No Secrets in Logs**: Secrets never exposed in application logs or browser storage

## Setup Instructions

### 1. ✅ Required APIs (Already Enabled)

The following APIs are already enabled in your project:

```bash
# ✅ Secret Manager API - ENABLED
gcloud services list --enabled --filter="name:secretmanager.googleapis.com"

# ✅ Cloud SQL Admin API - ENABLED  
gcloud services list --enabled --filter="name:sqladmin.googleapis.com"

# ✅ Cloud Build API - ENABLED
gcloud services list --enabled --filter="name:cloudbuild.googleapis.com"
```

**Status**: All required APIs are already enabled and ready for use.

### 2. Create Cloud SQL Instance

```bash
# Create PostgreSQL instance
gcloud sql instances create yourl-cloud-sql \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-west1 \
  --storage-type=SSD \
  --storage-size=10GB \
  --backup-start-time=02:00 \
  --maintenance-window-day=SUN \
  --maintenance-window-hour=03

# Create database
gcloud sql databases create yourl_cloud_db \
  --instance=yourl-cloud-sql

# Create user
gcloud sql users create yourl-cloud-user \
  --instance=yourl-cloud-sql \
  --password=YOUR_SECURE_PASSWORD
```

### 3. Configure Service Account Permissions

```bash
# Create service account for automation
gcloud iam service-accounts create automation-sa-yourl \
  --display-name="Yourl Cloud Automation Service Account"

# Grant Secret Manager access
gcloud projects add-iam-policy-binding root-wharf-383822 \
  --member="serviceAccount:automation-sa-yourl@root-wharf-383822.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Grant Cloud SQL access
gcloud projects add-iam-policy-binding root-wharf-383822 \
  --member="serviceAccount:automation-sa-yourl@root-wharf-383822.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

### 4. Initialize Secrets

```bash
# Initialize Secret Manager secrets
python scripts/deploy_with_code_rotation.py --project root-wharf-383822 --action init
```

## Usage

### Code Management

#### Get Current Code
```bash
python scripts/secret_manager_client.py --project root-wharf-383822 --action get-current
```

#### Get Next Code
```bash
python scripts/secret_manager_client.py --project root-wharf-383822 --action get-next
```

#### Rotate Codes
```bash
python scripts/deploy_with_code_rotation.py --project root-wharf-383822 --action rotate
```

#### Deploy with Code Rotation
```bash
python scripts/deploy_with_code_rotation.py --project root-wharf-383822 --action deploy
```

### Database Operations

#### Log Code History
```bash
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action log-history --code "CLOUD123!" --code-type "current"
```

#### Get Usage Statistics
```bash
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action get-stats --days 30
```

#### Create Authorization Record
```bash
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action create-auth --service-name "backend-api" --owner "cursor" --code "API123!" --access-level "read"
```

### Authorized API Access

#### Get Current Code (API)
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "X-Service-Name: your-service" \
     https://yourl.cloud/api/v1/current-code
```

#### Get Next Code (API)
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "X-Service-Name: your-service" \
     https://yourl.cloud/api/v1/next-code
```

#### Get Metadata (API)
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "X-Service-Name: your-service" \
     https://yourl.cloud/api/v1/metadata
```

## CI/CD Integration

### Cloud Build Configuration

The `cloudbuild.yaml` includes steps for:
- Building and deploying to Cloud Run
- Rotating marketing codes
- Logging to database
- Updating audit trails

### Environment Variables

Set these environment variables in your Cloud Run service:

```bash
GOOGLE_CLOUD_PROJECT=root-wharf-383822
DATABASE_CONNECTION_STRING=postgresql://user:pass@host:5432/db
```

## Security Best Practices

### Secret Manager
- All secrets are encrypted at rest
- Version history maintained for audit
- Access controlled via IAM
- No secrets in code or logs

### Cloud SQL
- All connections encrypted (SSL/TLS)
- Parameterized queries prevent injection
- Access logs maintained
- Automated backups enabled

### API Security
- API keys required for all access
- Service names must match authorization records
- Usage logged for audit
- Rate limiting recommended

## Monitoring and Audit

### Secret Manager Audit
```bash
# List secret versions
python scripts/secret_manager_client.py --project root-wharf-383822 --action list-versions --secret-name "projects/root-wharf-383822/secrets/yourl_marketing_code_current"
```

### Database Audit
```bash
# Get code history
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action get-history

# Get usage statistics
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action get-stats --days 30

# Get active authorizations
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action get-auths
```

## Emergency Procedures

### Code Rotation
```bash
# Emergency code rotation
python scripts/secret_manager_client.py --project root-wharf-383822 --action rotate --new-current "EMERGENCY123!" --new-next "NEXT456!"
```

### Revoke Authorization
```bash
# Revoke service access
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action revoke-auth --service-name "compromised-service"
```

### Database Recovery
```bash
# Restore from backup
gcloud sql instances restore yourl-cloud-sql \
  --restore-instance=yourl-cloud-sql-backup \
  --restore-time=2024-01-01T12:00:00Z
```

## Partner Onboarding

### 1. Create Partner Record
```bash
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action create-auth \
  --service-name "partner-service" \
  --owner "partner-company" \
  --code "PARTNER123!" \
  --access-level "read"
```

### 2. Provide API Documentation
- API endpoints: `/api/v1/current-code`, `/api/v1/next-code`, `/api/v1/metadata`
- Required headers: `X-API-Key`, `X-Service-Name`
- Rate limits: 100 requests/minute
- Authentication: API key validation

### 3. Monitor Usage
```bash
# Check partner usage
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action get-stats --days 7
```

## Troubleshooting

### Common Issues

1. **Secret Manager Access Denied**
   - Verify service account has `roles/secretmanager.secretAccessor`
   - Check project ID is correct

2. **Database Connection Failed**
   - Verify connection string format
   - Check Cloud SQL instance is running
   - Ensure IP is whitelisted

3. **Code Rotation Failed**
   - Check Secret Manager API is enabled
   - Verify service account permissions
   - Check for existing secrets

### Debug Commands

```bash
# Check deployment status
python scripts/deploy_with_code_rotation.py --project root-wharf-383822 --action status

# Test Secret Manager access
python scripts/secret_manager_client.py --project root-wharf-383822 --action metadata

# Test database connection
python scripts/database_client.py --connection-string "postgresql://user:pass@host:5432/db" --action get-auths
```

## Compliance and Reporting

### Audit Reports
- All code access logged with timestamps
- Usage statistics available by time period
- Authorization records with expiry tracking
- Partner onboarding audit trail

### Data Retention
- Secret Manager: Version history maintained
- Cloud SQL: Logs retained for 1 year
- Backup retention: 7 days automated

### Security Scanning
- Regular vulnerability scans
- Dependency updates
- Secret rotation monitoring
- Access pattern analysis
