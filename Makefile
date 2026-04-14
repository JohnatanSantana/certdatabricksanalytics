.PHONY: install run lock docker-build docker-up docker-down docker-logs clean

UV    := uv
ENTRY := src/app.py

install:
	$(UV) sync

run:
	PYTHONPATH=src $(UV) run streamlit run $(ENTRY)

lock:
	$(UV) lock

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
