# Add sampling and operators to Ins
import transf._ins as tomonkeypatch
from akangatu.insert import Insert
tomonkeypatch.Ins = Insert

# Populate namespace with custom operators for dynamic screening / inspection.
from akangatu.operator.binary.chain import Chain
from akangatu.operator.binary.stream import Stream
