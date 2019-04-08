from . import BaseHandler, DirNameHandler, RegFileHandler, SymlinkHandler
from .root import RootHandler
from ..common import subpath
from ..resolver import PathResolver


class BaseClusterMixIn(object):
    _svc_name = "clusters_service"


@PathResolver("clusters", parent=RootHandler)
class RootClustersHandler(BaseClusterMixIn, BaseHandler):
    content = []


@PathResolver(subpath("name"), parent=RootClustersHandler)
class ClusterNameHandler(BaseClusterMixIn, DirNameHandler):
    content = []


@PathResolver(["id"], parent=ClusterNameHandler)
class ClusterFileHandler(BaseClusterMixIn, RegFileHandler):
    pass


@PathResolver("data_center", parent=ClusterNameHandler)
class ClusterDataCenterHandler(BaseClusterMixIn, SymlinkHandler):
    _other_svc = "data_centers_service"
    _my_attr = "data_center"
    _lnk_fmt = "../../data_centers/{}"
