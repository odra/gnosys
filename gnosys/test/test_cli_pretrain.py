# SPDX-License-Identifier: AGPL-3.0-only
# gnosys.cli:pretrain tests
# Copyright (C) 2026 Leonardo Rossetti

from unittest.mock import MagicMock, patch

from gnosys.cli import cli


def test_pretrain_err(cli_runner):
    res = cli_runner.invoke(cli, ['pretrain']) 

    assert 2 == res.exit_code
    assert 'Missing option \'--source\'' in res.output


def test_pretrain_ok(cli_runner):
    ds_read_mock = MagicMock(return_value='foobar')

    with patch('gnosys.cli.datasource.read', ds_read_mock):
        res = cli_runner.invoke(cli, ['pretrain', '--source', 'file:///data.txt'])

    ds_read_mock.assert_called_with('file:///data.txt')
    assert 0 == res.exit_code
    assert '\n'.join([
        'Loading source: file:///data.txt',
        'Loaded',
        ''
    ]) == res.output
