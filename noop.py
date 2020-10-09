from akangatu.distep import DIStep
from transf.absdata import AbsData
from transf.mixin.config import asUnitset, asConfigLess
from transf.mixin.noop import asNoOp


class NoOp(asConfigLess, asUnitset, DIStep, asNoOp):
    def _process_(self, data: AbsData):
        return data
