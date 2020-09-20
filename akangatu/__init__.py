import transf._ins as tomonkeypatch
from akangatu.ins import Ins

# Add sampling and operators to Ins
tomonkeypatch.Ins = Ins
