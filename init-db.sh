#!/bin/bash
set -e

# Cek apakah role yang diinginkan sudah ada, jika tidak, buat role tersebut
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    DO
    \$body\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'odootest1') THEN
            CREATE USER odootest1 WITH SUPERUSER PASSWORD 'odootest1';
        END IF;
    END
    \$body\$;
EOSQL

# Cek apakah database yang diinginkan sudah ada, jika tidak, buat database tersebut
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    DO
    \$body\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'odootest1') THEN
            CREATE DATABASE odootest1 WITH OWNER = odoootest1;
        END IF;
    END
    \$body\$;
EOSQL
