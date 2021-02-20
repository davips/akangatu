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
#  along with akangatu  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.
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
#  along with akangatu  If not, see <http://www.gnu.org/licenses/>.
#

import inspect
import json
import traceback
from abc import abstractmethod, ABC
from collections.abc import Iterable
from copy import copy
from functools import cached_property, lru_cache
from time import sleep

from garoupa.decorator import classproperty
from garoupa.uuid import UUID
from akangatu.transf.customjson import CustomJSONEncoder
from akangatu.transf.mixin.identification import withIdentification
from akangatu.transf.mixin.printing import withPrinting


class Step(withIdentification, withPrinting, ABC):
    """Transform data according to a configuration.

    Children classes should implement _held_()"""
    isclass = True
    isdi = True
    isdd = False
    isoperator = False

    def __init__(self, **config):
        self.isclass = False
        if "sample_" in dir(self):
            # noinspection PyUnresolvedReferences
            self.sample = self.sample_  # from the future (DDStep)
        self._config = config["config_func"] if "config_func" in config else config

    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        if cls.isdi and any(hasattr(arg, "parent_uuid") for arg in args):
            print(f"Args: {args}\n")
            print(f"Data independent step {instance.name} is not allowed to have data in constructor!")
            exit()

        if "sample_" in dir(instance):
            # noinspection PyUnresolvedReferences
            instance.sample = instance.sample_  # due to DDStep and DIStep, mas não lembro quem usa

        # TODO: ensure every tranformer always provides a full config (i.e. complete init with default values)
        instance._args_kwargs = args, kwargs
        return instance

    def _held_(self):
        """Detect which params were explicitly given."""
        args, kwargs = self._args_kwargs
        newargs = args[1:] if self.isdd else args
        extrakwargs = dict(zip(self.config, newargs))
        repeated = {k: v for k, v in extrakwargs.items() if k in kwargs}
        if repeated:
            print(
                f"Impossible to discover names by lookin at config keys. \nArgs: {args}\nHINT: Consider using "
                f"keyworded args. Conflicting:",
                repeated)
            exit()
        kwargs.update(extrakwargs)
        return {k: v for k, v in kwargs.items() if k in self.config}

    def _asdict_(self):
        return {"id": self.id, "desc": self.desc}

    ###@cached_property
    @property
    def desc(self):
        return {"name": self.name, "path": self.context, "config": self.config}

    ###@cached_property
    @property
    def asdict_rec(self):
        """Convert all internal steps as dict as well, recursively, if any is present at configs."""
        dic = self.asdict.copy()
        cfg = dic["desc"]["config"]
        if "step" in cfg and not isinstance(cfg["step"], dict):
            dic["desc"]["config"]["step"] = cfg["step"].asdict_rec
        if "steps" in cfg:
            dic["desc"]["config"]["steps"] = [
                step if isinstance(step, dict) else step.asdict_rec for step in cfg["steps"]
            ]
        return dic

    def process(self, data, aslist=False, exit_on_error=True, maxtime=None):
        # print(self.longname)
        if data is None:
            print("Cannot process None.\nHint: perhaps some nonexistent inner data is being passed around ",
                  self.longname)
            exit()
        if not hasattr(data, "parent_uuid"):
            if not isinstance(data, Iterable):
                raise Exception("Data or iterable expected! Not:", type(data))
            # TODO: precisa passar aslist pra frente?
            mapped = map(self._core_process_, data)
            return list(mapped) if aslist else mapped
        out = self._core_process_(data)  # TODO: como passar exit_on_error e maxtime pro data.update?
        # datauuid = (data and data.uuid) or UUID()
        # if out.uuid != datauuid * self.uuid:
        #     print("Inconsistence detected!", (datauuid * self.uuid), "!=", out.uuid, (datauuid * self.uuid).n, "!=", out.uuid.n)
        #     print(self.name)
        #     print(self)
        #     for i in data.history:
        #     print(i.name, i.id)
        #     print()
        #     for i in out.history:
        #     print(i.name, i.id)
        #     print()
        #     exit()
        return out

    ###@cached_property
    @property
    def inner(self):
        return self._inner_()

    ###@cached_property
    @property
    def config_json(self):  # TODO aproveitar esse str no withPrinting?
        return json.dumps(self.config, cls=CustomJSONEncoder, sort_keys=True, ensure_ascii=False)

    ###@cached_property
    @property
    def config(self):
        if not hasattr(self, "_config"):
            raise Exception("Missing _config, perhaps a step implementation is calling super() lately inside __init__(). Step to check:", self.longname)
        if callable(self._config):
            return self._config()  # For lazy configgers like File.
        else:
            return self._config

    # noinspection PyPropertyAccess
    def makeupuuid(self, uuid):
        temp = copy(self)
        temp.uuid = uuid
        temp.id = uuid.id
        return temp

    @abstractmethod
    def _inner_(self):
        pass

    @abstractmethod
    def _core_process_(self, data):
        pass

    def _name_(self):
        return self.__class__.__name__

    ###@cached_property
    @property
    def longname(self):
        return self._longname_()

    @abstractmethod
    def _longname_(self):
        pass

    def _context_(self):
        return self.__class__.__module__
        # return inspect.getmodule(inspect.stack()[1][0]).__name__

    def _uuid_(self):
        uuid = UUID(json.dumps(self.desc, sort_keys=True, ensure_ascii=False, cls=CustomJSONEncoder).encode())
        return uuid

    @staticmethod
    def fromdict(dic):
        """Rebuild a Step instance from a dict."""
        id_ = dic["id"]
        name, path, config = dic["desc"]["name"], dic["desc"]["path"], dic["desc"]["config"]
        if "step" in config:
            if "steps" in config:
                raise Exception("A serialized Step cannot have both step and steps in config!")
            config["step"] = Step.fromdict(config["step"])
        elif "steps" in config:
            config["steps"] = [Step.fromdict(step) for step in config["steps"]]
        klass = Step.get_class(path, name)
        # TODO 'step'(s) can be a parameter of some sklearn alg! it should be marked as reserved word
        try:
            # print("Reborning...", type(config), type(klass), config)
            # print("    reborning ", klass)
            reborn = klass(**config)
            if reborn.uuid.id != id_:
                print("Recreated Step with wrong UUID:", reborn.uuid, "\nShould be:", id_, type(reborn), type(id_))
            return reborn
        except Exception as e:
            print(e)
            raise Exception(f"Problems building fromdict {name}@{path} with config\n{config}")

    @staticmethod
    def get_class(module, class_name):
        import importlib

        # print("get_class >>> ", module, class_name)
        module = importlib.import_module(module)
        class_ = getattr(module, class_name)
        return class_

    def translate(self, exception, data):
        traceback.print_exc()
        print()
        sleep(0.05)
        if not isinstance(exception, MissingField):
            print("Please override 'def translate(self, exception, data)' if you want this exception to be seen as a 'failure'.")
        print(f"During step...   {self.longname}   ...the following exception occurred:\n\t"+str(exception))
        exit()

    ###@cached_property
    @property
    def pid(self):
        """UUID of the process/transformation performed by this step.

        NoOp steps override this to have have puuid=identity"""
        return self.puuid.id

    ###@cached_property
    @property
    def puuid(self):
        """UUID of the process/transformation performed by this step.

        NoOp steps override this to have have puuid=identity"""
        return self.uuid

    def __hash__(self):
        return id(self)

    ###@cached_property
    @property
    def dump(self):
        raise Exception("Not implemented!")

class MissingField(Exception):
    def __init__(self, msg, data, field):
        super().__init__(msg)
        self.data = data
        self.field = field
