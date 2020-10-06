from akangatu.distep import DIStep
from transf.absdata import AbsData
from transf.mixin.config import asUnitset
from transf.mixin.noop import asNoOp


class NoOp(asUnitset, DIStep, asNoOp):
    def _process_(self, data: AbsData):
        return data
