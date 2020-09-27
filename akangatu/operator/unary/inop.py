from akangatu.container import Container1
from transf.absdata import AbsData


class In(Container1):
    def _process_(self, data: AbsData):
        newinner = self.step.process(data.inner)
        return data.replace(self, inner=newinner)
