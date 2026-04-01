import logging
from unittest.mock import patch

import pytest

from gnosys import log


def test_setup_logger_ok():
    with patch('gnosys.log.setup_logger', wraps=log.setup_logger) as m:
        for i in range(0, 3):
            logger = log.get_logger()
 

    assert logger
    m.assert_called_once()


@pytest.mark.parametrize('name,level', [
    ('mock', logging.DEBUG),
    (None, None),
])
def test_setup_logger_ok(name, level):
    opts = {}
    if name:
        opts['name'] = name
    if level:
        opts['level'] = level

    log.setup_logger(**opts)
    logger = log.get_logger()

    assert logger.name == name if name else 'gnosys'
    assert logger.level == level if level else logging.INFO
    assert len(logger.handlers) == 2
