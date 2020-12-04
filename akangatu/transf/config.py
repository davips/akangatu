#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the akangatu.transf project.
#  Please respect the license. Removing authorship by any means
#  (by code make up or closing the sources) or ignoring property rights
#  is a crime and is unethical regarding the effort and time spent here.
#  Relevant employers or funding agencies will be notified accordingly.
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
from contextlib import contextmanager
from multiprocessing import Lock as PLock
from threading import Lock as TLock

# Some global state, so we need to make it thread-safe; with a context manager.
threadLock = TLock()
processLock = PLock()


@contextmanager
def safety():
    with threadLock, processLock:
        yield


try:
    with open("config.json", "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    CONFIG = {}

CACHE = {}


def globalcache(method):  # TODO: make it LRU
    """Cache for a hashable applied to a hashable object or str"""
    def wrapper(step, data):
        # global CACHE
        key = hash(step) + hash(data)
        if key in CACHE:
            return CACHE[key]
        CACHE[key] = method(step, data)
        return CACHE[key]

    return wrapper
