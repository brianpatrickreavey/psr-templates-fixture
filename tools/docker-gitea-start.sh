#!/bin/bash
# Docker Gitea Start Script
# Starts Gitea, bootstraps with a test repository, ready for CLI access

set -e

GITEA_CONTAINER="act-gitea-local"
GITEA_PORT=3000
GITEA_DATA_DIR="/tmp/gitea-data"
REPO_NAME="test-repo"

# Get current user's UID and GID for proper file ownership
CURRENT_UID=$(id -u)
CURRENT_GID=$(id -g)

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
  -e USER_UID=${CURRENT_UID} \
  -e USER_GID=${CURRENT_GID} \
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

# Create admin user
echo "8. Creating admin user..."
docker exec ${GITEA_CONTAINER} \
  bash -c 'su-exec git /usr/local/bin/gitea admin user create --username=gitadmin --password=gitadmin123 --email=admin@local --admin --must-change-password=false' > /dev/null 2>&1
echo "   ✓ Admin user 'gitadmin' created"
echo ""

# Create repository via API
echo "9. Creating test repository via API..."
sleep 2  # Allow time for user creation to persist
REPO_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"${REPO_NAME}\",\"description\":\"Test repository\",\"private\":false,\"auto_init\":true}" \
  -u "gitadmin:gitadmin123" \
  http://localhost:${GITEA_PORT}/api/v1/user/repos)

if echo "${REPO_RESPONSE}" | grep -q "\"id\""; then
  echo "   ✓ Repository '${REPO_NAME}' created via API"
else
  echo "   ✗ Failed to create repository via API"
  echo "   Response: ${REPO_RESPONSE}"
  exit 1
fi
echo ""

# Verify CLI access
echo "10. Verifying CLI access..."
if curl -s http://localhost:${GITEA_PORT} > /dev/null 2>&1; then
  echo "   ✓ HTTP access: http://localhost:${GITEA_PORT}"
  echo "   ✓ Test repo available at: http://localhost:${GITEA_PORT}/gitadmin/${REPO_NAME}.git"
else
  echo "   ✗ Cannot access Gitea"
  exit 1
fi
echo ""

echo "=== Gitea is ready ==="
echo ""
echo "Login credentials:"
echo "  Username: gitadmin"
echo "  Password: gitadmin123"
echo ""
echo "To test CLI access:"
echo "  cd /tmp && rm -rf test-repo && mkdir test-repo && cd test-repo"
echo "  git init && git config user.email 'test@test.com' && git config user.name 'Test'"
echo "  echo 'test' > README.md && git add README.md && git commit -m 'Initial'"
echo "  git remote add origin http://gitadmin:gitadmin123@localhost:${GITEA_PORT}/gitadmin/${REPO_NAME}.git"
echo "  git push -u origin master"
echo ""
