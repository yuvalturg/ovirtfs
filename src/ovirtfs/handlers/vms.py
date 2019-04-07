from . import RootHandler
from ..resolver import PathResolver


@PathResolver("/vms")
class VMsHandler(RootHandler):
    _svc_name = "vms_service"
    _tag_name = "name"
