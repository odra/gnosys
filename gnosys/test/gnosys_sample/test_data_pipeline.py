import pytest
import torch

from gnosys.errors import GnosysError
from gnosys_sample.data import pipeline


@pytest.mark.parametrize(
    'text,expected_tokens,allowed_special',
    (
        ('sometext', [82, 908, 2302], None),
        ('text1<|endoftext|>text2', [5239, 16, 50256, 5239, 17], '<|endoftext|>')
    )
)
def test_tokenize_ok(text, expected_tokens, allowed_special):
    kw = {}
    if allowed_special:
        kw['allowed_special'] = {allowed_special}
    
    actual_tokens = pipeline.tokenize(text, **kw)

    assert expected_tokens == actual_tokens


@pytest.mark.parametrize(
    'text,errstr',
    (
        ('sometext<|endoftext|>', '[1] Encountered text corresponding to disallowed special token \'<|endoftext|>\'.'),
        (None, '[1] No text to encode')
    )
)
def test_tokenize_error(text, errstr):
    kw = {}

    with pytest.raises(GnosysError) as e:
        err = e
        pipeline.tokenize(text)

    assert errstr in str(err.value)


# @ai-marker
# ai-assisted: true
# ai-provider: Claude.ai
# ai-model-family: Claude Sonnet 4.6
# human-reviewed: true
def test_input_target_pairs(fixdir):
    with open(f'{fixdir}/the_veredict.txt', 'r') as f:
        token_ids = pipeline.tokenize(f.read())
    
    dataloader = pipeline.input_target_pairs(
        token_ids,
        batch_size=4,
        max_length=256,
        stride=128,
        shuffle=False,  # deterministic for testing
        drop_last=True,
        num_workers=0
    )
    
    batch = next(iter(dataloader))
    inputs, targets = batch
    
    assert inputs.shape == (4, 256)
    assert targets.shape == (4, 256)


# @ai-marker
# ai-assisted: true
# ai-provider: Claude.ai
# ai-model-family: Claude Sonnet 4.6
# human-reviewed: true
def test_embeddings():
    token_ids = list(range(1024))
    dataloader = pipeline.input_target_pairs(
        token_ids,
        batch_size=4,
        max_length=4,
        stride=2,
        shuffle=False,
        drop_last=True,
        num_workers=0
    )

    result = pipeline.embeddings(
        dataloader,
        seed=123,
        vocab_size=1024,
        output_dim=3,
        context_length=4
    )

    assert isinstance(result, torch.Tensor)
    assert result.shape == (4, 4, 3)
