from . import BaseHandler, DirNameHandler, RegFileHandler, SymlinkHandler
from .root import RootHandler
from ..common import subpath
from ..resolver import PathResolver


class BaseHostMixIn(object):
    _svc_name = "hosts_service"


@PathResolver("hosts", parent=RootHandler)
class RootHostsHandler(BaseHostMixIn, BaseHandler):
    content = []


@PathResolver(subpath("name"), parent=RootHostsHandler)
class HostNameHandler(BaseHostMixIn, DirNameHandler):
    content = []


@PathResolver(["id", "comment"], parent=HostNameHandler)
class HostFileHandler(BaseHostMixIn, RegFileHandler):
    pass


@PathResolver("cluster", parent=HostNameHandler)
class HostClusterHandler(BaseHostMixIn, SymlinkHandler):
    _other_svc = "clusters_service"
    _my_attr = "cluster"
    _lnk_fmt = "../../clusters/{}"
