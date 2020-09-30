#!/bin/bash
# init-postgres-db.sh
#
# Copied into ./docker-entrypoint-initdb.d and executed upon PostgreSQL installation.
# Uses environment variables set in .env.

set -e

psql -v ON_ERROR_STOP=1 --username "$DB_USER" <<-EOSQL
    CREATE DATABASE $DB_NAME;
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL
