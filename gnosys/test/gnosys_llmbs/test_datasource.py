# SPDX-License-Identifier: AGPL-3.0-only
# gnosys.datasources/__init__.py tests
# Copyright (C) 2026 Leonardo Rossetti

from unittest.mock import MagicMock, patch, mock_open

import pytest

from gnosys_llmbs import datasource


def test_read_from_file_ok():
    m = mock_open(read_data='foobar')
    
    with patch('builtins.open', m):
        res = datasource.read_from_file('/somepath')

    m.assert_called_once_with('/somepath', 'r')
    assert 'foobar' == res


def test_read_from_file_err():
    err = Exception('mock error')
    m = MagicMock(side_effect=err)
    
    with (patch('builtins.open', m), pytest.raises(Exception) as e):
        datasource.read_from_file('/somepath')

    m.assert_called_with('/somepath', 'r')
    assert err == e.value


def test_read_err():
    with pytest.raises(NotImplementedError):
        datasource.read('http://mysource')


def test_read_file_ok():
    m = MagicMock(return_value='foobar')

    with patch('gnosys_llmbs.datasource.read_from_file', m):
        res = datasource.read('file:///mydata.txt')

    assert 'foobar' == res
    m.assert_called_once_with('/mydata.txt')
