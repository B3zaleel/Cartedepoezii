-- Prepares the MySQL server for this project
DROP DATABASE IF EXISTS cartedepoezii_dev_db;
CREATE DATABASE cartedepoezii_dev_db;
CREATE USER IF NOT EXISTS
    'cartedepoezii_dev'@'localhost'
    IDENTIFIED BY 'cartedepoezii_dev_pwd';
GRANT ALL PRIVILEGES ON `cartedepoezii_dev_db`.*
    TO 'cartedepoezii_dev'@'localhost';
FLUSH PRIVILEGES;
