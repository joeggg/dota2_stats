.PHONY: api, parserr, ui, ui-dev

api:
	docker build -t dota2stats-api:latest -f docker/Dockerfile.api .

parserr:
	docker build -t dota2stats-parser:latest -f docker/Dockerfile.parser .

ui:
	docker build -t dota2stats-ui-requirements:latest -f docker/Dockerfile.ui.requirements .
	docker build -t dota2stats-ui:latest -f docker/Dockerfile.ui .

ui-dev:
	docker build -t dota2stats-ui:latest -f docker/Dockerfile.ui.dev .
