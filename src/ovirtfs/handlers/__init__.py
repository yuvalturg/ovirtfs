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

    def _get_object(self, args):
        if not self._service:
            return None
        fltr = "name=%s" % args["name"]
        objects = self._service.list(search=fltr)
        if not objects:
            raise RuntimeError("Missing object %s" % args)
        return objects[0]


class RootHandler(BaseHandler):
    def getattr(self, args):
        return dir_stat()

    def readdir(self, _):
        return [getattr(x, self._tag_name) for x in self._service.list()]


class DirNameHandler(BaseHandler):
    files = []
    links = []
    dirs = []

    def getattr(self, args):
        self._get_object(args)
        return dir_stat()

    def readdir(self, _):
        return self.files + self.links + self.dirs


class RegFileHandler(BaseHandler):
    def _get_value(self, args):
        host = self._get_object(args)
        return str(getattr(host, args["action"])) + "\n"

    def getattr(self, args):
        return file_stat(size=len(self._get_value(args)))

    def read(self, args):
        return self._get_value(args)


class SymlinkHandler(BaseHandler):
    _other_svc = None
    _my_attr = None
    _cmp_attr = "id"
    _ret_attr = "name"
    _lnk_fmt = None

    def __init__(self, connection):
        BaseHandler.__init__(self, connection)
        self._other_svc = getattr(connection.system_service(),
                                  self._other_svc)()

    def getattr(self, args):
        return link_stat()

    def readlink(self, args):
        obj = getattr(self._get_object(args), self._my_attr)
        objects = self._other_svc.list()
        val = [getattr(x, self._ret_attr) for x in objects if
               getattr(x, self._cmp_attr) == getattr(obj, self._cmp_attr)][0]
        return self._lnk_fmt.format(val)


def init():
    for _, modname, ispkg in pkgutil.iter_modules(__path__):
        LOG.debug("Found submodule %s (is a package: %s)", modname, ispkg)
        __import__(str(__package__) + "." + modname, fromlist="dummy")
