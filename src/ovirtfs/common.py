import stat
import fuse


def dir_stat(nlink=1):
    fst = fuse.Stat()
    fst.st_mode = stat.S_IFDIR | 0o755
    fst.st_nlink = nlink
    return fst


def file_stat(size=0, mode=0o444):
    fst = fuse.Stat()
    fst.st_mode = stat.S_IFREG | mode
    fst.st_nlink = 1
    fst.st_size = size
    return fst


def link_stat():
    fst = fuse.Stat()
    fst.st_mode = stat.S_IFLNK | 0o755
    fst.st_nlink = 1
    return fst


def subpath(name, options=None):
    optstr = "|".join(options) if options else ""
    return "(?P<{}>[^/]*{})".format(name, optstr)
