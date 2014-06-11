Simple Data Importer
====================

A simple, yet useful framework for data reading, processing and saving.

Given a data source (which may be a CSV file, Excel worksheet, DB query or any
iterable), the importer will iterate through the rows or objects, validating
all data before saving the record.

Getting started
---------------

Create your own:

```python
class MyImporter(BaseImporter):

    # fields is a list of dicts with the setup of each field read.
    # The fields are read and cleaned in this order.
    fields = [
        {
            'field_names': (),
            # One or more attribute or key names
            # The first will determine clean_* method name and row_values key

            'get_value': None,
            # A function (row_number, row, field_names) to return
            # the field value from a row or object.

            'required': False,
            # default: False. If True and the value is not provided, will
            # raise an RequiredFieldMissing exception

            'coerce': int,
            # A single-parameter callable applied to the value
            # BEFORE calling clean_field_name
        },
    ]

    def before_import(self):
        # Called before the import process
        pass

    def clean_field_name(self, row_number, row_values, value):
        # Validate and coerce value to desired type.
        # If an exception is raised, it will be passed to
        # exception_handler.

        # - row_values is the dict of values retrieved so far (in the same
        # order fields were provided).
        # - row_number is a 0-based index of the row being imported
        return value

    def clean(self, row_number, row_values):
        # Validate the entire row, after all clean_* have been called.
        # Must return the same row_values or a completely new object
        # that will be passed to save().
        # - row_values is the complete dict of values retrieved and cleaned
        return row_values

    def save(self, row_number, row_values):
        # Saves the record.
        # - row_values is the complete dict of values retrieved and cleaned
        pass

    def after_import(self):
        # Called after the import process.
        # This is always called, even when an exception is raised, so be
        # sure to check self.aborted for untreated errors.
        pass

    def exception_handler(self, row_number, exception):
        # Called when any exception is raised.
        # Return True to continue processing the next row.
        return False
```

Create an instance of `MyImporter` with any iterable (such as the ones in
`simpledataimporter.readers`):

```python
mycsv = SlugCSVReader('/path/to/file.csv')
myimporter = MyImporter(mycsv)
myimporter.run()  # run!
```

For each valid row, the function `save()` will be called.


Tips
----
At any time during the proccess, the following attributes are accessible:

- self.rows_saved: The number of rows that have been successfully saved.
- self.rows_processed: The number of rows that have been read and processed,
    even if it has not been saved.
- self.current_row: contains the object retrieved from source. Not available
    before and after import.
- self.current_row_number: the current row number (starting at 0).
- self.exception_count: The number of exceptions raised during the process.
- self.aborted: True if the process has been aborted by exception_handler.
