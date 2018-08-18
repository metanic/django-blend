import typing
import venusian

from zope import interface

from zope.interface import adapter

from django_blend import utilities

groups = {}

_internal = adapter.AdapterRegistry()
registry = adapter.AdapterRegistry()


def generate_interface():
    """ Create a new interface type with no specific implementaion details. """

    class GeneratedInterface(interface.Interface):
        """ An empty interface which was automatically generated """

        pass

    return GeneratedInterface



class IGroup(interface.Interface):
    pass


class Group(object):
    """ Provides shortcuts to filter the registry for specific item types. """

    def __init__(
        self,
        type_name, *,
        get_instantiation_arguments=None,
        instantiate=False,
        interface=None,
        using = []
    ):

        """ Create a new blending group for working with objects with the given type name """

        self.discovery_methods = []

        self.get_instantiation_arguments = get_instantiation_arguments
        self.instantiate = instantiate
        self.interface = interface or generate_interface()
        self.type_name = type_name

        for discovery_method in using:
            self.use(discovery_method)

        # Register the interface group internally
        _internal.register([], IGroup, type_name, self)

    def _instantiate(self, kind):
        if self.get_instantiation_arguments is not None:
            args, kwargs = self.get_instantiation_arguments(self, kind)
        else:
            args, kwargs = (), {}

        return kind()


    def item(self, name=None):
        """ Decorate a class to register it with this Group """

        def register_to_interface(kind):
            """ Register a given class """

            # We need to underscore this since apparently they broke scoping
            # of closures in Python 3.x
            _name = name

            if _name is None:
                _name = utilities.snake_case(
                    kind.__name__,
                    ignore_suffix=self.type_name,
                )

            interface.classImplements(kind, self.interface)

            if self.instantiate:
                kind = self._instantiate(kind)

            registry.register([], self.interface, _name, kind)

            return kind

        return register_to_interface

    def use(self, discovery_method: typing.Callable[[], None]):
        """ Assign the provided discovery method to this blending group """

        self.discovery_methods.append(discovery_method)

    def all(self):
        """ Get all items in the registry with this Group """

        return registry.lookupAll([], self.interface)

    def get(self, name: str):
        """ Get the object registered with this group by it's name """

        return registry.lookup([], self.interface, name)

    def discover(self):
        """ Call all discovery methods attached to this object """

        return [method() for method in self.discovery_methods]
