start:
	@NEXUS_TOKEN=$(NEXUS_TOKEN) BOT_TOKEN=$(BOT_TOKEN) docker-compose up --build -d

start-logs:
	@NEXUS_TOKEN=$(NEXUS_TOKEN) BOT_TOKEN=$(BOT_TOKEN) docker-compose up --build

start-python:
	@NEXUS_TOKEN=$(NEXUS_TOKEN) BOT_TOKEN=$(BOT_TOKEN) python -m vdbot