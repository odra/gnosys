# SPDX-License-Identifier: AGPL-3.0-only
# gnosys cli module
# Copyright (C) 2026 Leonardo Rossetti

from typing import Any, List

import click
import torch

from . import __version__ as gnosys_version
from . import datasource, tokenizer
from . import data as datalib


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
    for idx, source in enumerate(sources):
        if idx > 0:
            data.append(source_mark)
        click.echo(f'Loading source: {source}')
        data.append(datasource.read(source))
        click.echo(f'Loaded')

    # tokenize data
    click.echo('Initializing tokenization process...')
    t = tokenizer.Tokenizer(encoding_model)
    tokens = t.encode(''.join(data), extras={source_mark})
    click.echo(f'Total Tokens: {len(tokens)}')

    # create and load dataset
    click.echo('Sampling Data...')
    ds: Any  = datalib.create_dataset(tokens, max_length=max_length, stride=stride) #TODO: fix typing
    dl: Any  = datalib.create_data_loader(ds, batch_size=batch_size) #TODO: fix typing
    dl_iter = iter(dl)

    # create token embedding layer
    click.echo('Applying Embedding Layer...')
    inputs, targets = next(dl_iter)
    click.echo(f'Inputs shape: {inputs.shape}')
    token_embeddings = datalib.create_embeddings(inputs, vocab_size, output_dim)
    click.echo(f'Token Embeddings Shape: {token_embeddings.shape}')

    # create gpt absolute embedding layer
    pos_embeddings = datalib.create_embeddings(torch.arange(max_length), max_length, output_dim)
    click.echo(f'Pos Embeddings Shape: {pos_embeddings.shape}')

    # input embeddings
    input_embeddings = token_embeddings + pos_embeddings
    click.echo(f'Input Embeddings Shape: {input_embeddings.shape}')


def run() -> None:
    """run the click application"""
    cli()
