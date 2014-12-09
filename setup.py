# coding=utf-8

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages  # noqa

version = '1.0'
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

install_requires = [
    'ipython>=2.0',
    'db.py>=0.3.4',
]

setup(name='ipython-db',
      version=version,
      packages=find_packages('.'),
      include_package_data=True,
      description="Ipython db.py shell extension",
      long_description=README,
      classifiers=[
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Framework :: IPython',
          'Topic :: Database',
          'Topic :: Database :: Front-Ends',
          'Programming Language :: Python :: 2',
      ],
      keywords=['database', 'ipython', 'shell', 'db.py'],
      author='Dongweiming',
      author_email='ciici123@gmail.com',
      url='https://github.com/dongweiming/idb',
      download_url='https://github.com/dongweiming/idb/tarball/0.1',
      license='MIT',
      py_modules=['idb'],
      zip_safe=False,
      install_requires=install_requires,
      )
