import json
from abc import ABC, abstractmethod

from akangatu import Ins
from akangatu.mixin.sampling import withSampling
from cruipto.uuid import UUID
from transf.absdata import AbsData
from transf.customjsonencoder import CustomJSONEncoder
from transf.mixin.operand import asOperand
from transf.transformer import Transformer


class Container1(Transformer, withSampling, asOperand, ABC):
    def __init__(self, transformer):
        self.transformer = transformer
        self._config = {"transformer": transformer}
        self._inner = None  # InnocuousInnerData()

    def _core_transform_(self, data: AbsData):
        return self._transform_(data)

    def _config_(self):
        return self._config

    def _inner_(self):
        return self._inner

    def _parameters_(self):
        return {"transformer": self.transformer.parameters}

    @abstractmethod
    def _transform_(self, data: AbsData):
        pass

    def _uuid_(self):  # TODO: deduplicate code; mais um mixin? classe mãe?
        uuid = UUID(json.dumps(self.jsonable, sort_keys=True, ensure_ascii=False, cls=CustomJSONEncoder).encode())
        if self.inner:
            uuid = Ins(self.inner).uuid * uuid
        return uuid

    def _name_(self):
        return self.__class__.__name__

    def _longname_(self):
        return self.__class__.__name__ + f"[{self.transformer.longname}]"

    def __call__(self, inner):  # TODO: seed
        instance = self.__class__(self.transformer)
        instance._inner = inner
        return instance


class ContainerN(Transformer, withSampling, asOperand, ABC):
    def __init__(self, *transformers):
        self.transformers = [tr if isinstance(tr, Transformer) else tr() for tr in transformers]
        self._config = {"transformers": transformers}
        self._inner = None  # InnocuousInnerData()

    def _core_transform_(self, data: AbsData):
        return self._transform_(data)

    def _config_(self):
        return self._config

    def _inner_(self):
        return self._inner

    def _parameters_(self):
        return {"transformers": self.transformers.parameters}

    @abstractmethod
    def _transform_(self, data: AbsData):
        pass

    def _uuid_(self):
        uuid = UUID(json.dumps(self.jsonable, sort_keys=True).encode())
        if self.inner:
            uuid = Ins(self.inner).uuid * uuid
        return uuid

    def _longname_(self):
        return self.__class__.__name__ + f"[{' '.join([tr.longname for tr in self.transformers])}]"

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
