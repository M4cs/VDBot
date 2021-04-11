start:
	@BOT_TOKEN=$(BOT_TOKEN) docker-compose up --build -d

start-logs:
	@BOT_TOKEN=$(BOT_TOKEN) docker-compose up --build

start-python:
	@BOT_TOKEN=$(BOT_TOKEN) python -m vdbot