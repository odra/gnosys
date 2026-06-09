# SPDX-License-Identifier: AGPL-3.0-only
# module to handle pytorch datasets
# Copyright (C) 2026 Leonardo Rossetti

from typing import List, Tuple, TypeVar

import torch
from torch.utils.data import Dataset


TensorTuple = Tuple[torch.Tensor, torch.Tensor]

class GptDataset(Dataset[TensorTuple]):

    input_ids: List[torch.Tensor]
    target_ids: List[torch.Tensor]

    def __init__(self, token_ids: List[int], max_length: int, stride: int) -> None:
        """
        Create a new object instance, taking a list of token_ids (tokenized text) as input.

        It then proceeds to create input an target ids lists from this list (aka sliding window),
        with each list item being a torch.Tensor.
        """
        super()

        self.input_ids = []
        self.target_ids = []

        for i in range(0, len(token_ids) - max_length, stride):
            _input_ids = torch.tensor(token_ids[i:i+max_length])
            _target_ids = torch.tensor(token_ids[i+1:i + max_length + 1])

            self.input_ids.append(_input_ids)
            self.target_ids.append(_target_ids)

    def __len__(self) -> int:
        """Return dataset length"""
        return len(self.input_ids)

    def __getitem__(self, idx: int) -> TensorTuple:
        """
        Retrieve a dataset item both input_id and
        target_id as a tuple.
        """
        return (self.input_ids[idx], self.target_ids[idx])
