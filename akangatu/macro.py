from abc import abstractmethod, ABC
from functools import cached_property


class asMacro(ABC):
    @cached_property
    def transformer(self):
        return self._transformer_()

    @abstractmethod
    def _transformer_(self):
        pass

    def _transform_(self, data):
        return self.transformer.transform(data)
