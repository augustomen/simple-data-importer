# coding: utf-8
from csv import DictReader

from simpledataimporter.utils import slugify


class SlugDictReader(DictReader):
    """ Iterable reader for use with BaseImporter.
        If the fieldnames parameters is ommited, the first line will be
        considered to contain the column names. All names are slugified.

        The constructor is the same as csv.DictReader:
        http://docs.python.org/2/library/csv.html#csv.DictReader

        class csv.DictReader(csvfile, fieldnames=None, restkey=None,
                             restval=None, dialect='excel', *args, **kwds)
    """

    def __init__(self, *args, **kwargs):
        DictReader.__init__(self, *args, **kwargs)
        self._fieldnames = map(slugify, self.fieldnames)
