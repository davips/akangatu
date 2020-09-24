from functools import cached_property

import transf.operator as op
from akangatu.container import ContainerN


class Chain(op.Mul, ContainerN):
    def __init__(self, *transformers):
        super().__init__(*transformers)
        ContainerN.__init__(self, *transformers)

    def _transform_(self, data):  # TODO: expose internal models
        for transf in self.transformers:
            data = transf.transform(data)
        return data

    def _longname_(self):
        return '*'.join([tr.longname for tr in self.transformers])

    def _uuid_(self):
        uuid = self.transformers[0].uuid
        for transf in self.transformers[1:]:
            uuid *= transf.uuid
        return uuid
