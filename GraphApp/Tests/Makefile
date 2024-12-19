.PHONY: all start test stop ui # Phony files protects makefile incase any files are made sharing the name of these targets

all: start testfiles ui stop  # Starts the server, runs all backend and frontend tests, and closes the server
test: start testfiles stop # Starts the server, runs all backend tests, and closes the server
ui: start testui stop # Starts the server, then creates docker container and tests UI.

start: # Starts the server
	@cd ../ && ./TRGserver.py &

testfiles: api helpers access admin 

api:
	pytest -v api_test.py

helpers:
	pytest -v helpers_test.py

access:
	pytest -v access_db_test.py

admin:
	pytest -v admin_tool_test.py

stop: # Stops the server
	pkill -f ../TRGserver.py

testui:
	docker build -t selenium-webdriver UITest/
	docker run --network="host" --rm -v $(pwd):/app selenium-webdriver
