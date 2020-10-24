from aiuna.content.data import Data
from akangatu.container import Container1
from akangatu.innerchecking import EnsureInner


class In(Container1):
    def _process_(self, data: Data):
        data = EnsureInner().process(data)
        newinner = lambda: self.step.process(data.inner)
        return data.update(self, inner=newinner)
