# coding: utf-8
import re
import unicodedata


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    Taken from django.template.defaultfilters
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '_', value)


def get_any_attribute(obj, attribute_names):
    """
    Returns a tuple with (value, value_found) of the first found attribute in
    attribute_names that obj contains.
    """
    value = None
    value_found = False
    for alias in attribute_names:
        try:
            value = obj[alias]
        except (TypeError, KeyError, IndexError):
            try:
                value = getattr(obj, alias)
            except AttributeError:
                continue
        value_found = True
        break
    return (value, value_found)
