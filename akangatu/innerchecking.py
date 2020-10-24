from aiuna.content.data import Data
from akangatu.distep import DIStep
from transf.mixin.config import asConfigLess
from transf.mixin.noop import asNoOp


class EnsureNoInner(asNoOp, asConfigLess, DIStep):
    def _process_(self, data: Data):
        if data.hasinner:
            print("Cannot proceed with inner data!", data.inner.id)
            exit()
        return data


class EnsureInner(asNoOp, asConfigLess, DIStep):
    def _process_(self, data: Data):
        if not data.hasinner:
            print("Cannot proceed without inner data!\n", data.id, ":", data.history ^ "longname")
            # raise Exception
            exit()
        return data  # TODO: esses caras não aparecem no hist, mas poderiam ter placeholders; vale a pena? só se o histórico fosse usado p/ reconstruir expression original
