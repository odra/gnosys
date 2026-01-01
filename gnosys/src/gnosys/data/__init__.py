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
from .source import DataSource, FileDataSource, HttpDataSource


def load_source(source: DataSource) -> str:
    """
    Load data from a data source implementation and return its content as a string.
    """
    with source.load() as data:
        return data


def build_source(uri: str) -> DataSource:
    """
    Build a DataSource implementation based on URI.

    Raises NotImplementedError if an invalid uri scheme is used.

    Supported schemes:

    - file://
    - http://
    - https://
    """
    if uri.startswith('file://'):
        return FileDataSource(uri.replace('file://', ''))
    elif uri.startswith('http://') or uri.startswith('https://'):
        return HttpDataSource(uri)
    else:
        raise NotImplementedError
