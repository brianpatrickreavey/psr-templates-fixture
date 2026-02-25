#!/bin/bash
# Docker Gitea Start Script
# Starts Gitea, bootstraps with a test repository, ready for CLI access

set -e

GITEA_CONTAINER="act-gitea-local"
GITEA_PORT=3000
GITEA_DATA_DIR="/tmp/gitea-data"
REPO_NAME="psr-templates-fixture"

# Extract the origin owner from git remote (e.g., brianpatrickreavey from github.com/brianpatrickreavey/repo)
ORIGIN_URL=$(git config --get remote.origin.url 2>/dev/null || echo "")
if [ -z "$ORIGIN_URL" ]; then
  echo "Error: Could not determine git origin URL"
  exit 1
fi
GITEA_USER=$(echo "$ORIGIN_URL" | sed -E 's|.*[:/]([^/]+)/.*|\1|')

# Gitea admin password (for the origin user in Gitea)
GITEA_PASS="gitea-secure-pass-123"

# Get current user's UID and GID for proper file ownership
# If running as root (UID 0), use a non-root UID instead (Gitea won't run as root)
CURRENT_UID=$(id -u)
if [ "$CURRENT_UID" -eq 0 ]; then
  GITEA_UID=1000
  GITEA_GID=1000
else
  GITEA_UID=$CURRENT_UID
  GITEA_GID=$(id -g)
fi

echo "=== Docker Gitea Bootstrap Script ==="
echo ""

# Clean up existing container
echo "1. Cleaning up any existing Gitea container..."
docker rm -f ${GITEA_CONTAINER} 2>/dev/null || true
echo "   ✓ Done"
echo ""

# Prepare data directory
echo "2. Preparing data directory at ${GITEA_DATA_DIR}..."
mkdir -p ${GITEA_DATA_DIR}/conf
mkdir -p ${GITEA_DATA_DIR}/git/repositories
mkdir -p ${GITEA_DATA_DIR}/git/.ssh
mkdir -p ${GITEA_DATA_DIR}/ssh
# Make directories world-writable so any UID can write to them
chmod 777 ${GITEA_DATA_DIR}
chmod 777 ${GITEA_DATA_DIR}/git
chmod 777 ${GITEA_DATA_DIR}/git/.ssh
chmod 777 ${GITEA_DATA_DIR}/ssh
echo "   ✓ Done"
echo ""

# Generate minimal config
echo "3. Generating Gitea configuration..."
bash ./tools/gitea-config-gen.sh ${GITEA_DATA_DIR}/conf/app.ini
echo "   ✓ Done"
echo ""

# Start Gitea container with INSTALL_LOCK
echo "4. Starting Gitea container on port ${GITEA_PORT}..."
docker run -d \
  --name ${GITEA_CONTAINER} \
  -p ${GITEA_PORT}:3000 \
  -p 2222:22 \
  -v ${GITEA_DATA_DIR}:/data \
  -e USER_UID=${GITEA_UID} \
  -e USER_GID=${GITEA_GID} \
  -e GITEA__security__INSTALL_LOCK=true \
  gitea/gitea:latest > /dev/null
echo "   ✓ Container started (ID: $(docker ps --filter name=${GITEA_CONTAINER} -q))"
echo ""

# Wait for Gitea to be ready
echo "5. Waiting for Gitea to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
  if curl -s http://localhost:${GITEA_PORT} > /dev/null 2>&1; then
    echo "   ✓ Gitea is responding"
    break
  fi
  if [ $attempt -eq $((max_attempts - 1)) ]; then
    echo "   ✗ Gitea failed to start after ${max_attempts} seconds"
    docker logs ${GITEA_CONTAINER} 2>&1 | tail -20
    exit 1
  fi
  sleep 1
  attempt=$((attempt + 1))
done
echo ""

# Run database migration
echo "6. Running database migration..."
docker exec ${GITEA_CONTAINER} \
  bash -c 'su-exec git /usr/local/bin/gitea migrate' > /dev/null 2>&1
echo "   ✓ Database migration complete"
echo ""

# Fix permissions on git repositories directory for the git user
echo "7. Fixing permissions on git repositories directory..."
docker exec ${GITEA_CONTAINER} \
  bash -c 'chown -R git:git /data/git && chmod -R 755 /data/git' > /dev/null 2>&1
echo "   ✓ Permissions fixed"
echo ""

# Create admin user (idempotent - check first)
echo "8. Creating admin user '${GITEA_USER}'..."
# Check if user already exists
if curl -sf -u ${GITEA_USER}:${GITEA_PASS} http://localhost:${GITEA_PORT}/api/v1/user > /dev/null 2>&1; then
  echo "   ℹ Admin user '${GITEA_USER}' already exists"
else
  # Create the user - use bash -c to properly invoke su-exec
  docker exec ${GITEA_CONTAINER} bash -c "su-exec git /usr/local/bin/gitea admin user create --username=${GITEA_USER} --password=${GITEA_PASS} --email=admin@local --admin --must-change-password=false" 2>&1 | grep -q "successfully created" && echo "   ✓ Admin user '${GITEA_USER}' created" || echo "   ⚠ Failed to create admin user"
fi
echo ""

# Wait for API to be ready with admin credentials
echo "8b. Waiting for API to be ready with admin credentials..."
sleep 3
max_attempts=10
attempt=0
while [ $attempt -lt $max_attempts ]; do
  if curl -sf -u ${GITEA_USER}:${GITEA_PASS} http://localhost:${GITEA_PORT}/api/v1/user > /dev/null 2>&1; then
    echo "   ✓ API is ready"
    break
  fi
  sleep 1
  attempt=$((attempt + 1))
done
echo ""

# Create repository via API (idempotent - register in Gitea database)
echo "9. Creating fixture repository via API..."
sleep 1

# Use API to create repository - don't fail if it already exists
REPO_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"${REPO_NAME}\",\"description\":\"PSR Templates Fixture\",\"private\":false,\"auto_init\":true}" \
  -u ${GITEA_USER}:${GITEA_PASS} \
  http://localhost:${GITEA_PORT}/api/v1/user/repos 2>&1) || true

if echo "${REPO_RESPONSE}" | grep -q '"id"'; then
  echo "   ✓ Repository '${REPO_NAME}' created via API"
elif echo "${REPO_RESPONSE}" | grep -q 'already exists'; then
  echo "   ℹ Repository '${REPO_NAME}' already exists"
else
  echo "   ⚠ Repository creation response:"
  echo "   ${REPO_RESPONSE}"
fi
echo ""

# Populate repository with fixture files via mirror clone
echo "9b. Populating repository with fixture files..."

# Capture script directory BEFORE changing directories
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FIXTURE_ROOT="$(dirname "${SCRIPT_DIR}")"

WORK_DIR="/tmp/gitea-populate-${REPO_NAME}"
rm -rf "${WORK_DIR}"
mkdir -p "${WORK_DIR}"
cd "${WORK_DIR}"

# Clone the fixture repo as a bare mirror to preserve all history
# This gets the complete repository state including all commits and branches
git clone --mirror "${FIXTURE_ROOT}" "${WORK_DIR}/mirror.git" 2>/dev/null || {
  # Fallback: If not in a git repo, initialize and commit fixture files
  git init
  git config user.name "Gitea Setup"
  git config user.email "setup@gitea.local"
  
  # Copy fixture files from the current psr-templates-fixture directory
  if [ -f "${FIXTURE_ROOT}/Makefile" ] && [ -f "${FIXTURE_ROOT}/pyproject.toml" ]; then
    cp -r "${FIXTURE_ROOT}"/* "${WORK_DIR}/" 2>/dev/null || true
    rm -rf "${WORK_DIR}/.pytest_cache" "${WORK_DIR}/__pycache__" "${WORK_DIR}/.artifacts" "${WORK_DIR}/.venv" 
    find "${WORK_DIR}" -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
    find "${WORK_DIR}" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
  fi
  
  git add -A
  git commit -m "Initial fixture setup" || true
}

# Push the repository to Gitea
if [ -d "${WORK_DIR}/mirror.git" ]; then
  cd "${WORK_DIR}/mirror.git"
  git push --mirror "http://${GITEA_USER}:${GITEA_PASS}@localhost:${GITEA_PORT}/${GITEA_USER}/${REPO_NAME}.git" 2>/dev/null || {
    echo "   ⚠ Mirror push failed, trying alternative"
  }
else
  # Standard push for non-mirror repo
  cd "${WORK_DIR}"
  git remote add origin "http://${GITEA_USER}:${GITEA_PASS}@localhost:${GITEA_PORT}/${GITEA_USER}/${REPO_NAME}.git" 2>/dev/null || true
  git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || true
fi

echo "   ✓ Repository populated"
echo ""

# Verify CLI access
echo "10. Creating authentication token..."
# Check if token already exists (by name pattern)
TOKEN_NAME="workflow-$(date +%s)"
TOKEN_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"${TOKEN_NAME}\",\"scopes\":[\"all\"]}" \
  -u "${GITEA_USER}:${GITEA_PASS}" \
  http://localhost:${GITEA_PORT}/api/v1/users/${GITEA_USER}/tokens 2>&1) || true

GITEA_TOKEN=$(echo "${TOKEN_RESPONSE}" | grep -o '"sha1":"[^"]*' | cut -d'"' -f4)
if [ -n "$GITEA_TOKEN" ]; then
  echo "   ✓ Authentication token created"
  echo "GITEA_USER=${GITEA_USER}"
  echo "GITEA_PASS=${GITEA_PASS}"
  echo "GITEA_TOKEN=${GITEA_TOKEN}"
else
  echo "   ⚠ Failed to create token"
  echo "   Response: ${TOKEN_RESPONSE}"
fi
echo ""

# Verify CLI access
echo "11. Verifying CLI access..."
if curl -s http://localhost:${GITEA_PORT} > /dev/null 2>&1; then
  echo "   ✓ HTTP access: http://localhost:${GITEA_PORT}"
  echo "   ✓ Test repo available at: http://localhost:${GITEA_PORT}/${GITEA_USER}/${REPO_NAME}.git"
else
  echo "   ✗ Cannot access Gitea"
  exit 1
fi
echo ""

echo "=== Gitea is ready ==="
echo ""
echo "Login credentials:"
echo "  Username: ${GITEA_USER}"
echo "  Password: ${GITEA_PASS}"
echo ""
echo "To test CLI access:"
echo "  cd /tmp && rm -rf ${REPO_NAME}-test && mkdir ${REPO_NAME}-test && cd ${REPO_NAME}-test"
echo "  git init && git config user.email 'test@test.com' && git config user.name 'Test'"
echo "  echo 'test' > README.md && git add README.md && git commit -m 'Initial'"
echo "  git remote add origin http://${GITEA_USER}:${GITEA_PASS}@localhost:${GITEA_PORT}/${GITEA_USER}/${REPO_NAME}.git"
echo "  git push -u origin master"
echo ""
