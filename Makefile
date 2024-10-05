PYTHON3 := python3
PYTHON3_VER := $(shell python3 -V | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
PYTHON3_VER_REQ := 3.10
VIRTUAL_ENV ?= .venv
VENV_ACTIVATE_FILE = $(VIRTUAL_ENV)/bin/activate
VENV_ACTIVATE = . $(VENV_ACTIVATE_FILE)

GREEN = \033[0;32m
RED = \033[0;31m
YELLOW = \033[0;33m
RESET = \033[0m

.PHONY: all venv install

all: install

include tools.mk

venv:
	@if [[ ! -f $(VENV_ACTIVATE_FILE) ]]; then \
		printf "🚧 Creating $(YELLOW)python3$(RESET) venv...\n"; \
		python3 -m venv $(VIRTUAL_ENV); \
		printf "✅ Created $(YELLOW)python3$(RESET) venv under $(YELLOW)$(PWD)/$(VIRTUAL_ENV)$(RESET)\n"; \
	fi;

install: venv
	@printf "🚧 Upgrading $(YELLOW)pip$(RESET)...\n"
	@$(VENV_ACTIVATE) ; pip install --upgrade pip wheel
	@printf "🚧 Installing project dependencies...\n"
	@$(VENV_ACTIVATE) ; pip install -e .[develop]

clean:
	rm -rf .venv

clean-pycache:
	- find . -name "__pycache__" -prune -exec rm -rf -- \{\} \;

lint: venv
	@$(VENV_ACTIVATE) ; ruff check

fmt: venv
	@$(VENV_ACTIVATE) ; ruff format

