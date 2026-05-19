# SPDX-License-Identifier: AGPL-3.0-only
# gnosys cli module
# Copyright (C) 2026 Leonardo Rossetti

from typing import List

import click

from . import __version__ as gnosys_version
from . import datasource


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
def pretrain(sources: List[str], source_mark: str) -> None:
    """pretrain stage"""
    data = []
    for idx, source in enumerate(sources):
        if idx > 0:
            data.append(source_mark)
        click.echo(f'Loading source: {source}')
        data.append(datasource.read(source))
        click.echo(f'Loaded')


def run() -> None:
    """run the click application"""
    cli()
