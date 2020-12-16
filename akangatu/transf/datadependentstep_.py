#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the akangatu project.
#  Please respect the license. Removing authorship by any means
#  (by code make up or closing the sources) or ignoring property rights
#  is a crime and is unethical regarding the effort and time spent here.
#  Relevant employers or funding agencies will be notified accordingly.
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
#  along with akangatu  If not, see <http://www.gnu.org/licenses/>.
#

import json
from abc import abstractmethod, ABC

from garoupa.uuid import UUID
from akangatu.transf._ins import Ins
from akangatu.transf.customjson import CustomJSONEncoder
from akangatu.transf.step import Step


class DataDependentStep_(Step, ABC):
    """ A step dependent on (training) data """
    isdi = False
    isdd = True

    def __init__(self, inner, **config):
        super().__init__(**config)
        if inner:
            if not hasattr(inner, "parent_uuid"):
                raise Exception("First argument to a data dependent step should be the training data! Not", type(inner))
            self._inner = inner
        else:
            self._inner = None

    def _core_process_(self, data):
        if not self.inner:
            if not data.hasinner:
                print("--------------------------------------")
                print(f"{self.name} needs (training) inner data at constructor or inside (testing) data!")
                exit()
            # noinspection PyArgumentList
            # newobj = self.__class__(**self.config)
            # return self.__class__._process_(newobj, data, data.inner)
            return self._process_(data)

        if data.hasinner:
            print(f"Training data for {self.name} given at constructor and also as inner data:", self.inner.id)
            exit()

        # Externally given inner data.
        innertransf = Ins(self.inner)
        # noinspection PyProtectedMember
        return self.makeupuuid(innertransf.uuid.t * self.uuid)._process_(innertransf.process(data))

    @abstractmethod
    def _process_(self, data):
        pass

    def _inner_(self):
        return self._inner

    def _uuid_(self):  # TODO:deduplicate serialization and enforce stability and calculation reuse
        uuid = UUID(json.dumps(self.desc, sort_keys=True, ensure_ascii=False, cls=CustomJSONEncoder).encode())
        if self.inner:
            uuid = Ins(self.inner).uuid * uuid
        return uuid

    def __call__(self, *args, **kwargs):
        if any(map(lambda s: hasattr(s, "parent_uuid"), args)):
            raise Exception(f"Inner data already given at {self.name} constructor!", self.inner)
        kwargs.update(self._held_())
        try:
            # noinspection PyArgumentList
            instance = self.__class__(*args, **kwargs)
            return instance
        except TypeError as e:
            if "__init__() got multiple values for argument" in str(e):
                param = str(e).split("'")[1]
                raise Exception(f"Parameter [{param}] was already set for this {self.name} step.")

    def _longname_(self):
        return self.__class__.__name__
