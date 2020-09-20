from abc import ABC

from akangatu.mixin.sampling import withSampling
from transf.ddtransf import DDTransf_
from transf.mixin.operand import asOperand


class DataDependent(DDTransf_, withSampling, asOperand, ABC):
    """Operable and sampleable (training)data-dependent transformer"""

    def _parameters_(self):
        return self._from_file()
