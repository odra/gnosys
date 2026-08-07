# SPDX-License-Identifier: AGPL-3.0-only
# gnosys logging module
# Copyright (C) 2026 Leonardo Rossetti
import sys
import typing
import logging


class DefaultFormatter(logging.Formatter):
    """
    Default formatter class.
    """
    def __init__(self) -> None:
        super().__init__(fmt='[%(levelname)s] %(name)s: %(message)s',
                         datefmt='%Y-%m-%d %H:%M:%S')

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


def build_logger(name: str = 'gnosys', 
                 level: int = logging.INFO,
                 stdout_handler: typing.Optional[logging.Handler] = None,
                 stderr_handler: typing.Optional[logging.Handler] = None,
                 formatter: logging.Formatter = DefaultFormatter()) -> logging.Logger:
    """
    Setup a new logger.
    """
    logger = logging.getLogger(name)

    logger.handlers = []
    logger.addHandler(stdout_handler if stdout_handler else StdoutHandler(formatter))
    logger.addHandler(stderr_handler if stderr_handler else StderrHandler(formatter))

    logger.setLevel(level)

    return logger
