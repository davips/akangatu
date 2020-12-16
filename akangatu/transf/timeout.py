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

from numpy import Inf

from akangatu.linalghelper import islazy
from akangatu.transf.dataindependentstep_ import DataIndependentStep_


class Timeout(DataIndependentStep_):
    """Mark Data object as a result of time out.

    field: place of call where time out happened.
    Void the field if it is still lazy."""

    def __init__(self, limit, field=None):
        super().__init__(limit=limit, field=field)
        self.field = field
        self.limit = limit

    def _process_(self, data):
        newmatrices = {"timeout": True, "duration": self.limit}  # WARN: assume 'duration' will be equals to 'limit'
        if self.field:
            if not islazy(data.matrices[self.field]):
                raise Exception(f"Inconsistency: specified lazy field {self.field} is expected to be callable.")
            # None here means : field unavailable due to previous problems
            newmatrices[self.field] = None
        # TODO Let the target field have the worst possible value, since the step didn't finish.
        if self.comparable:
            newmatrices[data.comparable[0]] = -Inf

        return data.update(self, **newmatrices)
