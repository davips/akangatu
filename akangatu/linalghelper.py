#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the akangatu project.
#  Please respect the license - more about this in the section (*) below.
#
#  akangatu is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  akangatu is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with akangatu.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.
#
#
#  akangatu.transf is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  akangatu.transf is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with akangatu.transf.  If not, see <http://www.gnu.org/licenses/>.
#

import json
from types import GeneratorType, FunctionType
from typing import Optional, Iterator

import numpy as np  # type: ignore
from numpy import ndarray

from garoupa.uuid import UUID


def _as_vector(mat: ndarray) -> ndarray:
    size = max(mat.shape[0], mat.shape[1])
    try:
        return mat.reshape(size)
    except Exception as e:
        print(f"Expecting a matrix {mat}, with a single row or column, i.e. as a column-vector or a row-vector...")
        exit()


def _as_column_vector(vec: ndarray) -> ndarray:
    return vec.reshape(len(vec), 1)


def mat2vec(m: ndarray, default: ndarray = None) -> ndarray:
    return default if m is None else _as_vector(m)


def _mat2sca(m: ndarray, default: float = None) -> Optional[float]:
    return default if m is None else m[0][0]


def field_as_matrix(name, field_value):
    """Given a field, return its corresponding matrix or itself if it is a list."""

    # Special fields.
    if name in ["inner", "stream"]:
        return field_value

    # Matrix given directly.
    if isinstance(field_value, ndarray) and len(field_value.shape) == 2:
        return field_value

    # Vector.
    if isinstance(field_value, ndarray) and len(field_value.shape) == 1:
        return _as_column_vector(field_value)

    # Scalar.
    if isinstance(field_value, int):
        return np.array(field_value, ndmin=2)

    # Still unevaluated.
    if islazy(field_value):
        return field_value

    # Other types.
    if isinstance(field_value, (list, Iterator)):  # GeneratorType, map
        return field_value

    print(f"{name} has unknown field type: ", type(field_value))
    raise Exception(f"{name} has unknown field type: ", type(field_value), "shape:", field_value.shape)


def islazy(field):
    return isinstance(field, FunctionType) and not isinstance(field, GeneratorType)


def fields2matrices(fields):
    matrices = {}
    for name, value in fields.items():
        if len(name) == 1:
            name = name.upper()
        matrices[name] = field_as_matrix(name, value)
    return matrices


# def evolve(uuid, steps):
#     for step in steps:
#     uuid *= step.uuid
#     return uuid


def evolve_id(uuid, uuids, step, fields):
    """Return UUID/UUIDs after transformations."""

    # Update matrix UUIDs.
    uuids_ = uuids.copy()
    for name, value in fields.items():
        # If it is a new matrix, assign a UUID for its birth.
        if name in uuids:
            muuid = uuids[name]
        else:  # fallback options:
            if uuid == UUID():  # whole data creation (e.g. from File; remember that fields are not lazy in this case)
                muuid = UUID(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
                             if isinstance(value, list) else value.tobytes())
            else:
                # only matrix creation (avoids packing for transformations aside from New/File etc)
                # It is expected that fields resulting from real transformations will not repeat by chance,
                # so we there is no concern about wasting storage/bandwidth sending identical contents with different uuids.
                # Such situation is impossible in practice, unless for really small/trivial contents.
                muuid = uuid * UUID(bytes(name, "latin1"))

        # Transform UUID.
        muuid *= step.uuid
        uuids_[name] = muuid

    # Update UUID.
    uuid *= step.uuid

    return uuid, uuids_
