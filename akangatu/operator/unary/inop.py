from aiuna.content.data import Data
from akangatu.container import Container1
from akangatu.fieldchecking import Ensure


class In(Container1):
    def _process_(self, data: Data):
        data = Ensure("inner").process(data)
        newinner = lambda: self.step.process(data.inner)
        return data.update(self, inner=newinner)
