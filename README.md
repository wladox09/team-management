# Getting started

## Activar el ambiente virtual

source team-management/bin/activate

## Instalar todas las librerías

pip install -r requirements.txt

## Migraciones de django

python manage.py makemigrations

python manage.py migrate

## Run server

python manage.py runserver o python manage.py runserver localhost:3000

## Run Tasks

python manage.py process_tasks
