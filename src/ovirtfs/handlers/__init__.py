import os
import pkgutil
import logging

from ..common import dir_stat, file_stat, link_stat

LOG = logging.getLogger(__package__)


class BaseHandler(object):
    _svc_name = None
    _tag_name = "name"

    def __init__(self, connection):
        self._service = None
        if self._svc_name:
            self._service = getattr(connection.system_service(),
                                    self._svc_name)()

    def _get_object(self, params):
        if not self._service:
            return None
        fltr = "{}={}".format(self._tag_name, params[self._tag_name])
        objects = self._service.list(search=fltr)
        if not objects:
            raise RuntimeError("Missing object %s" % params)
        return objects[0]

    def getattr(self, params):
        return dir_stat()

    def readdir(self, _):
        return [getattr(x, self._tag_name) for x in self._service.list()]


class DirNameHandler(BaseHandler):
    content = []

    def getattr(self, params):
        self._get_object(params)
        return dir_stat()

    def readdir(self, _):
        return self.content


class FileHandler(BaseHandler):
    def __init__(self, connection):
        BaseHandler.__init__(self, connection)
        self._data = None
        self._length = 0

    def getattr(self, params):
        self._set_data(params)
        return file_stat(size=len(self._data))

    def read(self, params):
        return self._data


class RawAttrFileHandler(FileHandler):
    def _set_data(self, params):
        obj = self._get_object(params)
        self._data = str(getattr(obj, params["attr"])) + "\n"


class SymlinkHandler(BaseHandler):
    _other_svc = None
    _my_attr = None # link name
    _cmp_attr = "id"
    _ret_attr = "name"
    _lnk_fmt = None # link target

    def __init__(self, connection):
        BaseHandler.__init__(self, connection)
        self._other_svc = getattr(connection.system_service(),
                                  self._other_svc)()

    def getattr(self, params):
        return link_stat()

    def readlink(self, params):
        obj = getattr(self._get_object(params), self._my_attr)
        objects = self._other_svc.list()
        val = [getattr(x, self._ret_attr) for x in objects if
               getattr(x, self._cmp_attr) == getattr(obj, self._cmp_attr)][0]
        return self._lnk_fmt.format(val)


def init():
    for _, modname, ispkg in pkgutil.iter_modules(__path__):
        LOG.debug("Found submodule %s (is a package: %s)", modname, ispkg)
        __import__(str(__package__) + "." + modname, fromlist="dummy")
