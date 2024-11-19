up:
	docker compose up --build --remove-orphans

up-prod:
	docker compose -f production.yml up --build --remove-orphans -d

down:
	docker compose down

downv:
	docker compose down -v

ssh:
	ssh -p 2222 root@localhost