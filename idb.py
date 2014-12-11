# coding=utf-8

import os.path
from functools import wraps
from operator import attrgetter
from urlparse import urlparse

from db import DB
from IPython.core.magic import Magics, magics_class, line_magic


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
class SQLDB(Magics):
    _db = None

    @line_magic('db_connect')
    def conn(self, parameter_s):
        """Conenct to database in ipython shell.
        Examples::
            %db_connect
            %db_connect postgresql://user:pass@localhost:port/database
        """
        uri = urlparse(parameter_s)

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
    def db(self, parameter_s):
        return self._db

    @line_magic('save_credentials')
    @check_db
    def save_credentials(self, parameter_s):
        if not parameter_s:
            print '[ERROR]Please Specify credentials name'
        else:
            self._db.save_credentials(profile=parameter_s)
            print 'Save credentials [] successful!'.format(parameter_s[0])

    @line_magic('use_credentials')
    @check_db
    def use_credentials(self, credential):
        self._db = DB(profile=credential)
        return self._db

    @line_magic('table')
    @check_db
    def table(self, parameter_s):
        p = parameter_s.split()
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
    def find_column(self, parameter_s):
        p = parameter_s.split()
        if not parameter_s:
            print '[ERROR]Please Specify column wildcard'
        else:
            return self._db.find_column(*p)

    @line_magic('find_table')
    @check_db
    def find_table(self, parameter_s):
        if not parameter_s:
            print '[ERROR]Please Specify table wildcard'
        else:
            return self._db.find_table(parameter_s)

    @line_magic('query')
    @check_db
    def query(self, parameter_s):
        if not parameter_s:
            print '[ERROR]Please Specify sql query'
        else:
            return self._db.query(parameter_s)

    @line_magic('query_from_file')
    @check_db
    def query_from_file(self, parameter_s):
        if not parameter_s:
            print '[ERROR]Please Specify sql filepath'
        elif not os.path.exists(parameter_s):
            print '[ERROR]This file {} not exists'.format(parameter_s)
        else:
            return self._db.query_from_file(parameter_s)


def load_ipython_extension(ipython):
    ipython.register_magics(SQLDB)
