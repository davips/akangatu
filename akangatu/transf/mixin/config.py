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

# noinspection PyUnusedFunction,PyMethodMayBeStatic,PyUnusedClass
class asUnitset:
    def _parameters_(self):
        return {}


class asConfigLess(asUnitset):
    def __init__(self):
        super().__init__()