# SPDX-License-Identifier: AGPL-3.0-only
# gnosys.cli:version
# Copyright (C) 2026 Leonardo Rossetti
from gnosys_llmbs.cli import cli


def test_version(cli_runner):
    res = cli_runner.invoke(cli, ['version'])

    assert 0 == res.exit_code
    assert 'v0.0.1\n' == res.stdout
