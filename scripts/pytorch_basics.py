#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# pytorch random script
# Copyright (C) 2026 Leonardo Rossetti
import torch


def is_cuda_available():
    return torch.cuda.is_available()


if __name__ == '__main__':
    print(f'Cuda: {is_cuda_available()}')
