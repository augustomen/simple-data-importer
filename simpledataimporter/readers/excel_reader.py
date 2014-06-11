# coding: utf-8
import sys
import xlrd
import datetime

from simpledataimporter.utils import slugify


def excel_str(value):
    """ Meant to be used as `coerce` option. Will transform numbers to a
        string. According to xlrd documentation, all strings are presented
        as unicode. """
    if value is None:
        return None

    if isinstance(value, float) and not (value % 1):
        # Excel will store ints as floats, so check for a decimal part and
        # cast to int.
        return str(int(value))

    if sys.version_info[0] <= 2:
        return unicode(value)
    else:
        return str(value)


class ExcelReader(object):
    """ Iterable reader for use with BaseImporter.
        The constructor is the same as used with open_workbook [1]
        [1] https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html?p=4966#__init__.open_workbook-function

        You must provide one of:
        filename: a string that contains the location to the file.
        file_contents: a string or an mmap.mmap object with the contents of
            the file.

        fieldnames are taken from the first row.
    """
    def __init__(self, *args, **kwargs):
        self._workbook = xlrd.open_workbook(*args, **kwargs)
        self._active_worksheet = None
        self._fieldnames = None

    def __len__(self):
        return self.worksheet.nrows - 1

    def __iter__(self):
        fields = self.fieldnames
        worksheet = self.worksheet
        for nrow in range(1, len(self) + 1):
            row = worksheet.row(nrow)
            yield dict(zip(fields, map(self.cell_value, row)))

    def cell_value(self, cell):
        """ Takes a xlrd.Cell and returns the Python native value. """
        value = cell.value
        if cell.ctype == xlrd.XL_CELL_DATE and value > 60:
            value = datetime.datetime(
                *xlrd.xldate_as_tuple(value, self._workbook.datemode))
        elif cell.ctype == xlrd.XL_CELL_BOOLEAN:
            value = bool(value)
        elif cell.ctype == xlrd.XL_CELL_ERROR:
            value = xlrd.error_text_from_code(value)
        return value

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            self._fieldnames = self.worksheet.row_values(0)
        return self._fieldnames

    @property
    def workbook(self):
        return self._workbook

    def activate_worksheet(self, index):
        if isinstance(index, int):
            self._active_worksheet = self._workbook.sheet_by_index(index)
        else:
            self._active_worksheet = self.workbook.get_sheet_by_name(index)
        return self._active_worksheet

    @property
    def worksheet(self):
        if self._active_worksheet is None:
            self.activate_worksheet(0)
        return self._active_worksheet


class SlugExcelReader(ExcelReader):
    """ Same as ExcelReader, but all field names are slugified. """

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            self._fieldnames = map(
                slugify, super(SlugExcelReader, self).fieldnames)
        return self._fieldnames
