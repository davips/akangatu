#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the akangatu project.
#  Please respect the license - more about this in the section (*) below.
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
#  along with akangatu.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

from akangatu.container import ContainerN
import akangatu.transf.operator as op
from akangatu.transf.config import CACHE


class CachedProduct(op.Pow, ContainerN):
    def __init__(self, *args, steps=None):
        if args and steps:
            print("Wrong args: instantiating CachedProduct is not recommended, use operator ** instead.")
            exit()
        if args:
            steps = args
        # noinspection PyUnresolvedReferences
        from more_itertools import intersperse
        steps = list(intersperse(CACHE["cache"], steps))
        op.Operator.__init__(self, *steps)
        ContainerN.__init__(self, steps)

    def _process_(self, data):  # TODO: expose internal models
        for step in self.steps:
            # print(11111111111111111111111111, step, 222222222222222222222222222)
            data = step.process(data)
        return data

    # @cached_property
    # def data(self):
    #     """Result of a transformation from Root data."""
    #     from aiuna.content.root import Root
    #     return self.process(Root)

    #TODO:
    #  colocar um campo mutable lastinner_m/lastmodel_m pra facilitar pegar um model de dentro do chain sem ter que reescrever o pipe até o momento
    # @lru_cache
    # def models(self, data=None):
    #     """Models."""
    #     if self.inner and data:
    #     print("Cannot provide data for a model in a step that already was initialized with an inner data!")
    #     exit()
    #     inner =self.inner or data
    #     models = []
    #     for step in self.steps:
    #     if "model" in step.__dict__:
    #         models.append(step.model(step.inner))
    #     elif "models" in step.__dict__:
    #         models += step.models
    #     return models

    def _longname_(self):
        return ' * '.join([tr.longname for tr in self.steps])

    def _uuid_(self):
        uuid = self.steps[0].uuid
        for transf in self.steps[1:]:
            uuid *= transf.uuid
        return uuid
