#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# Sincronizar migraciones SIN borrar tablas existentes
python manage.py migrate --run-syncdb