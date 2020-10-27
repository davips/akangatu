from aiuna.content.data import Data
from akangatu.distep import DIStep
from transf.mixin.noop import asNoOp


class Forbid(asNoOp, DIStep):
    def __init__(self, field):
        super().__init__(field=field)
        self.field = field

    def _process_(self, data: Data):
        if self.field in data:
            print("Cannot proceed with data containg the field", self.field)
            exit()
        return data


class Ensure(asNoOp, DIStep):
    def __init__(self, field):
        super().__init__(field=field)
        self.field = field

    def _process_(self, data: Data):
        if self.field not in data:
            # raise Exception
            exit()
        return data  # TODO: esses caras não aparecem no hist, mas poderiam ter placeholders; vale a pena? só se o histórico fosse usado p/ reconstruir expression original
