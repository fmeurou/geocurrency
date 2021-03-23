"""
Settings for Units module
"""
from django.conf import settings

# This will display these units in the list of units
ADDITIONAL_UNITS = {}

# Show units with prefixed values in APIs
PREFIXED_UNITS_DISPLAY = {
    'meter': ['milli', 'centi', 'kilo'],
    'gram': ['milli', 'kilo'],
    'second': ['micro', 'milli'],
    'ampere': ['milli'],
}
