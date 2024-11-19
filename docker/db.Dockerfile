FROM mysql:latest

COPY ./db-init.sql /docker-entrypoint-initdb.d/1.sql 