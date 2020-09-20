from akangatu.mixin.operators import withOperators
from akangatu.mixin.sampling import withSampling
from transf._ins import Ins as Ins_


class Ins(Ins_, withSampling, withOperators):
    pass
