from . import RootHandler, DirNameHandler, RegFileHandler
from ..common import subpath
from ..resolver import PathResolver


class BaseStorageDomainMixIn(object):
    _svc_name = "storage_domains_service"


@PathResolver("/storage_domains")
class StorageDomainsHandler(BaseStorageDomainMixIn, RootHandler):
    pass


@PathResolver("/storage_domains/{}".format(subpath("name")))
class StorageDomainNameHandler(BaseStorageDomainMixIn, DirNameHandler):
    files = ["id"]


@PathResolver("/storage_domains/{}/{}".format(
    subpath("name"),
    subpath("action", StorageDomainNameHandler.files)
    )
             )
class StorageDomainFileHandler(BaseStorageDomainMixIn, RegFileHandler):
    pass
