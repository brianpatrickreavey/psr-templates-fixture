#!/bin/bash
# Initialize Gitea repository with psr-templates-fixture files for ACT local testing
# This script runs only in ACT mode and assumes Gitea is already running via Docker
# Started by: make start-gitea

set -e

GITEA_URL="http://localhost:3000"
REPO_NAME="test-repo"
# Use file:// protocol for local pushes (works from workflow container)
REPO_FULL_URL="file:///data/git/repositories/${REPO_NAME}.git"
WORK_DIR="/tmp/test-repo-work"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[Gitea Init] Starting repository initialization...${NC}"

# Wait for gitea to be healthy
wait_for_gitea() {
    local timeout=30
    local elapsed=0
    
    echo -e "${YELLOW}[Gitea Init] Waiting for Gitea at ${GITEA_URL}...${NC}"
    
    while [ $elapsed -lt $timeout ]; do
        if curl -s "${GITEA_URL}" > /dev/null 2>&1; then
            echo -e "${GREEN}[Gitea Init] Gitea is healthy${NC}"
            return 0
        fi
        sleep 1
        elapsed=$((elapsed + 1))
    done
    
    echo -e "${RED}[Gitea Init] ERROR: Timeout waiting for Gitea after ${timeout}s${NC}"
    return 1
}

# Initialize repository
init_repo() {
    echo -e "${YELLOW}[Gitea Init] Initializing repository...${NC}"
    
    # Clean work directory
    rm -rf "${WORK_DIR}"
    mkdir -p "${WORK_DIR}"
    cd "${WORK_DIR}"
    
    # Initialize git repo
    git init
    git config user.name "GitHub Actions"
    git config user.email "actions@github.com"
    git remote add origin "${REPO_FULL_URL}"
    
    # Copy fixture files
    echo -e "${YELLOW}[Gitea Init] Copying psr-templates-fixture files...${NC}"
    # Look for fixture files in parent directory (since we're in /tmp/test-repo-work after git init)
    # The workflow calls this from the fixture root, so check common paths
    FIXTURE_ROOT=""
    for path in .. /home/bpreavey/Code/psr-templates-fixture $(pwd); do
        if [ -f "${path}/Makefile" ] && [ -f "${path}/pyproject.toml" ]; then
            FIXTURE_ROOT="${path}"
            break
        fi
    done
    
    if [ -z "${FIXTURE_ROOT}" ]; then
        echo -e "${YELLOW}[Gitea Init] Warning: Could not locate fixture root, copying will be skipped${NC}"
    else
        echo -e "${YELLOW}[Gitea Init] Using fixture root: ${FIXTURE_ROOT}${NC}"
        find "${FIXTURE_ROOT}" \
            -maxdepth 2 \
            ! -path '*/.git/*' \
            ! -path '*/.github/*' \
            ! -path '*/.*' \
            ! -path '*/__pycache__/*' \
            ! -path '*/.pytest_cache/*' \
            ! -path '*/node_modules/*' \
            ! -name '*.pyc' \
            -type f \
            -exec bash -c 'mkdir -p "'"${WORK_DIR}"'/$(dirname {})" && cp "{}" "'"${WORK_DIR}"'/{}"' \;
    fi
    
    # Create initial commit
    echo -e "${YELLOW}[Gitea Init] Creating initial commit...${NC}"
    git add -A
    
    if [ -n "$(git status --porcelain)" ]; then
        git commit -m "Initial commit for ACT testing"
        echo -e "${GREEN}[Gitea Init] Initial commit created${NC}"
    else
        echo -e "${YELLOW}[Gitea Init] No files to commit, creating empty commit...${NC}"
        # Create an empty initial commit
        git commit --allow-empty -m "Initial empty commit for ACT testing"
        echo -e "${GREEN}[Gitea Init] Empty initial commit created${NC}"
    fi
    
    # Create bare repository in Gitea's repository root directory
    echo -e "${YELLOW}[Gitea Init] Creating bare repository in Gitea container...${NC}"
    local gitea_container=${GITEA_CONTAINER:-"act-gitea-local"}
    local gitea_repo_path="/data/git/repositories/${REPO_NAME}.git"
    
    if docker exec "${gitea_container}" mkdir -p "$(dirname "${gitea_repo_path}")" && \
       docker exec "${gitea_container}" git init --bare "${gitea_repo_path}" 2>&1 | grep -q "Initialized"; then
        echo -e "${GREEN}[Gitea Init] Bare repository created at ${gitea_repo_path}${NC}"
    else
        echo -e "${RED}[Gitea Init] ERROR: Failed to create bare repository${NC}"
        return 1
    fi
    
    # Push to Gitea
    echo -e "${YELLOW}[Gitea Init] Pushing to remote: ${REPO_FULL_URL}${NC}"
    
    # Push to main; if that fails (branch name/ref issue), try master
    if git push -u origin main 2>&1; then
        echo -e "${GREEN}[Gitea Init] Successfully pushed to main${NC}"
    else
        echo -e "${YELLOW}[Gitea Init] main branch push failed, trying master...${NC}"
        if git push -u origin master 2>&1; then
            echo -e "${GREEN}[Gitea Init] Successfully pushed to master${NC}"
        else
            echo -e "${RED}[Gitea Init] ERROR: Failed to push to both main and master${NC}"
            return 1
        fi
    fi
    
    cd - > /dev/null
    
    echo -e "${GREEN}[Gitea Init] Repository populated${NC}"
}

# Cleanup function (optional)
cleanup_repo() {
    echo -e "${YELLOW}[Gitea Init] Cleaning up test repository${NC}"
    rm -rf "${WORK_DIR}"
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
        echo -e "${YELLOW}[Gitea Init] Not running in ACT mode (ACT env var not set). Skipping initialization.${NC}"
        return 0
    fi
    
    # Wait for gitea to be healthy
    if ! wait_for_gitea; then
        echo -e "${RED}[Gitea Init] Failed to connect to Gitea${NC}"
        return 1
    fi
    
    # Initialize repository
    if ! init_repo; then
        echo -e "${RED}[Gitea Init] Failed to initialize repository${NC}"
        return 1
    fi
    
    echo -e "${GREEN}[Gitea Init] Initialization complete!${NC}"
    echo -e "${GREEN}[Gitea Init] Git URL: ${REPO_FULL_URL}${NC}"
    echo -e "${GREEN}[Gitea Init] Repository available at: ${GITEA_URL}/test-repo${NC}"
}

main "$@"
