from functools import cached_property

import ring as ring

from transf.absdata import InnocuousInnerData
from transf.operator import Mul
from transf.transformer import Transformer


class Chain(Mul, Transformer):
    def _inner_(self):
        return self._inner

    def __init__(self, *transformers):
        super().__init__(*transformers)
        self.transformers = transformers
        self._config = {"transformers": transformers}
        self._inner = InnocuousInnerData()

    def _core_transform_(self, data):  # TODO: expose internal models
        for transf in self.transformers:
            data = transf.transform(data)
        return data

    def _config_(self):
        return self._config

    def sample(self, track=False):  # TODO: seed
        return Chain(*[transf.sample(track) for transf in self.transformers])

    @cached_property
    def parameters(self):  # override
        # return Parameters(self.name, self.context, {"transformers": [transf.parameters for transf in self.transformers]})
        return {"transformers": [transf.parameters for transf in self.transformers]}

    def __call__(self, inner):  # TODO: seed
        instance = self.__class__(*self.transformers)
        instance._inner = inner
        return instance


def traverse(params):
    """Assume all containers are configless"""
    # TODO: terminar essa tentativa de percorrer e talvez casar com tracking de valores previos
    for k, v in params.items():
        if k == "transformers":
            for transf in v:
                traverse(transf.parameters)
        else:
            pass
