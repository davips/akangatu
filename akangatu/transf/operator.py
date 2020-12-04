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

import akangatu.transf.mixin.metaoperand as meop


class Operator:
    """Generic associative binary operator for any purpose.

    Each child concrete class should extend one of the needed aliases below: Add, Sub, Mul, ...
    It agglutinates a sequence of the same operator as a single final multi-valued one.
    The new operator definitions should be parsed at least one time before use,
    that is why mixin asOperand forces the implementer to declare a list of their operators.

    See mixin asOperand for more info.
    """

    def __init__(self, *operands):
        self.operands = operands
        self.isoperator = True

    def __add__(self, other):
        return meop.operate(Add, self, other)

    def __sub__(self, other):
        return meop.operate(Sub, self, other)

    def __mul__(self, other):
        return meop.operate(Mul, self, other)

    def __floordiv__(self, other):
        return meop.operate(FloorDiv, self, other)

    def __truediv__(self, other):
        return meop.operate(TrueDiv, self, other)

    def __mod__(self, other):
        return meop.operate(Mod, self, other)

    def __pow__(self, other):
        return meop.operate(Pow, self, other)

    def __lshift__(self, other):
        return meop.operate(LShift, self, other)

    def __rshift__(self, other):
        return meop.operate(RShif, self, other)

    def __and__(self, other):
        return meop.operate(And, self, other)

    def __xor__(self, other):
        return meop.operate(Xor, self, other)

    def __or__(self, other):
        return meop.operate(Or, self, other)

    def __matmul__(self, other):
        return meop.operate(MatMul, self, other)

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


class Add(Operator):
    pass


class Sub(Operator):
    pass


class Mul(Operator):
    pass


class FloorDiv(Operator):
    pass


class TrueDiv(Operator):
    pass


class Mod(Operator):
    pass


class Pow(Operator):
    pass


class LShift(Operator):
    pass


class RShif(Operator):
    pass


class And(Operator):
    pass


class Xor(Operator):
    pass


class Or(Operator):
    pass


class LT(Operator):
    pass


class LE(Operator):
    pass


class Eq(Operator):
    pass


class NE(Operator):
    pass


class GE(Operator):
    pass


class GT(Operator):
    pass


class MatMul(Operator):
    pass
