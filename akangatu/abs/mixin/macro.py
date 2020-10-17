from abc import abstractmethod, ABC
from functools import cached_property

from aiuna.content.data import Data
from akangatu.abs.delimiter import Begin, End
from transf._ins import Ins
from transf.mixin.identification import withIdentification


class asMacro(withIdentification, ABC):  # TODO: todo container precisa passar inner data pra dentro?
    @cached_property
    def step(self):
        step = self._step_()
        return Begin(step) * step * End(step)

    @abstractmethod
    def _step_(self):
        pass

    def _process_(self, data):
        return self.step.process(data)

    def _uuid_(self):  # TODO:deduplicate serialization and enforce stability and calculation reuse
        uuid = self.step.uuid
        if self.inner:
            uuid = Ins(self.inner).uuid * uuid
        return uuid

    def __call__(self, inner):  # TODO: seed
        if not isinstance(inner, Data):
            raise Exception("When calling a configured data dependent step, you should pass the training data! Not", type(inner))
        instance = self.__class__()
        instance._inner = inner
        return instance
