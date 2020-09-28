from abc import abstractmethod, ABC
from functools import cached_property

from akangatu import Insert
from akangatu.delimiter import Begin, End
from cruipto.uuid import UUID
from transf.absdata import AbsData
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
            uuid = Insert(self.inner).uuid * uuid
        return uuid

    def __call__(self, inner):  # TODO: seed
        if not isinstance(inner, AbsData):
            raise Exception("When calling a configured data dependent step, you should pass the training data! Not", type(inner))
        instance = self.__class__()
        instance._inner = inner
        return instance
