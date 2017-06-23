#!/usr/bin/env bash

if [[ $1 == "prod" ]]
then
    cd site_app && ./manage.py collectstatic
fi

$VIRTUAL_ENV/bin/uwsgi --ini ./site_app/uwsgi.ini:local --virtualenv $VIRTUAL_ENV &
WELSHSERVER_PID=$!

cd site_app/york && node server.js &
#YORK_PID=$!

#cd ..
python3 ./host/host_server.py 4263
wait $WELSHSERVER_PID
