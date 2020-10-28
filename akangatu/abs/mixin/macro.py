#  Copyright (c) 2020. Davi Pereira dos Santos
#      This file is part of the akangatu project.
#      Please respect the license. Removing authorship by any means
#      (by code make up or closing the sources) or ignoring property rights
#      is a crime and is unethical regarding the effort and time spent here.
#      Relevant employers or funding agencies will be notified accordingly.
#
#      akangatu is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      akangatu is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with akangatu.  If not, see <http://www.gnu.org/licenses/>.
#

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
