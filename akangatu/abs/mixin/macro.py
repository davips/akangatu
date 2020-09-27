from abc import abstractmethod, ABC
from functools import cached_property

from akangatu.delimiter import Begin, End
from transf.mixin.identification import withIdentification


class asMacro(withIdentification, ABC):  # TODO: todo container precisa passar inner data pra dentro?
    @cached_property
    def step(self):
        step = self._step_()
        if self.inner and callable(step):
            step = step(self.inner)
        return Begin(step) * step * End(step)

    @abstractmethod
    def _step_(self):
        pass

    def _process_(self, data):
        return self.step.process(data)

    def _uuid_(self):
        return self.step.uuid

    def __call__(self, inner):  # TODO: seed
        instance = self.__class__()
        instance._inner = inner
        return instance
