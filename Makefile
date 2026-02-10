DEV_TAG=test_aiti_guru:dev
POSTGRESQL_CONTAINER_NAME=postgres

.PHONY: venv clean stop build external run

venv:
	# Create virtual environment.
	python3.12 -m venv venv
	./venv/bin/pip3 -q install --upgrade pip wheel
	./venv/bin/pip3 -q install -r requirements.txt


clean:
	# Reset all containers and volumes.
	docker compose -f external.compose.yml -f dev.compose.yml -f test.compose.yml down --remove-orphans --volumes --timeout 1

stop:
	# Stop all containers.
	docker compose -f external.compose.yml -f dev.compose.yml down --remove-orphans --timeout 1

build: stop
	# Build image.
	docker build -q -t postgres:dev ./external/postgres
	docker build -q -t $(DEV_TAG) .

external: venv build
	# Run containers with db`s and other common services.
	docker compose -f external.compose.yml up -d --quiet-pull
	timeout 30s bash -c "until docker exec ${POSTGRESQL_CONTAINER_NAME} pg_isready ; do sleep 1 ; done"

run: external
	# Run app in container.
	docker compose -f dev.compose.yml up --abort-on-container-exit

