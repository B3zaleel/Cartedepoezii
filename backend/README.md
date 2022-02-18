# Cartedepoezii Backend

This is the API layer for Cartedepoezii.

## Requirements

+ PostgreSQL 12+
+ Python3

## Environment Variables

The required environment variables can be stored in a file named `.env.local` and each line should have the format `Name: Value`. The table below lists the environment variables that will be used by this server:

| Name | Description |
|:-|:-|
| DB_DIALECT_DRIVER | |
| DB_USER | The user with read and write access to the database. |
| DB_PWORD | The password of the user with read and write access to the database. |
| DB_HOST | The host of the database server. |
| DB_PORT | The database port SQLAlchemy connects to. |
| DB_NAME | The name of the database. |
| APP_ENV | The application's environment (dev/test) |
| APP_MAX_SIGNIN_TRIES | The maximum number of sign in attempts a user can make in succession. |
| IMG_CDN_PUB_KEY | Imagekit.io public key. |
| IMG_CDN_PRI_KEY | Imagekit.io private key. |
| IMG_CDN_URL_EPT | Imagekit.io url endpoint. |
| APP_SECRET_KEY | Secret key for this application. |

## How To Start

+ Install `libpq-dev`.
+ Install the Python3 dependencies using `pip3 install -r requirements.txt`.
+ Start the database service using `sudo service postgresql start`.
+ Open an interactive shell with the `postgres` user by running `sudo -s -u postgres`.
+ Run `psql -f data/DBSetup_PostgreSQL.sql` in the interactive shell and exit.
+ Run the server using `./run.bash`.
