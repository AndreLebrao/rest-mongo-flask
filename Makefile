NAME=rest-mongo-flask

up:
	docker compose up -d 
down:
	docker compose down --remove-orphans


local:
	flask --app flaskr run --debug