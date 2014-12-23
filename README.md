idb
===

ipython [db.py](https://github.com/yhat/db.py) shell extension.

Databases Supported
===

- PostgreSQL
- MySQL
- SQLite
- Redshift
- MS SQL Server
- Oracle

Install
=======

use github:

    In [1]: %install_ext https://raw.githubusercontent.com/dongweiming/idb/master/idb.py
    In [2]: %load_ext idb

    git clone https://github.com/dongweiming/idb
    cd idb
    python setup.py install

use pip:

    pip install ipython-db
    In [1]: %load_ext idb

Usage
=============

You can see this example ipynb: http://nbviewer.ipython.org/github/dongweiming/idb/blob/master/examples/db-example.ipynb
