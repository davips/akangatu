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

from aiuna.content.data import Data
from akangatu.container import Container1
from akangatu.fieldchecking import Ensure


class In(Container1):
    def _process_(self, data: Data):
        data = Ensure("inner").process(data)
        newinner = lambda: self.step.process(data.inner)
        return data.update(self, inner=newinner)
