from akangatu.distep import DIStep
from transf.absdata import AbsData
from transf.mixin.noop import asNoOp


class EnsureNoInner(asNoOp, DIStep):
    def __init__(self):
        super().__init__({})

    def _process_(self, data: AbsData):
        if data.inner:
            print("Cannot proceed with inner data!", data.inner.id)
            exit()
        return data


class EnsureInner(asNoOp, DIStep):
    def __init__(self):
        super().__init__({})

    def _process_(self, data: AbsData):
        if not data.inner:
            print("Cannot proceed without inner data!\n", data.id, ":", data.history)
            exit()
        return data  # TODO: esses caras não aparecem no hist, mas poderiam ter placeholders; vale a pena? só se o histórico fosse usado p/ reconstruir expression original
