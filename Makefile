up:
	docker compose up -d --build 
down:
	docker compose down -v 
restart: down up