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

import pytest

from gnosys import config, errors, data


def test_build_source_ok(monkeypatch):
    # config item
    item = config.Provider(provider='foo.bar:FooBar', options={'uri': 'file:///foo.bar'})
    
    # mock objects
    ## Data Source mock implemention, it does not need to do anything
    mock_datasource = MagicMock()
    ## provider.parse mock object
    mock_parse = MagicMock()
    mock_parse.return_value = ('foo.bar', 'FooBar')
    ## provider.load mock object
    mock_load = MagicMock()
    mock_load.return_value = mock_datasource

    monkeypatch.setattr(
        data.provider,
        'parse',
        mock_parse
    )

    monkeypatch.setattr(
        data.provider,
        'load',
        mock_load
    )

    source = data.build_source(item)

    mock_datasource.from_uri.assert_called_with('file:///foo.bar')
    mock_parse.assert_called_with('foo.bar:FooBar')
    mock_load.assert_called_with('foo.bar', 'FooBar')


@pytest.mark.parametrize(
    'provider,options,error',
    [
        ('foo.bar:FooBar', None, AssertionError),
        ('pathlib:Path', {'not_uri': 'something'}, errors.GnosysError),
    ]
)
def test_build_source_err(monkeypatch, provider, options, error):
    # config item
    item = config.Provider(provider=provider, options=options)
    
    with pytest.raises(error):   
        data.build_source(item)
