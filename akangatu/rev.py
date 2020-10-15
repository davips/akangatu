from aiuna.content.data import Data
from akangatu.container import Container1


class Rev(Container1):  # may not need new() from Container1
    """Useful to revert uuid of NoOps like Begin, End,"""

    def _process_(self, data: Data):
        return data.update(self)

    def _uuid_(self):
        return self.step.uuid.t

    def _longname_(self):
        return f" x {self.step.longname[3:]}"
