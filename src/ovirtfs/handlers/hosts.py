import logging

from . import RootHandler, DirNameHandler, RegFileHandler, SymlinkHandler
from ..common import subpath
from ..resolver import PathResolver

LOG = logging.getLogger(__package__)


class BaseHostMixIn(object):
    _svc_name = "hosts_service"


@PathResolver("/hosts")
class RootHostsHandler(BaseHostMixIn, RootHandler):
    pass


@PathResolver("/hosts/{}".format(subpath("name")))
class HostNameHandler(BaseHostMixIn, DirNameHandler):
    files = ["status", "address", "comment", "id"]
    links = ["cluster"]


@PathResolver("/hosts/{}/{}".format(
    subpath("name"),
    subpath("action", HostNameHandler.files)
    )
             )
class HostFileHandler(BaseHostMixIn, RegFileHandler):
    pass


@PathResolver("/hosts/{}/cluster".format(subpath("name")))
class HostClusterHandler(BaseHostMixIn, SymlinkHandler):
    _other_svc = "clusters_service"
    _my_attr = "cluster"
    _lnk_fmt = "../clusters/{}"
