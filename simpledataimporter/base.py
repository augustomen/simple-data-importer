# coding: utf-8

from simpledataimporter.utils import get_any_attribute


class BaseImporter(object):
    """ The base class for all importers.

    fields = {
        'field_name': {
            # all arguments are optional
            'get_value': None,
                # a function (row_number, row, field) to return
                # the field value from a row or object. If
                # specified, 'aliases' is ignored
            'aliases': (),
                # one of more alternative attribute or key names
            'required': False,
                # default: False
            'coerce': int,
                # a single-parameter callable applied to the value
                # BEFORE calling clean_field_name
        }
    }
    """
    fields = {}

    def __init__(self, source):
        """ source must be an iterable """
        self._source = source
        self.rows_saved = 0
        self.rows_processed = 0

    def before_import(self):
        """ Called before the import process """
        pass

    def save(self, row_number, row):
        """ Saves the record.
            row will be complete. """
        raise NotImplementedError()

    def after_import(self):
        """ Called after the import process.
            This is always called, even when there is an exception, so be
            careful. """
        pass

    def exception_handler(self, row_number, row, exception):
        """ Called when any exception is raised.
            Return True to continue processing the next row. """
        return False

    def run(self):
        self.rows_saved = 0
        self.rows_processed = 0

        self.before_import()
        try:
            for field_name, options in self.fields:
                if not isinstance(options, dict):
                    raise TypeError(
                        "BaseImporter.fields['%s'] must be a dict." %
                        field_name)
                aliases = [field_name]
                aliases.extend(options.get('aliases', []))
                options['_field_names'] = aliases
                options['_coerce'] = options.get('coerce', lambda x: x)
                options['_clean'] = getattr(
                    self, 'clean_%s' % field_name, self._fake_clean)

            for row_number, row in enumerate(self._source):
                try:
                    """ row is an object, dict or list with field names
                        specified by fields. In the case of a list, field_name
                        (the fields dict key) must be an index.
                    """
                    for field_name, options in self.fields.items():
                        value = None
                        if options.get('get_value'):
                            value = options.get('get_value')(
                                row_number, row, field_name)
                        else:
                            _field_names = options['_field_names']
                            value, value_found = get_any_attribute(
                                value, _field_names)
                            if not value_found and options.get('required'):
                                raise AttributeError(
                                    "'%s' has no attributes %s" %
                                    (type(value), ", ".join(_field_names)))

                        value = options['_coerce'](value)
                        value = options['_clean'](row_number, row, value)

                    row = self.clean(row_number, row)
                    self.save(row_number, row)
                    self.rows_saved += 1
                except Exception as exc:
                    if not self.exception_handler(row_number, row, exc):
                        break
                finally:
                    self.rows_processed += 1
        finally:
            self.after_import()

    def _fake_clean(self, row_number, row, value):
        return value
