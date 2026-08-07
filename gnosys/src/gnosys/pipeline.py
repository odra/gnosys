# SPDX-License-Identifier: AGPL-3.0-only
# gnosys pipeline API
# Copyright (C) 2026 Leonardo Rossetti

import enum
import inspect
from dataclasses import dataclass
from collections import OrderedDict
from collections.abc import Mapping
from contextlib import contextmanager
from typing import Any, Callable, Dict, Generic, Generator, Iterator, Optional, ParamSpec, TypeVar

from .context import ctx


class PipelineStepStatus(enum.Enum):
    """
    Enum to represent a step state.

    Some convenience methods are provided to easy interaction.
    """
    VOID = 0
    RUNNING = 1
    SUCCESS = 2
    FAILURE = 3
    
    def is_running(self) -> bool:
        """Return true if the task is being executed"""
        return self.value == 1

    def is_done(self) -> bool:
        """Return true if the task finished its execution"""
        return self.value > 1

    def is_ok(self) -> bool:
        """True if the task finished with success"""
        return self.value == 2

    def is_error(self) -> bool:
        """True if an exception was raised during its execution"""
        return self.value == 3


class PipelineTask:
    """
    A class that holds task metadata info (name, etc) and a reference
    to the actual function to be executed.
    """
    name: str

    def __init__(self, fn: Callable[..., Any], custom_name: Optional[str] = None) -> None:
        """
        Create a new object instance to be used in pipelines as a step task.

        A `custom_name` can be provided, it will use the full package
        and function name by default (i.e mod1.mod2.mod3:fn).
        Keep in mind that names must be unique within a pipeline.
        """
        if custom_name is None:
            fn_module = inspect.getmodule(fn)
            assert fn_module
            self.name = f'{fn_module.__name__}:{fn.__name__}'
        else:
            self.name = custom_name
        self.fn = fn

    def exec(self, *args: Any, **kwargs: Any) -> Any:
        """Execute function"""
        return self.fn(*args, **kwargs)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Make the object callable.Uses `self.exec`."""
        return self.exec(*args, **kwargs)

    def __str__(self) -> str:
        """Return the function name"""
        return self.name


@dataclass
class PipelineStep:
    """
    Pipeline step dataclass.

    It Stores a task object to be called, the result status and the result itself.

    The result will hold the actual task (function) result or an exception.
    """
    task: PipelineTask
    status: PipelineStepStatus
    result: Any


class Pipeline:
    """
    A pipeline class that will run N tasks.
    
    Tasks are just plai python functions which are
    registered using the `self.task` as a decorator
    or `self.register_task` to an actual function.

    Tasks are executed by invoking `self.run` or
    using a Pipeline instance as a callee,
    `self.__call__`is just a wrapper of `self._run`.

    The pipeline runs each registered task sequentially through
    generators until the last function is executed.

    The returned value of a given task or function is passed as
    input to the next task in the pipeline queue. The first
    task or function uses whataver was passed to `self.run` as
    its input.
    """

    name: str
    steps: Dict[str, PipelineStep]
    data: Mapping[str, Any] | None

    def __init__(self, name: str, data: Mapping[str, Any] | None = None) -> None:
        """Create a new Pipeline instance"""

        self.name = name
        self.steps = OrderedDict()
        self.data = data

    @property
    def ctx(self) -> Any:
        """
        Return context object. To be used in steps.
        """

        return ctx.get()

    @contextmanager
    def inputs(self, data: Mapping[str, Any]) -> Iterator[Pipeline]:
        """
        Context manager to use a Pipeline instance with different inputs (self.data).
        """

        old_data = self.data
        self.data = data

        try:
            yield self
        finally:
            self.data = old_data
       
    def register_step(self, fn: Callable[..., Any], name: Optional[str] = None) -> None:
        """Adds a task  as pipeline step"""

        task = PipelineTask(fn, custom_name=name)
        self.steps[str(task)] = PipelineStep(task, PipelineStepStatus.VOID, None)

    def step(self, name: str | None = None) -> Callable[..., Any]:
        """Decorator to add a function as a pipeline step"""

        def decorator(fn: Callable[..., Any], name: str | None = name) -> Callable[..., Any]:
            self.register_step(fn, name=name)
            return fn
        return decorator

    def run(self, *args: Any, **kwargs: Any) -> Generator[PipelineStep]:
        """Run the pipeline via a generator. Each interaction return an executed step."""

        result = None
        token = ctx.set(self.data)

        for idx, step_name in enumerate(self.steps):
            try:
                self.steps[step_name].status = PipelineStepStatus.RUNNING

                if idx == 0:
                    result = self.steps[step_name].task(*args, **kwargs)
                else:
                    result = self.steps[step_name].task(result)
            except Exception as e:
                self.steps[step_name].status = PipelineStepStatus.FAILURE
                self.steps[step_name].result = e
                raise e

            self.steps[step_name].status = PipelineStepStatus.SUCCESS
            self.steps[step_name].result = result
    
            yield self.steps[step_name]

        ctx.reset(token)

    def __call__(self, *args: Any, **kwargs: Any) -> Generator[PipelineStep]:
        """Wrapper of `self.run`"""

        return self.run(*args, **kwargs)

    def __len__(self) -> int:
        """Return the length of `self.steps`"""

        return len(self.steps)
