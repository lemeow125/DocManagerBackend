#!/bin/bash

cd docmanager_backend/
python manage.py graph_models -o ../documentation/erd/app_models.png
python manage.py spectacular --color --file schema.yml
python manage.py migrate
if [ ! -d "static" ]; then
    echo "Generating static files"
    python manage.py collectstatic --noinput
fi
    tmux new-session -d -s "API File Watcher" "cd /app/docmanager_backend && python manage.py start_watcher"
if [ "$DEBUG" = 'True' ]; then
    python manage.py runserver "0.0.0.0:8000"
else
    gunicorn --workers 8 --bind 0.0.0.0:8000 config.wsgi:application
fi
