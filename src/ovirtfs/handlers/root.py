from . import DirNameHandler
from ..resolver import PathResolver


@PathResolver("/")
class RootHandler(DirNameHandler):
    content = []
