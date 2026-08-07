# SPDX-License-Identifier: AGPL-3.0-only
# gnosys:pipeline.py tests
# Copyright (C) 2026 Leonardo Rossetti

import inspect

import pytest

from gnosys import pipeline


@pytest.mark.parametrize('status,is_running,is_done,is_ok,is_error', [
    (pipeline.PipelineStepStatus.VOID, False, False, False, False),
    (pipeline.PipelineStepStatus.RUNNING, True, False, False, False),
    (pipeline.PipelineStepStatus.SUCCESS, False, True, True, False),
    (pipeline.PipelineStepStatus.FAILURE, False, True, False, True)
])
def test_pipeline_status(status, is_running, is_done, is_ok, is_error):
    assert is_running is status.is_running()
    assert is_done is status.is_done()
    assert is_ok is status.is_ok()
    assert is_error is status.is_error()


@pytest.mark.parametrize('fn,fn_name,fn_args,fn_kwargs,fn_res', [
    (lambda n: n + n, None, [2], {}, 4),
    (lambda n: n + n, 'lambda_sum', [2], {}, 4),
    (sum, None, [[2, 3]], {}, 5)
])
def test_pipeline_task(fn, fn_name, fn_args, fn_kwargs, fn_res):
    task = pipeline.PipelineTask(fn, custom_name=fn_name)

    if fn_name is None:
        fn_module = inspect.getmodule(fn)
        fn_name = f'{fn_module.__name__}:{fn.__name__}'

    assert fn_name == str(task)
    assert fn_res == task.exec(*fn_args, **fn_kwargs)
    assert fn_res == task(*fn_args, **fn_kwargs)


def test_pipeline_simple_ok():
    p = pipeline.Pipeline('test_pipeline')
    assert len(p) == 0

    p.register_step(lambda n: n + n, name='lambda_sum')
    assert len(p) == 1

    @p.step()
    def sub(n):
        return n - 1
    assert len(p) == 2

    r = None
    for step in p.run(2):
        r = step.result
    assert 3 == r
    assert 2 == len([True for s in p.steps.values() if s.status.is_ok()])


def test_pipeline_ctx_ok():
    p = pipeline.Pipeline('test_pipeline', {'n': 5})
    assert len(p) == 0

    p.register_step(lambda n: n + n, name='lambda_sum')
    assert len(p) == 1

    @p.step()
    def sub(n):
        return n - 1 + p.ctx['n']
    assert len(p) == 2

    r = None
    for step in p.run(2):
        r = step.result
    assert 8 == r
    assert 2 == len([True for s in p.steps.values() if s.status.is_ok()])
    assert None is p.ctx
