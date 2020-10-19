class UnitSystemNotFound(Exception):
    message = "Unit system name is not valid"


class DimensionNotFound(Exception):
    message = "Dimension not found in the registry"


class UnitNotFound(Exception):
    message = "Unit not found in the registry"


class UnitDuplicateError(Exception):
    message = "Unit with the same code already exists in the registry"


class UnitDimensionError(Exception):
    message = "Unit dimensionality is not valid for the registry"


class UnitConverterInitError(Exception):
    message = 'Error during initialization of converter'


class UnitConverterConvertError(Exception):
    message = 'Error converting values'
