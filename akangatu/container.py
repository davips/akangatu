#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the akangatu project.
#  Please respect the license - more about this in the section (*) below.
#
#  akangatu is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  akangatu is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with akangatu.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

import json
from abc import ABC, abstractmethod

from akangatu.abs.mixin.sampling import withSampling
from akangatu.transf._ins import Ins
from akangatu.transf.customjson import CustomJSONEncoder
from akangatu.transf.mixin.operand import asOperand
from akangatu.transf.step import Step


class Container1(Step, withSampling, asOperand, ABC):
    # REMINDER: Container1 cannot have config by itself, because sampling it should sample its step,
    #   and the sampled parameter values need to be passed somehow to its step.
    def __init__(self, step, **config):
        config = config.copy()
        step = step if isinstance(step, Step) else step(**config)
        config["step"] = step
        super().__init__(**config)
        self.step = step
        self._inner = None

    def _core_process_(self, data):
        return self._process_(data)

    def _inner_(self):
        return self._inner

    def _parameters_(self):
        return {"step": self.step.parameters}

    @abstractmethod
    def _process_(self, data):
        pass

    def _uuid_(self):  # TODO: deduplicate code; mais um mixin? classe mãe?
        from garoupa.uuid import UUID
        uuid = UUID(json.dumps(self.desc, sort_keys=True, ensure_ascii=False, cls=CustomJSONEncoder).encode())
        if self.inner:
            uuid = Ins(self.inner).uuid * uuid
        return uuid

    def _name_(self):
        return self.__class__.__name__

    def _longname_(self):
        return self.__class__.__name__ + f"[{self.step.longname}]"

    def __call__(self, inner):  # TODO: seed
        if not hasattr(inner, "hasinners"):  # just checking its a Data
            raise Exception("When calling a configured data dependent step, you should pass the training data! Not",
                            type(inner))
        instance = self.__class__(self.step)
        instance._inner = inner
        return instance


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

    def _core_process_(self, data):
        return self._process_(data)

    def _inner_(self):
        return self._inner

    def _parameters_(self):  # TODO:will config match with stepclass?
        return {"steps": [step.parameters for step in self.steps]}

    @abstractmethod
    def _process_(self, data):
        pass

    def __call__(self, inner):  # TODO: seed
        if not hasattr(inner, "hasinners"):  # just checking its a Data
            raise Exception("When calling a configured data dependent step, you should pass the training data! Not",
                            type(inner))
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
