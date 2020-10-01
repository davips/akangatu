from functools import cached_property
from itertools import takewhile

import transf.operator as op
from aiuna.content.specialdata import Root
from akangatu.container import ContainerN
from transf.mixin.streamhandler import asStreamHandler


class Chain(asStreamHandler, op.Mul, ContainerN):
    def __init__(self, *args, steps=None):
        if args and steps:
            print("Wrong args: instantiating Chain is not recommended, use operator * instead.")
            exit()
        if args:
            steps = args
        super().__init__(*steps)
        ContainerN.__init__(self, steps)

    def _workers_(self):
        def badstep(step):
            print(f"Non streamer {step} is not expected to come before reduce!")

        workers = takewhile(lambda step: step if isinstance(step, asStreamHandler) else badstep(step), self.steps)
        return zip(map(lambda step: step.workers, workers))

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
