#
# ovirtfs -- The oVirt filesystem
#

pyovirtfsdir = $(pythondir)/@PACKAGE_NAME@
pyovirtfshandlersdir = $(pyovirtfsdir)/handlers


dist_pyovirtfs_PYTHON = \
	$(srcdir)/src/ovirtfs/*.py


dist_pyovirtfshandlers_PYTHON = \
	$(srcdir)/src/ovirtfs/handlers/*.py


dist_sbin_SCRIPTS = \
	$(srcdir)/scripts/mount.ovirtfs


dist_noinst_DATA = \
    LICENSE \
    ovirtfs.spec \
    $(NULL)

EXTRA_DIST = \
	autogen.sh \
	README.md \
	LICENSE \
	AUTHORS \
	$(NULL)

DISTCLEANFILES = \
    $(srcdir)/config.log \
	$(srcdir)/config.status \
    $(srcdir)/Makefile.in \
    $(srcdir)/configure \
    $(srcdir)/install-sh \
	$(srcdir)/missing \
    $(srcdir)/py-compile \
    $(srcdir)/config.guess \
	$(srcdir)/config.sub \
    $(srcdir)/aclocal.m4 \
    $(NULL)

rpm: dist
	rpmbuild -ta *.xz

check:
	@echo "[CHECK] pyflakes"
	find . -xdev -name \*.py | xargs pyflakes
	@echo "[CHECK] pylint"
	find . -xdev -name \*.py | xargs pylint-2
	@echo "[CHECK] pep8"
	find . -xdev -name \*.py | xargs pep8


clean-local:
	-rm -rf autom4te.cache *.tar.xz
	-find -name "*.pyc" -exec rm -f {} \;
