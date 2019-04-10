from . import BaseHandler, DirNameHandler, FileHandler
from ..resolver import PathResolver


@PathResolver("/")
class RootHandler(DirNameHandler):
    content = []


@PathResolver("demofile", parent=RootHandler)
class DemoFileHandler(FileHandler):
    def _set_data(self, params):
        self._data = "ovirtfs is cool\n"
