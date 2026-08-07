# SPDX-License-Identifier: AGPL-3.0-only
# module to handle text tokenization
# Copyright (C) 2026 Leonardo Rossetti

from typing import List, Optional, Set

import tiktoken


class Tokenizer:
    """
    Tokenizer class tha uses the tiktoken library to encode text into tokens.
    """
    model: str
    backend: tiktoken.core.Encoding

    def __init__(self, model: str) -> None:
        """
        Create a new object instance to use the tiktoken library.

        Available models can be found at: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        """
        self.backend = tiktoken.get_encoding(model)

    def encode(self,  data: str, extras: Optional[Set[str]] = None) -> List[int]:
        """encode text data into a list of Tokens"""

        if not extras:
            return self.backend.encode(data)
    
        return self.backend.encode(data, allowed_special=extras)

    def decode(self, data: List[int]) -> str:
        """decode an encoded list of tokens into a string"""

        return self.backend.decode(data)
