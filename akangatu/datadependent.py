from abc import ABC

from akangatu.mixin.operators import withOperators
from akangatu.mixin.sampling import withSampling
from transf.ddtransf import DDTransf_


class DataDependent(DDTransf_, withSampling, withOperators, ABC):
    """Operable and sampleable (training)data-dependent transformer"""
