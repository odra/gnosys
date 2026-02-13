from contextlib import contextmanager
from typing import Any, Generator, Iterator, Protocol, TypeVar

from .source import DataSource


SourceT = TypeVar('SourceT')

DataT = TypeVar('DataT')

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

        def inject(self, *args: DataSource) -> Iterator['LLMDataPipeline[str, pytorch.Tensor]']:
          for ds in args:
            with ds.load() as raw_data:
               ...

        def __call__(self, data: str) -> Generator[Any, Any, DataT]:
          vocab = yield self.build_vocab()
          tokens = yield self.tokenize(vocab)
          tensors = yield self.to_tensors(tokens, data)

          return tensors
    """

    @contextmanager
    def inject(self, *args: DataSource) -> Iterator['DataPipeline[SourceT, DataT]']:
        """
        This method will be used to inject "train data" before transforming the data.

        Example: an LLM embedder would use some text to build a vocabulary.
        """
        pass

    def __call__(self, data: SourceT) -> Generator[Any, Any, DataT]:
        """
        Run the pipeline. Implementations are encouraged to split their
        pipelines into tasks (instance methods) and yield those until the
        final result is achieved and be returned.
        """
        pass
