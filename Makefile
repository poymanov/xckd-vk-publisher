.PHONY : run flush

.DEFAULT_GOAL := run

run:
	docker-compose run app python main.py

flush:
	docker-compose down -v --rmi all