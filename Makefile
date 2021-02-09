build:
	docker build --pull -t recurr_txns:latest .

run: build
	docker run -it recurr_txns:latest $(INPUT_FILE)

format:
	pipenv run black .
