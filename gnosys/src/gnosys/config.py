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
from dataclasses import dataclass
from typing import Any, Dict

import yaml


@dataclass(frozen=True)
class ConfigData:
    """
    Data class to hold configuration data/input.
    """
    pass


class Config():
    """
    Class to load and parse user defined configuration into a ConfigData object.
    """
    data: ConfigData

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initializes a Config objects and sets a ConfigData object based on a "data" dict.
        """
        self.data = ConfigData()

    @classmethod
    def from_path(cls, path: pathlib.Path) -> 'Config':
        """
        Loads config text data from a file (yaml or json) and creates a new instance. 
        """
        with path.open('r') as f:
            data = yaml.safe_load(f)

        assert 'gnosys' in data
        
        return cls(data['gnosys'])

    def __eq__(self, other: Any) -> bool:
        """
        Compare two Config objects by comparing their internal `data` properties.
        """
        if not isinstance(other, Config):
            raise NotImplementedError
        return self.data == other.data
