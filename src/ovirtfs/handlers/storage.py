from . import BaseHandler, DirNameHandler, RawAttrFileHandler
from .root import RootHandler
from ..common import subpath
from ..resolver import PathResolver


class BaseStorageDomainMixIn(object):
    _svc_name = "storage_domains_service"


@PathResolver("storage_domains", parent=RootHandler)
class StorageDomainsHandler(BaseStorageDomainMixIn, BaseHandler):
    content = []


@PathResolver(subpath("name"), parent=StorageDomainsHandler)
class StorageDomainNameHandler(BaseStorageDomainMixIn, DirNameHandler):
    content = []


@PathResolver(["id"], parent=StorageDomainNameHandler)
class StorageDomainFileHandler(BaseStorageDomainMixIn, RawAttrFileHandler):
    pass
