from abc import ABC

from aiuna.content.data import Data
# HINT: dataclasses does not work inside operate(): "object type has no isclass attribute"
from akangatu.container import Container1
from transf.step import Step


class asMarker(Step, ABC):
    """Appears in history"""

    def _process_(self, data: Data):
        return data.update(self)


class B(asMarker, Container1):
    def _longname_(self):
        return "   { " + self.step.steps[0].name


class E(asMarker, Container1):
    def _longname_(self):
        return "   " + self.step.steps[0].name + " }"
