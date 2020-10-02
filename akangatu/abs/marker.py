from akangatu.container import Container1
from akangatu.rev import Rev
from transf.absdata import AbsData


class Marker(Container1):  # REMINDER: asNoOp aqui faria perder a identidade quando armazenado.
    def _process_(self, data: AbsData):
        return data.replace(self).replace(Rev(self))
