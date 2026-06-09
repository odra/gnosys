# SPDX-License-Identifier: AGPL-3.0-only
# common pytest functions and fixtures
# Copyright (C) 2026 Leonardo Rossetti
import os

from click.testing import CliRunner
import pytest


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def testdir():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def fixdir(testdir):
    return f'{testdir}/fixtures'
