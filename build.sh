#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Borrar base de datos vieja si existe
rm -f db.sqlite3

python manage.py collectstatic --no-input
python manage.py migrate