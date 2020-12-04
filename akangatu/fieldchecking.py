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

from akangatu.transf.mixin.noop import asNoOp

from akangatu.distep import DIStep


class Forbid(asNoOp, DIStep):
    def __init__(self, field):
        super().__init__(field=field)
        self.field = field

    def _process_(self, data):
        if self.field in data:
            print("Cannot proceed with data containg the field", self.field)
            exit()
        return data


class Ensure(asNoOp, DIStep):
    def __init__(self, field):
        super().__init__(field=field)
        self.field = field

    def _process_(self, data):
        if self.field not in data:
            raise Exception(f"Field {self.field} not in data!")
        return data  # TODO: esses caras não aparecem no hist, mas poderiam ter placeholders; vale a pena? só se o histórico fosse usado p/ reconstruir expression original
