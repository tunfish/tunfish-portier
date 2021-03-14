# =============
# Configuration
# =============

$(eval venv         := .venv)
$(eval pip          := $(venv)/bin/pip)
$(eval python       := $(venv)/bin/python)
$(eval pytest       := $(venv)/bin/pytest)


# =====
# Setup
# =====

# Setup Python virtualenv
setup-virtualenv:
	@test -e $(python) || python3 -m venv $(venv)

# Install requirements for development.
virtualenv-dev: setup-virtualenv
	@test -e $(pytest) || $(pip) install --upgrade --requirement=requirements-test.txt


# ==============
# Software tests
# ==============

.PHONY: test
pytest: setup-package

	@# Run pytest.
	$(pytest) tests -vvv

test: pytest
