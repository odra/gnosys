SHELL := /bin/bash
MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
# python vars
PY := /usr/bin/python
# pytest vars
PYTEST := $(PY) -m pytest
PYTEST_OPTS :=
# mypy vars
MYPY := /usr/bin/mypy
MYPY_OPTS := --strict
# project vars
SRC_DIR := $(MAKEFILE_DIR)src
TEST_DIR := $(MAKEFILE_DIR)test

# swallow extra CLI args so make doesn't error
%:
	@:

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: test/types/gnosys
test/types/gnosys:
	$(MYPY) $(MYPY_OPTS) $(SRC_DIR)/gnosys

.PHONY: test/types/gnosys_llmbs
test/types/gnosys_llmbs:
	$(MYPY) $(MYPY_OPTS) $(SRC_DIR)/gnosys_llmbs

.PHONY: test/types
test/types: test/types/gnosys test/types/gnosys_llmbs

.PHONY: test/gnosys
test/gnosys:
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)/gnosys

.PHONY: test/gnosys_llmbs
test/gnosys_llmbs:
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)/gnosys_llmbs

.PHONY: test
test: test/types test/gnosys test/gnosys_llmbs
