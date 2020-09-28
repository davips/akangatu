import json
from abc import ABC, abstractmethod

from akangatu import Insert
from akangatu.abs.mixin.sampling import withSampling
from cruipto.uuid import UUID
from transf.absdata import AbsData, InnocuousInnerData
from transf.customjsonencoder import CustomJSONEncoder
from transf.mixin.operand import asOperand
from transf.step import Step


class Container1(Step, withSampling, asOperand, ABC):
    def __init__(self, step):
        super().__init__({"step": step})
        self.step = step if isinstance(step, Step) else step()

        self._inner = InnocuousInnerData()  # TODO: ??

    def _core_process_(self, data: AbsData):
        return self._process_(data)

    def _inner_(self):
        return self._inner

    def _parameters_(self):
        return {"step": self.step.parameters}

    @abstractmethod
    def _process_(self, data: AbsData):
        pass

    def _uuid_(self):  # TODO: deduplicate code; mais um mixin? classe mãe?
        uuid = UUID(json.dumps(self.jsonable, sort_keys=True, ensure_ascii=False, cls=CustomJSONEncoder).encode())
        if self.inner:
            uuid = Insert(self.inner).uuid * uuid
        return uuid

    def _name_(self):
        return self.__class__.__name__

    def _longname_(self):
        return self.__class__.__name__ + f"[{self.step.longname}]"

    def __call__(self, inner):  # TODO: seed
        if not isinstance(inner, AbsData):
            raise Exception("When calling a configured data dependent step, you should pass the training data! Not", type(inner))
        instance = self.__class__(self.step)
        instance._inner = inner
        return instance


class ContainerN(Step, withSampling, asOperand, ABC):
    def __init__(self, *steps):
        super().__init__({"steps": steps})
        self.steps = [step if isinstance(step, Step) else step() for step in steps]
        self._inner = InnocuousInnerData()

    def _core_process_(self, data: AbsData):
        return self._process_(data)

    def _inner_(self):
        return self._inner

    def _parameters_(self):
        return {"steps": self.steps.parameters}

    @abstractmethod
    def _process_(self, data: AbsData):
        pass

    def __call__(self, inner):  # TODO: seed
        if not isinstance(inner, AbsData):
            raise Exception("When calling a configured data dependent step, you should pass the training data! Not", type(inner))
        instance = self.__class__(*self.steps)
        instance._inner = inner
        return instance


def traverse(params):
    """Assume all containers are configless"""
    # TODO: terminar essa tentativa de percorrer e talvez casar com tracking de valores previos
    for k, v in params.items():
        if k == "steps":
            for transf in v:
                traverse(transf.parameters)
        else:
            pass
