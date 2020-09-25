from abc import ABC

from aiuna.content.specialdata import Root
from akangatu.abs.mixin.sampling import withSampling
from transf.ditransf import DITransf_
from transf.mixin.operand import asOperand


class DataIndependent(DITransf_, withSampling, asOperand, ABC):
    """Operable and sampleable data transformer that doesn't dependent on (training) data."""

    def _core_transform_(self, data=None, lazy=False):  # override
        # This overriding is needed to convert None to Root (to avoid early dependence on aiuna)
        return self._transform_(data or Root)

    def _parameters_(self):
        return self._from_file()
