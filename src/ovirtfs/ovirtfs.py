import os
import errno
import traceback
import logging
import fuse

import ovirtsdk4 as sdk

from . import handlers
from .resolver import PathResolver

LOG = logging.getLogger(__package__)


class OVirtFS(fuse.Fuse):
    def __init__(self, *args, **kwargs):
        fuse.Fuse.__init__(self, *args, **kwargs)
        self.fqdn = None
        self.username = None
        self.password = None
        self._connection = None

    def initialize(self):
        handlers.init()
        self._connection = sdk.Connection(
            url='https://{}/ovirt-engine/api'.format(self.fqdn),
            username='{}@internal'.format(self.username),
            password=self.password,
            insecure=True,
            debug=True,
        )

    def getattr(self, path):
        LOG.debug("getattr() called for path=(%s)", path)
        handler, params = PathResolver.parse(path, self._connection)
        if handler is None:
            return -errno.ENOENT
        try:
            return handler.getattr(params)
        except RuntimeError:
            LOG.error(traceback.format_exc())
            return -errno.ENOENT

    def readdir(self, path, offset):
        LOG.debug("readdir() called with path=(%s) offset=(%s)", path, offset)
        handler, params = PathResolver.parse(path, self._connection)
        entries = handler.readdir(params)
        for entry in entries:
            yield fuse.Direntry(entry)

    def open(self, path, flags):
        LOG.debug("open() called for path=(%s)", path)
        handler, _ = PathResolver.parse(path, self._connection)
        if handler is None:
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES
        return 0

    def read(self, path, size, offset):
        handler, params = PathResolver.parse(path, self._connection)
        if handler is None:
            return -errno.ENOENT
        data = handler.read(params)
        slen = len(data)
        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = data[offset:offset+size]
        else:
            buf = ""
        return buf

    def readlink(self, path):
        LOG.debug("readlink() called for path=(%s)", path)
        handler, params = PathResolver.parse(path, self._connection)
        if handler is None:
            return -errno.ENOENT
        try:
            return handler.readlink(params)
        except RuntimeError:
            LOG.error(traceback.format_exc())
            return -errno.ENOENT
