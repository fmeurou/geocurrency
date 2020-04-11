#!/bin/bash

NAME="geocurrencies"                                  # Name of the application
DJANGODIR=/var/apps/envs/geocurrencies/geocurrency              # Django project directory
SOCKFILE=/var/apps/envs/geocurrencies/run/gunicorn.sock  # we will communicte using this unix socket
USER=apps                                        # the user to run as
GROUP=apps                                                              # the group to run as
NUM_WORKERS=2 #$(((`grep -c ^processor /proc/cpuinfo`) * 2 + 1))                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=geocurrencies.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=geocurrencies.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /var/apps/envs/geocurrencies/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /var/apps/envs/geocurrencies/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=0.0.0.0:8000 \
  --log-level=debug \
  --log-file=/var/log/geocurrencies/geocurrencies_unicorn.log
  --reload