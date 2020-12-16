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

# printing

import json
from abc import abstractmethod, ABC
from functools import cached_property

PRETTY_PRINTING = True


def enable_global_pretty_printing():
    global PRETTY_PRINTING
    PRETTY_PRINTING = True


def disable_global_pretty_printing():
    global PRETTY_PRINTING
    PRETTY_PRINTING = False


class withPrinting(ABC):
    """Mixin class to deal with string printing style"""
    pretty_printing = PRETTY_PRINTING

    @cached_property
    def asdict(self):
        self.pretty_printing = PRETTY_PRINTING
        return self._asdict_()

    @abstractmethod
    def _asdict_(self):
        pass

    def enable_pretty_printing(self):
        self.pretty_printing = True

    def disable_pretty_printing(self):
        self.pretty_printing = False

    def __str__(self, depth=""):
        from akangatu.transf.customjson import CustomJSONEncoder

        if self.pretty_printing:
            js_str = json.dumps(self, cls=CustomJSONEncoder, indent=4, ensure_ascii=False) # sort_keys=True,
            return js_str.replace("\n", "\n" + depth)

        js_str = json.dumps(self, cls=CustomJSONEncoder, indent=0, ensure_ascii=False) # sort_keys=True,
        return js_str.replace("\n", "")

    # __repr__ = __str__
