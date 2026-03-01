# Copyright (C) 2026 Leonardo Rossetti
# SPDX-License-Identifier: AGPL-3.0-only
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from collections.abc import Callable
from contextlib import AbstractContextManager
from typing import Any, Iterator, Literal, List, Optional, Protocol

from . import errors
from . import provider
from .config import ConfigOptionValues, Pipeline, Provider


class PipelineStep(Protocol):
    """
    A protocol is used to define a pipeline step since typing.Callable is not enough.

    A pipeline step defines a callable that will be invoked as a pipeline step,
    the first argument being the output of the previous step and **kwargs
    which contains whatever data is defined under the `options` key from a
    pipeline step provider.

    The returned value will be used as input for the next step or as the
    end result of the pipeline if said step is the last one.
    """
    def __call__(self, step_input: Any, **kwargs: ConfigOptionValues) -> Any:
        pass


def run(pipeline: Pipeline, data: Any) -> Iterator[Any]:
    """
    Run a pipeline, by iterating on each step. The provider of
    each step is loaded on demand and the output of the curent step is used
    as input for the next one, yielding each result in the process until
    the end.

    A parameter named "genesis_data" is used as input for the
    first interacton. Steps' options are passed as kwargs.

    Raises an error if steps has no items.
    """
    if len(pipeline.steps) == 0:
        raise errors.GnosysError('Pipeline has no steps to run.')
    
    step_res = data
    for step in pipeline.steps:
        step_fn = load_step(step)
        opts = step.options or dict()
        step_res = step_fn(step_res, **opts)
        yield step_res


def load_step(step_provider: Provider) -> PipelineStep:
    """
    Load a step from a provider defintion.

    A step is a callable object as defined in PipelineStep.
    """
    provider_pkg, provider_obj = provider.parse(step_provider.provider) 
    pipeline_step: PipelineStep = provider.load(provider_pkg, provider_obj)

    return pipeline_step
