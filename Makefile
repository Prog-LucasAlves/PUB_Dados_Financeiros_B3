SHELL=/bin/bash

install:
	python -m venv .venv
	.venv/scripts/activate
	pip install -r requirements.txt

run:
	cd Docker
	docker-compose up -d