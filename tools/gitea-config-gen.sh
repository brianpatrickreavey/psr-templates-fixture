#!/bin/bash
# Generate minimal app.ini configuration for Gitea with SQLite database
# This allows Gitea to skip the installation wizard and be ready immediately

set -e

OUTPUT_PATH="${1:-.gitea-app.ini}"

# Ensure the directory exists
mkdir -p "$(dirname "${OUTPUT_PATH}")"

cat > "${OUTPUT_PATH}" << 'EOF'
; Gitea minimal configuration for docker-local testing
; Database configuration
[database]
DB_TYPE = sqlite3
PATH = /data/gitea/gitea.db
LOG_SQL = false

; Repository configuration  
[repository]
ROOT_PATH = /data/git/repositories
SCRIPT_TYPE = bash
ENABLE_PUSH_CREATE_USER = true
ENABLE_PUSH_CREATE_ORG = true

; Server configuration
[server]
PROTOCOL = http
DOMAIN = localhost
ROOT_URL = http://localhost:3000/
HTTP_ADDR = 0.0.0.0
HTTP_PORT = 3000
DISABLE_SSH = false
SSH_PROTOCOL = ssh
SSH_DOMAIN = localhost
START_SSH_SERVER = true
SSH_LISTEN_HOST = 0.0.0.0
SSH_LISTEN_PORT = 22
SSH_ROOT_PATH = /data/ssh

; Security
[security]
INSTALL_LOCK = true
SECRET_KEY = test_secret_key_change_this_in_production
INTERNAL_TOKEN = test_token_change_this_in_production

; Service
[service]
DISABLE_REGISTRATION = false
ALLOW_ONLY_EXTERNAL_REGISTRATION = false

; Mailer - disabled
[mailer]
ENABLED = false

; Session
[session]
PROVIDER = memory

; Log
[log]
MODE = console
LEVEL = info

; Git
[git]
DISABLE_DIFF_ALL = false
MAX_GIT_PROCESS_TIMEOUT = 60s

EOF

echo "Generated Gitea configuration at: ${OUTPUT_PATH}"
