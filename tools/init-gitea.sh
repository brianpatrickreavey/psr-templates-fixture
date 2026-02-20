#!/bin/bash
# Initialize gitea repository with psr-templates-fixture files for ACT local testing
# This script runs only in ACT mode and sets up a test repo for the workflow phases

set -e

# Configuration
GITEA_HOST="${GITEA_HOST:-localhost}"
GITEA_PORT="${GITEA_PORT:-3000}"
GITEA_URL="http://${GITEA_HOST}:${GITEA_PORT}"
REPO_NAME="test-repo"
REPO_PATH="/tmp/gitea-repos/${REPO_NAME}.git"
TEST_MOUNT="/tmp/test-repo-work"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[Gitea Init] Starting gitea repository initialization${NC}"

# Function to wait for gitea to be healthy
wait_for_gitea() {
    local timeout=30
    local elapsed=0
    
    echo -e "${YELLOW}[Gitea Init] Waiting for gitea to be ready...${NC}"
    
    while [ $elapsed -lt $timeout ]; do
        if curl -s "${GITEA_URL}" > /dev/null 2>&1; then
            echo -e "${GREEN}[Gitea Init] Gitea is healthy${NC}"
            return 0
        fi
        sleep 1
        elapsed=$((elapsed + 1))
    done
    
    echo -e "${RED}[Gitea Init] Timeout waiting for gitea after ${timeout}s${NC}"
    return 1
}

# Function to create bare repository
create_bare_repo() {
    echo -e "${YELLOW}[Gitea Init] Creating bare repository at ${REPO_PATH}${NC}"
    
    # Ensure directory exists
    mkdir -p "$(dirname "${REPO_PATH}")"
    
    # Initialize bare repo if it doesn't exist
    if [ ! -d "${REPO_PATH}" ]; then
        git init --bare "${REPO_PATH}"
        echo -e "${GREEN}[Gitea Init] Bare repository created${NC}"
    else
        echo -e "${YELLOW}[Gitea Init] Bare repository already exists, skipping creation${NC}"
    fi
}

# Function to populate repo with initial content
populate_repo() {
    echo -e "${YELLOW}[Gitea Init] Populating repository with psr-templates-fixture files${NC}"
    
    # Clean up any previous work directory
    rm -rf "${TEST_MOUNT}"
    mkdir -p "${TEST_MOUNT}"
    
    # Clone the bare repo to a working directory
    git clone "${REPO_PATH}" "${TEST_MOUNT}"
    
    # Copy psr-templates-fixture files (exclude .git and node_modules)
    echo -e "${YELLOW}[Gitea Init] Copying psr-templates-fixture files...${NC}"
    
    # Get the fixture repo root (one level up from where this script is)
    FIXTURE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    
    # Copy files, excluding git and common unneeded directories
    rsync -av \
        --exclude='.git' \
        --exclude='.github' \
        --exclude='.gitignore' \
        --exclude='__pycache__' \
        --exclude='.pytest_cache' \
        --exclude='.actrc' \
        --exclude='ACT-GITEA-PLAN.md' \
        --exclude='node_modules' \
        --exclude='.venv' \
        --exclude='venv' \
        "${FIXTURE_ROOT}/" "${TEST_MOUNT}/" || true
    
    # Configure git in the work directory
    cd "${TEST_MOUNT}"
    git config user.name "GitHub Actions"
    git config user.email "actions@github.com"
    
    # Create initial commit if there are changes
    if [ -n "$(git status --porcelain)" ]; then
        git add -A
        git commit -m "Initial commit for ACT testing"
        echo -e "${GREEN}[Gitea Init] Initial commit created${NC}"
    else
        echo -e "${YELLOW}[Gitea Init] No changes to commit${NC}"
    fi
    
    # Push to bare repo
    git push origin main || git push origin master || true
    
    cd - > /dev/null
    
    echo -e "${GREEN}[Gitea Init] Repository populated${NC}"
}

# Function to clean up (optional, called with --cleanup flag)
cleanup_repo() {
    echo -e "${YELLOW}[Gitea Init] Cleaning up test repository${NC}"
    
    # Remove work directory
    rm -rf "${TEST_MOUNT}"
    
    # Remove bare repository
    rm -rf "${REPO_PATH}"
    
    echo -e "${GREEN}[Gitea Init] Cleanup complete${NC}"
}

# Main execution
main() {
    if [ "$1" == "--cleanup" ]; then
        cleanup_repo
        return 0
    fi
    
    # Check if we're in ACT mode
    if [ -z "${ACT}" ]; then
        echo -e "${YELLOW}[Gitea Init] Not running in ACT mode (ACT env var not set). Skipping gitea init.${NC}"
        return 0
    fi
    
    # Wait for gitea
    if ! wait_for_gitea; then
        echo -e "${RED}[Gitea Init] Failed to connect to gitea${NC}"
        return 1
    fi
    
    # Create and populate repo
    create_bare_repo
    populate_repo
    
    echo -e "${GREEN}[Gitea Init] Gitea initialization complete!${NC}"
    echo -e "${GREEN}[Gitea Init] Repository available at: ${GITEA_URL}/api/v1/repos/test-repo${NC}"
    echo -e "${GREEN}[Gitea Init] Git URL: http://${GITEA_HOST}:${GITEA_PORT}/test-repo.git${NC}"
}

main "$@"
