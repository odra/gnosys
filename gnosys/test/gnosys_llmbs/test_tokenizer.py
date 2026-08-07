# SPDX-License-Identifier: AGPL-3.0-only
# gnosys.tokenizer tests
# Copyright (C) 2026 Leonardo Rossetti

from gnosys_llmbs.tokenizer import Tokenizer


def test_simple_ok():
    text = 'foo bar'
    t = Tokenizer('gpt2')
    encoded = t.encode(text)

    assert [21943, 2318] == encoded
    assert text == t.decode(encoded)


def test_extras_ok():
    text = 'foo bar <|endoftext|> bar foo'
    t = Tokenizer('gpt2')
    encoded = t.encode(text, extras={'<|endoftext|>'})

    assert [21943, 2318, 220, 50256, 2318, 22944] == encoded
    assert text == t.decode(encoded)
