from abc import abstractmethod, ABC
from functools import cached_property

from akangatu.delimiter import Begin, End
from transf.mixin.identification import withIdentification


class asMacro(withIdentification, ABC):
    @cached_property
    def transformer(self):
        transformer = self._transformer_()
        return Begin(transformer.id) * transformer * End(transformer.id)

    @abstractmethod
    def _transformer_(self):
        pass

    def _transform_(self, data):
        return self.transformer.transform(data)

    def _uuid_(self):
        return self.transformer.uuid
