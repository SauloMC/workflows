#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-staging}"
APP_NAME="${APP_NAME:-workflow-demo}"
DEPLOY_HOST="${DEPLOY_HOST:-}"
DEPLOY_PATH="${DEPLOY_PATH:-/var/www/workflow-demo}"
DEPLOY_USER="${DEPLOY_USER:-deploy}"
DEPLOY_PORT="${DEPLOY_PORT:-22}"

if [[ -z "${DEPLOY_HOST}" ]]; then
  echo "ERROR: DEPLOY_HOST is required. Example: export DEPLOY_HOST=example.com" >&2
  exit 1
fi

if [[ ! -f "frontend/package.json" ]]; then
  echo "ERROR: frontend package.json not found. Run from repository root." >&2
  exit 1
fi

if [[ "${ENVIRONMENT}" == "production" ]]; then
  echo "INFO: production deploy requires manual approval via GitHub environment approval gate."
fi

echo "INFO: Building frontend bundle for ${ENVIRONMENT}"
cd frontend
npm ci
npm run build
cd ..

echo "INFO: Preparing deployment archive"
mkdir -p .deploy
cp -R frontend/dist .deploy/dist
cp -R backend .deploy/backend

echo "INFO: Deploying to ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH} using SSH"
ssh -p "${DEPLOY_PORT}" "${DEPLOY_USER}@${DEPLOY_HOST}" "mkdir -p '${DEPLOY_PATH}'"
scp -P "${DEPLOY_PORT}" -r .deploy/* "${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/"

echo "INFO: Deployment of ${APP_NAME} to ${ENVIRONMENT} completed successfully"
