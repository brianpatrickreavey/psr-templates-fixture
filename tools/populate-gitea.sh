#!/bin/bash
# Populate Gitea repository with psr-templates-fixture files for testing
# Standalone script (does not require ACT to be running)
# Prerequisites: Gitea running on localhost:3000 with test-repo created

set -e

GITEA_PORT=3000
GITEA_URL="http://localhost:${GITEA_PORT}"
GITEA_ADMIN_USER="gitadmin"
GITEA_ADMIN_PASS="gitadmin123"
REPO_NAME="test-repo"
REPO_FULL_URL="${GITEA_URL}/${GITEA_ADMIN_USER}/${REPO_NAME}.git"
WORK_DIR="/tmp/test-repo-populate"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}[Gitea Populate] Starting repository population...${NC}"

# Wait for gitea to be healthy
wait_for_gitea() {
    local timeout=30
    local elapsed=0

    echo -e "${YELLOW}[Gitea Populate] Waiting for Gitea at ${GITEA_URL}...${NC}"

    while [ $elapsed -lt $timeout ]; do
        if curl -s "${GITEA_URL}" > /dev/null 2>&1; then
            echo -e "${GREEN}[Gitea Populate] Gitea is healthy${NC}"
            return 0
        fi
        sleep 1
        elapsed=$((elapsed + 1))
    done

    echo -e "${RED}[Gitea Populate] ERROR: Timeout waiting for Gitea after ${timeout}s${NC}"
    return 1
}

# Populate repository
populate_repo() {
    echo -e "${YELLOW}[Gitea Populate] Initializing repository...${NC}"

    # Configure git credential helper
    echo -e "${YELLOW}[Gitea Populate] Configuring git credential storage...${NC}"
    git config --global credential.helper store

    # Pre-populate git credentials file
    mkdir -p ~/.git-credentials.d
    cat > ~/.git-credentials << 'CREDS'
http://gitadmin:gitadmin123@localhost:3000
CREDS
    chmod 600 ~/.git-credentials

    # Clean work directory
    rm -rf "${WORK_DIR}"
    mkdir -p "${WORK_DIR}"
    cd "${WORK_DIR}"

    # Initialize git repo
    git init
    git config user.name "Test Harness"
    git config user.email "test@example.com"
    git remote add origin "${REPO_FULL_URL}"

    # Copy fixture files
    echo -e "${YELLOW}[Gitea Populate] Copying psr-templates-fixture files...${NC}"

    # Get the repo root - try multiple methods
    FIXTURE_ROOT=""

    # Try: if script is in a tools/ directory
    if [ -d "$(dirname "$0")/.." ]; then
        FIXTURE_ROOT="$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)"
    fi

    # Try: current working directory
    if [ ! -f "${FIXTURE_ROOT}/Makefile" ] || [ ! -f "${FIXTURE_ROOT}/pyproject.toml" ]; then
        if [ -f "./Makefile" ] && [ -f "./pyproject.toml" ]; then
            FIXTURE_ROOT="$(pwd)"
        fi
    fi

    # Try: from fixture path directly
    if [ ! -f "${FIXTURE_ROOT}/Makefile" ] || [ ! -f "${FIXTURE_ROOT}/pyproject.toml" ]; then
        FIXTURE_ROOT="/home/bpreavey/Code/psr-templates-fixture"
    fi

    if [ ! -f "${FIXTURE_ROOT}/Makefile" ] || [ ! -f "${FIXTURE_ROOT}/pyproject.toml" ]; then
        echo -e "${RED}[Gitea Populate] ERROR: Could not locate fixture root. Tried: ${FIXTURE_ROOT}${NC}"
        return 1
    fi

    echo -e "${YELLOW}[Gitea Populate] Using fixture root: ${FIXTURE_ROOT}${NC}"

    # Copy all files except .git (which we'll initialize separately)
    find "${FIXTURE_ROOT}" \
        ! -path '*/.git/*' \
        -type f \
        -exec bash -c 'mkdir -p "'"${WORK_DIR}"'/$(dirname "{}" | sed "s|^'"${FIXTURE_ROOT}"'/||")" && cp "{}" "'"${WORK_DIR}"'/$(echo "{}" | sed "s|^'"${FIXTURE_ROOT}"'/||")"' \;

    # Create initial commit
    echo -e "${YELLOW}[Gitea Populate] Creating initial commit...${NC}"
    git add -A

    if [ -n "$(git status --porcelain)" ]; then
        git commit -m "Initial commit for test harness"
        echo -e "${GREEN}[Gitea Populate] Initial commit created${NC}"
    else
        echo -e "${YELLOW}[Gitea Populate] No files to commit${NC}"
        return 1
    fi

    # Push to Gitea using HTTP auth
    echo -e "${YELLOW}[Gitea Populate] Pushing to remote: ${REPO_FULL_URL}...${NC}"

    # Get current branch name
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    echo -e "${YELLOW}[Gitea Populate] Current branch: ${CURRENT_BRANCH}${NC}"

    # Fetch first to see what's on remote
    echo -e "${YELLOW}[Gitea Populate] Fetching from remote...${NC}"
    git fetch origin 2>&1 || echo -e "${YELLOW}[Gitea Populate] Fetch info: remote may be empty${NC}"

    # Get the remote's default branch
    REMOTE_DEFAULT=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@.*/@@' || echo "master")
    echo -e "${YELLOW}[Gitea Populate] Remote default branch: ${REMOTE_DEFAULT}${NC}"

    # Try to push the current branch
    if git push -u origin "${CURRENT_BRANCH}" 2>&1; then
        echo -e "${GREEN}[Gitea Populate] Successfully pushed ${CURRENT_BRANCH}${NC}"
    else
        # Force push if needed
        echo -e "${YELLOW}[Gitea Populate] Push failed, trying force push...${NC}"
        if git push -f -u origin "${CURRENT_BRANCH}" 2>&1; then
            echo -e "${GREEN}[Gitea Populate] Successfully force pushed ${CURRENT_BRANCH}${NC}"
        else
            echo -e "${RED}[Gitea Populate] ERROR: Failed to push to repository${NC}"
            return 1
        fi
    fi

    cd - > /dev/null

    echo -e "${GREEN}[Gitea Populate] Repository populated${NC}"
}

# Cleanup function
cleanup() {
    echo -e "${YELLOW}[Gitea Populate] Cleaning up work directory${NC}"
    rm -rf "${WORK_DIR}"
    echo -e "${GREEN}[Gitea Populate] Cleanup complete${NC}"
}

# Main execution
main() {
    # Wait for gitea to be healthy
    if ! wait_for_gitea; then
        echo -e "${RED}[Gitea Populate] Failed to connect to Gitea${NC}"
        return 1
    fi

    # Populate repository
    if ! populate_repo; then
        echo -e "${RED}[Gitea Populate] Failed to populate repository${NC}"
        return 1
    fi

    # Cleanup
    cleanup

    echo -e "${GREEN}[Gitea Populate] Population complete!${NC}"
    echo -e "${GREEN}[Gitea Populate] Git URL: ${REPO_FULL_URL}${NC}"
    echo -e "${GREEN}[Gitea Populate] Repository available at: ${GITEA_URL}/${GITEA_ADMIN_USER}/${REPO_NAME}${NC}"
}

main "$@"
