from abc import abstractmethod, ABC
from dataclasses import dataclass
from functools import cached_property

from akangatu.dataindependent import DataIndependent
from cruipto.uuid import UUID
from transf.absdata import AbsData
from transf.mixin.identification import withIdentification


class asMacro(withIdentification, ABC):
    @cached_property
    def transformer(self):
        transformer = self._transformer_()
        return Begin(self.name) * transformer * End(self.name)

    @abstractmethod
    def _transformer_(self):
        pass

    def _transform_(self, data):
        return self.transformer.transform(data)

    def _uuid_(self):
        return self.transformer.uuid


class Begin(DataIndependent):  # HINT: dataclasses does not work inside operate(): "object type has no isclass attribute"
    def __init__(self, transfname):
        self.transfname = transfname

    def _transform_(self, data: AbsData):
        return data.replace(self)

    def _config_(self):
        return {"transfname": self.transfname}

    def _uuid_(self):
        return UUID.identity

    def _longname_(self):
        return super().name + f"({self.transfname})"


class End(Begin):
    pass
