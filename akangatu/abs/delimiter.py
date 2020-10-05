from abc import abstractmethod, ABC
from functools import cached_property

from akangatu.container import Container1
from akangatu.rev import Rev
from transf.absdata import AbsData
from transf.mixin.noop import asNoOp


class BadStep(Exception):
    """Ill-implemented Step"""


class Delimiter(asNoOp, Container1, ABC):
    """Only internal step and its reverse are visible

    step should be a marker (mixed in with asMarker).
    Misleading indentity uuid will emerge otherwise."""

    # REMINDER?: should be asNoOp since the important UUIDs stay within Data history.
    # REMINDER: cannot be asNoOp since the process should appear in history as self
    # CONCLUSION: it is impossible to have a uuid different from history,
    # that's why chain and all noop disappear, e nem faria sentido aparecer idmat no historico,
    # marker seria a grande exceção que teria efeito nulo mas precisa aparecer.
    # SOLUTION: the implementer/user should Rev the marker
    # FINAL: we provide both visible and invisible versions of the marker
    def _process_(self, data: AbsData):
        from akangatu.marker import asMarker
        if not issubclass(self.wrapper, asMarker):
            raise BadStep("Step for a reversed Marker should be mixed in with asMarker")
        wrapped = self.wrapper(self.step)
        return (wrapped * Rev(wrapped)).process(data)

    @cached_property
    def wrapper(self):
        return self._wrapper_()

    @abstractmethod
    def _wrapper_(self):
        pass


class Begin(Delimiter):
    def _wrapper_(self):
        from akangatu.marker import B
        return B


class End(Delimiter):
    def _wrapper_(self):
        from akangatu.marker import E
        return E
