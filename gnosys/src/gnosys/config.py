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
from dataclasses import dataclass, field
from typing import Any, Dict, List

import yaml

from . import errors


@dataclass(frozen=True)
class ConfigDataSource:
    """Config datasource, requires an URI and a provider"""
    uri: str
    provider: str


@dataclass(frozen=True)
class ConfigDataSources:
    """
    Data source config, to be parsed from the "data" user config defintion.
    """
    sources: List[ConfigDataSource]


@dataclass(frozen=True)
class ConfigData:
    """
    Data class to hold configuration data/input.
    """
    data: ConfigDataSources


class Config():
    """
    Class to load and parse user defined configuration into a ConfigData object.
    """
    data: ConfigData

    def __init__(self, cfg: Dict[str, Any]) -> None:
        """
        Initializes a Config objects and sets a ConfigData object based on a "data" dict.
        """
        data_obj = cfg['data']

        self.data = ConfigData(
            data=ConfigDataSources(
                sources=[ConfigDataSource(s['uri'], s['provider']) for s in data_obj['sources']]
            )
        )

    @classmethod
    def from_path(cls, path: pathlib.Path) -> 'Config':
        """
        Loads config text data from a file (yaml or json) and creates a new instance. 
        """
        try:
            with path.open('r') as f:
                data = yaml.safe_load(f)
        except OSError as e:
            _errmsg = e.strerror or f'Fail to read config at {path}'
            _errcode = e.errno or 1
            raise errors.GnosysError(_errmsg, errcode=_errcode)

        if not 'gnosys' in data:
            raise errors.GnosysError('"gnosys" key not found in gnosys.yml')
        
        return cls(data['gnosys'])

    def __eq__(self, other: Any) -> bool:
        """
        Compare two Config objects by comparing their internal `data` properties.
        """
        if not isinstance(other, Config):
            raise NotImplementedError
        return self.data == other.data
