from akangatu.abs.mixin.sampling import withSampling
from transf._ins import Ins as Ins_
from transf.mixin.operand import asOperand


class Ins(Ins_, withSampling, asOperand):
    def _parameters_(self):
        return {"inner": [self.inner.id]}
