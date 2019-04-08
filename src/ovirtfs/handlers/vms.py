from . import BaseHandler
from .root import RootHandler
from ..resolver import PathResolver


class BaseVMsMixIn(object):
    _svc_name = "vms_service"


@PathResolver("vms", parent=RootHandler)
class RootVMsHandler(BaseVMsMixIn, BaseHandler):
    content = []
