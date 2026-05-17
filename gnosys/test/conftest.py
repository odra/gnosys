# SPDX-License-Identifier: AGPL-3.0-only
# common pytest functions and fixtures
# Copyright (C) 2026 Leonardo Rossetti
from click.testing import CliRunner
import pytest


@pytest.fixture
def cli_runner():
    return CliRunner()
