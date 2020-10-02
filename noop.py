from akangatu.distep import DIStep
from transf.absdata import AbsData
from transf.mixin.noop import asNoOp


class NoOp(DIStep, asNoOp):
    def __init__(self):
        super().__init__({})

    def _process_(self, data: AbsData):
        return data
