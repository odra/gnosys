# SPDX-License-Identifier: AGPL-3.0-only
# gnosys cli module
# Copyright (C) 2026 Leonardo Rossetti

from typing import Any, List

import click
import torch

from . import __version__ as gnosys_version
from . import datasource, tokenizer
from . import data as datalib
from . import llm

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
    """build llm stage"""
    # show variables
    click.echo(f'Inputs')
    click.echo(f'\tSource Mark: {source_mark}')
    click.echo(f'\tEncoding: {encoding_model}')
    click.echo(f'\tMax Length: {max_length}')
    click.echo(f'\tStride: {stride}')
    click.echo(f'\tBatch Size: {batch_size}')

    # fetch data sources
    data = []
    for source, content in llm.fetch_datasources(sources, source_mark):
        if source:
            click.echo(f'Loading source: {source}')
        data.append(content)
        if source:
            click.echo(f'Loaded')
 
    # tokenize data
    click.echo('Initializing tokenization process...')
    tokens = llm.encode_data(encoding_model, data, extras={source_mark})
    click.echo(f'Total Tokens: {len(tokens)}')

    # create and load dataset
    click.echo('Sampling Data...')
    dl: Any = llm.create_data_loader(tokens, max_length=max_length, stride=stride, batch_size=batch_size)

    # create token embedding layer
    click.echo('Applying Embedding Layer...')
    inputs, targets = next(iter(dl))
    click.echo(f'Inputs shape: {inputs.shape}')

    token_embeddings = llm.create_embeddings(vocab_size, output_dim, data_loader=dl)
    click.echo(f'Token Embeddings Shape: {token_embeddings.shape}')

    # create gpt absolute embedding layer
    pos_embeddings = llm.create_embeddings(max_length, output_dim)
    click.echo(f'Pos Embeddings Shape: {pos_embeddings.shape}')

    # input embeddings
    input_embeddings = token_embeddings + pos_embeddings
    click.echo(f'Input Embeddings Shape: {input_embeddings.shape}')


def run() -> None:
    """run the click application"""
    cli()
