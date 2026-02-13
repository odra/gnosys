from contextlib import contextmanager
from typing import Any, Generator, Iterator


import pytorch # type: ignore
from gnosys import data as datalib

 
class TextToTensorPipeline:
    """
    A data pipeline that transforms rawtext into pytorch tensors.
    """

    @contextmanager
    def inject(self, *args: datalib.source.DataSource) -> Iterator['TextToTensorPipeline']:
        """
        """
        for ds in args:
            data = datalib.load_source(ds)
        
        try:
            yield self
        finally:
            pass

    def __call__(self, data: str) -> Generator[Any, Any, pytorch.Tensor]:
        """
        """
        yield None

        return pytorch.tensor([]) 
