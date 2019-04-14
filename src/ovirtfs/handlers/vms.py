from . import BaseHandler, DirNameHandler, RawAttrFileHandler
from .root import RootHandler
from ..common import subpath
from ..resolver import PathResolver


class BaseVMsMixIn(object):
    _svc_name = "vms_service"


@PathResolver("vms", parent=RootHandler)
class RootVMsHandler(BaseVMsMixIn, BaseHandler):
    content = []


@PathResolver(subpath("name"), parent=RootVMsHandler)
class VMNameHandler(BaseVMsMixIn, DirNameHandler):
    content = []


@PathResolver(["id", "comment"], parent=VMNameHandler)
class VMFileHandler(BaseVMsMixIn, RawAttrFileHandler):
    pass
