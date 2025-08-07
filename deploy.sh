#!/bin/bash
# yourl.cloud - Google Cloud Deployment Script
# ===========================================
# 
# Yourl-Cloud Inc. - AI-Friendly Service Hub
# Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="yourl-cloud-inc"
REGION="us-central1"
SERVICE_NAME="yourl-cloud"
SESSION_ID="f1d78acb-de07-46e0-bfa7-f5b75e3c0c49"

echo -e "${BLUE}🚀 Yourl-Cloud Inc. - Google Cloud Deployment${NC}"
echo -e "${BLUE}=============================================${NC}"
echo -e "${YELLOW}Session ID: ${SESSION_ID}${NC}"
echo -e "${YELLOW}Project ID: ${PROJECT_ID}${NC}"
echo -e "${YELLOW}Region: ${REGION}${NC}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud SDK is not installed.${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${YELLOW}⚠️  Not authenticated with Google Cloud.${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
echo -e "${BLUE}📋 Setting project to ${PROJECT_ID}...${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${BLUE}🔧 Enabling required APIs...${NC}"
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy
echo -e "${BLUE}🏗️  Building and deploying to Google App Engine...${NC}"
gcloud app deploy app.yaml --quiet

# Get the deployed URL
echo -e "${BLUE}🌐 Getting deployment URL...${NC}"
DEPLOYED_URL=$(gcloud app browse --no-launch-browser)
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌍 Your application is available at: ${DEPLOYED_URL}${NC}"

# Show status
echo -e "${BLUE}📊 Checking application status...${NC}"
gcloud app describe

echo ""
echo -e "${GREEN}🎉 Yourl-Cloud Inc. is now live on Google Cloud!${NC}"
echo -e "${YELLOW}📝 Next steps:${NC}"
echo -e "  1. Set up custom domain (optional)"
echo -e "  2. Configure SSL certificates"
echo -e "  3. Set up monitoring and logging"
echo -e "  4. Configure CI/CD pipeline"
echo ""
echo -e "${BLUE}🔗 Useful commands:${NC}"
echo -e "  - View logs: gcloud app logs tail -s default"
echo -e "  - Check status: gcloud app describe"
echo -e "  - Open app: gcloud app browse"
echo ""
