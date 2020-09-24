from akangatu.container import Container1
from transf.absdata import AbsData
from transf.transformer import Transformer


class Rev(Container1):  # may not need new() from Container1
    """Useful to revert uuid of NoOps like Begin, End,"""
    def _transform_(self, data: AbsData):
        return data.replace(self)

    def _uuid_(self):
        return self.transformer.uuid.t
