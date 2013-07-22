====================
Simple Data Importer
====================

A simple, yet useful framework for data reading, processing and saving.

Given a data source (which may be a CSV file, Excel worksheet, DB query or any
iterable), the importer will iterate through the rows or objects, validating
all data before saving the record.

Getting started
---------------

Create your own:

    class MyImporter(BaseImporter):

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

        def before_import(self):
            """ Called before the import process """
            pass

        def clean_field_name(self, row_number, row, value):
            """ Validate and coerce value to desired type.
                ValidationError may be raise any time and will not cause the
                    import process to be stopped.
                Any other Exception raised will stop the process.

                row is a dict with {'field_name': value} - it may be incomplete!
                row_number is a 0-based index of the row being imported
            """
            return value

        def clean(self, row_number, row):
            """ Validate the entire row, after all clean_field_name's have been
                called. Must return the same row or a completely new object that
                will be passed to save().
            """
            return value

        def save(self, row_number, row):
            """ Saves the record.
                row will be complete. """
            pass

        def after_import(self):
            """ Called after the import process.
                This is always called, even when an exception is raised, so be
                careful.
                self.rows_saved contains the number of rows saved without
                raising an exception. """
            pass

        def exception_handler(self, row_number, row, exception):
        """ Called when any exception is raised.
            Return True to continue processing the next row. """
        return False


Create an instance of MyImporter with any iterable (such as the ones in
dataimporter2.readers):

    mycsv = SlugCSVReader('/path/to/file.csv')
    myimporter = MyImporter(mycsv)
    myimporter.run()  # run!

For each valid row, the function save() will be called.
