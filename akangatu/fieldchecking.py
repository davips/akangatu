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
from akangatu.distep import DIStep
from transf.mixin.noop import asNoOp


class Forbid(asNoOp, DIStep):
    def __init__(self, field):
        super().__init__(field=field)
        self.field = field

    def _process_(self, data: Data):
        if self.field in data:
            print("Cannot proceed with data containg the field", self.field)
            exit()
        return data


class Ensure(asNoOp, DIStep):
    def __init__(self, field):
        super().__init__(field=field)
        self.field = field

    def _process_(self, data: Data):
        if self.field not in data:
            # raise Exception
            exit()
        return data  # TODO: esses caras não aparecem no hist, mas poderiam ter placeholders; vale a pena? só se o histórico fosse usado p/ reconstruir expression original
