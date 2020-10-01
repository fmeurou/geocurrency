import logging
from datetime import date

import pint
from django.utils.translation import ugettext as _
from geocurrency.converters.models import BaseConverter, ConverterResult, ConverterResultDetail, ConverterResultError

from . import UNIT_EXTENDED_DEFINITION


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


class UnitFamily:
    family = None
    units = []

    def __init__(self, family: str, units: [Unit]):
        self.family = family
        self.units = units


class UnitSystem:
    ureg = None
    system_name = None
    system = None

    def __init__(self, system_name='SI', fmt_locale='en'):
        found = False
        for available_system in UnitSystem.available_systems():
            if system_name.lower() == available_system.lower():
                system_name = available_system
                found = True
        if not found:
            raise ValueError("Invalid unit system")
        self.system_name = system_name
        try:
            self.ureg = pint.UnitRegistry(system=system_name, fmt_locale=fmt_locale)
            self.system = getattr(self.ureg.sys, system_name)
        except (FileNotFoundError, AttributeError):
            raise ValueError("Invalid unit system")

    @classmethod
    def available_systems(cls) -> [str]:
        """
        List of available Unit Systems
        :return: Array of string
        """
        ureg = pint.UnitRegistry(system='SI')
        return dir(ureg.sys)

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
        return Unit(unit_system=self, code=unit_name)

    @property
    def units(self):
        """
        Wrapper used by serializer
        """
        return [UnitFamily(family=family, units=units) for family, units in self.units_per_family().items()]

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
        return Unit.dimensionality_string(unit_system=self.system, unit_str=unit)

    def units_per_family(self) -> []:
        """
        List of units per dimension.
        Dimension is the dimension as identified in Units.UNIT_EXTENDED_DEFINITION
        :return: array of dict of dimensions, with lists of unit strings
        """
        units_array = self.available_unit_names()
        output = {}
        for unit_str in units_array:
            try:
                unit = self.unit(unit_name=unit_str)
            except ValueError:
                continue
            try:
                output[str(unit.family)].append(unit)
            except KeyError:
                output[str(unit.family)] = [unit]
        return output

    def units_per_dimensionality(self) -> {}:
        """
        List of units per dimension
        :return: dict of dimensions, with lists of unit strings
        """
        units_array = self.available_unit_names()
        output = {}
        for unit_str in units_array:
            dimension = Unit.dimensionality_string(self, unit_str)
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
        return set([Unit.dimensionality_string(self, unit_str) for unit_str in dir(self.system)])


class Unit:
    unit_system = None
    code = None
    unit = None

    def __init__(self, unit_system: UnitSystem, code: str, ):
        """
        :param unit_system: UnitSystem instance
        :param code: code of the pint.Unit
        """
        self.unit_system = unit_system
        self.code = code
        try:
            self.unit = getattr(unit_system.system, code)
        except pint.errors.UndefinedUnitError:
            raise ValueError("invalid unit for system")

    @classmethod
    def is_valid(self, name):
        us_si = UnitSystem(system_name='SI')
        all_units = []
        for us in us_si.available_systems():
            all_units.extend(dir(getattr(us_si.ureg.sys, us)))
        return name in set(all_units)

    @property
    def family(self):
        return self.unit_family(self.code)

    @property
    def name(self):
        return self.unit_name(self.code)

    @property
    def symbol(self):
        return self.unit_symbol(self.code)

    @property
    def dimension(self):
        return self.unit.dimensionality

    @staticmethod
    def unit_family(unit_str: str) -> str:
        try:
            ext_unit = UNIT_EXTENDED_DEFINITION.get(unit_str)
            return ext_unit['family']
        except (KeyError, TypeError) as e:
            logging.error(f'No UNIT_EXTENDED_DEFINITION for unit {unit_str}')
            return ''

    @staticmethod
    def unit_name(unit_str: str) -> str:
        try:
            ext_unit = UNIT_EXTENDED_DEFINITION.get(unit_str)
            return ext_unit['name']
        except (KeyError, TypeError) as e:
            logging.error(f'No UNIT_EXTENDED_DEFINITION for unit {unit_str}')
            return unit_str

    @staticmethod
    def unit_symbol(unit_str: str) -> str:
        try:
            ext_unit = UNIT_EXTENDED_DEFINITION.get(unit_str)
            return ext_unit['symbol']
        except (KeyError, TypeError) as e:
            logging.error(f'No UNIT_EXTENDED_DEFINITION for unit {unit_str}')
            return ''

    @staticmethod
    def dimensionality_string(unit_system: UnitSystem, unit_str: str) -> str:
        """
        Converts pint dimensionality string to human readable string
        :param unit_system: UnitSystem
        :param unit_str: Unit name
        :return: str
        """
        ds = str(getattr(unit_system.ureg, unit_str).dimensionality).replace('[', '').replace(']', '')
        ds = ds.replace(' ** ', '^')
        ds = ds.split()
        return ' '.join([_(d) for d in ds])

    @staticmethod
    def translated_name(unit_system: UnitSystem, unit_str: str) -> str:
        return '{}'.format(unit_system.ureg[unit_str])

    @property
    def readable_dimension(self):
        """
        Wrapper around Unit.dimensionality_string
        """
        return Unit.dimensionality_string(unit_system=self.unit_system, unit_str=self.code)


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
        self.unit = Unit(unit_system=self.system, code=base_unit)
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
        from .serializers import UnitAmountSerializer
        errors = []
        for line in data:
            serializer = UnitAmountSerializer(data=line)
            if serializer.is_valid():
                self.data.append(serializer.create(serializer.validated_data))
            else:
                errors.append(serializer.errors)
        return errors

    @classmethod
    def load(cls, id: str) -> UnitConverter:
        uc = super(UnitConverter, cls).load(id)
        uc.system = UnitSystem(system_name=uc.base_system)
        uc.unit = Unit(unit_system=uc.system, code=uc.base_unit)
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


class UnitConversionPayload:
    data = None
    base_system = ''
    base_unit = ''
    key = ''
    batch_id = ''
    eob = False

    def __init__(self, base_system, base_unit, data=None, key=None, batch_id=None, eob=False):
        self.data = data
        self.base_system = base_system
        self.base_unit = base_unit
        self.key = key
        self.batch_id = batch_id
        self.eob = eob
