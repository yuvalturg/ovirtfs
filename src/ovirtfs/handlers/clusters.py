from . import RootHandler, DirNameHandler, RegFileHandler, SymlinkHandler
from ..common import subpath
from ..resolver import PathResolver


class BaseClusterMixIn(object):
    _svc_name = "clusters_service"


@PathResolver("/clusters")
class RootClustersHandler(BaseClusterMixIn, RootHandler):
    pass


@PathResolver("/clusters/{}".format(subpath("name")))
class ClusterNameHandler(BaseClusterMixIn, DirNameHandler):
    files = ["id"]
    links = ["data_center"]


@PathResolver("/clusters/{}/{}".format(
    subpath("name"),
    subpath("action", ClusterNameHandler.files)
    )
             )
class ClusterFileHandler(BaseClusterMixIn, RegFileHandler):
    pass


@PathResolver("/clusters/{}/data_center".format(subpath("name")))
class ClusterDataCenterHandler(BaseClusterMixIn, SymlinkHandler):
    _other_svc = "data_centers_service"
    _my_attr = "data_center"
    _lnk_fmt = "../../data_centers/{}"
