from abc import abstractmethod, ABC
from functools import cached_property

from akangatu.container import Container1
from akangatu.distep import DIStep
from akangatu.rev import Rev
from cruipto.uuid import UUID
from transf.absdata import AbsData
from transf.mixin.identification import withIdentification


class Marker(Container1):
    def _process_(self, data: AbsData):
        return data.replace(self).replace(Rev(self))

    def _uuid_(self):
        return UUID.identity

# HINT: dataclasses does not work inside operate(): "object type has no isclass attribute"