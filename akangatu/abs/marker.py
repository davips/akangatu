from abc import abstractmethod, ABC
from functools import cached_property

from akangatu.dataindependent import DataIndependent
from akangatu.rev import Rev
from transf.absdata import AbsData
from transf.mixin.identification import withIdentification


class Marker(DataIndependent, ABC):  # HINT: dataclasses does not work inside operate(): "object type has no isclass attribute"
    def __init__(self, transfuuid):
        self._transfuuid = transfuuid

    def _transform_(self, data: AbsData):
        return data.replace(self).replace(Rev(self))

    def _config_(self):
        return {"transfname": self._transfuuid}
