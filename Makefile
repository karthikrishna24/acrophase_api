.PHONY: build start restart stop test

# Regular commands
build:
	docker-compose build

start:
	docker-compose up -d

restart:
	docker-compose restart

stop:
	docker-compose down

# Test command
test:
	docker-compose -f docker-compose.test.yml up -d test_db
	docker-compose -f docker-compose.test.yml run --rm test_app
	docker-compose -f docker-compose.test.yml down
