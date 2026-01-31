#!/bin/bash
# Add data sources to OtterStax after startup

set -e

OTTERSTAX_URL="${OTTERSTAX_URL:-http://localhost:8085}"

echo "Waiting for OtterStax to be ready..."
until curl -sf "${OTTERSTAX_URL}/health" > /dev/null 2>&1; do
    sleep 2
done
echo "OtterStax is ready!"

echo "Adding campaigns data source..."
curl -X POST "${OTTERSTAX_URL}/add_connection" \
  -H "Content-Type: application/json" \
  -d '{
    "alias": "campaigns",
    "host": "mariadb1",
    "port": "3306",
    "username": "user1",
    "password": "password1",
    "database": "db1",
    "table": ""
  }'
echo ""

echo "Adding impressions data source..."
curl -X POST "${OTTERSTAX_URL}/add_connection" \
  -H "Content-Type: application/json" \
  -d '{
    "alias": "impressions",
    "host": "mariadb2",
    "port": "3306",
    "username": "user2",
    "password": "password2",
    "database": "db2",
    "table": ""
  }'
echo ""

echo "Data sources configured successfully!"
