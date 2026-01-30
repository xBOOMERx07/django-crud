#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# FORZAR MIGRACIÓN: Primero borrar el registro de migraciones
python manage.py migrate --fake tasks zero
python manage.py migrate tasks

# Migrar el resto
python manage.py migrate