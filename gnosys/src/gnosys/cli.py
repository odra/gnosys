# SPDX-License-Identifier: AGPL-3.0-only
# gnosys cli module
# Copyright (C) 2026 Leonardo Rossetti

from typing import Any, List
from collections import deque

import click
import torch

from . import __version__ as gnosys_version
from . import datasource, tokenizer
from . import data as datalib
from . import llm
from .llm.pipeline import llm_pipeline

@click.group
def cli() -> None:
    """gnosys"""
    pass


@cli.command
def version() -> None:
    """show program version"""
    click.echo(f'v{gnosys_version}')

@cli.command
@click.option('--source', 'sources', multiple=True, type=str, required=True, help='data source uri (can be used more than once)')
@click.option('--source-mark', type=str, default='<|endoftext|>', help='delimeter between sources raw data (default: <|endoftext|>)')
@click.option('--encoding', 'encoding_model', type=str, default='gpt2', help='openai/tiktoken encoding model to use (default: gpt2)')
@click.option('--max-length', type=int, default=256)
@click.option('--stride', type=int, default=128)
@click.option('--batch-size', type=int, default=4)
@click.option('--vocab-size', type=int, default=50527)
@click.option('--output-dim', type=int, default=256)
def build_llm(sources: List[str], source_mark: str, encoding_model: str,
              max_length: int, stride: int, batch_size: int,
              vocab_size: int, output_dim: int) -> None:
    pipeline_vars = {
        'source_mark': source_mark,
        'encoding_model': encoding_model,
        'max_length': max_length,
        'stride': stride,
        'batch_size': batch_size,
        'vocab_size': vocab_size,
        'output_dim': output_dim
    }

    click.echo(f'Inputs')
    click.echo(f'\tSource Mark: {source_mark}')
    click.echo(f'\tEncoding: {encoding_model}')
    click.echo(f'\tMax Length: {max_length}')
    click.echo(f'\tStride: {stride}')
    click.echo(f'\tBatch Size: {batch_size}')

    with llm_pipeline.inputs(pipeline_vars) as p:
        deque(p(sources), maxlen=0)


def run() -> None:
    """run the click application"""
    cli()
