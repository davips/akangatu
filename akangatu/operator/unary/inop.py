from akangatu.container import Container1
from transf.absdata import AbsData


class In(Container1):
    def __init__(self, transformer):
        super().__init__(transformer)
        self.transformer = transformer
        self._config = {"transformer": transformer}

    def _transform_(self, data: AbsData):
        newinner = self.transformer.transform(data.inner)
        return data.replace(self, inner=newinner)
