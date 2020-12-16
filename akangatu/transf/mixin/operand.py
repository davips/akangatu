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

from akangatu.transf.mixin.metaoperand import MetaOperand, operate
from akangatu.transf.operator import *


class asOperand(metaclass=MetaOperand):
    """Generic associative binary operators for Python objects.

    See class Operator.

    The return type is defined by each operation. E.g.:
        Duck() * Cat * Dog() returns MyProductOfAnimals(Duck(), Cat, Dog())
        Duck() - Cat - Dog returns MyUnionOfAnimals(Duck(), Cat, Dog)
    MyProductOfAnimals and MyUnionOfAnimals should extend one of the operator aliases: Add, Sub, Mul, ...
    They will be detected dynamically as operators at the time of an operation.
    """
    isoperator = False
    isclass = False

    def __add__(self, other):
        return operate(Add, self, other)

    def __sub__(self, other):
        return operate(Sub, self, other)

    def __mul__(self, other):
        return operate(Mul, self, other)

    def __floordiv__(self, other):
        return operate(FloorDiv, self, other)

    def __truediv__(self, other):
        return operate(TrueDiv, self, other)

    def __mod__(self, other):
        return operate(Mod, self, other)

    def __pow__(self, other):
        return operate(Pow, self, other)

    def __and__(self, other):
        return operate(And, self, other)

    def __xor__(self, other):
        return operate(Xor, self, other)

    def __or__(self, other):
        return operate(Or, self, other)

    def __matmul__(self, other):
        return operate(MatMul, self, other)

    def __lt__(self, other):
        return meop.operate(LT, self, other)

    def __le__(self, other):
        return meop.operate(LE, self, other)

    def __ne__(self, other):
        return meop.operate(NE, self, other)

    def __ge__(self, other):
        return meop.operate(GE, self, other)

    def __gt__(self, other):
        return meop.operate(GT, self, other)

    def __rmul__(self, other):
        return meop.operate(Mul, other, self)

# TODO: make r version for all operators?
