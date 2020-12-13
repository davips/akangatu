# #  Copyright (c) 2020. Davi Pereira dos Santos
# #  This file is part of the akangatu project.
# #  Please respect the license - more about this in the section (*) below.
# #
# #  akangatu is free software: you can redistribute it and/or modify
# #  it under the terms of the GNU General Public License as published by
# #  the Free Software Foundation, either version 3 of the License, or
# #  (at your option) any later version.
# #
# #  akangatu is distributed in the hope that it will be useful,
# #  but WITHOUT ANY WARRANTY; without even the implied warranty of
# #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #  GNU General Public License for more details.
# #
# #  You should have received a copy of the GNU General Public License
# #  along with akangatu.  If not, see <http://www.gnu.org/licenses/>.
# #
# #  (*) Removing authorship by any means, e.g. by distribution of derived
# #  works or verbatim, obfuscated, compiled or rewritten versions of any
# #  part of this work is a crime and is unethical regarding the effort and
# #  time spent here.
# #  Relevant employers or funding agencies will be notified accordingly.
#
# from abc import ABC
#
# # HINT: dataclasses does not work inside operate(): "object type has no isclass attribute"
# from akangatu.container import Container1
# from akangatu.transf.step import Step
#
#
# class asMarker(Step, ABC):
#     """Appears in history"""
#
#     def _process_(self, data):
#         return data.update(self)
#
#
# class B(asMarker, Container1):
#     """"""
#     # def _longname_(self):
#     #     return "   { " + str(list(s.longname for s in self.step.steps))
#
#
# class E(asMarker, Container1):
#     """"""
#     # def _longname_(self):
#     #     return "   " + self.step.steps[0].name + " }"
