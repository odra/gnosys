# SPDX-License-Identifier: AGPL-3.0-only
# module to handle raw data loading
# Copyright (C) 2026 Leonardo Rossetti

def read_from_file(path: str) -> str:
    """Load data from file"""
    with open(path, 'r') as f:
        return f.read()


def read(uri: str) -> str:
    """
    Read data source from a uri.
    Supported schemes:
    
    - file://
    """
    if uri.startswith('file://'):
        return read_from_file(uri.split('://')[1])

    raise NotImplementedError(f'Data source not supported: {uri}')
