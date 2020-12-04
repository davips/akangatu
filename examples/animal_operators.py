from akangatu.transf.mixin.operand import asOperand
from akangatu.transf.operator import Add, Mul

"""Illustrative example of how to create operators."""


class Zoo(Add):
    def __str__(self):
        return " + ".join(str(op) for op in self.operands)


class CartesianZoo(Mul):
    def __str__(self):
        return " * ".join(str(op) for op in self.operands)


class Animal(asOperand):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}:{self.__class__.__name__}"


class Dog(Animal):
    """"""


class Duck(Animal):
    """"""


a = Duck("q") + Duck + Dog * Duck("b")
print(a + Dog)
