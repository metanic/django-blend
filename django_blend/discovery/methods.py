import importlib
import sys

from django.conf import settings

from django_blend import utilities
from django_blend.discovery import scanning


class PackageDiscovery(object):
    """ Discovers blending groups by importing packages and their submodules

    """

    def __init__(self, package_name: str):
        self.scan = scan
        self.ignore = ignore

    def __call__(self):
        """ Import all modules and submodules within an entire Python package

        """

        return scanning.scanner.scan(
            self.package_name,
            ignore=self.ignore,
            onerror=utilities.permit_import_errors,
        )


class InstalledAppsDiscovery(object):
    def __init__(self, *, subpackage_name: str = None):
        self.subpackage_name = subpackage_name

    def import_module(self, module_name: str):
        # If we were given a module suffix, only import that submodule
        if self.subpackage_name is not None:
            module_name += '.' + self.subpackage_name

        try:
            return importlib.import_module(module_name)
        except ImportError:
            pass

    def __call__(self):
        return [
            self.import_module(app_name)
            for app_name in settings.INSTALLED_APPS
        ]
