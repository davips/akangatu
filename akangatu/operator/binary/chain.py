from functools import cached_property
import transf.operator as op
from aiuna.content.specialdata import Root
from akangatu.container import ContainerN


class Chain(op.Mul, ContainerN):
    def __init__(self, *args, steps=None):
        if args and steps:
            print("Wrong args: instantiating Chain is not recommended, use operator * instead.")
            exit()
        if args:
            steps = args
        super().__init__(*steps)
        ContainerN.__init__(self, steps)

    def _process_(self, data):  # TODO: expose internal models
        for transf in self.steps:
            data = transf.process(data)
        return data

    @cached_property
    def data(self):
        """Result of a transformation from Root data."""
        return self.process(Root)

    def _longname_(self):
        return '*'.join([tr.longname for tr in self.steps])

    def _uuid_(self):
        uuid = self.steps[0].uuid
        for transf in self.steps[1:]:
            uuid *= transf.uuid
        return uuid
