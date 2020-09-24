from akangatu.container import Container1
from transf.absdata import AbsData


class In(Container1):
    def _transform_(self, data: AbsData):
        newinner = self.transformer.transform(data.inner)
        return data.replace(self, inner=newinner)
