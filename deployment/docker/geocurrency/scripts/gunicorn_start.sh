#!/bin/bash

NAME="geocurrencies"                                  # Name of the application
DJANGODIR=/var/apps/api              # Django project directory
SOCKFILE=/var/run/gunicorn.sock  # we will communicte using this unix socket
USER=apps                                        # the user to run as
GROUP=apps                                                              # the group to run as
NUM_WORKERS=2 #$(((`grep -c ^processor /proc/cpuinfo`) * 2 + 1))                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=settings             # which settings file should Django use
DJANGO_WSGI_MODULE=api.api.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=0.0.0.0:8000 \
  --log-level=debug \
  --log-file=/var/apps/logs/gunicorn.log
  --reload