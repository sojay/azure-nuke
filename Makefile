.PHONY: help build test clean docs install dev lint format

help:
	@echo "Available commands:"
	@echo "  build     - Build the package and binary"
	@echo "  test      - Run tests"
	@echo "  clean     - Clean build artifacts"
	@echo "  docs      - Build documentation"
	@echo "  install   - Install package in development mode"
	@echo "  dev       - Install development dependencies"
	@echo "  lint      - Run linting"
	@echo "  format    - Format code"

build:
	./scripts/build.sh

test:
	pytest tests/ -v

clean:
	rm -rf build/ dist/ *.egg-info/ site/ .pytest_cache/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	mkdocs build

docs-serve:
	mkdocs serve

install:
	pip install -e .

dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black pylint flake8 mkdocs mkdocs-material mkdocs-mermaid2-plugin

lint:
	pylint src/ aznuke/
	flake8 src/ aznuke/

format:
	black src/ aznuke/ tests/
	isort src/ aznuke/ tests/

release:
	@echo "Usage: make release VERSION=x.x.x"
	@if [ -z "$(VERSION)" ]; then echo "VERSION is required"; exit 1; fi
	./scripts/release.sh $(VERSION) 