# Copyright (C) 2026 Leonardo Rossetti
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
import importlib.util
from typing import Any, Tuple, TypeVar

T = TypeVar('T')


def parse(path: str) -> Tuple[str, str]:
    """
    Parses a path such as `a.b.c:obj`.

    `obj` can be a class or function to to be used or called as provider.
    """
    parts = path.split(':')

    assert len(parts) == 2

    return parts[0], parts[1]


def load(pkg_path: str, obj_name: str) -> Any:
    """
    Loads object_name from pkg_path using importlib.

    typical example:

    obj: SomeType = load('a.b.c', 'D') 
    """
    if pkg_path in sys.modules:
        return getattr(sys.modules[pkg_path], obj_name)

    spec = importlib.util.find_spec(pkg_path)
    assert spec
    assert spec.loader

    module = importlib.util.module_from_spec(spec)
    assert module

    sys.modules[pkg_path] = module
    spec.loader.exec_module(module)

    return getattr(module, obj_name)
