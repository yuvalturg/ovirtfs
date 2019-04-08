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
        handlers.init()
        self._connection = sdk.Connection(
            url='https://192.168.122.115/ovirt-engine/api',
            username='admin@internal',
            password='ovirt',
            insecure=True,
            debug=True,
        )

    def getattr(self, path):
        LOG.debug("getattr() called for path=(%s)", path)
        handler, args = PathResolver.get_handler_args(path, self._connection)
        if handler is None:
            return -errno.ENOENT
        try:
            return handler.getattr(args)
        except RuntimeError:
            LOG.error(traceback.format_exc())
            return -errno.ENOENT

    def readdir(self, path, offset):
        LOG.debug("readdir() called with path=(%s) offset=(%s)", path, offset)
        handler, args = PathResolver.get_handler_args(path, self._connection)
        entries = handler.readdir(args)
        for entry in entries:
            yield fuse.Direntry(entry)

    def open(self, path, flags):
        LOG.debug("open() called for path=(%s)", path)
        handler, _ = PathResolver.get_handler_args(path, self._connection)
        if handler is None:
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES
        return 0

    def read(self, path, size, offset):
        handler, args = PathResolver.get_handler_args(path, self._connection)
        if handler is None:
            return -errno.ENOENT
        data = handler.read(args)
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
        handler, args = PathResolver.get_handler_args(path, self._connection)
        if handler is None:
            return -errno.ENOENT
        try:
            return handler.readlink(args)
        except RuntimeError:
            LOG.error(traceback.format_exc())
            return -errno.ENOENT
