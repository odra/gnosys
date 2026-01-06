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
from contextlib import contextmanager
from typing import Iterator, Protocol

import requests


class DataSource(Protocol):
    """
    Data source protocol which define methods for actual implementations to
    load data from a given source (url, file, etc).
    """
    
    @classmethod
    def from_uri(cls, uri: str) -> 'DataSource':
        """
        Create a new instance from an URI string.

        URI contains the information neeeded for a data source implementation
        to load data content from. 
        """
        pass

    @contextmanager
    def load(self) -> Iterator[str]:
        """
        Open data for reading with a context manager object returning a string.
        """
        pass
