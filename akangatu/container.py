import json
from abc import ABC, abstractmethod
from functools import cached_property

from aiuna.content.data import Data
from aiuna.content.root import Root
from akangatu.abs.mixin.sampling import withSampling
from cruipto.uuid import UUID
from transf._ins import Ins
from transf.customjson import CustomJSONEncoder
from transf.mixin.operand import asOperand
from transf.step import Step


class Container1(Step, withSampling, asOperand, ABC):
    # noinspection PyDefaultArgument
    def __init__(self, step, **config):
        config = config.copy()
        step = step if isinstance(step, Step) else step()
        config["step"] = step
        super().__init__(**config)
        self.step = step
        self._inner = None

    def _core_process_(self, data: Data):
        return self._process_(data)

    def _inner_(self):
        return self._inner

    def _parameters_(self):
        return {"step": self.step.parameters}

    @abstractmethod
    def _process_(self, data: Data):
        pass

    def _uuid_(self):  # TODO: deduplicate code; mais um mixin? classe mãe?
        uuid = UUID(json.dumps(self.desc, sort_keys=True, ensure_ascii=False, cls=CustomJSONEncoder).encode())
        if self.inner:
            uuid = Ins(self.inner).uuid * uuid
        return uuid

    def _name_(self):
        return self.__class__.__name__

    def _longname_(self):
        return self.__class__.__name__ + f"[{self.step.longname}]"

    def __call__(self, inner):  # TODO: seed
        if not isinstance(inner, Data):
            raise Exception("When calling a configured data dependent step, you should pass the training data! Not", type(inner))
        instance = self.__class__(self.step)
        instance._inner = inner
        return instance

    @cached_property
    def data(self):
        """Result of a transformation from Root data."""
        return self.process(Root)


class ContainerN(Step, withSampling, asOperand, ABC):
    def __init__(self, steps):
        self.steps = []
        for step in steps:
            # print(type(step))
            if not isinstance(step, Step):
                try:
                    step = step()
                except Exception as e:
                    print(e)
                    print("Wrong arg for ContainerN:", step)
                    exit()
            self.steps.append(step)
        super().__init__(steps=self.steps)
        self._inner = None

    def _core_process_(self, data: Data):
        return self._process_(data)

    def _inner_(self):
        return self._inner

    def _parameters_(self):  # TODO:will config match with stepclass?
        return {"steps": [step.parameters for step in self.steps]}

    @abstractmethod
    def _process_(self, data: Data):
        pass

    def __call__(self, inner):  # TODO: seed
        if not isinstance(inner, Data):
            raise Exception("When calling a configured data dependent step, you should pass the training data! Not", type(inner))
        instance = self.__class__(*self.steps)
        instance._inner = inner
        return instance


# TODO: unpredictable steps (e.g. recommenders) can have uuid U based on config as usual,
#  and the history of the data being processed can also grow internally as usual and generate the actual uuid A, but, at the end,
#  a corrective uuid X need to be appended, just like a final step F.
#  A * X = U      X = U / A
#  F can be called Alias, because it adds a new uuid for the same resulting data.
#  The only downside is that Cache cannot take advantage of a previously stored A, because it only nows U upfront.
#  A partial workaround is to keep a table of aliases (or just write two entries),
#  so at least when one have A they can look for a previously stored U.


def traverse(params):
    """Assume all containers are configless"""
    # TODO: terminar essa tentativa de percorrer e talvez casar com tracking de valores previos
    for k, v in params.items():
        if k == "steps":
            for transf in v:
                traverse(transf.parameters)
        else:
            pass
