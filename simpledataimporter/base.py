# coding: utf-8

from simpledataimporter.utils import get_any_attribute


class RequiredFieldMissing(Exception):
    pass


class BaseImporter(object):
    """ The base class for all importers.

    fields is a list of dicts with the setup of each field read.
    The fields are read and cleaned in this order.
    fields = [
        {
            'field_names': (),
            # One or more attribute or key names
            # The first will determine clean_* method name and row_values key

            'get_value': None,
            # a function (row_number, row, field) to return
            # the field value from a row or object. If
            # specified, 'field_names' is ignored.

            'required': False,
            # default: False. If True and the value is not provided, will
            # raise an RequiredFieldMissing exception

            'coerce': int,
            # a single-parameter callable applied to the value
            # BEFORE calling clean_field_name
        },
    ]
    """
    fields = []

    def __init__(self, source):
        """ source must be an iterable """
        self._source = source
        self._reset()

    def _reset(self):
        """ Don't call directly. """
        self.current_row = None
        self.current_row_number = 0
        self.rows_saved = 0
        self.rows_processed = 0
        self.exception_count = 0
        self.aborted = False

    def _fake_clean(self, row_number, row_values, value):
        return value

    def before_import(self):
        """ Called before the import process """
        pass

    def after_import(self):
        """ Called after the import process.
            This is always called, even when an exception is raised, so be
            careful.
        """
        pass

    def run(self):
        self._reset()
        self.before_import()
        try:
            for field_index, options in enumerate(self.fields):
                if not isinstance(options, dict):
                    raise TypeError(
                        "BaseImporter.fields[%s] must be a dict." %
                        field_index)

                field_names = options.get('field_names')
                if field_names in (None, (), [], ''):
                    raise AttributeError(
                        "At least one field_name must be supplied to "
                        "BaseImporter.fields[%s]." % field_index)
                if not isinstance(field_names, (list, tuple)):
                    field_names = (field_names,)
                    options['field_names'] = field_names

                options.setdefault('coerce', lambda x: x)

                if not options.get('_clean'):
                    # You can specify your own clean method by setting
                    # the '_clean' key in fields.
                    options['_clean'] = getattr(
                        self, 'clean_%s' % field_names[0], self._fake_clean)

            for row_number, row in enumerate(self._source):
                self.current_row_number = row_number
                self.current_row = row
                try:
                    """ row is an object, dict or list with field names
                        specified by fields. In the case of a list, field_names
                        should contain an index.
                    """
                    row_values = {}
                    for options in self.fields:
                        field_names = options['field_names']
                        value = None
                        if options.get('get_value'):
                            value = options.get('get_value')(
                                row_number, row, field_names)
                        else:
                            value, value_found = get_any_attribute(
                                row, field_names)

                        if value is None and options.get('required'):
                            raise RequiredFieldMissing(
                                "Source has no attribute %s" % field_names[0])

                        value = options['coerce'](value)
                        value = options['_clean'](
                            row_number, row_values, value)
                        row_values[field_names[0]] = value

                    row_values = self.clean(row_number, row_values)
                    self.save(row_number, row_values)
                    self.rows_saved += 1
                except Exception as exc:
                    self.exception_count += 1
                    if not self.exception_handler(row_number, row, exc):
                        self.aborted = True
                        break
                finally:
                    self.rows_processed += 1

            self.current_row = None
        finally:
            self.after_import()

    def clean(self, row_number, row_values):
        return row_values

    def save(self, row_number, row_values):
        """ Saves the record.
            row_values is the complete dict of values retrieved and cleaned
        """
        raise NotImplementedError()

    def exception_handler(self, row_number, row, exception):
        """ Called when any exception is raised.
            Return True to continue processing the next row. """
        return False
