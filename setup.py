import os
from setuptools import setup, find_packages
import appname


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="appname",
    version=appname.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    keywords='django data import',
    packages=find_packages(),
    author='augustomen',
    author_email='augustocmen@yahoo.com.br',
    url="",
    include_package_data=True,
    test_suite='appname.tests.runtests.runtests',
)
