import os
from setuptools import setup, find_packages
import simpledataimporter


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="simpledataimporter",
    version=simpledataimporter.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    keywords='data import csv xls xlsx',
    packages=find_packages(),
    author='Augusto Men',
    author_email='augustocmen@yahoo.com.br',
    url="",
    include_package_data=True,
)
