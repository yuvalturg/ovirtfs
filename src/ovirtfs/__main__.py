import sys
import logging
import fuse

from .ovirtfs import OVirtFS

fuse.fuse_python_api = (0, 2)


def main():
    usage = "Userpace filesystem for oVirt environments" + fuse.Fuse.fusage
    server = OVirtFS(version="%prog " + fuse.__version__,
                     usage=usage, dash_s_do='setsingle')
    server.parser.add_option(mountopt="fqdn", metavar="FQDN",
                             default=server.username,
                             help="oVirt engine FQDN")
    server.parser.add_option(mountopt="username", metavar="USERNAME",
                             help="oVirt administrator username")
    server.parser.add_option(mountopt="password", metavar="PASSWORD",
                             help="oVirt administrator password")
    server.parse(values=server, errex=1)
    server.initialize()
    server.main()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    main()
