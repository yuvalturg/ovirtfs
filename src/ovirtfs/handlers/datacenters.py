from . import BaseHandler, DirNameHandler, RawAttrFileHandler
from .root import RootHandler
from ..common import subpath
from ..resolver import PathResolver


class BaseDataCenterMixIn(object):
    _svc_name = "data_centers_service"


@PathResolver("data_centers", parent=RootHandler)
class RootDataCentersHandler(BaseDataCenterMixIn, BaseHandler):
    content = []


@PathResolver(subpath("name"), parent=RootDataCentersHandler)
class DataCenterNameHandler(BaseDataCenterMixIn, DirNameHandler):
    content = []


@PathResolver(["id"], parent=DataCenterNameHandler)
class DataCenterFileHandler(BaseDataCenterMixIn, RawAttrFileHandler):
    pass
