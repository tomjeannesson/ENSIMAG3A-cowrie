up:
	docker compose up --build --remove-orphans

down:
	docker compose down

downv:
	docker compose down -v

ssh:
	ssh -p 2222 root@localhost