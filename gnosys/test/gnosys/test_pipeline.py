# Copyright (C) 2026 Leonardo Rossetti
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
from unittest.mock import MagicMock, patch

import pytest

from gnosys import config, pipeline
from gnosys.errors import GnosysError


def test_load_step_ok():
    provider = config.Provider('foo.bar:foobar')
    mock_load = MagicMock(return_value=lambda data, **opts: data)

    with patch('gnosys.pipeline.load_step', side_effect=mock_load):
        step = pipeline.load_step(provider)

    assert 'data' == step('data')
    mock_load.assert_called_once_with(provider)


def test_run_pipeline_ok():
    mock_fn1 = MagicMock(side_effect=lambda data, **opts: f'{data}_fn1')
    mock_fn2 = MagicMock(side_effect=lambda data, **opts: f'{data}_fn2')
    mock_fn3 = MagicMock(side_effect=lambda data, **opts: f'{data}_fn3')

    with patch('gnosys.pipeline.load_step', side_effect=[mock_fn1, mock_fn2, mock_fn3]):
        p = config.Pipeline(steps=[
            MagicMock(options={}),
            MagicMock(options={}),
            MagicMock(options={})
        ])
        results = list(pipeline.run(p, 'fn0'))
    
    assert results == ["fn0_fn1", "fn0_fn1_fn2", "fn0_fn1_fn2_fn3"]
    mock_fn1.assert_called_once_with("fn0")
    mock_fn2.assert_called_once_with("fn0_fn1")
    mock_fn3.assert_called_once_with("fn0_fn1_fn2")


def test_run_pipeline_error_no_steps():
    p = config.Pipeline(steps=[])

    with pytest.raises(GnosysError) as e:
        next(pipeline.run(p, 'somedata'))

    assert '[1] Pipeline has no steps to run.' == str(e.value)
