from akangatu.container import Container1
from akangatu.rev import Rev
from transf.absdata import AbsData
from transf.mixin.noop import asNoOp


class Marker(asNoOp, Container1):  # REMINDER: should be asNoOp since inside Data stay import UUIDs.
    def _process_(self, data: AbsData):
        return data.replace(self).replace(Rev(self))
