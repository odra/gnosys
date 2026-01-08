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
from unittest.mock import MagicMock

import pytest

from gnosys import errors, provider


def test_parse_ok():
    path = 'foo.bar:FooBar'

    provider_pkg, provider_obj = provider.parse(path)

    assert 'foo.bar' == provider_pkg
    assert 'FooBar' == provider_obj


@pytest.mark.parametrize(
    'path',
    ['foo.bar', 'foo:bar:FooBar']
)
def test_parse_err(path):
    with pytest.raises(errors.GnosysError):
        provider.parse(path)


@pytest.mark.parametrize(
    'path,is_loaded',
    [
        ('pathlib:Path', True),
        ('foor.bar:FooBar', False)
    ]
)
def test_load_ok(monkeypatch, path, is_loaded):
    path_pkg, path_obj = path.split(':')

    # spec mock
    mock_spec = MagicMock()
    mock_spec.loader.exec_module = MagicMock()
    mock_find_spec = MagicMock(return_value=mock_spec)
    monkeypatch.setattr(
        provider.importlib.util,
        'find_spec',
        mock_find_spec
    )

    # module mock
    mock_module = MagicMock()
    setattr(mock_module, path_obj, MagicMock())
    mock_module_from_spec = MagicMock(return_value=mock_module)
    monkeypatch.setattr(
        provider.importlib.util,
        'module_from_spec',
        mock_module_from_spec
    )
    
    obj = provider.load(path_pkg, path_obj)
 
    if not is_loaded:
        mock_module_from_spec.assert_called_once()
        mock_find_spec.assert_called_with(path_pkg)
        mock_spec.loader.exec_module.assert_called_once()
    else:
        mock_module_from_spec.assert_not_called()
        mock_find_spec.assert_not_called()
        mock_spec.loader.exec_module.assert_not_called()

    assert path_pkg in sys.modules
    assert obj

@pytest.mark.parametrize(
    'path,is_loaded,find_spec,spec_loader,module_from_spec',
    [
        ('pathlib:Path', True, None, None, None),
        ('foo.bar:FoorBar', False, MagicMock(return_value=None), None, None),
        ('foo.bar:FoorBar', False, MagicMock(), None, None),
        ('foo.bar:FoorBar', False, MagicMock(), MagicMock(), MagicMock(return_value=None)),
    ]
)
def test_load_error(monkeypatch, path, is_loaded, find_spec, spec_loader, module_from_spec):
    if is_loaded:
        return
    
    # spec mock
    mock_spec = MagicMock()
    mock_spec.loader = spec_loader
    find_spec.return_value = mock_spec
    monkeypatch.setattr(
        provider.importlib.util,
        'find_spec',
        find_spec
    )

    # module mock
    monkeypatch.setattr(
        provider.importlib.util,
        'module_from_spec',
        module_from_spec
    )

    with pytest.raises(errors.GnosysError):
        provider.load(*path.split(':'))
