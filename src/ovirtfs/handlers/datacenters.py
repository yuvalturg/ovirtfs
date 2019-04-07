from . import BaseHandler, RootHandler
from ..common import subpath, dir_stat
from ..resolver import PathResolver


@PathResolver("/datacenters")
class DataCentersHandler(RootHandler):
    _svc_name = "data_centers_service"
    _tag_name = "name"


@PathResolver("/datacenters/{}".format(subpath("name")))
class DCNameHandler(BaseHandler):
    def __init__(self, connection):
        self._service = connection.system_service().data_centers_service()

    def getattr(self, args):
        return dir_stat()

    def readdir(self, args):
        return []
