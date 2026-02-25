from enum import Enum
from contextlib import contextmanager
from typing import Any, Generator, Iterator, Protocol, TypeVar

from .source import DataSource


SourceT = TypeVar('SourceT')

DataT = TypeVar('DataT')

class DataPipelineStep(Enum):
    """
    Enum to be used when yielding internal methods (or steps).

    Not much for now, just something to verify the type for.
    """
    NEXT = 0


class DataPipeline(Protocol[SourceT, DataT]):
    """
    A pipeline class that transforms data from a given source SourceT into parsed data DataT.

    It has a `inject` method which serves the purpose of injecting datasources to be used during the
    transformation process and a `__call__` method which runs the pipeline.

    The class uses generics to define types it transforms data from and to something else. A good
    example would be an implementation that transforms string text into pytorch sensors.

    The __call__ method expects a generator, so each pipeline "step" can be yieled, until
    the final result can be returned.


    Pseudo LLM implementation:

    
    .. code-block:: python

      class LLMDataPipeline:

        vocab: Dict[str, int]

        def inject(self, *args: SourceT) -> Iterator['LLMDataPipeline[str, pytorch.Tensor]']:
          for ds in args:
            with ds.load() as raw_data:
               ...

        def __call__(self, data: str) -> Iterator[DataPipelineStep | DataT]:
          yield self.build_vocab() # return DataPipelineStep::NEXT
          yield self.tokenize(vocab) # return DataPipelineStep::NEXT
          yield self.to_tensors(tokens, data) # return something that is DataT (loop stops)
    """

    @contextmanager
    def inject(self, *args: SourceT) -> Iterator['DataPipeline[SourceT, DataT]']:
        """
        This method will be used to inject "train data" before transforming the data.

        Example: an LLM embedder would use some text to build a vocabulary.
        """
        pass

    def __call__(self, data: SourceT) -> Iterator[DataPipelineStep | DataT]:
        """
        Run the pipeline. Implementations are encouraged to split their
        pipelines into tasks (instance methods) and yield those until the
        final result is achieved and be returned.
        """
        pass
