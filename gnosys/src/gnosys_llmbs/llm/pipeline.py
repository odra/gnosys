# SPDX-License-Identifier: AGPL-3.0-only
# llm pipeline
# Copyright (C) 2026 Leonardo Rossetti

from typing import Any, cast, Dict, Generator, List, Optional, Set, Tuple, TypeVar

import torch
from torch.utils.data import Dataset, DataLoader

from . import fetch_datasources, encode_data, create_data_loader, create_embeddings, T
from gnosys import pipeline


llm_pipeline = pipeline.Pipeline('llm_pipeline')


@llm_pipeline.step()
def _fetch_datasources() -> List[str]:
    sources = llm_pipeline.ctx['sources']
    source_mark:str = llm_pipeline.ctx['source_mark']

    data = []
    for source, content in fetch_datasources(sources, source_mark):
        if source:
            llm_pipeline.logger.info(f'Loading source: {source}')
        data.append(content)
        if source:
            llm_pipeline.logger.info('Loaded')

    return data


@llm_pipeline.step()
def encode_datasources(data: List[str]) -> List[int]:
    llm_pipeline.logger.info('Initializing tokenization process...')
    encoding_model = llm_pipeline.ctx['encoding_model']
    extras = {llm_pipeline.ctx['source_mark']}
    
    tokens = encode_data(encoding_model, data, extras)
    llm_pipeline.logger.info(f'Total Tokens: {len(tokens)}')

    return tokens


@llm_pipeline.step()
def create_torch_dataloader(token_ids: List[int]) -> DataLoader[T]:
    max_length: int = llm_pipeline.ctx['max_length']
    stride: int = llm_pipeline.ctx['stride']
    batch_size: int = llm_pipeline.ctx['batch_size']
    shuffle: bool = llm_pipeline.ctx.get('shuffle', False)
    drop_last: bool = llm_pipeline.ctx.get('drop_last', True)
    num_workers: int = llm_pipeline.ctx.get('num_workers', 0)

    llm_pipeline.logger.info('Creating Pytorch GPT Dataloader...')

    return create_data_loader(token_ids, max_length,
                              stride,batch_size,
                              shuffle, drop_last,
                              num_workers)

@llm_pipeline.step()
def add_embeddings_to_dataloader(dataloader: Optional[DataLoader[T]]) -> torch.Tensor:
    max_length = llm_pipeline.ctx['max_length']
    output_dim = llm_pipeline.ctx['output_dim']
    vocab_size = llm_pipeline.ctx['vocab_size']

    llm_pipeline.logger.info('Applying Embedding Layer...')

    token_embeddings = create_embeddings(vocab_size, output_dim, data_loader=dataloader)
    llm_pipeline.logger.info(f'Token Embeddings Shape: {token_embeddings.shape}')  

    pos_embeddings = create_embeddings(max_length, output_dim)
    llm_pipeline.logger.info(f'Pos Embeddings Shape: {pos_embeddings.shape}')

    input_embeddings = token_embeddings + pos_embeddings
    llm_pipeline.logger.info(f'Input Embeddings Shape: {input_embeddings.shape}')
    
    return input_embeddings
