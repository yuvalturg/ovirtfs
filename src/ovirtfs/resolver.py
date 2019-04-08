import re
import logging

from .handlers import BaseHandler

LOG = logging.getLogger(__package__)


class PathResolver(object):
    _registry = {}
    _instances = {}

    def __init__(self, path):
        self._path = path

    def __call__(self, cls):
        class Wrapper(cls):
            cls.path = self._path
            if issubclass(cls, BaseHandler):
                self._registry[re.compile(self._path + "$")] = cls
                LOG.debug("Registered class %s for path [%s]", cls, self._path)
            else:
                LOG.warn("Class %s is not a handler, skipping", cls)
        return Wrapper

    @staticmethod
    def parse(path, connection):
        for rpath, rcls in PathResolver._registry.items():
            match = rpath.search(path)
            if not match:
                continue
            params = match.groupdict()
            LOG.debug("Handler %s for [%s], params=%s", rcls, path, params)
            if rcls not in PathResolver._instances:
                PathResolver._instances[rcls] = rcls(connection)
            return PathResolver._instances[rcls], params
        LOG.error("Handler was not found for path [%s]", path)
        return None, None
