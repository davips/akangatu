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
# from functools import cached_property


class withIdentification(ABC):
    ###@cached_property
    @property
    def name(self):
        return self._name_()

    ###@cached_property
    @property
    def context(self):
        return self._context_()

    ###@cached_property
    @property
    def uuid(self):
        return self._uuid_()

    @property
    def id(self):
        return self.uuid.id

    @abstractmethod
    def _name_(self):
        pass

    @abstractmethod
    def _context_(self):
        pass

    @abstractmethod
    def _uuid_(self):
        pass

    def __hash__(self):
        return self.uuid.n

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id
