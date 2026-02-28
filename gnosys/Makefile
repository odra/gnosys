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
SRC_DIR := $(MAKEFILE_DIR)/./src
TEST_DIR := $(MAKEFILE_DIR)/./test

# swallow extra CLI args so make doesn't error
%:
	@:

.PHONY: test/types/gnosys
test/types/gnosys:
	$(MYPY) $(MYPY_OPTS) $(SRC_DIR)/gnosys

.PHONY: test/types/gnosys_sample
test/types/gnosys_sample:
	$(MYPY) $(MYPY_OPTS) $(SRC_DIR)/gnosys_sample

.PHONY: test/types
test/types: test/types/gnosys test/types/gnosys_sample
	$(MYPY) $(MYPY_OPTS) $(SRC_DIR)

.PHONY: test/gnosys
test/gnosys: test/types/gnosys
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)/gnosys

.PHONY: test/gnosys_sample
test/gnosys_sample: test/types/gnosys_sample
	PYTHONPATH=$(SRC_DIR) $(PYTEST) $(PYTEST_OPTS) $(TEST_DIR)/gnosys_sample

.PHONY: test
test: test/types test/gnosys test/gnosys_sample

.PHONY: run/sample
run/samples/llm: 
	(cd samples/llm; PYTHONPATH=$(SRC_DIR) $(PY) -m gnosys build)
