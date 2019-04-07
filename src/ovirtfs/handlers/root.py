from . import DirNameHandler
from ..resolver import PathResolver


@PathResolver("/")
class SlashdotHandler(DirNameHandler):
    dirs = ["hosts", "clusters", "vms", "datacenters"]
