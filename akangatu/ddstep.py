from abc import ABC

from akangatu.abs.mixin.sampling import withSampling
from transf.ddtransf import DataDependentStep_
from transf.mixin.operand import asOperand


class DDStep(DataDependentStep_, withSampling, asOperand, ABC):
    """Operable and sampleable (training)data-dependent step"""

    def _parameters_(self):
        return self._from_file()
