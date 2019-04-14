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
        handler, params = PathResolver.parse(path, self._connection)
        LOG.debug("Getting attributes with %s, params=%s", handler, params)
        if handler is None:
            return -errno.ENOENT
        try:
            return handler.getattr(params)
        except RuntimeError:
            LOG.error(traceback.format_exc())
            return -errno.ENOENT

    def readdir(self, path, offset):
        handler, params = PathResolver.parse(path, self._connection)
        LOG.debug("Reading directory with %s, params=%s", handler, params)
        entries = handler.readdir(params)
        for entry in entries:
            yield fuse.Direntry(entry)

    def open(self, path, flags):
        handler, params = PathResolver.parse(path, self._connection)
        LOG.debug("Opening file with %s, params=%s", handler, params)
        if handler is None:
            return -errno.ENOENT
        # TODO - check modes
        # accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        # if (flags & accmode) != os.O_RDONLY:
        #     return -errno.EACCES
        return 0

    def read(self, path, size, offset):
        handler, params = PathResolver.parse(path, self._connection)
        LOG.debug("Reading file with %s, params=%s", handler, params)
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

    def truncate(self, path, size):
        handler, params = PathResolver.parse(path, self._connection)
        LOG.debug("Truncate called for handler=%s, params=%s", handler, params)
        if handler is None:
            return -errno.ENOENT
        return 0

    def write(self, path, buf, offset):
        handler, params = PathResolver.parse(path, self._connection)
        LOG.debug("Writing to file handler=%s, params=%s", handler, params)
        if handler is None:
            return -errno.ENOENT
        try:
            return handler.write(buf, params)
        except RuntimeError:
            return -errno.EINVAL

    def readlink(self, path):
        handler, params = PathResolver.parse(path, self._connection)
        LOG.debug("Reading symlink with %s, params=%s", handler, params)
        if handler is None:
            return -errno.ENOENT
        try:
            return handler.readlink(params)
        except RuntimeError:
            LOG.error(traceback.format_exc())
            return -errno.ENOENT

    def rename(self, old, new):
        old_h, old_p = PathResolver.parse(old, self._connection)
        new_h, new_p = PathResolver.parse(new, self._connection)
        LOG.debug("Rename %s -> %s with %s and %s", old, new, old_h, new_h)
        if None in (old_h, new_h):
            return -errno.EINVAL
        try:
            return old_h.rename(new_h, old_p, new_p)
        except RuntimeError:
            LOG.error(traceback.format_exc())
            return -errno.EINVAL
