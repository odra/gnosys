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
from typing import List, Protocol, TypeVar
from dataclasses import dataclass


EncodeT = TypeVar('EncodeT')
DecodeT = TypeVar('DecodeT')


@dataclass(frozen=True)
class Tokenizer(Protocol[EncodeT, DecodeT]):
    """
    Tokenizer protocol to be implemented by implementations.
    """

    def encode(self, data: EncodeT) -> List[DecodeT]:
        """
        Encode input data EncodeT into a list of  DecodeT.

        Typical example: encode a str (natural language text) into tensors.
        """
        pass

    def decode(self, data: List[DecodeT]) -> EncodeT:
        """
        Decode encoded data DecodeT back into EncodeT.
        """
        pass
