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
import sys
import typing
import logging


__logger: typing.Optional[logging.Logger] = None


class DefaultFormatter(logging.Formatter):
    """
    Default formatter class.
    """
    def __init__(self) -> None:
        super().__init__(fmt='%(asctime)s [%(levelname)-8s] %(name)s: %(message)s',
                         datefmt='"%Y-%m-%d %H:%M:%S')

class MaxLevelFilter(logging.Filter):
    """Rejects any record at or above the given level (used to cap stdout)."""
 
    def __init__(self, max_level: int) -> None:
        super().__init__()
        self.max_level = max_level
 
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < self.max_level


class StdoutHandler(logging.StreamHandler[typing.TextIO]):
    """Handles DEBUG, INFO, WARNING — everything below ERROR."""

    def __init__(self, formatter: logging.Formatter) -> None:
        super().__init__(sys.stdout)
        self.setLevel(logging.DEBUG)
        self.addFilter(MaxLevelFilter(logging.ERROR))
        self.setFormatter(formatter)
 
 
class StderrHandler(logging.StreamHandler[typing.TextIO]):
    """Handles ERROR and CRITICAL only."""

    def __init__(self, formatter: logging.Formatter) -> None:
        super().__init__(sys.stderr)
        self.setLevel(logging.ERROR)
        self.setFormatter(formatter)


def setup_logger(name: str = 'gnosys', 
                 level: int = logging.INFO,
                 stdout_handler: typing.Optional[logging.Handler] = None,
                 stderr_handler: typing.Optional[logging.Handler] = None,
                 formatter: logging.Formatter = DefaultFormatter()) -> None:
    """
    Setup a new logger.
    """
    global __logger

    __logger = logging.getLogger(name)

    __logger.handlers = []
    __logger.addHandler(stdout_handler if stdout_handler else StdoutHandler(formatter))
    __logger.addHandler(stderr_handler if stderr_handler else StderrHandler(formatter))

    __logger.setLevel(level)


def get_logger() -> logging.Logger:
    """
    Return a logger. Setups a new one if __logger is None.
    """
    global __logger

    if __logger is None:
        setup_logger()

    assert __logger

    return __logger 
