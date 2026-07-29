# SPDX-License-Identifier: AGPL-3.0-only
# llm module
# Copyright (C) 2026 Leonardo Rossetti

from typing import cast, Generator, List, Optional, Set, Tuple, TypeVar

import torch
from torch.utils.data import Dataset, DataLoader

from gnosys import datasource, tokenizer
from gnosys.data.dataset import GptDataset


T = TypeVar('T')


def fetch_datasources(sources: List[str], source_mark: str) -> Generator[Tuple[str, str]]:
    """Load/Fetch raw datasources"""

    for idx, source in enumerate(sources):
        if idx > 0:
            yield ('', source_mark)

        yield (source, datasource.read(source))


def encode_data(encoding_model: str, data: List[str], extras: Optional[Set[str]] = None) -> List[int]:
    """Encode data into tokens"""

    backend = tokenizer.Tokenizer(encoding_model)
    
    return backend.encode(''.join(data), extras=extras)


def create_data_loader(token_ids: List[int], max_length: int = 4, stride: int = 256,
                       batch_size: int = 256, shuffle: bool = False,
                       drop_last: bool = True, num_workers: int = 0) -> DataLoader[T]:
    """
    Create a pytorch DataLodader from a dataset.
    Both Dataset and DataLoader must be use the same generic type.
    """

    dataset = GptDataset(token_ids, max_length, stride) 

    return DataLoader(cast(Dataset[T], dataset),
                      batch_size=batch_size,
                      shuffle=shuffle,
                      drop_last=drop_last,
                      num_workers=num_workers)


def create_embeddings(max_length: int, output_dim: int, data_loader: Optional[DataLoader[T]] = None) -> torch.Tensor:
    layer = torch.nn.Embedding(max_length, output_dim)

    if data_loader is None:
        return cast(torch.Tensor, layer(torch.arange(max_length)))

    dl_iter = iter(data_loader)
    input_tokens, target_tokens =  next(dl_iter)

    return cast(torch.Tensor, layer(input_tokens))
