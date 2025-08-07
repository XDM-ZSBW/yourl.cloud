#!/bin/bash

# Deployment script for Yourl.Cloud
# Author: Yourl Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

echo "🚀 Deploying Yourl.Cloud to Google Cloud Run..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install Google Cloud SDK first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run 'gcloud auth login' first."
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project ID set. Please run 'gcloud config set project YOUR_PROJECT_ID' first."
    exit 1
fi

echo "📋 Project ID: $PROJECT_ID"

# Build and deploy using Cloud Build
echo "🔨 Building and deploying with Cloud Build..."
gcloud builds submit --config cloudbuild.yaml

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Your application should be available at:"
    echo "   https://yourl-cloud-$(echo $PROJECT_ID | cut -d'-' -f1)-uc.a.run.app"
    echo ""
    echo "🔐 Demo password: yourl2024"
    echo "📊 Health check: https://yourl-cloud-$(echo $PROJECT_ID | cut -d'-' -f1)-uc.a.run.app/health"
else
    echo "❌ Deployment failed. Please check the logs above."
    exit 1
fi
