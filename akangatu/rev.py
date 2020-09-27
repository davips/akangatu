from akangatu.container import Container1
from transf.absdata import AbsData
from transf.step import Step


class Rev(Container1):  # may not need new() from Container1
    """Useful to revert uuid of NoOps like Begin, End,"""

    def _process_(self, data: AbsData):
        return data.replace(self)

    def _uuid_(self):
        return self.step.uuid.t

    def _longname_(self):
        return f" x {self.step.longname[3:]}"
