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

from abc import abstractmethod, ABC

from akangatu.transf.step import Step


class DataIndependentStep_(Step, ABC):
    """ A step that doesn't dependent on (training) data """

    def _inner_(self):
        return None

    def _core_process_(self, data, lazy=False):
        return self._process_(data)

    @abstractmethod
    def _process_(self, data):
        pass

    def _longname_(self):
        return self.__class__.__name__

    def asunion(self):
        """step.asunion == step + Empty"""

    def __call__(self, *args, **kwargs):
        kwargs.update(self._held_())
        try:
            # noinspection PyArgumentList
            instance = self.__class__(*args, **kwargs)
            return instance
        except TypeError as e:
            if "__init__() got multiple values for argument" in str(e):
                param = str(e).split("'")[1]
                raise Exception(f"Parameter [{param}] was already set for this {self.name} step.")
