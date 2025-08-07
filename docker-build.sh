#!/bin/bash

# yourl.cloud - Docker Build Script
# =================================
# 
# Easy Docker build and run script
# Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="yourl-cloud"
CONTAINER_NAME="yourl-cloud"
PORT="8080"

echo -e "${BLUE}🚀 yourl.cloud Docker Build Script${NC}"
echo -e "${BLUE}=====================================${NC}"
echo -e "Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49"
echo ""

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker is running${NC}"
}

# Function to build the image
build_image() {
    echo -e "${YELLOW}🔨 Building Docker image...${NC}"
    docker build -t $IMAGE_NAME .
    echo -e "${GREEN}✅ Image built successfully${NC}"
}

# Function to stop and remove existing container
cleanup_container() {
    if docker ps -a --format "table {{.Names}}" | grep -q $CONTAINER_NAME; then
        echo -e "${YELLOW}🔄 Stopping existing container...${NC}"
        docker stop $CONTAINER_NAME > /dev/null 2>&1 || true
        docker rm $CONTAINER_NAME > /dev/null 2>&1 || true
        echo -e "${GREEN}✅ Container cleaned up${NC}"
    fi
}

# Function to run the container
run_container() {
    echo -e "${YELLOW}🚀 Starting container...${NC}"
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:80 \
        --restart unless-stopped \
        $IMAGE_NAME
    
    echo -e "${GREEN}✅ Container started successfully${NC}"
    echo -e "${BLUE}🌐 Access your application at: http://localhost:$PORT${NC}"
    echo -e "${BLUE}🏥 Health check: http://localhost:$PORT/health${NC}"
    echo -e "${BLUE}📊 Status: http://localhost:$PORT/status${NC}"
}

# Function to show logs
show_logs() {
    echo -e "${YELLOW}📋 Container logs:${NC}"
    docker logs $CONTAINER_NAME
}

# Function to show container status
show_status() {
    echo -e "${YELLOW}📊 Container status:${NC}"
    docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

# Main script
main() {
    case "${1:-build}" in
        "build")
            check_docker
            build_image
            ;;
        "run")
            check_docker
            cleanup_container
            run_container
            ;;
        "start")
            check_docker
            if docker ps --format "table {{.Names}}" | grep -q $CONTAINER_NAME; then
                echo -e "${GREEN}✅ Container is already running${NC}"
                show_status
            else
                run_container
            fi
            ;;
        "stop")
            if docker ps --format "table {{.Names}}" | grep -q $CONTAINER_NAME; then
                echo -e "${YELLOW}🛑 Stopping container...${NC}"
                docker stop $CONTAINER_NAME
                echo -e "${GREEN}✅ Container stopped${NC}"
            else
                echo -e "${YELLOW}⚠️  Container is not running${NC}"
            fi
            ;;
        "logs")
            if docker ps --format "table {{.Names}}" | grep -q $CONTAINER_NAME; then
                show_logs
            else
                echo -e "${RED}❌ Container is not running${NC}"
            fi
            ;;
        "status")
            show_status
            ;;
        "clean")
            echo -e "${YELLOW}🧹 Cleaning up...${NC}"
            cleanup_container
            docker rmi $IMAGE_NAME > /dev/null 2>&1 || true
            echo -e "${GREEN}✅ Cleanup completed${NC}"
            ;;
        "help")
            echo -e "${BLUE}Usage: $0 [command]${NC}"
            echo ""
            echo "Commands:"
            echo "  build   - Build the Docker image"
            echo "  run     - Build and run the container"
            echo "  start   - Start the container (if not running)"
            echo "  stop    - Stop the container"
            echo "  logs    - Show container logs"
            echo "  status  - Show container status"
            echo "  clean   - Clean up container and image"
            echo "  help    - Show this help message"
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $1${NC}"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
