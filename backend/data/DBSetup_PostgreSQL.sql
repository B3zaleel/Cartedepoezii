-- Prepares the PostgreSQL server for this project
DROP DATABASE IF EXISTS cartedepoezii_dev_db;

CREATE DATABASE cartedepoezii_dev_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE cartedepoezii_dev_db
    IS 'The database for cartedepoezii.';

CREATE ROLE
    cartedepoezii_dev
    WITH
    LOGIN
    REPLICATION
    BYPASSRLS
    PASSWORD 'cartedepoezii_dev_pwd';

GRANT CONNECT ON DATABASE cartedepoezii_dev_db
    TO cartedepoezii_dev;
GRANT SELECT ON ALL TABLES IN SCHEMA public
    TO cartedepoezii_dev;
