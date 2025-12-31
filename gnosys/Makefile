SHELL := /bin/bash
# python vars
PY := /usr/bin/python
# pytest vars
PYTEST := $(PY) -m pytest
PYTEST_OPTS :=
# mypy vars
MYPY := /usr/bin/mypy
MYPY_OPTS := --strict
# project vars
SRC_DIR := ./src
TEST_DIR := ./test

.PHONY: test/types
test/types:
	$(MYPY) $(MYPY_OPTS) $(SRC_DIR)

.PHONY: test
test: test/types
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)

