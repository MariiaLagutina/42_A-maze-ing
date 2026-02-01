.PHONY: install run debug clean lint lint-strict

PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin
ARGS := $(wordlist 2, 999, $(MAKECMDGOALS))

install:
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
	fi
	@$(BIN)/pip install --upgrade pip
	@$(BIN)/pip install -e ./mazegen
	@$(BIN)/pip install flake8 mypy numpy termcolor readchar

run:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Please run 'make install' first"; \
		exit 1; \
	fi
	@$(BIN)/python a_maze_ing.py $(ARGS)

debug:
	@$(BIN)/python -m pdb a_maze_ing.py $(ARGS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete

lint:
	@$(BIN)/flake8 .
	@$(BIN)/mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	@$(BIN)/flake8 .
	@$(BIN)/mypy . --strict
