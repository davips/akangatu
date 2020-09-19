from abc import ABC

from aiuna.content.specialdata import NoData
from akangatu.mixin.operators import withOperators
from akangatu.mixin.sampling import withSampling
from transf.dataindependent import DataIndependent_


class DataIndependent(DataIndependent_, withSampling, withOperators, ABC):
    """Operable and sampleable data transformer that doesn't dependent on (training) data."""
    def _internal_transform_(self, data=None, lazy=False):  # override
        # This overriding is needed to convert None to NoData (to avoid early dependence on aiuna)
        return self._transform_(data or NoData)
