#!/usr/bin/env bash
# Starts the server
# service postgresql restart
declare -A ENV_VARS
File_Lines=()

# read environment variables from file (.env.local)
readarray -t File_Lines < <(cat .env.local)
for ((i = 0; i < "${#File_Lines[@]}"; i++)) do
    line="${File_Lines[i]}"
    ENV_VARS["$(echo "$line" | cut -d ':' -f1)"]="$(echo "$line" | cut -d ' ' -f2-)"
done

env DB_URL="${ENV_VARS['DB_URL']}" \
    APP_MAX_SIGNIN_TRIES="${ENV_VARS['APP_MAX_SIGNIN_TRIES']}" \
    HOST="${ENV_VARS['HOST']}" \
    IMG_CDN_PUB_KEY="${ENV_VARS['IMG_CDN_PUB_KEY']}" \
    IMG_CDN_PRI_KEY="${ENV_VARS['IMG_CDN_PRI_KEY']}" \
    IMG_CDN_URL_EPT="${ENV_VARS['IMG_CDN_URL_EPT']}" \
    GOOGLE_MAIL_SENDER="${ENV_VARS['GOOGLE_MAIL_SENDER']}" \
    WEB_CLIENT_DOMAIN="${ENV_VARS['WEB_CLIENT_DOMAIN']}" \
    APP_SECRET_KEY="${ENV_VARS['APP_SECRET_KEY']}" \
    python3 -m api.v1.server
