# coding=utf-8

import os.path
from functools import wraps
from operator import attrgetter
from urlparse import urlparse

from db import DB
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.config.configurable import Configurable


def get_or_none(attr):
    return attr if attr else None


def check_db(func):
    @wraps(func)
    def deco(*args):
        if args[0]._db is None:
            print '[ERROR]Please make connection: `con = %db_connect xx` or `%use_credentials xx` first!'  # noqa
            return
        return func(*args)
    return deco


@magics_class
class SQLDB(Magics, Configurable):
    _db = None

    def __init__(self, shell):
        Configurable.__init__(self, config=shell.config)
        Magics.__init__(self, shell=shell)
        self.shell.configurables.append(self)

    @line_magic('db_connect')
    def conn(self, line):
        """Conenct to database in ipython shell.
        Examples::
            %db_connect
            %db_connect postgresql://user:pass@localhost:port/database
        """
        uri = urlparse(line)

        if not uri.scheme:
            params = {
                'dbtype': 'sqlite',
                'filename': os.path.join(os.path.expanduser('~'), 'db.sqlite')
            }
        elif uri.scheme == 'sqlite':
            params = {
                'dbtype': 'sqlite',
                'filename': uri.path
            }
        else:
            params = {
                'username': get_or_none(uri.username),
                'password': get_or_none(uri.password),
                'hostname': get_or_none(uri.hostname),
                'port': get_or_none(uri.port),
                'dbname': get_or_none(uri.path[1:])
            }

        self._db = DB(**params)

        return self._db

    @line_magic('db')
    def db(self, line):
        return self._db

    @line_magic('save_credentials')
    @check_db
    def save_credentials(self, line):
        if not line:
            print '[ERROR]Please Specify credentials name'
        else:
            self._db.save_credentials(profile=line)
            print 'Save credentials [] successful!'.format(line[0])

    @line_magic('use_credentials')
    @check_db
    def use_credentials(self, credential):
        self._db = DB(profile=credential)
        return self._db

    @line_magic('table')
    @check_db
    def table(self, line):
        p = line.split()
        l = len(p)
        if l == 1:
            if not p[0]:
                return self._db.tables
            else:
                return attrgetter(p[0])(self._db.tables)
        else:
            data = self._db.tables
            for c in p:
                if c in ['head', 'sample', 'unique', 'count', 'all', 'query']:
                    data = attrgetter(c)(data)()
                else:
                    data = attrgetter(c)(data)
            return data

    @line_magic('find_column')
    @check_db
    def find_column(self, line):
        p = line.split()
        if not line:
            print '[ERROR]Please Specify column wildcard'
        else:
            return self._db.find_column(*p)

    @line_magic('find_table')
    @check_db
    def find_table(self, line):
        if not line:
            print '[ERROR]Please Specify table wildcard'
        else:
            return self._db.find_table(line)

    @line_magic('query')
    @check_db
    def query(self, line):
        if not line:
            print '[ERROR]Please Specify sql query'
        else:
            return self._db.query(line)

    @line_magic('query')
    @check_db
    def query_from_file(self, line):
        if not line:
            print '[ERROR]Please Specify sql filepath'
        else:
            return self._db.query_from_file(line)


def load_ipython_extension(ipython):
    ipython.register_magics(SQLDB)
