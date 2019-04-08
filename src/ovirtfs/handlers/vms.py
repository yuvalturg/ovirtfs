from . import RootHandler
from ..resolver import PathResolver


class BaseVMsMixIn(object):
    _svc_name = "vms_service"


@PathResolver("/vms")
class RootVMsHandler(BaseVMsMixIn, RootHandler):
    pass
