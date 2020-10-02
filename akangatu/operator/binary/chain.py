from functools import cached_property, lru_cache
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

    #TODO:
    #  colocar um campo mutable lastinner_m/lastmodel_m pra facilitar pegar um model de dentro do chain sem ter que reescrever o pipe até o momento
    # @lru_cache
    # def models(self, data=None):
    #     """Models."""
    #     if self.inner and data:
    #         print("Cannot provide data for a model in a step that already was initialized with an inner data!")
    #         exit()
    #     inner =self.inner or data
    #     models = []
    #     for step in self.steps:
    #         if "model" in step.__dict__:
    #             models.append(step.model(step.inner))
    #         elif "models" in step.__dict__:
    #             models += step.models
    #     return models

    def _longname_(self):
        return '*'.join([tr.longname for tr in self.steps])

    def _uuid_(self):
        uuid = self.steps[0].uuid
        for transf in self.steps[1:]:
            uuid *= transf.uuid
        return uuid
