# SPDX-License-Identifier: AGPL-3.0-only
# gnosys.cli:build_llm tests
# Copyright (C) 2026 Leonardo Rossetti

import logging
from unittest.mock import MagicMock, patch

from gnosys_llmbs.cli import cli


def test_build_llm_err(cli_runner):
    res = cli_runner.invoke(cli, ['build-llm']) 

    assert 2 == res.exit_code
    assert 'Missing option \'--source\'' in res.output


def test_build_llm_ok(cli_runner, fixdir, caplog):
    caplog.set_level(logging.INFO)
    
    res = cli_runner.invoke(cli, ['build-llm', '--source', f'file://{fixdir}/the_verdict.txt'])

    assert 0 == res.exit_code
    assert [
    'Pipeline<llm_pipeline>.PipelineStep<gnosys_llmbs.llm.pipeline:_fetch_datasources>.start',
    f'Loading source: file://{fixdir}/the_verdict.txt',
    'Loaded',
    'Pipeline<llm_pipeline>.PipelineStep<gnosys_llmbs.llm.pipeline:_fetch_datasources>.done',
    'Pipeline<llm_pipeline>.PipelineStep<gnosys_llmbs.llm.pipeline:encode_datasources>.start',
    'Initializing tokenization process...',
    'Total Tokens: 5146',
    'Pipeline<llm_pipeline>.PipelineStep<gnosys_llmbs.llm.pipeline:encode_datasources>.done',
    'Pipeline<llm_pipeline>.PipelineStep<gnosys_llmbs.llm.pipeline:create_torch_dataloader>.start',
    'Creating Pytorch GPT Dataloader...',
    'Pipeline<llm_pipeline>.PipelineStep<gnosys_llmbs.llm.pipeline:create_torch_dataloader>.done',
    'Pipeline<llm_pipeline>.PipelineStep<gnosys_llmbs.llm.pipeline:add_embeddings_to_dataloader>.start',
    'Applying Embedding Layer...',
    'Token Embeddings Shape: torch.Size([4, 256, 256])',
    'Pos Embeddings Shape: torch.Size([256, 256])',
    'Input Embeddings Shape: torch.Size([4, 256, 256])',
    'Pipeline<llm_pipeline>.PipelineStep<gnosys_llmbs.llm.pipeline:add_embeddings_to_dataloader>.done',
    ] == [r.message for r in caplog.records]
