#!/bin/bash

# Validate blog deployment
# Usage: ./scripts/validate-blog.sh

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
DOMAIN="shivamm.info"
VPS_IP="134.199.180.26"
SSH_TARGET="root@${VPS_IP}"
TIMEOUT=10

FAILED=0
PASSED=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Blog Deployment Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to run a check
check() {
    local name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "Checking ${name}... "
    
    result=$(eval "$command" 2>/dev/null || echo "FAILED")
    
    if [[ "$result" == *"$expected"* ]]; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        echo -e "  ${YELLOW}Expected: ${expected}${NC}"
        echo -e "  ${YELLOW}Got: ${result}${NC}"
        ((FAILED++))
        return 1
    fi
}

echo -e "${BLUE}--- Container Status ---${NC}"

# Check blog container is running
check "blog container running" \
    "ssh -o ConnectTimeout=${TIMEOUT} ${SSH_TARGET} 'docker ps --filter name=blog --format \"{{.Status}}\"'" \
    "Up"

echo ""
echo -e "${BLUE}--- Blog Endpoint ---${NC}"

# Check blog returns 200
check "Blog HTTPS returns 200" \
    "curl -s -o /dev/null -w '%{http_code}' --max-time ${TIMEOUT} -L https://${DOMAIN}/blog/" \
    "200"

echo ""
echo -e "${BLUE}--- Content Validation ---${NC}"

# Check blog contains expected content
check "Blog contains site title" \
    "curl -s --max-time ${TIMEOUT} -L https://${DOMAIN}/blog/ | grep -o 'Shivam'" \
    "Shivam"

# Check blog has Docusaurus structure
check "Blog has Docusaurus elements" \
    "curl -s --max-time ${TIMEOUT} -L https://${DOMAIN}/blog/ | grep -o 'docusaurus'" \
    "docusaurus"

echo ""
echo -e "${BLUE}========================================${NC}"

# Summary
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All ${PASSED} validations passed!${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "Blog is live at: ${GREEN}https://${DOMAIN}/blog${NC}"
    exit 0
else
    echo -e "${RED}✗ ${FAILED} validation(s) failed, ${PASSED} passed${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Please check the failed items above.${NC}"
    exit 1
fi
