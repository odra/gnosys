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
import logging
from unittest.mock import MagicMock, patch

from gnosys import cli


# @ai-marker
# ai-assisted: true
# ai-provider: OpenAI
# ai-model-family: GPT-5-class
# human-reviewed: true
def test_build_ok(cli_runner, monkeypatch, caplog):
    # mock config
    cfg = {
        'data': {
            'sources': [
                { 
                    'provider': 'gnosys_sample.datasources:FileDataSource',
                    'options': {
                        'uri': 'file:///data.txt'
                    }
                }
            ],
            'pipeline': {
                'steps': [
                    {
                        'provider': 'foo.bar:foobar',
                        'options': {}
                    }
                ]
            }
        }
    }
    mock_cfg_data = MagicMock()
    mock_cfg = MagicMock(return_value=cli.Config(cfg))
    monkeypatch.setattr(cli.Config, 'from_path', mock_cfg)

    # mock data source
    mock_datasource = MagicMock()
    mock_load_source = MagicMock(return_value='data')
    monkeypatch.setattr(cli.data, 'load_source', mock_load_source)

    mock_pipeline_run = MagicMock(return_value='my pipeline')
    with patch('gnosys.cli.pipeline.run', side_effect=mock_pipeline_run), caplog.at_level(logging.INFO):
        res = cli_runner.invoke(cli.cli, ['build'])

    # assert function calls
    mock_cfg.assert_called_once()
    mock_load_source.assert_called_once()

    # assert cli result and output
    assert 0 == res.exit_code
    assert [
        ('INFO', 'Loading data sources'),
        ('INFO', 'Loading source: Provider(provider=\'gnosys_sample.datasources:FileDataSource\', options={\'uri\': \'file:///data.txt\'})'),
        ('INFO', 'Running Data Pipeline')
    ] == [(r.levelname, r.message) for r in caplog.records]


def test_build_error_config(cli_runner, monkeypatch):
    # mock config
    mock_cfg = MagicMock(side_effect=FileNotFoundError)
    monkeypatch.setattr(cli.Config, 'from_path', mock_cfg)
    
    res = cli_runner.invoke(cli.cli, ['build'])

    # assert cli error result
    assert 1 == res.exit_code


def test_build_error_content(cli_runner, monkeypatch):
    # mock config
    mock_cfg_data = MagicMock()
    mock_cfg_data.data.data.sources = [
        'file:///data.txt'
    ]
    mock_cfg = MagicMock(return_value=mock_cfg_data)
    monkeypatch.setattr(cli.Config, 'from_path', mock_cfg)

    # mock data source
    mock_datasource = MagicMock()
    mock_build_source = MagicMock(return_value=mock_datasource)
    mock_load_source = MagicMock(return_value='')
    monkeypatch.setattr(cli.data, 'load_source', mock_load_source)    
    
    res = cli_runner.invoke(cli.cli, ['build'])

    assert 1 == res.exit_code

