#!/bin/bash

# Deploy blog container to VPS
# Usage: ./scripts/deploy-blog.sh [SSH_USER@]SSH_HOST

set -e

# Parse arguments
if [ $# -eq 1 ]; then
    if [[ "$1" == *"@"* ]]; then
        SSH_USER="${1%%@*}"
        SERVER_HOST="${1##*@}"
    else
        SERVER_HOST="$1"
        SSH_USER="${SSH_USER:-root}"
    fi
elif [ $# -eq 0 ]; then
    SERVER_HOST="${SSH_HOST:-}"
    SSH_USER="${SSH_USER:-root}"
else
    echo "Usage: $0 [SSH_USER@]SSH_HOST"
    exit 1
fi

if [ -z "$SERVER_HOST" ]; then
    echo "Error: SSH_HOST is required"
    exit 1
fi

SSH_TARGET="${SSH_USER}@${SERVER_HOST}"
REMOTE_DIR="/opt/personal-site"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo -e "${RED}Error: .env file not found${NC}"
    exit 1
fi

# Validate required variables
if [ -z "$DOCKER_REGISTRY" ] || [ -z "$DOCKER_USERNAME" ]; then
    echo -e "${RED}Error: DOCKER_REGISTRY and DOCKER_USERNAME must be set in .env${NC}"
    exit 1
fi

# Check for GitHub PAT if using GitHub Container Registry
if [ "$DOCKER_REGISTRY" = "ghcr.io" ]; then
    if [ -z "$CR_PAT" ]; then
        if [ -f ~/Documents/secrets/github-pat.txt ]; then
            export CR_PAT=$(cat ~/Documents/secrets/github-pat.txt)
            echo -e "${GREEN}✓ Loaded GitHub PAT from ~/Documents/secrets/github-pat.txt${NC}"
        else
            echo -e "${RED}Error: CR_PAT not set and ~/Documents/secrets/github-pat.txt not found${NC}"
            exit 1
        fi
    fi
fi

BLOG_IMAGE="${DOCKER_REGISTRY}/${DOCKER_USERNAME}/${IMAGE_BLOG}:${IMAGE_TAG}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Deploying Blog from Registry${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Server:   ${SERVER_HOST}${NC}"
echo -e "${BLUE}  Image:    ${BLOG_IMAGE}${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Step 1: Test SSH connection
echo -e "${YELLOW}[1/4] Testing SSH connection...${NC}"
if ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$SSH_TARGET" "echo 'SSH connection successful'" 2>/dev/null; then
    echo -e "${GREEN}✓ SSH connection successful${NC}\n"
else
    echo -e "${RED}✗ SSH connection failed${NC}"
    exit 1
fi

# Step 2: Login to registry on VPS
echo -e "${YELLOW}[2/4] Logging into registry on VPS...${NC}"
if [ "$DOCKER_REGISTRY" = "ghcr.io" ] && [ -n "$CR_PAT" ]; then
    ssh "$SSH_TARGET" bash << ENDSSH
        echo '$CR_PAT' | docker login ghcr.io -u $DOCKER_USERNAME --password-stdin > /dev/null 2>&1
ENDSSH
    echo -e "${GREEN}✓ Logged into GHCR on VPS${NC}\n"
fi

# Step 3: Pull and start blog container
echo -e "${YELLOW}[3/4] Pulling and starting blog container...${NC}"
ssh "$SSH_TARGET" bash << ENDSSH
    cd $REMOTE_DIR
    
    # Export environment variables
    export \$(cat .env | grep -v '^#' | xargs)
    
    # Pull latest blog image
    echo "Pulling blog image..."
    docker pull $BLOG_IMAGE
    
    # Stop and remove existing blog container
    echo "Stopping existing blog container..."
    docker stop blog 2>/dev/null || true
    docker rm blog 2>/dev/null || true
    
    # Start new blog container
    echo "Starting blog container..."
    docker run -d \
        --name blog \
        --network personal-site_web \
        --restart unless-stopped \
        $BLOG_IMAGE
    
    # Wait for container to start
    sleep 3
    
    # Show status
    echo ""
    echo "Blog container status:"
    docker ps --filter name=blog
ENDSSH
echo -e "${GREEN}✓ Blog container started${NC}\n"

# Step 4: Verify deployment
echo -e "${YELLOW}[4/4] Verifying deployment...${NC}"
ssh "$SSH_TARGET" bash << 'ENDSSH'
    if docker ps --filter name=blog | grep -q "Up"; then
        echo "✓ Blog container is running"
        
        # Test blog endpoint
        if curl -s -H "Host: shivamm.info" -o /dev/null -w "%{http_code}" http://localhost/blog/ 2>/dev/null | grep -q "200\|301\|302"; then
            echo "✓ Blog is responding"
        else
            echo "! Blog endpoint test inconclusive (may need nginx reload)"
        fi
    else
        echo "✗ Blog container may not be running"
        exit 1
    fi
ENDSSH
echo -e "${GREEN}✓ Deployment verified${NC}\n"

# Final status
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Blog deployment completed!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${BLUE}Access URL:${NC}"
echo -e "  • Blog: ${GREEN}https://shivamm.info/blog${NC}"
echo -e ""
echo -e "${YELLOW}Note: Make sure nginx-proxy is updated to route /blog traffic${NC}"
echo -e ""
