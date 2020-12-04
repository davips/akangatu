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

from abc import ABCMeta

import akangatu.transf.operator as ops


def operate(operator, a, b):
    # TODO: ensure only one subclass per operator
    # TODO: cache the dict and risk to be outdated?
    from akangatu.transf.step import Step
    if hasattr(a, "isclass") and a.isclass:
        a = a()
    if hasattr(b, "isclass") and b.isclass:
        b = b()
    if not isinstance(a, (Step, MetaOperand)) or not isinstance(b, (Step, MetaOperand)):
        raise Exception(f"Operator {operator} undefined for {a.__class__.__name__} and {b.__class__.__name__}")

    operators = {op: op.__subclasses__()[0] for op in ops.Operator.__subclasses__() if op.__subclasses__()}
    if operator in operators:
        operator = operators[operator]
    # noinspection PyTypeHints
    if b.isoperator:  # and isinstance(b, operator):
        return b.__class__(a, *b.operands)
    elif a.isoperator:  # and isinstance(a, operator):
        return a.__class__(*a.operands, b)
    return operator(a, b)


class MetaOperand(ABCMeta):
    """Generic associative binary operators for Python classes.

    See class Operator and mixin asOperand.
    """
    isoperator = False
    isclass = True

    def __add__(cls, other):
        return operate(ops.Add, cls, other)

    def __sub__(cls, other):
        return operate(ops.Sub, cls, other)

    def __mul__(cls, other):
        return operate(ops.Mul, cls, other)

    def __floordiv__(cls, other):
        return operate(ops.FloorDiv, cls, other)

    def __truediv__(cls, other):
        return operate(ops.TrueDiv, cls, other)

    def __mod__(cls, other):
        return operate(ops.Mod, cls, other)

    def __pow__(cls, other):
        return operate(ops.Pow, cls, other)

    def __and__(cls, other):
        return operate(ops.And, cls, other)

    def __xor__(cls, other):
        return operate(ops.Xor, cls, other)

    def __or__(cls, other):
        return operate(ops.Or, cls, other)

    def __matmul__(cls, other):
        return operate(ops.MatMul, cls, other)

    def __lt__(cls, other):
        return operate(ops.LT, cls, other)

    def __le__(cls, other):
        return operate(ops.LE, cls, other)

    def __ne__(cls, other):
        return operate(ops.NE, cls, other)

    def __ge__(cls, other):
        return operate(ops.GE, cls, other)

    def __gt__(cls, other):
        return operate(ops.GT, cls, other)

    def __rmul__(cls, other):
        return operate(ops.Mul, other, cls)

    def __str__(self):
        return self.__name__
