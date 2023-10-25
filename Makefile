include ./.env

default:
	make build
	make up
	make initdb
	make mkuser

initdb:
	docker exec ${APP_NAME}-app ./manage.py migrate

mkuser:
	docker exec -it ${APP_NAME}-app ./manage.py createsuperuser

static:
	docker exec ${APP_NAME}-app ./manage.py collectstatic --noinput

build:
	docker-compose build

up:
	docker-compose up -d
