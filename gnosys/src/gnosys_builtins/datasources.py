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
import pathlib
from typing import Iterator
from contextlib import contextmanager

import requests


class FileDataSource:
    """
    Data source implementation that loads data from a local file.
    """
    path: pathlib.Path

    def __init__(self, path: str) -> None:
        """
        Initialize a new object instance
        taking a mandatory path argument.
        """
        self.path = pathlib.Path(path)

    @classmethod
    def from_uri(cls, uri: str) -> 'FileDataSource':
        return cls(uri.replace('file://', ''))

    @contextmanager
    def load(self) -> Iterator[str]:
        """
        Read the file and return its content.
        """
        f = self.path.open('r')
        
        try:
            yield f.read()
        finally:
            f.close()


class HttpDataSource:
    """
    Data source implementation that loads data from a http(s) url.
    """
    url: str

    def __init__(self, url: str) -> None:
        """
        Create a new object instance, using an url as a parameter
        to be used to download the data content.
        """
        self.url = url

    @classmethod
    def from_uri(cls, uri: str) -> 'HttpDataSource':
        return cls(uri)


    @contextmanager
    def load(self) -> Iterator[str]:
        """
        Read the url over a get request and return its content.
        """
        res = requests.get(self.url)
        res.raise_for_status()

        try:
            yield res.text
        finally:
            res.close()
