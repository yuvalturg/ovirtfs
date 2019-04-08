from . import BaseHandler, DirNameHandler, RegFileHandler
from ..resolver import PathResolver


@PathResolver("/")
class RootHandler(DirNameHandler):
    content = []


@PathResolver("demofile", parent=RootHandler)
class DemoFileHandler(RegFileHandler):
    def _get_value(self, params):
        return "ovirtfs is cool\n"
