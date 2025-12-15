#!/bin/bash
set -e

# Create support_triage database if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    SELECT 'CREATE DATABASE support_triage'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'support_triage')\gexec
EOSQL

echo "Database 'support_triage' created or already exists"
