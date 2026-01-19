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

.PHONY: test/types/gnosys
test/types/gnosys:
	$(MYPY) $(MYPY_OPTS) $(SRC_DIR)/gnosys

.PHONY: test/types/gnosys_sample
test/types/gnosys_builtins:
	$(MYPY) $(MYPY_OPTS) $(SRC_DIR)/gnosys_sample

.PHONY: test/types
test/types: test/types/gnosys test/types/gnosys_sample
	$(MYPY) $(MYPY_OPTS) $(SRC_DIR)

.PHONY: test/gnosys
test/gnosys: test/types/gnosys
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)/gnosys

.PHONY: test/gnosys_sample
test/gnosys_builtins: test/types/gnosys_sample
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)/gnosys_sample

.PHONY: test
test: test/types test/gnosys test/gnosys_sample
