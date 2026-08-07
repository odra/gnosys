# SPDX-License-Identifier: AGPL-3.0-only
# gnosys:log.py tests
# Copyright (C) 2026 Leonardo Rossetti

import logging
from unittest.mock import patch

import pytest

from gnosys import log


@pytest.mark.parametrize('name,level', [
    ('mock', logging.DEBUG),
    (None, None),
])
def test_build_logger_ok(name, level):
    opts = {}
    if name:
        opts['name'] = name
    if level:
        opts['level'] = level

    logger = log.build_logger(**opts)

    assert logger.name == name if name else 'gnosys'
    assert logger.level == level if level else logging.INFO
    assert len(logger.handlers) == 2
