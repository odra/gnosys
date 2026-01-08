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
import sys
import pathlib

import click

from . import __version__ as gnosys_version
from . import data, errors, provider
from .data.source import DataSource
from .config import Config


def msg(msg: str, kind: str = 'info') -> str:
    """
    Create a formatted string for the CLI's output.

    Using the log module is probably a better solution to this.
    """
    return f'[gnosys.{kind}] {msg}'


@click.group
def cli() -> None:
    """
    gnosys is something.
    """


@cli.command
def version() -> None:
    """
    Show program version
    """
    click.echo(f'v{gnosys_version}')


@cli.command
def build() -> None:
    """
    Build a model using a gnosys.yml file in the current directory.
    """
    cfg_path = pathlib.Path('gnosys.yml')
    config = Config.from_path(cfg_path)
    cfg = config.data

    click.echo(msg('Loading data sources'))
    for source in cfg.data.sources:
        click.echo(msg(f'Loading source: {source}'))
        # parse provider pkg name and class
        ds_provider_pkg, ds_provider_obj = provider.parse(source.provider)
        # import provider using importlib
        DataSourceCls: DataSource = provider.load(ds_provider_pkg, ds_provider_obj)
        # create new data source provider instance from uri
        datasource = DataSourceCls.from_uri(source.uri)
        # load and assert content
        content = data.load_source(datasource)
        assert content


def run() -> None:
    """
    Run the gnosys CLI application.
    """
    try:
        cli()
    except errors.GnosysError as err:
        print(str(err), file=sys.stderr)
