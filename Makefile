.PHONY: install run debug clean lint lint-strict installation_check

SYS_PYTHON := python3
VENV := .venv
PYTHON := $(VENV)/bin/python3
ARGS := $(wordlist 2, 999, $(MAKECMDGOALS))

$(VENV)/pyvenv.cfg:
	@echo "Creating virtual environment..."
	@$(SYS_PYTHON) -m venv $(VENV)

$(VENV): $(VENV)/pyvenv.cfg
	@$(SYS_PYTHON) -m venv $(VENV)

install: $(VENV)
	@$(PYTHON) -m pip install --upgrade pip flake8 mypy numpy termcolor readchar

installation_check:
	@if [ ! -f "$(VENV)/pyvenv.cfg" ]; then \
		echo "Virtual environment missing. Run 'make install'." >&2; \
		exit 1; \
	fi
	@if ! $(PYTHON) -c "import sys" >/dev/null 2>&1; then \
		echo "Virtual environment Python is broken. Removing it..." >&2; \
		rm -rf $(VENV); \
		echo "Please run 'make install' to recreate the virtual environment." >&2; \
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
	find . -type d -name "mazegen.egg-info" -exec rm -rf {} +
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