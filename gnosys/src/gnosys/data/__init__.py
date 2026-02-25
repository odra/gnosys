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
from typing import Any, List, Optional

from .source import DataSource
from gnosys import errors, provider
from gnosys.config import Provider


def load_source(source: DataSource) -> str:
    """
    Load data from a data source implementation and return its content as a string.
    """
    with source.load() as data:
        return data


def build_source(source: Provider) -> DataSource:
    """
    Build a new DataSource implementation from a source Provider by
    loading and creating a new provider.

    The soruce.options dict should contain an `uri` key with the source uri.
    """
    assert source.options

    ds_provider_pkg, ds_provider_obj = provider.parse(source.provider) 
    DataSourceCls: DataSource = provider.load(ds_provider_pkg, ds_provider_obj)

    if not 'uri' in source.options:
        raise errors.GnosysError('Missing uri key from source.options')
    
    return DataSourceCls.from_uri(str(source.options['uri']))
