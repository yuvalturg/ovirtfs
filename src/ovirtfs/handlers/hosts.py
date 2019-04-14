import errno
import logging

from . import BaseHandler, DirNameHandler, RawAttrFileHandler, SymlinkHandler
from .root import RootHandler
from ..common import subpath
from ..resolver import PathResolver


LOG = logging.getLogger(__name__)


class BaseHostMixIn(object):
    _svc_name = "hosts_service"


@PathResolver("hosts", parent=RootHandler)
class RootHostsHandler(BaseHostMixIn, BaseHandler):
    content = []


@PathResolver(subpath("name"), parent=RootHostsHandler)
class HostNameHandler(BaseHostMixIn, DirNameHandler):
    content = []


@PathResolver(["id", "comment"], parent=HostNameHandler)
class HostFileHandler(BaseHostMixIn, RawAttrFileHandler):
    pass


@PathResolver(["status"], parent=HostNameHandler)
class HostStatusHandler(BaseHostMixIn, RawAttrFileHandler):
    _mode = 0o644

    def write(self, buf, params):
        host = self._get_object(params)
        if not host:
            return -errno.ENOENT
        svc = self._service.host_service(host.id)
        val = buf.strip()
        if val in ("active", "up", "1"):
            LOG.debug("Activating host (%s)", host.name)
            svc.activate()
        elif val in ("inactive", "down", "0"):
            LOG.debug("Deactivating host (%s)", host.name)
            svc.deactivate()
        return len(buf)


@PathResolver("cluster", parent=HostNameHandler)
class HostClusterHandler(BaseHostMixIn, SymlinkHandler):
    _other_svc = "clusters_service"
    _my_attr = "cluster"
    _lnk_fmt = "../../clusters/{}"
