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
import pathlib
from unittest.mock import MagicMock

import pytest
import requests

from gnosys_builtins import datasources


# @ai-marker
# ai-assisted: true
# ai-provider: OpenAI
# ai-model-family: GPT-5-class
# human-reviewed: true
def test_datasource_file_ok():
    mock_file = MagicMock()
    mock_file.read.return_value = 'my text'

    source = datasources.FileDataSource('/some-file.txt')
    source.path = MagicMock()
    source.path.open.return_value = mock_file

    with source.load() as content:
        assert 'my text' == content

    source.path.open.assert_called_once()
    mock_file.read.assert_called_once()
    mock_file.close.assert_called_once()


# @ai-marker
# ai-assisted: true
# ai-provider: OpenAI
# ai-model-family: GPT-5-class
# human-reviewed: true
def test_datasource_file_error():
    source = datasources.FileDataSource('/some-file.txt')
    source.path = MagicMock()
    source.path.open.side_effect = FileNotFoundError

    with pytest.raises(OSError):
        with source.load():
            pass

    source.path.open.assert_called_once()
    source.path.open.return_value.read.assert_not_called()
    source.path.open.return_value.close.assert_not_called()


# @ai-marker
# ai-assisted: true
# ai-provider: OpenAI
# ai-model-Family: GPT-5-class
# human-reviewed: true
def test_datasource_http_ok():
    mock_res = MagicMock()
    mock_res.text = 'my text'
    datasources.requests.get = MagicMock(return_value=mock_res)

    source = datasources.HttpDataSource('https://someurl.com/data.txt')

    with source.load() as content:
        assert 'my text' == content

    datasources.requests.get.assert_called_once_with('https://someurl.com/data.txt')
    mock_res.raise_for_status.assert_called_once()
    mock_res.close.assert_called_once()


# @ai-marker
# ai-assisted: true
# ai-provider: OpenAI
# ai-model-family: GPT-5-class
# human-reviewed: true
def test_datasource_http_error(): 
    mock_res = MagicMock()
    mock_res.raise_for_status.side_effect = requests.HTTPError('Something')
    datasources.requests.get = MagicMock(return_value=mock_res)

    source = datasources.HttpDataSource('https://someurl.com/data.txt')

    with pytest.raises(requests.RequestException):
        with source.load() as content:
            pass

    datasources.requests.get.assert_called_once_with('https://someurl.com/data.txt')
    mock_res.raise_for_status.assert_called_once()
    mock_res.close.assert_not_called()
