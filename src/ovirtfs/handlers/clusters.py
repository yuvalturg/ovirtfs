from . import BaseHandler, RootHandler
from ..common import subpath, dir_stat, file_stat, link_stat
from ..resolver import PathResolver


@PathResolver("/clusters")
class ClustersHandler(RootHandler):
    _svc_name = "clusters_service"
    _tag_name = "name"


class BaseClusterHandler(BaseHandler):
    def __init__(self, connection):
        self._service = connection.system_service().clusters_service()

    def _get_cluster(self, args):
        fltr = "name=%s" % args["name"]
        clusters = self._service.list(search=fltr)
        if not clusters:
            raise RuntimeError("Missing cluster %s" % args)
        return clusters[0]


@PathResolver("/clusters/{}".format(subpath("name")))
class ClusterNameHandler(BaseClusterHandler):
    files = ["id"]
    links = ["datacenter"]
    dirs = []

    def getattr(self, args):
        self._get_cluster(args)
        return dir_stat()

    def readdir(self, args):
        return self.files + self.links + self.dirs


@PathResolver("/clusters/{}/{}".format(
                subpath("name"),
                subpath("action", ClusterNameHandler.files)
                )
             )
class ClusterFilesHandler(BaseClusterHandler):
    def _get_value(self, args):
        cluster = self._get_cluster(args)
        return str(getattr(cluster, args["action"])) + "\n"

    def getattr(self, args):
        return file_stat(size=len(self._get_value(args)))

    def read(self, args):
        return self._get_value(args)


@PathResolver("/clusters/{}/datacenter".format(subpath("name")))
class ClusterDCHandler(BaseClusterHandler):
    def __init__(self, connection):
        BaseClusterHandler.__init__(self, connection)
        self._dc_svc = connection.system_service().data_centers_service()

    def getattr(self, args):
        return link_stat()

    def readlink(self, args):
        datacenter = self._get_cluster(args).data_center
        datacenters = self._dc_svc.list()
        name = [x.name for x in datacenters if x.id == datacenter.id][0]
        return "../datacenters/{}".format(name)
