# SPDX-License-Identifier: AGPL-3.0-only
# data module
# Copyright (C) 2026 Leonardo Rossetti

from typing import cast, List, TypeVar

import torch
from torch.utils.data import Dataset, DataLoader

from .dataset import GptDataset, TensorTuple


T = TypeVar('T')


def create_dataset(token_ids: List[int], max_length: int = 4, stride: int = 256) -> Dataset[T]:
    """
    Create a new Dataset from a list of token ids.
    """

    dataset = GptDataset(token_ids, max_length, stride)

    return cast(Dataset[T], dataset)
    

def create_data_loader(dataset: Dataset[T],
                       batch_size: int = 256, shuffle: bool = False,
                       drop_last: bool = True, num_workers: int = 0) -> DataLoader[T]:
    """
    Create a pytorch DataLodader from a dataset.
    Both Dataset and DataLoader must be use the same generic type.
    """

    return DataLoader(dataset,
                      batch_size=batch_size,
                      shuffle=shuffle,
                      drop_last=drop_last,
                      num_workers=num_workers)


def create_embedding_layer(length: int, dim: int) -> torch.nn.modules.sparse.Embedding:
    """create an embedding layer"""

    return torch.nn.Embedding(length, dim)


def create_embeddings(data: torch.Tensor, length: int, dim: int) -> torch.Tensor:
    """create embeddings"""

    layer = create_embedding_layer(length, dim)
    
    return cast(torch.Tensor, layer(data))
