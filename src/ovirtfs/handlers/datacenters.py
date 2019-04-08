from . import RootHandler, DirNameHandler, RegFileHandler
from ..common import subpath
from ..resolver import PathResolver


class BaseDataCenterMixIn(object):
    _svc_name = "data_centers_service"


@PathResolver("/data_centers")
class RootDataCentersHandler(BaseDataCenterMixIn, RootHandler):
    pass


@PathResolver("/data_centers/{}".format(subpath("name")))
class DataCenterNameHandler(BaseDataCenterMixIn, DirNameHandler):
    files = ["id"]


@PathResolver("/data_centers/{}/{}".format(
    subpath("name"),
    subpath("action", DataCenterNameHandler.files)
    )
             )
class DataCenterFileHandler(BaseDataCenterMixIn, RegFileHandler):
    pass
