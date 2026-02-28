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
from unittest.mock import MagicMock

from gnosys import config, data
from gnosys_sample import datasources


def test_load_source_file_ok():
    mock_file = MagicMock()
    mock_file.read.return_value = 'my text'

    source = datasources.FileDataSource('/some-file.txt')
    source.path = MagicMock()
    source.path.open.return_value = mock_file

    assert 'my text' == data.load_source(source)


def test_load_source_http_ok():
    mock_res = MagicMock()
    mock_res.text = 'my text'
    datasources.requests.get = MagicMock(return_value=mock_res)

    source = datasources.HttpDataSource('https://someurl.com/data.txt')

    assert 'my text' == data.load_source(source)


def test_build_source_file_ok():
    mock_file = MagicMock()
    mock_file.read.return_value = 'my text'

    source = datasources.FileDataSource('/some-file.txt')
    source.path = MagicMock()
    source.path.open.return_value = mock_file

    assert 'my text' == data.load_source(source)
