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
import pytest

from gnosys import errors


@pytest.mark.parametrize(
    'err,errstr',
    [
        (errors.GnosysError('foo'), '[1] foo'),
        (errors.GnosysError('bar', 2), '[2] bar'),
        (errors.GnosysError('foobar', errcode=5), '[5] foobar'),
    ]
)
def test_base_ok(err, errstr):
    assert str(err) == errstr

    with pytest.raises(err.__class__):
        raise err
