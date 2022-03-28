.PHONY: test
test:
	docker-compose run -e STAGE=test order-service pytest .

.PHONY: install
install: requirements/dev.txt
	pip install -Ur requirements/dev.txt

.PHONY: run_dev
run_dev:
	docker-compose up --build --force-recreate  --remove-orphans

.PHONY: migrate
migrate:
	docker-compose run order-service alembic upgrade head
