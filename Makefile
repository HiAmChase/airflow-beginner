AIRFLOW_INIT_SERVICE=airflow-init

init:
	docker compose up ${AIRFLOW_INIT_SERVICE}

run:
	docker compose up -d

stop:
	docker compose down -v