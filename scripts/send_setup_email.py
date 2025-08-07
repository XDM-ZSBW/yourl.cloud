import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_setup_instructions():
    # Load SendGrid API key from environment variable
    api_key = os.environ.get('SENDGRID_API_KEY')
    
    # Email content with markdown formatting
    email_content = """
# Cloud Build Automation Setup Instructions for yourl.cloud

## Overview
This guide will help you set up automated build notifications and GitHub status updates for your yourl.cloud project.

## Prerequisites
1. Google Cloud Platform account with billing enabled
2. SendGrid account for email notifications
3. GitHub repository admin access

## Step-by-Step Setup Instructions

### 1. SendGrid Setup (for Email Notifications)
1. Create a SendGrid account at https://signup.sendgrid.com/
2. Create an API key:
   - Go to Settings > API Keys
   - Click "Create API Key"
   - Name: "Cloud Build Notifications"
   - Permissions: "Mail Send" (Full Access)
   - Copy the generated API key

3. Store the API key in Google Cloud Secret Manager:
```bash
gcloud secrets create sendgrid-api-key --data-file=/path/to/api/key
```

### 2. Deploy the Notification Cloud Function
1. Go to Google Cloud Console > Cloud Functions
2. Click "Create Function"
3. Basic settings:
   - Name: sendBuildNotification
   - Region: us-central1 (same as your Cloud Run)
   - Trigger: HTTP
   - Runtime: Python 3.9+

4. Copy the code from scripts/cloud-function/main.py
5. Add requirements from scripts/cloud-function/requirements.txt
6. Set environment variable:
   - Name: SENDGRID_API_KEY
   - Value: Select from Secret Manager > sendgrid-api-key

### 3. GitHub Authentication Setup
1. Create a GitHub Personal Access Token:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Click "Generate new token"
   - Name: "Cloud Build Status Updates"
   - Permissions: repo:status
   - Copy the generated token

2. Store the token in Secret Manager:
```bash
gcloud secrets create github-token --data-file=/path/to/token
```

### 4. Configure Cloud Build Service Account
1. Go to IAM & Admin > Service Accounts
2. Find the Cloud Build service account (ends with @cloudbuild.gserviceaccount.com)
3. Add these roles:
   - Cloud Functions Invoker
   - Secret Manager Secret Accessor

### 5. Create Cloud Build Trigger
1. Go to Cloud Build > Triggers
2. Click "Create Trigger"
3. Configure:
   - Name: yourl-cloud-auto-build
   - Event: Push to a branch
   - Source: Your GitHub repository
   - Branch: ^main$ (regex)
   - Configuration: Cloud Build configuration file
   - Location: /cloudbuild.yaml

## Verification
1. Make a small change to your repository
2. Push to main branch
3. You should receive an email notification
4. Check GitHub commit status for the build status

## Troubleshooting
If you don't receive notifications:
1. Check Cloud Build logs
2. Verify Cloud Function logs
3. Ensure all IAM permissions are correct
4. Verify secrets are accessible

Need help? Contact me at bcherrman@gmail.com

"""
    
    try:
        sg = SendGridAPIClient(api_key)
        message = Mail(
            from_email='cloud-build@yourl.cloud',
            to_emails='bcherrman@gmail.com',
            subject='yourl.cloud - Cloud Build Automation Setup Instructions',
            html_content=email_content
        )
        response = sg.send(message)
        print(f"Email sent successfully! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    send_setup_instructions()
