.PHONY: install run docker-build docker-up docker-down docker-logs clean

PYTHON    := python3
PIP       := $(PYTHON) -m pip
STREAMLIT := $(PYTHON) -m streamlit
ENTRY     := src/app.py

install:
	$(PIP) install -r requirements.txt

run:
	PYTHONPATH=src $(STREAMLIT) run $(ENTRY)

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
