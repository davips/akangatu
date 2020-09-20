# Add sampling and operators to Ins
import transf._ins as tomonkeypatch
from akangatu.ins import Ins
tomonkeypatch.Ins = Ins

# Populate namespace with custom operators for dynamic screening / inspection.
from akangatu.operator.binary.chain import Chain
from akangatu.operator.binary.stream import Stream
