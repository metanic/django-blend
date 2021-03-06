""" Provides convention-over-configuration for your Django projects

This project provides tooling to help with defining and discovering
implementations of conventions in your Django projects, so that the usual
approach of excessive configuration can be narrowed down only where it makes
sense.

"""

import sys

from . import discovery
from .discovery import Group
from .discovery import IGroup
from .discovery.scanning import scanner


__all__ = (
    '__version__',
    'version_string',
    'name',
    'long_description',
    'short_description',
)


__version__ = (0, 0, 0)


def version_string(version=__version__):
    """ Provides the version string for this project """

    version_string = '.'.join(map(str, version[:3]))

    if len(version) > 3:
        version_string += '-' + '-'.join(version[3:])

    return version_string


def name():
    """ Provides a user-friendly name of the projec.t

    This can be used to get the name wherever it may be useful. One example
    case is that this is used to determine the name of the package in the
    Python package index. This is defined as a function so that the behavior
    can be easily overridden if necessary, but usually can remain as is.
    
    """

    return __name__


def long_description(content=' '.join(__doc__.split('\n')[1:])):
    """ Provides a human-readable description for this project """

    return content


def short_description():
    """ Provides a summarized project desription """

    return long_description(content=__doc__.split('\n', 1)[0])



def autodiscover():
    """ Discover any objects which have been added to any blending groups """

    scanner.scan(sys.modules[__name__])

    for _, group in discovery._internal.lookupAll([], IGroup):
        group.discover()
