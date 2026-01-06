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
import os

from click.testing import CliRunner
import pytest


@pytest.fixture
def testdir():
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def fixdir(testdir):
    return f'{testdir}/fixtures'


@pytest.fixture
def cfg():
    return {
        'data': {
            'sources': [
                {'uri': 'file:///my/data/file.txt', 'provider': 'gnosys_builtins.datasource:FileDataSource'},
                {'uri': 'http://my-url/file.txt', 'provider': 'gnosys_builtins.datasource:HttpDataSource'}
            ]
        }
    }


@pytest.fixture
def cli_runner():
    return CliRunner()
