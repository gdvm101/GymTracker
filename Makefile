PYTHON ?= python3
VENV := backend/.venv
PY := $(abspath $(VENV)/bin/python)

.PHONY: setup migrate seed backend frontend test test-unit test-integration test-ui build

setup:
	$(PYTHON) -m venv $(VENV)
	"$(PY)" -m pip install -r backend/requirements.txt -r backend/requirements-dev.txt
	cd frontend && npm ci
	@test -f backend/.env || cp backend/.env.example backend/.env

migrate:
	cd backend && "$(PY)" -m alembic upgrade head

seed:
	cd backend && "$(PY)" -m app.tools.seed_exercises

backend:
	cd backend && "$(PY)" -m uvicorn app.main:app --host 127.0.0.1 --port 8000

frontend:
	cd frontend && npm run dev -- --host localhost --port 5173 --strictPort

test: test-unit test-integration test-ui

test-unit:
	cd backend && "$(PY)" -m pytest -q tests/unit

test-integration:
	cd backend && "$(PY)" -m pytest -q tests/integration

test-ui:
	cd frontend && npm run test:unit

build:
	cd frontend && npm run build
