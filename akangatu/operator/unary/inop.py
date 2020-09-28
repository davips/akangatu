from akangatu.container import Container1
from akangatu.innerchecking import EnsureInner
from transf.absdata import AbsData


class In(Container1):
    def _process_(self, data: AbsData):
        data = EnsureInner().process(data)
        newinner = self.step.process(data.inner)
        return data.replace(self, inner=newinner)
