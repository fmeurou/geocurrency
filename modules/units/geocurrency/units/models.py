from datetime import date

import pint
from django.utils.translation import ugettext as _

from geocurrency.converters.models import BaseConverter, ConverterResult, ConverterResultDetail, ConverterResultError


class Amount:
    system = None
    unit = None
    value = 0
    date_obj = None

    def __init__(self, system: str, unit: str, value: float, date_obj: date = None):
        self.system = system
        self.unit = unit
        self.value = value
        self.date_obj = date_obj

    def __repr__(self):
        return f'{self.value} {self.unit} ({self.system})'


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

    @classmethod
    def is_valid(cls, system: str) -> bool:
        us = cls()
        return system in us.available_systems()

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


class UnitConverter:
    pass


class UnitConverter(BaseConverter):
    base_system = None
    base_unit = None

    def __init__(self, base_system: str, base_unit: str, id: str = None):
        super(UnitConverter, self).__init__(id=id)
        self.base_system = base_system
        self.base_unit = base_unit
        self.system = UnitSystem(system_name=base_system)
        self.unit = Unit(unit_system=self.system, name=base_unit)
        self.compatible_units = [str(u) for u in self.unit.unit.compatible_units()]

    def add_data(self, data: []) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        errors = super(UnitConverter, self).add_data(data)
        return errors

    def check_data(self, data):
        """
        Validates that the data contains
        - currency (str)
        - amount (float)
        - date (YYYY-MM-DD)
        """
        from .serializers import AmountSerializer
        errors = []
        for line in data:
            serializer = AmountSerializer(data=line)
            if serializer.is_valid():
                self.data.append(serializer.create(serializer.validated_data))
            else:
                errors.append(serializer.errors)
        return errors

    @classmethod
    def load(cls, id: str) -> UnitConverter:
        uc = super(UnitConverter, cls).load(id)
        uc.system = UnitSystem(system_name=uc.base_system)
        uc.unit = Unit(unit_system=uc.system, name=uc.base_unit)
        return uc

    def save(self):
        system = self.system
        unit = self.unit
        self.system = None
        self.unit = None
        super(UnitConverter, self).save()
        self.system = system
        self.unit = unit

    def convert(self) -> ConverterResult:
        """
        Converts data to base unit in base system
        """

        result = ConverterResult(id=self.id, target=self.base_unit)
        us = UnitSystem(system_name=self.base_system)
        Q_ = us.ureg.Quantity
        for amount in self.data:
            if amount.unit not in self.compatible_units:
                error = ConverterResultError(
                    unit=amount.unit,
                    original_value=amount.value,
                    date=amount.date_obj,
                    error=_('Incompatible units')
                )
                result.errors.append(error)
                continue
            try:
                quantity = Q_(amount.value, amount.unit)
                out = quantity.to(self.base_unit)
                result.increment_sum(out.magnitude)
                detail = ConverterResultDetail(
                    unit=amount.unit,
                    original_value=amount.value,
                    date=amount.date_obj,
                    conversion_rate=0,
                    converted_value=out.magnitude
                )
                result.detail.append(detail)
            except pint.UndefinedUnitError:
                error = ConverterResultError(
                    unit=amount.currency,
                    original_value=amount.amount,
                    date=amount.date_obj,
                    error=_('Undefined unit in the registry')
                )
                result.errors.append(error)
        self.end_batch(result.end_batch())
        return result
