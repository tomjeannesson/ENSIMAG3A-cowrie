up:
	docker compose up --build --remove-orphans

down:
	docker compose down

ssh:
	ssh -p 2222 root@localhost