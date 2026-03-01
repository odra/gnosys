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
from typing import AbstractSet, Any, List, Literal, Optional, Tuple

import torch
import tiktoken
from torch.utils.data import DataLoader, Dataset

from gnosys.errors import GnosysError


class SampleDataset(Dataset[Any]):
    """
    A sample dataset class that implements a pytorch Dataset.
    """
    def __init__(self, token_ids: List[int], max_length: int, stride: int) -> None:
        self.input_ids = []
        self.target_ids = []

        for i in range(0, len(token_ids) - max_length, stride):
            input_chunk = token_ids[i:i + max_length]
            target_chunk = token_ids[i + 1: i + max_length + 1]
            
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))

    def __len__(self) -> int:
        return len(self.input_ids)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.input_ids[idx], self.target_ids[idx]


def tokenize(text: str, model: str = 'gpt2', allowed_special: Literal['all'] | AbstractSet[str] = set()) -> List[int]:
    """
    Tokenize a given text using OpenAI's tiktoken library. Defaults to gpt2 if no model is provided.

    Return a list of tokens (int).
    """
    if not text:
        raise GnosysError('No text to encode')

    enc = tiktoken.get_encoding(model)

    _allowed_special = allowed_special
    if not type(_allowed_special) is str:
        _allowed_special = set(allowed_special)

    try:
        return enc.encode(text, allowed_special=_allowed_special)
    except ValueError as e:
        raise GnosysError(str(e))


def input_target_pairs(token_ids: List[int],
                       batch_size: int = 4, max_length: int = 256, stride: int = 128,
                       shuffle: bool = True, drop_last: bool = True, num_workers: int  = 0) -> DataLoader[SampleDataset]:
    """
    Create a pytorch Dataloader that uses a dataset to batch the usage of input and target ids.
    """
    dataset = SampleDataset(token_ids, max_length, stride)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, drop_last=drop_last, num_workers=num_workers)

    return dataloader


def embeddings(dataloader: DataLoader[SampleDataset], seed: int = 123, vocab_size: int = 6, output_dim: int = 3, context_length: int = 4) -> torch.Tensor:
    """
    Uses a pytorch Dataloader to create absolute positional embeddings.
    """
    data = iter(dataloader)
    inputs, targets = next(data)

    torch.manual_seed(seed)
    # token embeddings
    token_embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
    token_embeddings = token_embedding_layer(inputs)
    # absolute position embedding
    pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)
    pos_embeddings = pos_embedding_layer(torch.arange(context_length))
    # input embeddings
    input_embeddings: torch.Tensor = token_embeddings + pos_embeddings

    return input_embeddings
