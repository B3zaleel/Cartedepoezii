# Cartedepoezii Backend

This is the API layer for Cartedepoezii.

## Requirements

+ PostgreSQL 12+
+ Python3

## Environment Variables

The required environment variables should be stored in a file named `.env.local` and each line should have the format `Name: Value`. The table below lists the environment variables that will be used by this server:

| Name | Description |
|:-|:-|
| DB_URL | The URL of the postgreSQL database to connect to. |
| APP_MAX_SIGNIN_TRIES | The maximum number of sign in attempts a user can make in succession. |
| IMG_CDN_PUB_KEY | Imagekit.io public key. |
| IMG_CDN_PRI_KEY | Imagekit.io private key. |
| IMG_CDN_URL_EPT | Imagekit.io url endpoint. |
| GOOGLE_MAIL_SENDER | The email address of the account responsible for sending emails to users. |
| WEB_CLIENT_DOMAIN | The domain name of the web client. |
| APP_SECRET_KEY | The secret key for this application. |

## How To Start

+ Install `libpq-dev`.
+ Install the Python3 dependencies using `pip3 install -r requirements.txt`.
+ Start the database service using `sudo service postgresql start`.
+ Open an interactive shell with the `postgres` user by running `sudo -s -u postgres`.
+ Run `psql -f data/DBSetup_PostgreSQL.sql` in the interactive shell and exit.
+ Run the server using `./run.bash`.

## Viewing The Documentation

+ Install `redoc-cli` with `npm install -g redoc-cli`.
+ Build the docs with `redoc-cli bundle api/v1/OpenAPI_Specs.json -o index.html`.
+ Open the `index.html` file from the current directory.
