build:
	docker compose up --build

up:
	docker compose up

v:
	docker compose down -v

down:
	docker compose down

migrations:
	docker compose exec backend python src/manage.py makemigrations

migrate:
	docker compose exec backend python src/manage.py migrate

test:
	docker compose exec backend pytest src/medbook/tests/ -v --color=yes

logs-frontend:
	docker logs medbook-frontend-1 --tail=100 -f

logs-backend:
	docker logs medbook-backend-1 --tail=100 -f

logs-db:
	docker logs medbook-db-1 --tail=100 -f

shell-backend:
	docker exec -it medbook-backend-1 sh

status:
	docker ps --filter "name=medbook-*"