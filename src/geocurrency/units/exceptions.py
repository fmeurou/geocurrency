"""
Units exception classes
"""


class UnitSystemNotFound(Exception):
    """
    UnitSystem not found exception
    """
    message = "Unit system name is not valid"


class DimensionNotFound(Exception):
    """
    Dimension not found exception
    """
    message = "Dimension not found in the registry"


class UnitNotFound(Exception):
    """
    Unit not found exception
    """
    message = "Unit not found in the registry"


class UnitDuplicateError(Exception):
    """
    Error duplicating unit
    """
    message = "Unit with the same code already exists in the registry"


class UnitValueError(Exception):
    """
    Error creating unit
    """
    message = "Unit values are inconsistent"


class UnitDimensionError(Exception):
    """
    Invalid dimension for the unit system
    """
    message = "Unit dimensionality is not valid for the registry"


class UnitConverterInitError(Exception):
    """
    Converter cannot be initialized
    """
    message = 'Error during initialization of converter'


class UnitConverterConvertError(Exception):
    """
    Error converting units
    """
    message = 'Error converting values'


class ExpressionCalculatorInitError(Exception):
    """
    Error initializing  Calculator
    """
    message = "Error initializing Expression calculator"
