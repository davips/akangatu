import json
from functools import cached_property

from numpy.random.mtrand import choice

from transf.absdata import InnocuousInnerData


class withSampling:
    """Transform data according to a sampleable configuration.

    Should be inherited together with a descendent of Transformer
    (because 'name' and 'held' attributes are needed)
    and the implementer should override sample() at 'init':
    self.sample = self.sample_
    """
    inner = InnocuousInnerData()

    @cached_property
    def held(self):
        # noinspection PyUnresolvedReferences
        return self._held_()

    # noinspection PyUnresolvedReferences
    @cached_property
    def parameters(self):
        filename = f"kururu/resources/parameters/{self.name}.json"
        try:
            with open(filename, "r") as f:
                # return Parameters(self.name, self.context, json.load(f))
                params = json.load(f)
                del params["meta-info"]
                for k, v in self.held.items():
                    params[k] = [v]
                return params
        except FileNotFoundError:
            raise Exception(f"Impossible to sample. Missing parameters file:{filename}!")

    @classmethod
    def sample(cls, track=False):
        return cls().sample_(track)

    def sample_(self, track=False):  # TODO: seed
        config, choices = {}, {}

        def sample(dic):
            for k, content in dic.items():  # TODO: nested dicts / key tracks from the root node
                if isinstance(content, dict):
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
