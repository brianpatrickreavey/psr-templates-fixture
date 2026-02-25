#!/bin/bash
# Initialize Gitea repository with psr-templates-fixture files for ACT local testing
# This script runs only in ACT mode. Expects: Gitea already running with credentials gitadmin/gitadmin123
# Pre-existing repo: test-repo already created via Gitea API (created by docker-gitea-start.sh)

set -e

# Get the repo root (where this script is called from)
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

GITEA_PORT=3000
GITEA_URL="http://localhost:${GITEA_PORT}"
GITEA_ADMIN_USER="gitadmin"
GITEA_ADMIN_PASS="gitadmin123"
REPO_NAME="test-repo"
REPO_FULL_URL="${GITEA_URL}/${GITEA_ADMIN_USER}/${REPO_NAME}.git"
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
    
    # Configure git credential helper to store credentials
    echo -e "${YELLOW}[Gitea Init] Configuring git credential storage...${NC}"
    git config --global credential.helper store
    
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
    
    FIXTURE_ROOT="${REPO_ROOT}"
    if [ ! -f "${FIXTURE_ROOT}/Makefile" ] || [ ! -f "${FIXTURE_ROOT}/pyproject.toml" ]; then
        # Fallback search
        for path in /home/bpreavey/Code/psr-templates-fixture $(pwd)/.. $(pwd)/../..; do
            if [ -f "${path}/Makefile" ] && [ -f "${path}/pyproject.toml" ]; then
                FIXTURE_ROOT="${path}"
                break
            fi
        done
    fi
    
    if [ ! -f "${FIXTURE_ROOT}/Makefile" ]; then
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
            -exec bash -c 'mkdir -p "'"${WORK_DIR}"'/$(dirname "{}" | sed "s|^'"${FIXTURE_ROOT}"'/||")" && cp "{}" "'"${WORK_DIR}"'/$(echo "{}" | sed "s|^'"${FIXTURE_ROOT}"'/||")"' \;
    fi
    
    # Create initial commit
    echo -e "${YELLOW}[Gitea Init] Creating initial commit...${NC}"
    git add -A
    
    if [ -n "$(git status --porcelain)" ]; then
        git commit -m "Initial commit for ACT testing"
        echo -e "${GREEN}[Gitea Init] Initial commit created${NC}"
    else
        echo -e "${YELLOW}[Gitea Init] No files to commit, creating empty commit...${NC}"
        git commit --allow-empty -m "Initial empty commit for ACT testing"
        echo -e "${GREEN}[Gitea Init] Empty initial commit created${NC}"
    fi
    
    # Push to Gitea using HTTP auth
    echo -e "${YELLOW}[Gitea Init] Pushing to remote: ${REPO_FULL_URL}...${NC}"
    
    # Get current branch name
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    echo -e "${YELLOW}[Gitea Init] Current branch: ${CURRENT_BRANCH}${NC}"
    
    # Fetch first to see what's on remote
    echo -e "${YELLOW}[Gitea Init] Fetching from remote...${NC}"
    git fetch origin 2>&1 || echo -e "${YELLOW}[Gitea Init] Fetch returned non-zero (might be OK for empty repo)${NC}"
    
    # Get the remote's default branch
    REMOTE_DEFAULT=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@.*/@@' || echo "main")
    echo -e "${YELLOW}[Gitea Init] Remote default branch: ${REMOTE_DEFAULT}${NC}"
    
    # Try to push the current branch first
    if git push -u origin "${CURRENT_BRANCH}:${REMOTE_DEFAULT}" 2>&1; then
        echo -e "${GREEN}[Gitea Init] Successfully pushed ${CURRENT_BRANCH} to ${REMOTE_DEFAULT}${NC}"
    else
        # If that failed, try simple push of current branch
        if git push -u origin "${CURRENT_BRANCH}" 2>&1; then
            echo -e "${GREEN}[Gitea Init] Successfully pushed ${CURRENT_BRANCH}${NC}"
        else
            # Last resort: force push
            echo -e "${YELLOW}[Gitea Init] Push failed, trying force push...${NC}"
            if git push -f -u origin "${CURRENT_BRANCH}" 2>&1; then
                echo -e "${GREEN}[Gitea Init] Successfully force pushed ${CURRENT_BRANCH}${NC}"
            else
                echo -e "${RED}[Gitea Init] ERROR: Failed to push to repository${NC}"
                return 1
            fi
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
    echo -e "${GREEN}[Gitea Init] Repository available at: ${GITEA_URL}/${GITEA_ADMIN_USER}/${REPO_NAME}${NC}"
}

main "$@"

