from akangatu.abs.delimiter import Delimiter

# HINT: dataclasses does not work inside operate(): "object type has no isclass attribute"
from akangatu.container import Container1
from transf.absdata import AbsData
from transf.absstep import AbsStep


class asMarker(AbsStep):
    """Appears in history"""

    def _process_(self, data: AbsData):
        return data.update(self)


class B(asMarker, Container1):
    def _longname_(self):
        return "   { " + self.step.steps[0].name


class E(asMarker, Container1):
    def _longname_(self):
        return "   " + self.step.steps[0].name + " }"

