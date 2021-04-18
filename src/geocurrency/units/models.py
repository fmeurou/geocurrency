"""
Units models
"""

import logging
import re
from datetime import date

import pint.systems
import uncertainties
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from sympy import sympify, SympifyError

from geocurrency.converters.models import BaseConverter, ConverterResult, \
    ConverterResultDetail, ConverterResultError, ConverterLoadError
from . import UNIT_EXTENDED_DEFINITION, DIMENSIONS, UNIT_SYSTEM_BASE_AND_DERIVED_UNITS, \
    ADDITIONAL_BASE_UNITS, PREFIX_SYMBOL
from .exceptions import *
from .settings import ADDITIONAL_UNITS, PREFIXED_UNITS_DISPLAY


class Quantity:
    """
    Quantity class
    """
    system = None
    unit = None
    value = 0
    date_obj = None

    def __init__(self, system: str, unit: str, value: float, date_obj: date = None):
        """
        Initialize quantity on unit system
        """
        self.system = system
        self.unit = unit
        self.value = value
        self.date_obj = date_obj

    def __repr__(self):
        """
        Look beautiful
        """
        return f'{self.value} {self.unit} ({self.system})'


class Unit:
    """
    Unit mock for hinting
    """
    pass


class UnitSystem:
    """
    Pint UnitRegistry wrapper
    """
    ureg = None
    system_name = None
    system = None
    _additional_units = set()

    def __init__(self, system_name: str = 'SI', fmt_locale: str = 'en', user: User = None,
                 key: str = None):
        """
        Initialize UnitSystem from name and user / key information for loading custom units
        """
        found = False
        for available_system in UnitSystem.available_systems():
            if system_name.lower() == available_system.lower():
                system_name = available_system
                found = True
        if not found:
            raise UnitSystemNotFound("Invalid unit system")
        self.system_name = system_name
        try:
            additional_units_settings = settings.GEOCURRENCY_ADDITIONAL_UNITS
        except AttributeError:
            additional_units_settings = ADDITIONAL_UNITS
        try:
            self.ureg = pint.UnitRegistry(system=system_name, fmt_locale=fmt_locale)
            self.system = getattr(self.ureg.sys, system_name)
            self._load_additional_units(units=ADDITIONAL_BASE_UNITS)
            self._load_additional_units(units=additional_units_settings)
            if user:
                self._load_custom_units(user=user, key=key)
            self._rebuild_cache()
        except (FileNotFoundError, AttributeError):
            raise UnitSystemNotFound("Invalid unit system")

    def _rebuild_cache(self):
        """
        Rebuild registry cache
        It should be in the define method of the registry
        """
        self.ureg._build_cache()

    def _load_additional_units(self, units: dict, redefine: bool = False) -> bool:
        """
        Load additional base units in registry
        """
        available_units = self.available_unit_names()
        if self.system_name not in units:
            logging.warning(f"error loading additional units for {self.system_name}")
            return False
        added_units = []
        for key, items in units[self.system_name].items():
            if key not in available_units:
                self.ureg.define(f"{key} = {items['relation']} = {items['symbol']}")
                added_units.append(key)
            elif redefine:
                self.ureg.redefine(f"{key} = {items['relation']} = {items['symbol']}")
        self._additional_units = self._additional_units | set(added_units)
        return True

    def _load_custom_units(self, user: User, key: str = None, redefine: bool = False) -> bool:
        """
        Load custom units in registry
        """
        if user and user.is_authenticated:
            if user.is_superuser:
                qs = CustomUnit.objects.all()
            else:
                qs = CustomUnit.objects.filter(user=user)
            if key:
                qs = qs.filter(key=key)
        else:
            qs = CustomUnit.objects.filter(pk=-1)
        qs = qs.filter(unit_system=self.system_name)
        available_units = self.available_unit_names()
        added_units = []
        for cu in qs:
            props = [cu.code, cu.relation]
            if cu.symbol:
                props.append(cu.symbol)
            if cu.alias:
                props.append(cu.alias)
            definition = " = ".join(props)
            if cu.code not in available_units:
                self.ureg.define(definition)
                added_units.append(cu.code)
            elif redefine:
                self.ureg.redefine(definition)
            else:
                logging.error(f"{cu.code} already defined in registry")
        self._additional_units = self._additional_units | set(added_units)
        return True

    def _test_additional_units(self, units: dict) -> bool:
        """
        Load and check dimensionality of ADDITIONAL_BASE_UNITS values
        """
        if self.system_name not in units:
            return False
        for key in units[self.system_name].keys():
            try:
                self.unit(key).dimensionality and True
            except pint.errors.UndefinedUnitError:
                return False
        return True

    def add_definition(self, code, relation, symbol, alias):
        """
        Add a new unit definition to a UnitSystem, and rebuild cache
        :param code: code of the unit
        :param relation: relation to other units (e.g.: 3 kg/m)
        :param symbol: short unit representation
        :param alias: other name for unit
        """
        self.ureg.define(f"{code} = {relation} = {symbol} = {alias}")
        self._rebuild_cache()

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
        """
        Check validity of the UnitSystem
        :param system: name of the unit system
        """
        us = cls()
        return system in us.available_systems()

    def current_system(self) -> pint.UnitRegistry:
        """
        Return current pint.UnitRegistry
        """
        return self.ureg

    def unit(self, unit_name):
        """
        Create a Object in the UnitSystem
        :param unit_name: name of the unit in the unit system
        """
        return Unit(unit_system=self, code=unit_name)

    def available_unit_names(self) -> [str]:
        """
        List of available units for a given Unit system
        :return: Array of names of Unit systems
        """
        try:
            prefixed_units_display = settings.GEOCURRENCY_PREFIXED_UNITS_DISPLAY
        except AttributeError:
            prefixed_units_display = PREFIXED_UNITS_DISPLAY
        prefixed_units = []
        for key, prefixes in prefixed_units_display.items():
            for prefix in prefixes:
                prefixed_units.append(prefix + key)
        return sorted(prefixed_units + dir(getattr(self.ureg.sys, self.system_name))
                      + list(self._additional_units))

    def unit_dimensionality(self, unit: str) -> str:
        """
        User friendly representation of the dimension
        :param unit: name of the unit to display
        :return: Human readable dimension
        """
        return Unit.dimensionality_string(unit_system=self.system, unit_str=unit)

    def available_dimensions(self, ordering: str = 'name') -> {}:
        """
        Return available dimensions for the UnitSystem
        :param ordering: sort result by attribute
        """
        descending = False
        if ordering and ordering[0] == '-':
            ordering = ordering[1:]
            descending = True
        if ordering not in ['code', 'name', 'dimension']:
            ordering = 'name'
        return sorted([Dimension(unit_system=self, code=dim) for dim in DIMENSIONS.keys()],
                      key=lambda x: getattr(x, ordering, ''), reverse=descending)

    @property
    def _ureg_dimensions(self):
        """
        return dimensions with units
        """
        dimensions = []
        for dim in self.ureg._dimensions:
            try:
                if not self.ureg.get_compatible_units(dim):
                    continue
                dimensions.append(dim)
            except KeyError:
                continue
        return dimensions

    def _get_dimension_dimensionality(self, dimension: str) -> {}:
        """
        Return the dimensionality of a dimension based on the first compatible unit
        """
        try:
            for dim in self.ureg.get_compatible_units(dimension):
                return self.ureg.get_base_units(dim)[1]
        except KeyError:
            return {}

    def _generate_dimension_delta_dictionnary(self) -> {}:
        """
        Generate the dict to put in DIMENSIONS
        """
        output = {}
        for dim in self._ureg_dimensions:
            if dim not in DIMENSIONS:
                output[dim] = {
                    'name': f'_({dim})',
                    'dimension': str(self._get_dimension_dimensionality(dim)),
                    'symbol': ''
                }
        return output

    def units_per_dimension(self, dimensions: [str]) -> {}:
        """
        Return units grouped by dimension
        :param dimensions: restrict list of dimensions
        """
        output = {}
        registry_dimensions = dimensions or DIMENSIONS.keys()
        for dim in registry_dimensions:
            dimension = Dimension(unit_system=self, code=dim)
            try:
                units = self.ureg.get_compatible_units(dim)
                if units:
                    output[dim] = units
            except KeyError:
                continue
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


class Dimension:
    """
    Dimenion of a Unit
    """
    unit_system = None
    code = None
    name = None
    dimension = None

    def __init__(self, unit_system: UnitSystem, code: str):
        """
        Initialize a Dimension in a UnitSystem
        """
        try:
            dimension = DIMENSIONS[code]
            self.unit_system = unit_system
            self.code = code
            self.name = dimension['name']
            self.dimension = dimension['dimension']
        except (ValueError, KeyError) as e:
            logging.warning(str(e))
            self.code = None
        if not self.code:
            raise DimensionNotFound

    def __repr__(self):
        """
        Look beautiful
        """
        return self.code

    def units(self, user=None, key=None) -> [Unit]:
        """
        List of units for this dimension
        :param user: optional user for custom units
        :param key: optional key for custom units
        """
        if self.code == '[compounded]':
            return self._compounded_units
        if self.code == '[custom]':
            return self._custom_units(user=user, key=key)
        unit_list = []
        try:
            prefixed_units_display = settings.GEOCURRENCY_PREFIXED_UNITS_DISPLAY
        except AttributeError:
            prefixed_units_display = PREFIXED_UNITS_DISPLAY
        try:
            unit_list.append(
                self.unit_system.unit(
                    UNIT_SYSTEM_BASE_AND_DERIVED_UNITS[self.unit_system.system_name][self.code]
                )
            )
        except (KeyError, UnitNotFound):
            logging.warning(f"unable to find base unit for"
                            f"unit system {self.unit_system.system_name}"
                            f" and dimension {self.code}")
        try:
            unit_list.extend(
                [
                    Unit(unit_system=self.unit_system, pint_unit=unit)
                    for unit in self.unit_system.ureg.get_compatible_units(self.code)
                ])
        except KeyError as e:
            logging.warning(f"Cannot find compatible units for this dimension {self.code}")
        unit_names = [str(u) for u in unit_list]
        for unit, prefixes in prefixed_units_display.items():
            if unit in unit_names:
                for prefix in prefixes:
                    unit_list.append(self.unit_system.unit(unit_name=prefix + unit))
        return set(sorted(unit_list, key=lambda x: x.name))

    @property
    def _compounded_units(self):
        """
        List units that do not belong to a dimension
        """
        available_units = self.unit_system.available_unit_names()
        dimensioned_units = []
        for dimension_code in [d for d in DIMENSIONS.keys() if
                               d != '[compounded]' and d != '[custom]']:
            dimension = Dimension(unit_system=self.unit_system, code=dimension_code)
            dimensioned_units.extend([u.code for u in dimension.units()])
        return [self.unit_system.unit(au) for au in set(available_units) - set(dimensioned_units)]

    def _custom_units(self, user: User, key: str = None) -> [Unit]:
        """
        Return list of custom units
        :param user: User owning the units
        :param key: optional unit key
        """
        if user and user.is_authenticated:
            if user.is_superuser:
                custom_units = CustomUnit.objects.all()
            else:
                custom_units = CustomUnit.objects.filter(user=user)
            if key:
                custom_units = custom_units.filter(key=key)
            return [self.unit_system.unit(cu.code) for cu in custom_units]
        else:
            return []

    @property
    def base_unit(self):
        """
        Base unit for this dimension in this Unit System
        """
        try:
            return UNIT_SYSTEM_BASE_AND_DERIVED_UNITS[self.unit_system.system_name][self.code]
        except KeyError:
            logging.warning(
                f'dimension {self.dimension} is not part of '
                f'unit system {self.unit_system.system_name}')
            return None


class Unit:
    """
    Pint Unit wrapper
    """
    unit_system = None
    code = None
    unit = None

    def __init__(self, unit_system: UnitSystem, code: str = '', pint_unit: pint.Unit = None):
        """
        Initialize a Unit in a UnitSystem
        :param unit_system: UnitSystem instance
        :param code: code of the pint.Unit
        """
        self.unit_system = unit_system
        if pint_unit and isinstance(pint_unit, pint.Unit):
            self.code = str(pint_unit)
            self.unit = pint_unit
        elif code:
            self.code = code
            try:
                self.unit = getattr(unit_system.system, code)
            except pint.errors.UndefinedUnitError:
                raise UnitNotFound("invalid unit for system")
        else:
            raise UnitNotFound("invalid unit for system")

    def __repr__(self):
        return self.code

    @classmethod
    def is_valid(cls, name: str) -> bool:
        """
        Check the validity of a unit in a UnitSystem
        """
        try:
            us_si = UnitSystem(system_name='SI')
        except UnitSystemNotFound:
            return False
        try:
            return us_si.unit(unit_name=name) and True
        except pint.errors.UndefinedUnitError:
            return False

    @property
    def name(self) -> str:
        """
        Return name of the unit from table of units
        """
        return self.unit_name(self.code)

    @property
    def symbol(self) -> str:
        """
        Return symbol for Unit
        """
        return self.unit_symbol(self.code)

    @property
    def dimensions(self) -> [Dimension]:
        """
        Return Dimensions of Unit
        """
        dimensions = [Dimension(unit_system=self.unit_system, code=code) for code in
                      DIMENSIONS.keys()
                      if DIMENSIONS[code]['dimension'] == str(self.dimensionality)]
        return dimensions or '[compounded]'

    @staticmethod
    def base_unit(unit_str: str) -> (str, str):
        """
        Get base unit in case the unit is a prefixed unit
        :param unit_str: name of unit to check
        :return: base unit name, prefix
        """
        prefix = ''
        base_str = unit_str
        try:
            prefixed_units_display = settings.GEOCURRENCY_PREFIXED_UNITS_DISPLAY
        except AttributeError:
            prefixed_units_display = PREFIXED_UNITS_DISPLAY
        for base, prefixes in prefixed_units_display.items():
            for _prefix in prefixes:
                if unit_str == _prefix + base:
                    prefix = _prefix
                    base_str = base
        return base_str, prefix

    @staticmethod
    def unit_name(unit_str: str) -> str:
        """
        Get translated name from unit string
        :param unit_str: Name of unit
        """
        base_str, prefix = Unit.base_unit(unit_str=unit_str)
        try:
            ext_unit = UNIT_EXTENDED_DEFINITION.get(base_str)
            return prefix + str(ext_unit['name'])
        except (KeyError, TypeError) as e:
            logging.error(f'No UNIT_EXTENDED_DEFINITION for unit {base_str}')
            return unit_str

    @staticmethod
    def unit_symbol(unit_str: str) -> str:
        """
        Static function to get symbol from unit string
        :param unit_str: Name of unit
        """
        base_str, prefix = Unit.base_unit(unit_str=unit_str)
        try:
            prefix_symbol = PREFIX_SYMBOL[prefix]
            ext_unit = UNIT_EXTENDED_DEFINITION.get(base_str)
            return prefix_symbol + ext_unit['symbol']
        except (KeyError, TypeError) as e:
            logging.error(f'No UNIT_EXTENDED_DEFINITION for unit {base_str}')
            return ''

    @staticmethod
    def dimensionality_string(unit_system: UnitSystem, unit_str: str) -> str:
        """
        Converts pint dimensionality string to human readable string
        :param unit_system: UnitSystem
        :param unit_str: Unit name
        :return: str
        """
        ds = str(getattr(unit_system.ureg, unit_str).dimensionality).replace('[', '').replace(']',
                                                                                              '')
        ds = ds.replace(' ** ', '^')
        ds = ds.split()
        return ' '.join([_(d) for d in ds])

    @property
    def dimensionality(self):
        """
        Return dimensionality of a unit in Pint universe
        """
        try:
            return self.unit_system.ureg.get_base_units(self.code)[1]
        except KeyError:
            return ''

    @staticmethod
    def translated_name(unit_system: UnitSystem, unit_str: str) -> str:
        """
        Translated name of the unit
        """
        try:
            return '{}'.format(unit_system.ureg[unit_str])
        except KeyError:
            return unit_str

    @property
    def readable_dimension(self):
        """
        Wrapper around Unit.dimensionality_string
        """
        return Unit.dimensionality_string(unit_system=self.unit_system, unit_str=self.code)


class UnitConverter(BaseConverter):
    """
    Conversion between units
    """
    base_system = None
    base_unit = None
    user = None
    key = None

    def __init__(self, base_system: str, base_unit: str, user: User = None, key: key = None,
                 id: str = None):
        """
        Initialize the converter. It converts a payload into a destination unit
        """
        try:
            super().__init__(id=id)
            self.base_system = base_system
            self.base_unit = base_unit
            self.user = user
            self.key = key
            self.system = UnitSystem(system_name=base_system, user=user, key=key)
            self.unit = Unit(unit_system=self.system, code=base_unit)
        except (UnitSystemNotFound, UnitNotFound):
            raise UnitConverterInitError

    def add_data(self, data: []) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        errors = super().add_data(data)
        return errors

    def check_data(self, data):
        """
        Validates that the data contains
        system = str
        unit = str
        value = float
        date_obj ('YYYY-MM-DD')
        """
        from .serializers import QuantitySerializer
        errors = []
        for line in data:
            serializer = QuantitySerializer(data=line)
            if serializer.is_valid():
                self.data.append(serializer.create(serializer.validated_data))
            else:
                errors.append(serializer.errors)
        return errors

    @classmethod
    def load(cls, id: str, user: User = None, key: str = None) -> BaseConverter:
        """
        Load converter from ID
        """
        try:
            uc = super().load(id)
            uc.system = UnitSystem(system_name=uc.base_system, user=user, key=key)
            uc.unit = Unit(unit_system=uc.system, code=uc.base_unit)
            return uc
        except (UnitSystemNotFound, UnitNotFound, KeyError) as e:
            raise ConverterLoadError

    def save(self):
        """
        Save the converter to cache
        """
        system = self.system
        unit = self.unit
        self.system = None
        self.unit = None
        super().save()
        self.system = system
        self.unit = unit

    def convert(self) -> ConverterResult:
        """
        Converts data to base unit in base system
        """

        result = ConverterResult(id=self.id, target=self.base_unit)
        q_ = self.system.ureg.Quantity
        for quantity in self.data:
            try:
                pint_quantity = q_(quantity.value, quantity.unit)
                out = pint_quantity.to(self.base_unit)
                result.increment_sum(out.magnitude)
                detail = ConverterResultDetail(
                    unit=quantity.unit,
                    original_value=quantity.value,
                    date=quantity.date_obj,
                    conversion_rate=0,
                    converted_value=out.magnitude
                )
                result.detail.append(detail)
            except pint.UndefinedUnitError:
                error = ConverterResultError(
                    unit=quantity.unit,
                    original_value=quantity.value,
                    date=quantity.date_obj,
                    error=_('Undefined unit in the registry')
                )
                result.errors.append(error)
            except pint.DimensionalityError:
                error = ConverterResultError(
                    unit=quantity.unit,
                    original_value=quantity.value,
                    date=quantity.date_obj,
                    error=_('Dimensionality error, incompatible units')
                )
                result.errors.append(error)
        self.end_batch(result.end_batch())
        return result


class UnitConversionPayload:
    """
    Unit conversion payload
    """
    data = None
    base_system = ''
    base_unit = ''
    key = ''
    batch_id = ''
    eob = False

    def __init__(self, base_system: UnitSystem, base_unit: Unit, data=None, key: str = None,
                 batch_id: str = None, eob: bool = False):
        """
        Initialize conversion payload
        """
        self.data = data
        self.base_system = base_system
        self.base_unit = base_unit
        self.key = key
        self.batch_id = batch_id
        self.eob = eob


class CustomUnit(models.Model):
    """
    Additional unit for a user
    """
    AVAILABLE_SYSTEMS = (
        ('Planck', 'Planck'),
        ('SI', 'SI'),
        ('US', 'US'),
        ('atomic', 'atomic'),
        ('cgs', 'CGS'),
        ('imperial', 'imperial'),
        ('mks', 'mks'),
    )
    user = models.ForeignKey(User, related_name='units', on_delete=models.PROTECT)
    key = models.CharField("Categorization field (e.g.: customer ID)",
                           max_length=255, default=None, db_index=True, null=True, blank=True)
    unit_system = models.CharField("Unit system to register the unit in", max_length=20,
                                   choices=AVAILABLE_SYSTEMS)
    code = models.SlugField("technical name of the unit (e.g.: myUnit)")
    name = models.CharField("Human readable name (e.g.: My Unit)", max_length=255)
    relation = models.CharField("Relation to an existing unit (e.g.: 12 kg*m/s)", max_length=255)
    symbol = models.CharField("Symbol to use in a formula (e.g.: myu)", max_length=20, blank=True,
                              null=True)
    alias = models.CharField("Other code for this unit (e.g.: mybu)", max_length=20, null=True,
                             blank=True)

    class Meta:
        """
        Meta
        """
        unique_together = ('user', 'key', 'code')
        ordering = ['name', 'code']

    def save(self, *args, **kwargs):
        """
        Save custom unit to database
        """
        us = UnitSystem(system_name=self.unit_system)
        self.code = self.code.replace('-', '_')
        self.symbol = self.symbol.replace('-', '_')
        self.alias = self.alias.replace('-', '_')
        if self.code in us.available_unit_names():
            raise UnitDuplicateError
        try:
            us.add_definition(code=self.code, relation=self.relation, symbol=self.symbol,
                              alias=self.alias)
        except ValueError as e:
            raise UnitValueError(str(e)) from e
        try:
            us.unit(self.code).unit.dimensionality
        except pint.errors.UndefinedUnitError:
            raise UnitDimensionError
        return super(CustomUnit, self).save(*args, **kwargs)


class Operand:
    """
    Operand in a formula
    """
    name = None
    value = None
    unit = None
    uncertainty = None

    def __init__(self,
                 name: str = None,
                 value: float = 0,
                 unit: str = None,
                 uncertainty: str = None):
        """
        Initialize Operand
        :param name: name of the operand that appears in the formula
        :param value: float magnitude
        :param unit: units
        """
        self.name = name
        self.value = value
        self.unit = unit
        self.uncertainty = uncertainty
        if self.validate():
            self.uvalue = uncertainties.ufloat(value, self.parse_uncertainty())
        else:
            self.uvalue = uncertainties.ufloat(0, 0)

    def validate(self):
        """
        Validate operand
        """
        if not self.name or self.value is None or self.unit is None:
            return False
        try:
            float(self.value)
        except ValueError:
            return False
        try:
            self.parse_uncertainty()
        except (ValueError, AttributeError):
            return False
        return True

    def get_unit(self, unit_system: UnitSystem) -> str:
        """
        Transform unit if unit is a dimension
        """
        # Find dimensions
        exp = r'(?P<dim>\[\w+\])'
        replace_dict = {}
        for dimension_name in re.findall(exp, self.unit):
            try:
                dim = Dimension(unit_system=unit_system, code=dimension_name)
                replace_dict[dimension_name] = str(dim.units().pop())
            except DimensionNotFound:
                pass
        # Replace in formula
        for key, item in replace_dict.items():
            self.unit = self.unit.replace(key, item)
        return self.unit

    def get_magnitude(self):
        return self.uvalue.n

    def get_uncertainty(self):
        return self.uvalue.s

    def parse_uncertainty(self):
        if not self.uncertainty:
            return 0
        if self.uncertainty.endswith('%'):
            return self.value * float(self.uncertainty[:-1]) * 0.01
        else:
            return float(self.uncertainty)


class ComputationError(Exception):
    pass


class Expression:
    """
    Expression with operands
    """
    expression = None
    operands = None
    out_units = None

    def __init__(self, expression: str, operands: [Operand], out_units: str = None):
        """
        Initialize Expression
        :param expression: string expression with placeholders
        :param operands: List of Operand corresponding to placeholders
        """
        self.expression = expression
        self.operands = operands
        self.out_units = out_units

    def validate(self, unit_system: UnitSystem) -> (bool, str):
        """
        Validate syntax and homogeneity
        :param unit_system: UnitSystem
        """
        q_ = unit_system.ureg.Quantity
        if not self.expression:
            return False, "missing expression"
        try:
            sympify(self.expression.format(**{v.name: v.value for v in self.operands}))
        except SympifyError as e:
            return False, "Improper expression"
        for var in self.operands:
            if not var.validate():
                return False, "invalid operand"
        kwargs = {v.name: q_(v.value, v.unit) for v in self.operands}
        try:
            result = unit_system.ureg.parse_expression(self.expression, **kwargs)
        except KeyError:
            return False, "Missing operand"
        except pint.errors.DimensionalityError:
            return False, "Incoherent dimensions"
        if self.out_units:
            try:
                result.to(self.out_units)
            except pint.errors.DimensionalityError:
                return False, "Incoherent output dimensions"
        return True, ''

    def evaluate(self, unit_system: UnitSystem) -> pint.Quantity:
        """
        Validate formula
        """
        q_ = unit_system.ureg.Quantity
        is_valid, error = self.validate(unit_system=unit_system)
        if is_valid:
            kwargs = {v.name: q_(v.uvalue, v.unit) for v in self.operands}
            result = unit_system.ureg.parse_expression(self.expression, **kwargs)
            if self.out_units:
                return result.to(self.out_units)
            else:
                return result
        else:
            raise ComputationError(f"Invalid formula: {error}")


class CalculationPayload:
    """
    Calculation payload: caculate expressions
    """
    data = None
    unit_system = ''
    user = ''
    key = ''
    batch_id = ''
    eob = False

    def __init__(self, unit_system: UnitSystem, key: str = None, data: [] = None,
                 batch_id: str = None, eob: bool = False):
        """
        Initialize payload
        """
        self.data = data
        self.unit_system = unit_system
        self.key = key
        self.batch_id = batch_id
        self.eob = eob


class CalculationResultDetail:
    """
    Details of an evaluation
    """
    expression = None
    operands = None
    magnitude = None
    uncertainty = None
    unit = None

    def __init__(self, expression: str, operands: [],
                 magnitude: uncertainties.ufloat, unit: str):
        """
        Initialize detail
        :param expression: Expression in the form of a string e.g.: 3*{a} + 2 * {b}
        :param operands: List of Operands
        :param magnitude: result of the calculation
        :param units: dimension of the result
        :param uncertainty: uncertainty of the calculation
        """
        self.expression = expression
        self.operands = operands
        self.magnitude = magnitude.n
        self.uncertainty = magnitude.s
        self.unit = unit


class CalculationResultError:
    """
    Error details of a wrong calculation
    """
    expression = None
    operands = None
    calc_date = None
    error = None

    def __init__(self, expression: str, operands: [], calc_date: date, error: str):
        """
        Initialize error detail
        :param expression: Expression in the form of a string
        :param operands: List of Operands
        :param date: date of the evaluation
        :param error: Error description
        """
        self.expression = expression
        self.operands = operands
        self.calc_date = calc_date
        self.error = error


class CalculationResult:
    """
    Result of a batch of evaluations
    """
    id = None
    detail = []
    status = None
    errors = []

    def __init__(self, id: str = None, detail: [CalculationResultDetail] = None,
                 status: str = BaseConverter.INITIATED_STATUS,
                 errors: [CalculationResultError] = None):
        """
        Initialize result
        :param id: ID of the batch
        :param detail: List of CalculationResultDetail
        :param status: status of the batch
        :param errors: List of CalculationResultErrors
        """
        self.id = id
        self.detail = detail or []
        self.status = status
        self.errors = errors or []

    def end_batch(self):
        """
        Puts a finall status on the batch
        """
        if self.errors:
            self.status = BaseConverter.WITH_ERRORS
        else:
            self.status = BaseConverter.FINISHED
        return self.status


class ExpressionCalculator(BaseConverter):
    """
    Conversion between units
    """
    unit_system = None

    def __init__(self, unit_system: str, user: User = None, key: str = '', id: str = None):
        """
        Initiate ExpressionCalculator
        :param unit_system: unit system name
        :param user: User
        :param key: key of user
        :param id: ID of the batch
        """
        try:
            super().__init__(id=id)
            self.unit_system = unit_system
            self.user = user
            self.key = key
            self.system = UnitSystem(system_name=unit_system, user=self.user, key=self.key)
        except UnitSystemNotFound as e:
            raise ExpressionCalculatorInitError from e

    def add_data(self, data: []) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        errors = super().add_data(data)
        return errors

    def check_data(self, data):
        """
        Validates that the data contains
        - system (str)
        - unit (str)
        - value (float)
        - date (YYYY-MM-DD)
        """
        from .serializers import ExpressionSerializer
        errors = []
        for line in data:
            serializer = ExpressionSerializer(data=line)
            if serializer.is_valid(unit_system=self.system):
                self.data.append(serializer.create(serializer.validated_data))
            else:
                errors.append(serializer.errors)
        return errors

    @classmethod
    def load(cls, id: str, user: User = None, key: str = None) -> BaseConverter:
        """
        Load converter from batch
        :param id: ID of the batch
        :param user: Users object
        :param key: User defined category
        """
        try:
            uc = super().load(id)
            uc.system = UnitSystem(system_name=uc.unit_system, user=user, key=key)
            return uc
        except (UnitSystemNotFound, KeyError) as e:
            raise ConverterLoadError

    def save(self):
        """
        Save converter to caching system
        """
        system = self.system
        self.system = None
        super(ExpressionCalculator, self).save()
        self.system = system

    def convert(self) -> CalculationResult:
        """
        Converts data to base unit in base system
        """
        result = CalculationResult(id=self.id)
        for expression in self.data:
            valid, exp_error = expression.validate(unit_system=self.system)
            if not valid:
                error = CalculationResultError(
                    expression=expression.expression,
                    operands=expression.operands,
                    calc_date=date.today(),
                    error=exp_error
                )
                result.errors.append(error)
                continue
            try:
                out = expression.evaluate(unit_system=self.system)
            except ComputationError as e:
                error = CalculationResultError(
                    expression=expression.expression,
                    operands=expression.operands,
                    calc_date=date.today(),
                    error=str(e)
                )
                result.errors.append(error)
                continue
            detail = CalculationResultDetail(
                expression=expression.expression,
                operands=expression.operands,
                magnitude=out.magnitude,
                unit=out.units
            )
            result.detail.append(detail)
        self.end_batch(result.end_batch())
        return result
