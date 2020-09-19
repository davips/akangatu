from akangatu.operator.binary.chain import Chain
from akangatu.operator.binary.stream import Stream
from transf.mixin.operand import asOperand


class withOperators(asOperand):
    def available_operators(self):
        return [Chain, Stream]
