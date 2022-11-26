#!/bin/sh

echo The port number is: $SERVICE_PORT
if [ -n $SERVICE_PORT ]
then
    exec gunicorn --timeout 180 -b :$SERVICE_PORT --access-logfile - --error-logfile - run:app
fi
