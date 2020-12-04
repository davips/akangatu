#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the akangatu.transf project.
#  Please respect the license. Removing authorship by any means
#  (by code make up or closing the sources) or ignoring property rights
#  is a crime and is unethical regarding the effort and time spent here.
#  Relevant employers or funding agencies will be notified accordingly.
#
#  akangatu.transf is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  akangatu.transf is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with akangatu.transf.  If not, see <http://www.gnu.org/licenses/>.
#

from json import JSONEncoder, JSONDecoder
from types import FunctionType

import numpy as np

from akangatu.transf.mixin.metaoperand import MetaOperand


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if obj is not None:
            from cruipto.uuid import UUID
            if isinstance(obj, np.ndarray):
                return str(obj).split("\n")
            elif isinstance(obj, UUID):
                return obj.id
            elif isinstance(obj, FunctionType):
                return obj.__name__ # TODO stepfunc.name contemplado?
            elif isinstance(obj, MetaOperand):  # TODO: is this a problem?
                return obj()
            elif not isinstance(obj, (list, set, str, int, float, bytearray, bool)):  # other
                return obj.asdict if hasattr(obj, "asdict") else obj.aslist
        return JSONEncoder.default(self, obj)


class CustomJSONDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if obj is not None:
            from cruipto.uuid import UUID
            from akangatu.transf.step import Step
            # if isinstance(obj, str):  #np.ndarray
            #     return str(obj)
            if isinstance(obj, str) and len(obj) == UUID.digits:
                return UUID(obj)
            elif isinstance(obj, dict) and "id" in obj and all(x in obj["desc"] for x in ["name", "path", "config"]):
                return Step.recreate(obj)

        return obj
