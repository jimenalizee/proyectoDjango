#!/usr/bin/env bash
set -o errexit

pip install -r requirements/production.txt

# Si tu template necesita build de assets en Render (package.json tiene gulp build)
# Si esto falla por npm no disponible, te doy el plan B abajo.
npm ci
npm run build

python manage.py collectstatic --no-input
python manage.py migrate