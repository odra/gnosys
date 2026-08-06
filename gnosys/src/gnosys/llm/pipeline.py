# SPDX-License-Identifier: AGPL-3.0-only
# llm pipeline
# Copyright (C) 2026 Leonardo Rossetti

from typing import Any, cast, Dict, Generator, List, Optional, Set, Tuple, TypeVar

import torch
from torch.utils.data import Dataset, DataLoader

from . import fetch_datasources, encode_data, create_data_loader, create_embeddings, T
from gnosys import pipeline


llm_pipeline_vars:Dict[str, Any] = {}
llm_pipeline = pipeline.Pipeline('llm_pipeline', llm_pipeline_vars)


@llm_pipeline.step()
def _fetch_datasources(sources: List[str]) -> List[str]:
    source_mark:str = llm_pipeline.ctx['source_mark']

    data = []
    for source, content in fetch_datasources(sources, source_mark):
        if source:
            print(f'Loading source: {source}')
        data.append(content)
        if source:
            print('Loaded')

    return data


@llm_pipeline.step()
def encode_datasources(data: List[str]) -> List[int]:
    print('Initializing tokenization process...')
    encoding_model = llm_pipeline.ctx['encoding_model']
    extras = {llm_pipeline.ctx['source_mark']}
    
    tokens = encode_data(encoding_model, data, extras)
    print(f'Total Tokens: {len(tokens)}')

    return tokens


@llm_pipeline.step()
def create_torch_dataloader(token_ids: List[int]) -> DataLoader[T]:
    max_length: int = llm_pipeline.ctx['max_length']
    stride: int = llm_pipeline.ctx['stride']
    batch_size: int = llm_pipeline.ctx['batch_size']
    shuffle: bool = llm_pipeline.ctx.get('shuffle', False)
    drop_last: bool = llm_pipeline.ctx.get('drop_last', True)
    num_workers: int = llm_pipeline.ctx.get('num_workers', 0)

    print('Sampling Data...')

    return create_data_loader(token_ids, max_length,
                              stride,batch_size,
                              shuffle, drop_last,
                              num_workers)

@llm_pipeline.step()
def add_embeddings_to_dataloader(dataloader: Optional[DataLoader[T]]) -> torch.Tensor:
    max_length = llm_pipeline.ctx['max_length']
    output_dim = llm_pipeline.ctx['output_dim']
    vocab_size = llm_pipeline.ctx['vocab_size']

    print('Applying Embedding Layer...') 

    token_embeddings = create_embeddings(vocab_size, output_dim, data_loader=dataloader)
    print(f'Token Embeddings Shape: {token_embeddings.shape}')  

    pos_embeddings = create_embeddings(max_length, output_dim)
    print(f'Pos Embeddings Shape: {pos_embeddings.shape}')

    input_embeddings = token_embeddings + pos_embeddings
    print(f'Input Embeddings Shape: {input_embeddings.shape}')
    
    return input_embeddings
