# coding=utf-8

from operator import attrgetter
from urlparse import urlparse

from db import DB
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.config.configurable import Configurable


def get_or_none(attr):
    return attr if attr else None


def check_db(func):
    def deco(*args):
        if func.im_class._db is None:
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
                'filename': '~/db.sqlite'
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

    @line_magic('save_credentials')
    @check_db
    def save_credentials(self, line):
        if not line:
            print '[ERROR]Please Specify credentials name'
        else:
            self._db.save_credentials(profile=line)
            print 'Save credentials [] successful!'.format(line)

    @line_magic('use_credentials')
    @check_db
    def use_credentials(self, credential):
        self._db = DB(profile=credential)
        return self._db

    @line_magic('table')
    @check_db
    def table(self, *line):
        l = len(line)
        if not l:
            return self._db.tables
        elif l == 1:
            return attrgetter(line)(self._db.tables)
        else:
            data = self._db.tables
            for p in line:
                if p in ['head', 'sample', 'unique', 'count', 'all', 'query']:
                    data = attrgetter(p)(data)()
                else:
                    data = attrgetter(p)(data)
            return data

    @line_magic('find_column')
    @check_db
    def find_column(self, *line):
        if not len(line):
            print '[ERROR]Please Specify column wildcard'
        else:
            return self._db.find_column(*line)

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
            return self._db.query(query)


def load_ipython_extension(ipython):
    ipython.register_magics(SQLDB)
