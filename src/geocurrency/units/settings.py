# dict with hunan readable name, technical name, and symbol, and relation to a base unit
#
# {
#   'SI': {
#       'meter_per_square_centimeter' :
#       {
#           'name': _('meter per square centimeter'),
#           'symbol': 'm.cm⁻²',
#           'relation': '0.0001 meter / meter ** 2'
#       }
#   }
# }
# This will display these units in the list of units
ADDITIONAL_UNITS = {}

# Show units with prefixed values in APIs
PREFIXED_UNITS_DISPLAY = {
    'meter': ['milli', 'centi', 'kilo'],
    'gram': ['milli', 'kilo'],
    'second': ['micro', 'milli'],
    'ampere': ['milli'],
}
