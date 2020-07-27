import pint
from django.utils.translation import ugettext as _


def readable_dimension(dimension):
    return

class Unit:
    pass

class UnitSystem:
    ureg = None
    system_name = None
    system = None

    def __init__(self, system_name='SI'):
        self.system_name = system_name
        try:
            self.ureg = pint.UnitRegistry(system=system_name)
            self.system = getattr(self.ureg.sys, system_name)
        except (FileNotFoundError, AttributeError):
            raise ValueError("Invalid unit system")

    def available_systems(self) -> [str]:
        """
        List of available Unit Systems
        :return: Array of string
        """
        return dir(self.ureg.sys)

    def current_system(self) -> pint.UnitRegistry:
        """
        Return current pint.UnitRegistry
        """
        return self.ureg

    def unit(self, unit_name):
        return Unit(unit_system=self, name=unit_name)

    def available_unit_names(self) -> [str]:
        """
        List of available units for a given Unit system
        :return: Array of names of Unit systems
        """
        return dir(self.system)

    def unit_dimensionality(self, unit: str) -> str:
        """
        User friendly representation of the dimension
        :param unit: name of the unit to display
        :return: Human readable dimension
        """
        unit_obj = getattr(self.system, unit)
        return Unit.dimensionality_string(unit_obj=unit_obj)

    def units_per_dimensionality(self) -> {}:
        """
        List of units per dimension
        :param system: Unit system to use
        :return: dict of dimensions, with lists of unit strings
        """
        units_array = self.available_unit_names()
        output = {}
        for unit_str in units_array:
            dimension = self.unit_dimensionality(unit=unit_str)
            try:
                output[dimension].append(unit_str)
            except KeyError:
                output[dimension] = [unit_str]
        return output

    @property
    def dimensionalities(self) -> [str]:
        """
        List of dimensions available in the Unit system
        :return: list of dimensions for Unit system
        """
        return self.units_per_dimensionality().keys()


class Unit:
    unit_system = None
    name = None
    unit = None

    def __init__(self, unit_system: UnitSystem, name: str, ):
        """
        :param unit_system: UnitSystem instance
        :param name: name of the pint.Unit
        """
        self.unit_system = unit_system
        self.name = name
        try:
            self.unit = getattr(unit_system.system, name)
        except pint.errors.UndefinedUnitError:
            raise ValueError("invalid unit for system")

    @staticmethod
    def dimensionality_string(unit_obj: pint.Unit) -> str:
        """
        Converts pint dimensionality string to human readable string
        :param unit_obj: pint.Unit
        :return: str
        """
        ds = str(unit_obj.dimensionality).replace('[', '').replace(']', '')
        ds = ds.replace(' ** ', '^')
        ds = ds.split()
        return ' '.join([_(d) for d in ds])

    @property
    def readable_dimension(self):
        """
        Wrapper around Unit.dimensionality_string
        """
        return Unit.dimensionality_string(self.unit)