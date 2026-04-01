# Copyright (C) 2025 Leonardo Rossetti
# SPDX-License-Identifier: AGPL-3.0-only
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
