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
class GnosysError(Exception):
    """
    Base exception class for the gnosys project.

    It can be raised directly or inheried
    by other specialized error classes.
    """
    errmsg: str
    errcode: int

    def __init__(self, errmsg: str, errcode: int = 1) -> None:
        """
        Create a new error instance, with a message and code.
        
        Error code is optional and defaults to 1.
        """
        super().__init__(errmsg)

        self.errmsg = errmsg
        self.errcode = errcode

    def __str__(self) -> str:
        """User friendly represenation of the error"""
        return f'[{self.errcode}] {self.errmsg}'
