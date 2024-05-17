#!/bin/bash

NAME="prod-backend"
HOMEDIR="/Users/gayratbekakhmedov/projects/backend/arc_backend"
VENVDIR="/Users/gayratbekakhmedov/projects/backend/arc_backend/.env"
PROJECTDIR="$HOMEDIR"
SOCKFILE="/var/run/project name/pid.sock"
LOGFILE="/var/log/project name/gunicorn.log"
USER=sysadmin
NUM_WORKERS=2
TIMEOUT=90

echo "Starting $NAME as `whoami`"

cd "$PROJECTDIR"
source "$VENVDIR/bin/activate"

exec "$VENVDIR/bin/gunicorn" main:app \
  --name "$NAME" \
  --workers "$NUM_WORKERS" \
  --user="$USER" \
  --bind=unix:"$SOCKFILE" \
  --access-logfile "$LOGFILE" \
  --log-file "$LOGFILE" \
  --log-level=warning \
  --timeout "$TIMEOUT"
