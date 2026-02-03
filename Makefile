.PHONY: install run debug clean lint lint-strict

SYS_PYTHON := python3
VENV := .venv
PYTHON = $(VENV)/bin/python3
ARGS := $(wordlist 2, 999, $(MAKECMDGOALS))

$(VENV):
	@if [ ! -d "$(VENV)" ]; then \
		$(SYS_PYTHON) -m venv $(VENV); \
	fi

install: $(VENV)
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -e ./mazegen
	@$(PYTHON) -m pip install flake8 mypy numpy termcolor readchar

installation_check:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Please run 'make install' first"; \
		exit 1; \
	fi

run: installation_check
	@$(PYTHON) a_maze_ing.py $(ARGS)

debug: installation_check
	@$(PYTHON) -m pdb a_maze_ing.py $(ARGS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "mazegen_42.egg-info" -exec rm -rf {} +
	find . -name "*.pyc" -delete

lint: installation_check
	@$(PYTHON) -m flake8 --exclude .venv,venv,env .
	@$(PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: installation_check
	@$(PYTHON) -m flake8 --exclude .venv,venv,env .
	@$(PYTHON) -m mypy . --strict