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

import pytest

from gnosys.config import Config


def test_load_yaml_ok(fixdir, cfg):
    c = Config.from_path(pathlib.Path(f'{fixdir}/config.yml'))

    assert Config(cfg) == c


def test_load_yaml_error_filepath(fixdir):
    with pytest.raises(FileNotFoundError):
        Config.from_path(pathlib.Path(f'{fixdir}/config.ym'))


def test_load_yaml_error_format(fixdir):
    with pytest.raises(AssertionError):
        Config.from_path(pathlib.Path(f'{fixdir}/config.invalid.yml'))
