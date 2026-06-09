# SPDX-License-Identifier: AGPL-3.0-only
# gnosys.cli:build_llm tests
# Copyright (C) 2026 Leonardo Rossetti

from unittest.mock import MagicMock, patch

from gnosys.cli import cli


def test_build_llm_err(cli_runner):
    res = cli_runner.invoke(cli, ['build-llm']) 

    assert 2 == res.exit_code
    assert 'Missing option \'--source\'' in res.output


def test_build_llm_ok(cli_runner, fixdir):
    res = cli_runner.invoke(cli, ['build-llm', '--source', f'file:///{fixdir}/the_verdict.txt'])

    assert 0 == res.exit_code
    assert '\n'.join([
    'Inputs',
	'\tSource Mark: <|endoftext|>',
	'\tEncoding: gpt2',
	'\tMax Length: 256',
	'\tStride: 128',
	'\tBatch Size: 4',
    f'Loading source: file:///{fixdir}/the_verdict.txt',
    'Loaded',
    'Initializing tokenization process...',
    'Total Tokens: 5146',
    'Sampling Data...',
    'Applying Embedding Layer...',
    'Inputs shape: torch.Size([4, 256])',
    'Token Embeddings Shape: torch.Size([4, 256, 256])',
    'Pos Embeddings Shape: torch.Size([256, 256])',
    'Input Embeddings Shape: torch.Size([4, 256, 256])',
    ''
    ]) == res.output
