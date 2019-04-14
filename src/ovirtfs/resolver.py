import re
import os.path
import logging

from .common import subpath
from .handlers import BaseHandler

LOG = logging.getLogger(__package__)


class PathResolver(object):
    _registry = {}
    _instances = {}

    def __init__(self, path, parent=None):
        self._parent = parent
        self._path = path

    def __call__(self, cls):
        class Wrapper(cls):
            if self._parent:
                if isinstance(self._path, list):
                    self._parent.content.extend(self._path)
                    self._path = os.path.realpath(self._parent.path + "/" +
                                                  subpath("attr", self._path))
                else:
                    self._parent.content.append(self._path)
                    self._path = os.path.realpath(self._parent.path + "/" +
                                                  self._path)
            path = self._path
            if issubclass(cls, BaseHandler):
                self._registry[re.compile(self._path + "$")] = cls
                LOG.debug("Registered class %s for path [%s]", cls, self._path)
            else:
                LOG.warn("Class %s is not a handler, skipping", cls)
        return Wrapper

    @staticmethod
    def parse(path, connection):
        for rpath, rcls in PathResolver._registry.items():
            #LOG.debug("CMP path=%s with rpath=%s", path, rpath.pattern)
            match = rpath.search(path)
            if not match:
                continue
            params = match.groupdict()
            params.update({"rawpath": path})
            if rcls not in PathResolver._instances:
                PathResolver._instances[rcls] = rcls(connection)
            return PathResolver._instances[rcls], params
        return None, None
