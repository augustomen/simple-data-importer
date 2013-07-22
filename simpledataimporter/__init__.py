# coding: utf-8

# for importing: from dataimporter2 import SlugXLSXReader
from csv import DictReader
from readers.csv import SlugDictReader
from readers.excel import ExcelReader, SlugExcelReader


VERSION = (0, 1, 0, 'beta')
if VERSION[-1] != "final":  # pragma: no cover
    __version__ = '.'.join(map(str, VERSION))
else:  # pragma: no cover
    __version__ = '.'.join(map(str, VERSION[:-1]))
