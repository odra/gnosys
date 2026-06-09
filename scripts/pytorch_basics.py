#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# pytorch random script
# Copyright (C) 2026 Leonardo Rossetti
import torch
import tiktoken


def is_cuda_available():
    """checks if cuda is available"""
    return torch.cuda.is_available()


def create_tokenizer(model='gpt2'):
    return tiktoken.get_encoding(model)


def create_sliding_window(data, tokenizer, max_length=4, stride=1):
    input_ids = []
    target_ids = []
    encoded_data = tokenizer.encode(data)
     
    for i in range(0, len(encoded_data) - max_length, stride):
        input_ids_row = torch.tensor(encoded_data[i:i + max_length])
        target_ids_row = torch.tensor(encoded_data[i+1:i + max_length + 1])

        input_ids.append(input_ids_row)
        target_ids.append(target_ids_row)

    return (encoded_data, input_ids, target_ids)


def test_embedding_layer():
    input_ids = torch.tensor([2, 3, 5, 1])
    vocab_size = 6
    output_dim = 3
 
    torch.manual_seed(123)
    embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
    embeddings = embedding_layer(input_ids)

    # lookup action to get the corresponding embedding token id from the embedding layer
    # these are called "absolute positional embeddings"
    assert torch.equal(embeddings[0], embedding_layer.weight[2])
    assert torch.equal(embeddings[1], embedding_layer.weight[3])
    assert torch.equal(embeddings[2], embedding_layer.weight[5])
    assert torch.equal(embeddings[3], embedding_layer.weight[1])
    

if __name__ == '__main__':
    print(f'Cuda: {is_cuda_available()}')
    print()

    tokenizer = create_tokenizer()
    raw, x, y = create_sliding_window('Today is a sunny day.', tokenizer)
    print(raw)
    print(x)
    print(y)
    print()

    test_embedding_layer()
