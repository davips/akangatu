from abc import ABC

from akangatu.abs.mixin.sampling import withSampling
from transf.dataindependentstep_ import DataIndependentStep_
from transf.mixin.operand import asOperand


class DIStep(DataIndependentStep_, withSampling, asOperand, ABC):
    """Operable and sampleable data step that doesn't dependent on (training) data."""

    def _parameters_(self):
        return self._from_file()
