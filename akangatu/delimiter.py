from akangatu.abs.marker import Marker


class Begin(Marker):  # HINT: dataclasses does not work inside operate(): "object type has no isclass attribute"
    def _longname_(self):
        return "{-" + self._transfuuid


class End(Marker):
    def _longname_(self):
        return self._transfuuid + "-}"
