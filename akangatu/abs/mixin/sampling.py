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

import json
from abc import abstractmethod, ABC
from functools import cached_property


class withSampling(ABC):
    """Transform data according to a sampleable configuration.

    Should be inherited together with a descendent of Step
    (because 'name' and 'held' attributes are needed)
    and the implementer should override sample() at 'init':
    self.sample = self.sample_
    """
    inner = None

    ###@cached_property
    @property
    def held(self):
        # noinspection PyUnresolvedReferences
        return self._held_()

    # noinspection PyUnresolvedReferences
    ###@cached_property
    @property
    def parameters(self):
        params = self._parameters_()
        for k, v in self.held.items():
            params[k] = [v]
        return params

    @abstractmethod
    def _parameters_(self):
        pass

    def _from_file(self):
        from kururu import tool
        import os
        path = os.path.abspath(tool.__file__)
        filename = "/".join(path.split("/")[:-2]) + f"/resources/parameters/{self.name}.json"
        try:
            with open(filename, "r") as f:
                # return Parameters(self.name, self.context, json.load(f))
                params = json.load(f)
                del params["meta-info"]
                return params
        except FileNotFoundError:
            return {"Not implemented params": []}  # TODO
            raise Exception(f"Impossible to sample. Missing parameters file:{filename}!")

    @classmethod
    def sample(cls, track=False):
        return cls().sample_(track)

    def sample_(self, track=False):  # TODO: seed
        from numpy.random.mtrand import choice
        config, choices = {}, {}

        def sample(dic):
            for k, content in dic.items():  # TODO:(?) nested dicts / key tracks from the root node
                if k == "steps":
                    value = content
                    idx = 0
                elif isinstance(content, dict):
                    idx = choice(list(content.keys()))
                    sample(content[idx])
                    value = idx
                else:
                    idx = choice(range(len(content)))
                    value = content[idx]
                config[k] = value
                choices[k] = idx

        sample(self.parameters)

        # noinspection PyArgumentList
        obj = self.__class__(self.inner, **config) if self.inner else self.__class__(**config)
        return (obj, choices) if track else obj
