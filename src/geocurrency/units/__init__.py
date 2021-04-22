"""
Units module
"""

from django.utils.translation import ugettext_lazy as _, pgettext_lazy

DIMENSIONS = {
    '[length]': {'name': _('length'), 'dimension': 'meter', 'symbol': 'L'},
    '[time]': {'name': _('time'), 'dimension': 'second', 'symbol': 'T'},
    '[current]': {'name': _('current'), 'dimension': 'ampere', 'symbol': 'I'},
    '[luminosity]': {'name': _('luminosity'), 'dimension': 'candela * radian ** 2',
                     'symbol': 'J'},
    '[mass]': {'name': _('mass'), 'dimension': 'kilogram', 'symbol': 'M'},
    '[substance]': {'name': _('substance'), 'dimension': 'mole', 'symbol': 'N'},
    '[temperature]': {'name': _('temperature'), 'dimension': 'kelvin', 'symbol': 'Θ'},
    '[]': {'name': _('constant'), 'dimension': 'bit', 'symbol': 'b'},
    '[area]': {'name': _('area'), 'dimension': 'meter ** 2', 'symbol': 'L²'},
    '[volume]': {'name': _('volume'), 'dimension': 'meter ** 3', 'symbol': 'L³'},
    '[frequency]': {'name': _('frequency'), 'dimension': 'count / second',
                    'symbol': 'T⁻¹'},
    '[wavenumber]': {'name': _('wavenumber'), 'dimension': '1 / meter', 'symbol': 'L⁻¹'},
    '[velocity]': {'name': _('velocity'), 'dimension': 'meter / second',
                   'symbol': 'L.T⁻¹'},
    '[acceleration]': {'name': _('acceleration'), 'dimension': 'meter / second ** 2',
                       'symbol': 'L.T⁻²'},
    '[force]': {'name': _('force'), 'dimension': 'kilogram * meter / second ** 2',
                'symbol': 'F'},
    '[energy]': {'name': _('energy'), 'dimension': 'kilogram * meter ** 2 / second ** 2',
                 'symbol': 'E'},
    '[power]': {'name': _('power'), 'dimension': 'kilogram * meter ** 2 / second ** 3',
                'symbol': 'P'},
    '[density]': {'name': _('density'), 'dimension': 'kilogram / meter ** 3',
                  'symbol': 'M.L⁻³'},
    '[pressure]': {'name': _('pressure'), 'dimension': 'kilogram / meter / second ** 2',
                   'symbol': 'Pa'},
    '[torque]': {'name': _('torque'), 'dimension': 'kilogram * meter ** 2 / second ** 2',
                 'symbol': 'F.L'},
    '[viscosity]': {'name': _('viscosity'), 'dimension': 'kilogram / meter / second',
                    'symbol': 'M.L⁻¹.T⁻¹'},
    '[kinematic_viscosity]': {'name': _('kinematic viscosity'),
                              'dimension': 'meter ** 2 / second',
                              'symbol': 'L².T⁻¹'},
    '[fluidity]': {'name': _('fluidity'), 'dimension': 'meter * second / kilogram',
                   'symbol': 'L.T.M⁻¹'},
    '[concentration]': {'name': _('concentration'), 'dimension': 'mole / meter ** 3',
                        'symbol': 'N.L⁻³'},
    '[activity]': {'name': _('activity'), 'dimension': 'mole / second',
                   'symbol': 'N.T⁻¹'},
    '[entropy]': {'name': _('entropy'),
                  'dimension': 'kilogram * meter ** 2 / kelvin / second ** 2',
                  'symbol': ''},
    '[molar_entropy]': {'name': _('molar entropy'),
                        'dimension': 'kilogram * meter ** 2 / kelvin / mole / second ** 2',
                        'symbol': 'M.L².Θ⁻¹.N⁻¹.T⁻²'
                        },
    '[heat_transmission]': {'name': _('heat transmission'),
                            'dimension': 'kilogram / second ** 2',
                            'symbol': 'M.T⁻²'
                            },
    '[luminance]': {'name': _('luminance'),
                    'dimension': 'candela * radian ** 2 / meter ** 2',
                    'symbol': 'J.rad².L⁻²'
                    },
    '[luminous_flux]': {'name': _('luminous flux'),
                        'dimension': 'candela * radian ** 2', 'symbol': 'J.rad²'
                        },
    '[illuminance]': {'name': _('illuminance'),
                      'dimension': 'candela * radian ** 2 / meter ** 2',
                      'symbol': 'J.rad².L⁻²'
                      },
    '[intensity]': {'name': _('intensity'), 'dimension': 'kilogram / second ** 3',
                    'symbol': 'M.T⁻³'},
    '[charge]': {'name': _('charge'), 'dimension': 'ampere * second', 'symbol': 'Q'},
    '[electric_potential]': {'name': _('electric potential'),
                             'dimension': 'kilogram * meter ** 2 / ampere / second ** 3',
                             'symbol': 'V'
                             },
    '[electric_field]': {'name': _('electric field'),
                         'dimension': 'kilogram * meter / ampere / second ** 3',
                         'symbol': ''
                         },
    '[resistance]': {'name': _('resistance'),
                     'dimension': 'kilogram * meter ** 2 / ampere ** 2 / second ** 3',
                     'symbol': 'Ω'
                     },
    '[conductance]': {'name': _('conductance'),
                      'dimension': 'ampere ** 2 * second ** 3 / kilogram / meter ** 2',
                      'symbol': 'S'
                      },
    '[capacitance]': {'name': _('capacitance'),
                      'dimension': 'ampere ** 2 * second ** 4 / kilogram / meter ** 2',
                      'symbol': 'F'
                      },
    '[inductance]': {'name': _('inductance'),
                     'dimension': 'kilogram * meter ** 2 / ampere ** 2 / second ** 2',
                     'symbol': 'H'
                     },
    '[magnetic_flux]': {'name': _('magnetic flux'),
                        'dimension': 'kilogram * meter ** 2 / ampere / second ** 2',
                        'symbol': 'Wb'
                        },
    '[magnetic_field]': {'name': _('magnetic field'),
                         'dimension': 'kilogram / ampere / second ** 2',
                         'symbol': ''
                         },
    '[magnetomotive_force]': {'name': _('magnetomotive force'), 'dimension': 'ampere',
                              'symbol': 'I'
                              },
    '[electric_dipole]': {'name': _('electric dipole'),
                          'dimension': 'ampere * meter * second',
                          'symbol': ''
                          },
    '[electric_quadrupole]': {'name': _('electric quadrupole'),
                              'dimension': 'ampere * meter ** 2 * second',
                              'symbol': ''
                              },
    '[magnetic_dipole]': {'name': _('magnetic dipole'),
                          'dimension': 'ampere * meter ** 2', 'symbol': ''
                          },
    '[printing_unit]': {'name': _('printing unit'), 'dimension': 'pixel',
                        'symbol': 'pixel'
                        },
    '[gaussian_charge]': {'name': _('gaussian charge'),
                          'dimension': 'kilogram ** 0.5 * meter ** 1.5 / second',
                          'symbol': ''
                          },
    '[gaussian_current]': {'name': _('gaussian current'),
                           'dimension': 'kilogram ** 0.5 * meter ** 1.5 / second ** 2',
                           'symbol': ''
                           },
    '[gaussian_electric_potential]': {'name': _('gaussian electric potential'),
                                      'dimension': 'kilogram ** 0.5 * meter ** 0.5 / second',
                                      'symbol': ''
                                      },
    '[gaussian_electric_field]': {'name': _('gaussian electric field'),
                                  'dimension': 'kilogram ** 0.5 / meter ** 0.5 / second',
                                  'symbol': ''
                                  },
    '[gaussian_electric_displacement_field]': {
        'name': _('gaussian electric displacement field'),
        'dimension': 'kilogram ** 0.5 / meter ** 0.5 / second',
        'symbol': ''
    },
    '[gaussian_electric_flux]': {'name': _('gaussian electric flux'),
                                 'dimension': 'kilogram ** 0.5 * meter ** 1.5 / second',
                                 'symbol': ''
                                 },
    '[gaussian_magnetic_field]': {'name': _('gaussian magnetic field'),
                                  'dimension': 'kilogram ** 0.5 / meter ** 0.5 / second',
                                  'symbol': ''
                                  },
    '[gaussian_magnetic_field_strength]': {'name': _('gaussian magnetic field strength'),
                                           'dimension': 'kilogram ** 0.5 / meter ** 0.5 / second',
                                           'symbol': ''
                                           },
    '[gaussian_magnetic_flux]': {'name': _('gaussian magnetic flux'),
                                 'dimension': 'kilogram ** 0.5 * meter ** 1.5 / second',
                                 'symbol': ''
                                 },
    '[gaussian_resistance]': {'name': _('gaussian resistance'),
                              'dimension': 'second / meter',
                              'symbol': ''
                              },
    '[gaussian_resistivity]': {'name': _('gaussian resistivity'), 'dimension': 'second',
                               'symbol': ''
                               },
    '[gaussian_capacitance]': {'name': _('gaussian capacitance'), 'dimension': 'meter',
                               'symbol': ''
                               },
    '[gaussian_inductance]': {'name': _('gaussian inductance'),
                              'dimension': 'second ** 2 / meter',
                              'symbol': ''
                              },
    '[gaussian_conductance]': {'name': _('gaussian conductance'),
                               'dimension': 'meter / second',
                               'symbol': ''
                               },
    '[esu_charge]': {'name': _('esu charge'),
                     'dimension': 'kilogram ** 0.5 * meter ** 1.5 / second',
                     'symbol': ''
                     },
    '[esu_current]': {'name': _('esu current'),
                      'dimension': 'kilogram ** 0.5 * meter ** 1.5 / second ** 2',
                      'symbol': ''
                      },
    '[esu_electric_potential]': {'name': _('esu electric potential'),
                                 'dimension': 'kilogram ** 0.5 * meter ** 0.5 / second',
                                 'symbol': ''
                                 },
    '[esu_magnetic_flux]': {'name': _('esu magnetic flux'),
                            'dimension': 'kilogram ** 0.5 * meter ** 0.5',
                            'symbol': ''
                            },
    '[esu_magnetic_field]': {'name': _('esu magnetic field'),
                             'dimension': 'kilogram ** 0.5 / meter ** 1.5',
                             'symbol': ''
                             },
    '[compounded]': {'name': _('Compound dimension'),
                     'dimension': 'undefined',
                     'symbol': ''
                     },
    '[custom]': {'name': _('Custom dimension'), 'dimension': 'undefined', 'symbol': ''},
}

UNIT_SYSTEM_BASE_AND_DERIVED_UNITS = {
    'SI': {
        '[]': 'count',
        '[time]': 'second',
        '[length]': 'meter',
        '[mass]': 'kilogram',
        '[current]': 'ampere',
        '[temperature]': 'kelvin',
        '[substance]': 'mole',
        '[luminosity]': 'candela',
        '[area]': 'square_meter',
        '[volume]': 'cubic_meter',
        '[frequency]': 'meter_per_second',
        '[acceleration]': 'meter_per_square_second',
        '[force]': 'newton',
        '[energy]': 'joule',
        '[electric_charge]': 'coulomb',
        '[electric_potential]': 'volt',
        '[capacitance]': 'farad',
        '[resistance]': 'ohm',
        '[conductance]': 'siemens',
        '[magnetic_flux]': 'weber',
        '[inductance]': 'henry',
        '[luminous_flux]': 'lumen',
        '[illuminance]': 'lux',
        '[activity]': 'katal',
    },
    'Planck': {
        '[length]': 'planck_length',
        '[mass]': 'planck_mass',
        '[time]': 'planck_time',
        '[temperature]': 'planck_temperature',
        '[current]': 'planck_current'
    },
    'US': {
        '[length]': 'yard',
        '[mass]': 'pound'
    },
    'atomic': {
        '[length]': 'bohr',
        '[mass]': 'electron_mass',
        '[time]': 'atomic_unit_of_time',
        '[current]': 'atomic_unit_of_current',
        '[temperature]': 'atomic_unit_of_temperature'
    },
    'cgs': {
        '[length]': 'centimeter',
        '[mass]': 'gram',
        '[time]': 'second',
        '[velocity]': 'centimeter_per_second',
        '[acceleration]': 'galileo',
        '[force]': 'dyn',
        '[energy]': 'erg',
        '[power]': 'watt',
        '[pressure]': 'barye',
        '[dynamic_viscosity]': 'poise',
        '[kinematic_viscosity]': 'stokes',
        '[wavenumber]': 'reciprocal_centimeter'
    },
    'imperial': {
        '[length]': 'yard',
        '[mass]': 'pound'
    },
    'mks': {
        '[acceleration]': 'meter_per_square_second',
        '[capacitance]': 'farad',
        '[charge]': 'coulomb',
        '[current]': 'ampere',
        '[electric_field]': 'volt_per_meter',
        '[electric_potential]': 'volt',
        '[energy]': 'joule',
        '[power]': 'watt',
        '[force]': 'newton',
        '[inductance]': 'henry',
        '[length]': 'meter',
        '[magnetic_field]': 'tesla',
        '[magnetic_flux]': 'weber',
        '[mass]': 'kilogram',
        '[pressure]': 'pascal',
        '[resistance]': 'ohm',
        '[temperature]': 'kelvin',
        '[time]': 'second',
        '[velocity]': 'meter_per_second'
    }
}

PREFIX_SYMBOL = {
    'yotta': 'Y',
    'zetta': 'Z',
    'exa': 'E',
    'peta': 'P',
    'tera': 'T',
    'giga': 'G',
    'mega': 'M',
    'kilo': 'k',
    'hecto': 'h',
    'deca': 'da',
    'deci': 'd',
    'centi': 'c',
    'milli': 'm',
    'micro': 'μ',
    'nano': 'n',
    'pico': 'p',
    'femto': 'f',
    'atto': 'a',
    'zepto': 'z',
    'yocto': 'y'
}

ADDITIONAL_BASE_UNITS = {
    'SI': {
        'meter_per_second': {
            'name': _('meter per second'),
            'symbol': 'm.s⁻¹',
            'relation': '1 meter / second'
        },
        'meter_per_square_second': {
            'name': _('meter per square second'),
            'symbol': 'm.s⁻²',
            'relation': '1 meter / second ** 2'
        },
        'square_meter': {
            'name': _('square meter'),
            'symbol': 'm²',
            'relation': '1 meter ** 2'
        },
        'cubic_meter': {
            'name': _('cubic meter'),
            'symbol': 'm³',
            'relation': '1 meter ** 3'
        },
    }
}

# Dictionnary with translations
UNIT_EXTENDED_DEFINITION = {
    'K_alpha_Cu_d_220': {
        'name': _('Copper Kα'),
        'symbol': 'Cu Kα',
    },
    'K_alpha_Mo_d_220': {
        'name': _('Molybdenum K-α'),
        'symbol': 'MO Kα',
    },
    'K_alpha_W_d_220': {
        'name': _('Tungsten K-α'),
        'symbol': _('W Kα'),
    },
    'RKM': {
        'name': _('RKM'),
        'symbol': 'RKM',
        'obsolete': True,
    },
    'UK_force_ton': {
        'name': _('long ton-force'),
        'symbol': 'long ton-force',
        'obsolete': True,
    },
    'UK_hundredweight': {
        'name': 'long hundredweight',
        'symbol': 'long hundredweight',
        'obsolete': True,
    },
    'UK_ton': {
        'name': _('long ton'),
        'symbol': 'long ton',
        'obsolete': True,
    },
    'US_force_ton': {
        'name': _('short ton force'),
        'symbol': 'short ton-force',
        'obsolete': True,
    },
    'US_hundredweight': {
        'name': _('short hundredweight'),
        'symbol': 'short hundredweight',
        'obsolete': True,
    },
    'US_ton': {
        'name': _('short ton'),
        'symbol': 'short ton',
        'obsolete': True,
    },
    'US_international_ampere': {
        'name': _('US International Ampere'),
        'symbol': 'US international A',
        'obsolete': True,
    },
    'US_international_ohm': {
        'name': _('US international Ohm'),
        'symbol': 'US international Ω',
        'obsolete': True,
    },
    'US_international_volt': {
        'name': _('US international Volt'),
        'symbol': 'US international V',
        'obsolete': True,
    },
    'US_therm': {
        'name': _('US therm'),
        'symbol': 'thm',
    },
    'abampere': {
        'name': _('abampere'),
        'symbol': 'abA',
    },
    'abcoulomb': {
        'name': _('abcoulomb'),
        'symbol': 'abC',
    },
    'aberdeen': {
        'name': _('Aberdeen'),
        'symbol': 'aberdeen',
    },
    'abfarad': {
        'name': _('abfarad'),
        'symbol': 'abF',
    },
    'abhenry': {
        'name': _('abhenry'),
        'symbol': 'henry',
    },
    'abohm': {
        'name': _('abohm'),
        'symbol': 'abohm',
    },
    'absiemens': {
        'name': _('absiemens'),
        'symbol': 'absiemens',
    },
    'abvolt': {
        'name': _('abvolt'),
        'symbol': 'abV',
    },
    'acre': {
        'name': _('acre'),
        'symbol': 'acre',
    },
    'acre_foot': {
        'name': _('acre-foot'),
        'symbol': 'acre-foot',
    },
    'ampere': {
        'name': _('ampere'),
        'symbol': 'A',
    },
    'milliampere': {
        'name': _('milliampere'),
        'symbol': 'mA',
    },
    'ampere_turn': {
        'name': _('ampere-turn'),
        'symbol': 'At',
    },
    'angstrom': {
        'name': _('angstrom'),
        'symbol': 'Å',
    },
    'angstrom_star': {
        'name': _('angstrom star'),
        'symbol': 'Å*',
    },
    'apothecary_dram': {
        'name': _('apothecary dram'),
        'symbol': 'dr',
    },
    'apothecary_ounce': {
        'name': _('apothecary ounce'),
        'symbol': 'oz',
    },
    'apothecary_pound': {
        'name': _('apothecary pound'),
        'symbol': 'apothecary pound',
    },
    'arcminute': {
        'name': _('minute of arc'),
        'symbol': 'arcmin',
    },
    'arcsecond': {
        'name': _('second of arc'),
        'symbol': 'arcsec',
    },
    'are': {
        'name': _('are'),
        'symbol': 'are',
    },
    'astronomical_unit': {
        'name': _('astronomical unit'),
        'symbol': 'AU',
    },
    'atmosphere_liter': {
        'name': _('atmosphere liter'),
        'symbol': 'atmosphere liter',
    },
    'atomic_mass_constant': {
        'name': _('atomic mass constant'),
        'symbol': 'Da',
    },
    'atomic_unit_of_current': {
        'name': _('atomic unit of current'),
        'symbol': '',
    },
    'atomic_unit_of_electric_field': {
        'name': _('atomic unit of electric field'),
        'symbol': '',
    },
    'atomic_unit_of_force': {
        'name': _('atomic unit of force'),
        'symbol': 'atomic unit of force',
    },
    'atomic_unit_of_intensity': {
        'name': _('atomic unit of intensity'),
        'symbol': 'atomic unit of intensity',
    },
    'atomic_unit_of_temperature': {
        'name': _('atomic unit of temperature'),
        'symbol': 'atomic unit of temperature',
    },
    'atomic_unit_of_time': {
        'name': _('atomic unit of time'),
        'symbol': 'atomic unit of time',
    },
    'avogadro_constant': {
        'name': _('Avogadro constant'),
        'symbol': 'L',
    },
    'avogadro_number': {
        'name': _('Avogadro number'),
        'symbol': '',
    },
    'bag': {
        'name': _('bag'),
        'symbol': 'bag'
    },
    'bar': {
        'name': _('bar'),
        'symbol': 'bar'
    },
    'barn': {
        'name': _('barn'),
        'symbol': 'b'
    },
    'barrel': {
        'name': _('barrel'),
        'symbol': 'barrel'
    },
    'barye': {
        'name': _('barrye'),
        'symbol': 'Ba'
    },
    'baud': {
        'name': _('baud'),
        'symbol': 'Bd'
    },
    'becquerel': {
        'name': _('becquerel'),
        'symbol': 'Bq',
    },
    'beer_barrel': {
        'name': _('beer barrel'),
        'symbol': 'beer barrel'
    },
    'bel': {
        'name': _('bel'),
        'symbol': 'B'
    },
    'biot': {
        'name': _('biot'),
        'symbol': 'biot'
    },
    'biot_turn': {
        'name': _('biot turn'),
        'symbol': 'biot-turn'
    },
    'bit': {
        'name': _('bit'),
        'symbol': 'bit'
    },
    'bits_per_pixel': {
        'name': _('bits per pixel'),
        'symbol': 'bpp'
    },
    'board_foot': {
        'name': _('board foot'),
        'symbol': 'board-foot'
    },
    'bohr': {
        'name': _('bohr'),
        'symbol': 'bohr'
    },
    'bohr_magneton': {
        'name': _('bohr magneton'),
        'symbol': 'μB'
    },
    'boiler_horsepower': {
        'name': _('boiler horsepower'),
        'symbol': 'boiler hp'
    },
    'boltzmann_constant': {
        'name': _('boltzmann constant'),
        'symbol': 'kB'
    },
    'british_thermal_unit': {
        'name': _('british thermal unit'),
        'symbol': 'Btu'
    },
    'buckingham': {
        'name': _('buckingham'),
        'symbol': 'B'
    },
    'bushel': {
        'name': _('bushel'),
        'symbol': 'bsh'
    },
    'byte': {
        'name': _('byte'),
        'symbol': 'byte'
    },
    'cables_length': {
        'name': _('cable length'),
        'symbol': 'cable'
    },
    'calorie': {
        'name': _('calorie'),
        'symbol': 'calorie'
    },
    'candela': {
        'name': _('candela'),
        'symbol': 'cd'
    },
    'carat': {
        'name': _('carat'),
        'symbol': 'ct'
    },
    'centimeter_H2O': {
        'name': _('centimeter H20'),
        'symbol': 'cm H2O'
    },
    'centimeter_Hg': {
        'name': _('centimeter Hg'),
        'symbol': 'cm Hg'
    },
    'century': {
        'name': _('century'),
        'symbol': 'c.'
    },
    'chain': {
        'name': _('chain'),
        'symbol': 'chain'
    },
    'cicero': {
        'name': _('cicero'),
        'symbol': 'cicero'
    },
    'circular_mil': {
        'name': _('circular mil'),
        'symbol': 'mils'
    },
    'classical_electron_radius': {
        'name': _('classical electron radius'),
        'symbol': 're'
    },
    'clausius': {
        'name': _('clausius'),
        'symbol': 'clausius'
    },
    'common_year': {
        'name': _('common year'),
        'symbol': ''
    },
    'conductance_quantum': {
        'name': _('conductance quantum'),
        'symbol': 'G0'
    },
    'conventional_ampere_90': {
        'name': _('conventional ampere'),
        'symbol': 'A90'
    },
    'conventional_coulomb_90': {
        'name': _('conventional coulomb'),
        'symbol': 'C90'
    },
    'conventional_farad_90': {
        'name': _('conventional farad'),
        'symbol': 'F90'
    },
    'conventional_henry_90': {
        'name': _('conventional henry'),
        'symbol': 'H90',
    },
    'conventional_josephson_constant': {
        'name': _('conventional josephson constant'),
        'symbol': 'KJ'
    },
    'conventional_ohm_90': {
        'name': _('conventional ohm'),
        'symbol': 'Ω90'
    },
    'conventional_volt_90': {
        'name': _('conventional volt'),
        'symbol': 'V90'
    },
    'conventional_von_klitzing_constant': {
        'name': _('conventional Von Klitzing constant'),
        'symbol': 'RK',
    },
    'conventional_watt_90': {
        'name': _('conventional Watt'),
        'symbol': 'W90',
    },
    'coulomb': {
        'name': _('coulomb'),
        'symbol': 'C'
    },
    'coulomb_constant': {
        'name': _('coulomb constant'),
        'symbol': 'K'
    },
    'count': {
        'name': _('count'),
        'symbol': ''
    },
    'counts_per_second': {
        'name': _('counts per second'),
        'symbol': 'counts/s'
    },
    'css_pixel': {
        'name': _('CSS pixel'),
        'symbol': 'px'
    },
    'cubic_centimeter': {
        'name': _('cubic centimeter'),
        'symbol': 'cm³'
    },
    'cubic_millimmeter': {
        'name': _('cubic milliimeter'),
        'symbol': 'mm³'
    },
    'cubic_foot': {
        'name': _('cubic foot'),
        'symbol': 'cubic foot'
    },
    'cubic_inch': {
        'name': _('cubic inch'),
        'symbol': 'cubic inch'
    },
    'cubic_yard': {
        'name': _('cubic yard'),
        'symbol': 'cubic yard'
    },
    'cup': {
        'name': _('cup'),
        'symbol': 'cup'
    },
    'curie': {
        'name': _('curie'),
        'symbol': 'Ci'
    },
    'dalton': {
        'name': _('dalton'),
        'symbol': 'Da'
    },
    'darcy': {
        'name': _('darcy'),
        'symbol': 'D'
    },
    'day': {
        'name': _('day'),
        'symbol': pgettext_lazy('unit', 'day')
    },
    'debye': {
        'name': _('debye'),
        'symbol': 'D'
    },
    'decade': {
        'name': _('decade'),
        'symbol': pgettext_lazy('symbol', 'decade')
    },
    'decibel': {
        'name': _('decibel'),
        'symbol': 'dB'
    },
    'degree': {
        'name': _('degree'),
        'symbol': '°'
    },
    'degree_Celsius': {
        'name': _('degree Celsius'),
        'symbol': '°C'
    },
    'degree_Fahrenheit': {
        'name': _('degree Fahrenheit'),
        'symbol': '°F'
    },
    'degree_Rankine': {
        'name': _('degree Rankine'),
        'symbol': '°R'
    },
    'degree_Reaumur': {
        'name': _('degree Reaumur'),
        'symbol': '°Re'
    },
    'denier': {
        'name': _('denier'),
        'symbol': 'D'
    },
    'didot': {
        'name': _('didot'),
        'symbol': 'didot'
    },
    'dirac_constant': {
        'name': _('Dirac constant'),
        'symbol': 'ħ'
    },
    'dram': {
        'name': _('dram'),
        'symbol': 'dr'
    },
    'dry_barrel': {
        'name': _('dry barrel'),
        'symbol': 'dry barrel'
    },
    'dry_gallon': {
        'name': _('dry gallon'),
        'symbol': 'dry gallon'
    },
    'dry_pint': {
        'name': _('dry pint'),
        'symbol': 'dry pint'
    },
    'dry_quart': {
        'name': _('dry quart'),
        'symbol': 'dry quart'
    },
    'dtex': {
        'name': _('decitex'),
        'symbol': 'dtex'
    },
    'dyne': {
        'name': _('dyne'),
        'symbol': 'dyn'
    },
    'electrical_horsepower': {
        'name': _('eletcrical horsepower'),
        'symbol': 'HP'
    },
    'electron_g_factor': {
        'name': _('electron G-factor'),
        'symbol': 'electron G-factor'
    },
    'electron_mass': {
        'name': _('electron mass'),
        'symbol': 'me'
    },
    'electron_volt': {
        'name': _('electronvolt'),
        'symbol': 'eV'
    },
    'elementary_charge': {
        'name': _('elementary charge'),
        'symbol': 'e'
    },
    'entropy_unit': {
        'name': _('entropy unit'),
        'symbol': 'S'
    },
    'enzyme_unit': {
        'name': _('enzyme unit'),
        'symbol': 'U'
    },
    'eon': {
        'name': _('eon'),
        'symbol': 'eon'
    },
    'erg': {
        'name': _('erg'),
        'symbol': 'erg'
    },
    'farad': {
        'name': _('farad'),
        'symbol': 'F'
    },
    'faraday': {
        'name': _('faraday'),
        'symbol': 'faraday',
    },
    'faraday_constant': {
        'name': _('faraday constant'),
        'symbol': 'F',
    },
    'fathom': {
        'name': _('fathom'),
        'symbol': 'fathom',
    },
    'fermi': {
        'name': _('fermi'),
        'symbol': 'fm',
    },
    'fifteen_degree_calorie': {
        'name': _('fifteen degree calorie'),
        'symbol': 'fifteen degree calorie',
    },
    'fifth': {
        'name': _('fifth'),
        'symbol': 'fifth',
    },
    'fine_structure_constant': {
        'name': _('fine structure constant'),
        'symbol': 'α',
    },
    'first_radiation_constant': {
        'name': _('first radiation constant'),
        'symbol': 'c1',
    },
    'fluid_dram': {
        'name': _('fluid dram'),
        'symbol': 'fluid dr'
    },
    'fluid_ounce': {
        'name': _('fluid ounce'),
        'symbol': 'fluid ounce'
    },
    'foot': {
        'name': _('foot'),
        'symbol': 'foot'
    },
    'foot_H2O': {
        'name': _('foot H2O'),
        'symbol': 'foot H2O'
    },
    'foot_per_second': {
        'name': _('foot per second'),
        'symbol': 'foot per second'
    },
    'foot_pound': {
        'name': _('foot pound'),
        'symbol': 'foot pound'
    },
    'force_gram': {
        'name': _('gram-force'),
        'symbol': 'gram-force',
        'obsolete': True,
    },
    'force_kilogram': {
        'name': _('kilogram-force'),
        'symbol': 'kg-force',
        'obsolete': True,
    },
    'force_long_ton': {
        'name': _('long ton-force'),
        'symbol': 'long ton-force',
        'obsolete': True},
    'force_metric_ton': {
        'name': _('tonne-force'),
        'symbol': 'tf',
        'obsolete': True},
    'force_ounce': {
        'name': _('ounce-force'),
        'symbol': 'ounce force',
        'obsolete': True},
    'force_pound': {
        'name': _('pound-force'),
        'symbol': 'pound force',
        'obsolete': True},
    'force_ton': {
        'name': _('tonne-force'),
        'symbol': 'tf',
        'obsolete': True},
    'fortnight': {
        'name': _('fortnight'),
        'symbol': 'fortnight'
    },
    'franklin': {
        'name': _('franklin'),
        'symbol': 'Fr'
    },
    'furlong': {
        'name': _('furlong'),
        'symbol': 'furlong'
    },
    'galileo': {
        'name': _('galileo'),
        'symbol': 'Gal'
    },
    'gallon': {
        'name': _('gallon'),
        'symbol': 'gal'
    },
    'gamma': {
        'name': _('gamma'),
        'symbol': 'γ'
    },
    'gamma_mass': {
        'name': _('gamma'),
        'symbol': 'γ'
    },
    'gauss': {
        'name': _('gauss'),
        'symbol': 'G'
    },
    'gilbert': {
        'name': _('gilbert'),
        'symbol': 'Gb'
    },
    'gill': {
        'name': _('gill'),
        'symbol': 'gill',
    },
    'grade': {
        'name': _('grade'),
        'symbol': 'gr',
    },
    'grain': {
        'name': _('grain'),
        'symbol': 'grain',
    },
    'gram': {
        'name': _('gram'),
        'symbol': 'g',
    },
    'gray': {
        'name': _('gray'),
        'symbol': 'Gy',
    },
    'gregorian_year': {
        'name': _('gregorian year'),
        'symbol': pgettext_lazy('unit', 'gregorian year'),
    },
    'hand': {
        'name': _('hand'),
        'symbol': 'hand',
    },
    'hartree': {
        'name': _('hartree'),
        'symbol': 'Eh',
    },
    'hectare': {
        'name': _('hectare'),
        'symbol': 'ha',
    },
    'henry': {
        'name': _('henry'),
        'symbol': 'henry',
    },
    'hertz': {
        'name': _('hertz'),
        'symbol': 'Hz',
    },
    'hogshead': {
        'name': _('hogshead'),
        'symbol': 'hhd',
    },
    'horsepower': {
        'name': _('horsepower'),
        'symbol': 'HP',
    },
    'hour': {
        'name': _('hour'),
        'symbol': 'h',
    },
    'hundredweight': {
        'name': _('hundredweight'),
        'symbol': 'cwt',
    },
    'impedance_of_free_space': {
        'name': _('impedance of free space'),
        'symbol': 'Z0',
    },
    'imperial_barrel': {
        'name': _('imperial barrel'),
        'symbol': 'imperial barrel',
    },
    'imperial_bushel': {
        'name': _('imperial bushel'),
        'symbol': 'bsh',
    },
    'imperial_cup': {
        'name': _('imperial cup'),
        'symbol': 'imperial cup',
    },
    'imperial_fluid_drachm': {
        'name': _('imperial fluid drachm'),
        'symbol': 'ʒ',
    },
    'imperial_fluid_ounce': {
        'name': _('imperial fluid ounce'),
        'symbol': 'fl oz',
    },
    'imperial_fluid_scruple': {
        'name': _('imperial fluid scruple'),
        'symbol': '℈',
    },
    'imperial_gallon': {
        'name': _('imperial gallon'),
        'symbol': 'imperial gallon',
    },
    'imperial_gill': {
        'name': _('imperial gill'),
        'symbol': 'imperial gill',
    },
    'imperial_minim': {
        'name': _('imperial minim'),
        'symbol': 'min',
    },
    'imperial_peck': {
        'name': _('imperial peck'),
        'symbol': 'peck'
    },
    'imperial_pint': {
        'name': _('imperial pint'),
        'symbol': 'imperial pint'
    },
    'imperial_quart': {
        'name': _('imperial quart'),
        'symbol': 'imperial quart'
    },
    'inch': {
        'name': _('inch'),
        'symbol': 'inch'
    },
    'inch_H2O_39F': {
        'name': _('inch H20 39F'),
        'symbol': 'inch H20 39F'
    },
    'inch_H2O_60F': {
        'name': _('inch H20 60F'),
        'symbol': 'inch H20 60F'
    },
    'inch_Hg': {
        'name': _('inch Hg'),
        'symbol': 'inch Hg'
    },
    'inch_Hg_60F': {
        'name': _('inch Hg 60F'),
        'symbol': 'inch Hg 60F'
    },
    'international_british_thermal_unit': {
        'name': _('international Btu'),
        'symbol': 'international Btu'
    },
    'international_calorie': {
        'name': _('international calorie'),
        'symbol': 'international calorie'
    },
    'josephson_constant': {
        'name': _('Josephson constant'),
        'symbol': 'KJ'
    },
    'joule': {
        'name': _('Joule'),
        'symbol': 'J'
    },
    'jute': {
        'name': _('jute'),
        'symbol': 'jute'
    },
    'katal': {
        'name': _('katal'),
        'symbol': 'kat'
    },
    'kelvin': {
        'name': _('kelvin'),
        'symbol': 'K'
    },
    'kilometer_per_hour': {
        'name': _('kilometer per hour'),
        'symbol': 'km/hour'
    },
    'kilometer_per_second': {
        'name': _('kilometer per second'),
        'symbol': 'km/second'
    },
    'kip': {
        'name': _('kip'),
        'symbol': 'kip'
    },
    'kip_per_square_inch': {
        'name': _('kip per square inch'),
        'symbol': 'kip / sq inch'
    },
    'knot': {
        'name': _('knot'),
        'symbol': 'kt'
    },
    'lambda': {
        'name': _('lambda'),
        'symbol': 'λ'
    },
    'lambert': {
        'name': _('lambert'),
        'symbol': 'L'
    },
    'langley': {
        'name': _('langley'),
        'symbol': 'Ly'
    },
    'lattice_spacing_of_Si': {
        'name': _('lattice constant'),
        'symbol': 'Ly'
    },
    'league': {
        'name': _('league'),
        'symbol': 'league',
        'obsolete': True},
    'leap_year': {
        'name': _('leap year'),
        'symbol': _('year')
    },
    'light_year': {
        'name': _('light year'),
        'symbol': _('ly')
    },
    'link': {
        'name': _('link'),
        'symbol': _('li')
    },
    'liter': {
        'name': _('liter'),
        'symbol': _('L')
    },
    'ln10': {
        'name': _('log 10'),
        'symbol': _('ln10')
    },
    'long_hundredweight': {
        'name': _('long hundredweight'),
        'symbol': 'long hundredweight',
        'obsolete': True},
    'long_ton': {
        'name': _('long ton'),
        'symbol': 'long ton',
        'obsolete': True},
    'lumen': {
        'name': _('lumen'),
        'symbol': 'lm'
    },
    'lux': {
        'name': _('lux'),
        'symbol': 'lx'
    },
    'magnetic_flux_quantum': {
        'name': _('magnetic flux quantum'),
        'symbol': 'Φ'
    },
    'maxwell': {
        'name': _('maxwell'),
        'symbol': 'Mx'
    },
    'mean_international_ampere': {
        'name': _('mean international ampere'),
        'symbol': 'mean international A'
    },
    'mean_international_ohm': {
        'name': _('mean international Ohm'),
        'symbol': 'mean international Ω'
    },
    'mean_international_volt': {
        'name': _('mean international Volt'),
        'symbol': 'mean international V'
    },
    'mercury': {
        'name': _('density of mercury'),
        'symbol': ''
    },
    'mercury_60F': {
        'name': _('density of mercury 60F'),
        'symbol': ''
    },
    'meter': {
        'name': _('meter'),
        'symbol': 'm'
    },
    'metric_horsepower': {
        'name': _('metric horsepower'),
        'symbol': 'hp'
    },
    'metric_ton': {
        'name': _('metric ton'),
        'symbol': 't'
    },
    'micron': {
        'name': _('micron'),
        'symbol': 'μm'
    },
    'mil': {
        'name': _('mil'),
        'symbol': 'ml'
    },
    'mile': {
        'name': _('mile'),
        'symbol': 'mile'
    },
    'mile_per_hour': {
        'name': _('mile per hour'),
        'symbol': 'mph'
    },
    'millennium': {
        'name': _('millenium'),
        'symbol': _('millenium')
    },
    'milliarcsecond': {
        'name': _('milliarcsecond'),
        'symbol': 'mas'
    },
    'millimeter_Hg': {
        'name': _('Hg millimeter'),
        'symbol': 'mmHg'
    },
    'minim': {
        'name': _('minim'),
        'symbol': 'min'
    },
    'minute': {
        'name': _('minute'),
        'symbol': 'min'
    },
    'molar': {
        'name': _('molar'),
        'symbol': 'M'
    },
    'molar_gas_constant': {
        'name': _('molar gas constant'),
        'symbol': 'R'
    },
    'mole': {
        'name': _('mole'),
        'symbol': 'mol'
    },
    'month': {
        'name': _('month'),
        'symbol': 'm'
    },
    'nautical_mile': {
        'name': _('nautical mile'),
        'symbol': _('nm')
    },
    'neper': {
        'name': _('neper'),
        'symbol': _('Np')
    },
    'neutron_mass': {
        'name': _('neutron mass'),
        'symbol': 'mN'
    },
    'newton': {
        'name': _('newton'),
        'symbol': 'N'
    },
    'newtonian_constant_of_gravitation': {
        'name': _('newtonian constant of gravitation'),
        'symbol': 'N'
    },
    'nit': {
        'name': _('nit'),
        'symbol': 'cd/m²'
    },
    'nuclear_magneton': {
        'name': _('nuclear magneton'),
        'symbol': 'μN'
    },
    'number_english': {
        'name': _('number english'),
        'symbol': 'm/g'
    },
    'number_meter': {
        'name': _('number meter'),
        'symbol': 'm/g'
    },
    'oersted': {
        'name': _('oersted'),
        'symbol': 'Oe'
    },
    'ohm': {
        'name': _('ohm'),
        'symbol': 'Ω'
    },
    'oil_barrel': {
        'name': _('oil barrel'),
        'symbol': 'oil barrel'
    },
    'ounce': {
        'name': _('ounce'),
        'symbol': 'oz t'
    },
    'parsec': {
        'name': _('parsec'),
        'symbol': 'pc'
    },
    'particle': {
        'name': _('particle'),
        'symbol': 'particle'
    },
    'pascal': {
        'name': _('pascal'),
        'symbol': 'Pa'
    },
    'peak_sun_hour': {
        'name': _('peak sun hour'),
        'symbol': 'peak sun hour'
    },
    'peck': {
        'name': _('peck'),
        'symbol': 'peck'
    },
    'pennyweight': {
        'name': _('pennyweight'),
        'symbol': 'dwt'
    },
    'pi': {
        'name': 'pi',
        'symbol': 'π'
    },
    'pica': {
        'name': _('pica'),
        'symbol': 'pica'
    },
    'pint': {
        'name': _('pint'),
        'symbol': 'pt'
    },
    'pixel': {
        'name': _('pixel'),
        'symbol': 'px'
    },
    'pixels_per_centimeter': {
        'name': _('pixel per centimeter'),
        'symbol': 'ppcm'
    },
    'pixels_per_inch': {
        'name': _('pixel per inch'),
        'symbol': 'ppi'
    },
    'planck_constant': {
        'name': _('Planck constant'),
        'symbol': 'h'
    },
    'planck_current': {
        'name': _('Planck current'),
        'symbol': _('qP')
    },
    'planck_length': {
        'name': _('Planck current'),
        'symbol': _('lP')
    },
    'planck_mass': {
        'name': _('Planck mass'),
        'symbol': _('mP')
    },
    'planck_temperature': {
        'name': _('Planck temperature'),
        'symbol': _('TP')
    },
    'planck_time': {
        'name': _('Planck time'),
        'symbol': _('tP')
    },
    'point': {
        'name': _('point'),
        'symbol': 'pt'
    },
    'poise': {
        'name': _('poise'),
        'symbol': 'P'
    },
    'pound': {
        'name': _('pound'),
        'symbol': 'lb'
    },
    'pound_force_per_square_inch': {
        'name': _('pound force per square inch'),
        'symbol': 'lb-force/inch²'
    },
    'poundal': {
        'name': _('poundal'),
        'symbol': 'pdl'
    },
    'proton_mass': {
        'name': _('proton mass'),
        'symbol': 'mP'
    },
    'quadrillion_Btu': {
        'name': _('quadrillion Btu'),
        'symbol': 'quadrillion Btu'
    },
    'quart': {
        'name': _('quart'),
        'symbol': 'qt'
    },
    'quarter': {
        'name': _('quarter'),
        'symbol': 'qr'
    },
    'radian': {
        'name': _('radian'),
        'symbol': 'rad'
    },
    'rads': {
        'name': _('rads'),
        'symbol': 'rads'
    },
    'reciprocal_centimeter': {
        'name': _('reciprocal centimeter'),
        'symbol': 'cm⁻¹'
    },
    'refrigeration_ton': {
        'name': _('refrigeration ton'),
        'symbol': 'TR'
    },
    'rem': {
        'name': _('roentgen equivalent man'),
        'symbol': 'rem'
    },
    'revolutions_per_minute': {
        'name': _('revolutions per minute'),
        'symbol': _('rpm')
    },
    'revolutions_per_second': {
        'name': _('revolutions per second'),
        'symbol': _('rps')
    },
    'reyn': {
        'name': _('reyn'),
        'symbol': _('reyn')
    },
    'rhe': {
        'name': _('reciprocal poise'),
        'symbol': 'P⁻¹'
    },
    'rod': {
        'name': _('rod'),
        'symbol': 'rod'
    },
    'roentgen': {
        'name': _('roentgen'),
        'symbol': 'R'
    },
    'rutherford': {
        'name': _('rutherford'),
        'symbol': 'Rd'
    },
    'rydberg': {
        'name': _('rydberg'),
        'symbol': 'Ry'
    },
    'rydberg_constant': {
        'name': _('rydberg constant'),
        'symbol': 'R∞'
    },
    'scaled_point': {
        'name': _('scaled point'),
        'symbol': 'Pt'
    },
    'scruple': {
        'name': _('scruple'),
        'symbol': '℈'
    },
    'second': {
        'name': _('second'),
        'symbol': 's'
    },
    'millisecond': {
        'name': _('millisecond'),
        'symbol': 'ms'
    },
    'microsecond': {
        'name': _('microsecond'),
        'symbol': 'μs'
    },
    'second_radiation_constant': {
        'name': _('second radiation constant'),
        'symbol': 'c2'
    },
    'shake': {
        'name': _('shake'),
        'symbol': 'shake'
    },
    'shot': {
        'name': _('shot'),
        'symbol': 'shot'
    },
    'sidereal_day': {
        'name': _('sidereal day'),
        'symbol': pgettext_lazy('unit', 'sidereal day')
    },
    'sidereal_month': {
        'name': _('sidereal month'),
        'symbol': pgettext_lazy('unit', 'sidereal month')
    },
    'sidereal_year': {
        'name': _('sidereal year'),
        'symbol': pgettext_lazy('unit', 'sidereal year')
    },
    'siemens': {
        'name': _('siemens'),
        'symbol': 'S'
    },
    'sievert': {
        'name': _('sievert'),
        'symbol': 'Sv'
    },
    'slinch': {
        'name': _('slinch'),
        'symbol': 'slinch'
    },
    'slug': {
        'name': _('slug'),
        'symbol': 'slug'
    },
    'speed_of_light': {
        'name': _('speed of light'),
        'symbol': 'c'
    },
    'square_degree': {
        'name': _('square degree'),
        'symbol': '(°)²'
    },
    'square_foot': {
        'name': _('square foot'),
        'symbol': 'sq ft'
    },
    'square_inch': {
        'name': _('square inch'),
        'symbol': 'sq in'
    },
    'square_league': {
        'name': _('square league'),
        'symbol': 'sq league'
    },
    'square_mile': {
        'name': _('square mile'),
        'symbol': 'sq mile'
    },
    'square_rod': {
        'name': _('square rod'),
        'symbol': 'sq rod'
    },
    'square_survey_mile': {
        'name': _('square survey mile'),
        'symbol': 'sq survey mile'
    },
    'square_yard': {
        'name': _('square yard'),
        'symbol': 'sq yd'
    },
    'standard_atmosphere': {
        'name': _('standard atmosphere'),
        'symbol': 'atm'
    },
    'standard_gravity': {
        'name': _('standard gravity'),
        'symbol': 'g0'
    },
    'standard_liter_per_minute': {
        'name': _('standard liter per minute'),
        'symbol': 'SLM'
    },
    'statampere': {
        'name': 'statampere',
        'symbol': 'statA'
    },
    'statfarad': {
        'name': 'statfarad',
        'symbol': 'statF'
    },
    'stathenry': {
        'name': 'stathenry',
        'symbol': 'stathenry'
    },
    'statmho': {
        'name': 'statmho',
        'symbol': 'statmho'
    },
    'statohm': {
        'name': 'statohm',
        'symbol': 'statohm'
    },
    'stattesla': {
        'name': 'stattesla',
        'symbol': 'stattesla'
    },
    'statvolt': {
        'name': 'statvolt',
        'symbol': 'statvolt'
    },
    'statweber': {
        'name': 'statweber',
        'symbol': 'statweber'
    },
    'stefan_boltzmann_constant': {
        'name': _('Stefan-Boltzmann constant'),
        'symbol': 'σ'
    },
    'steradian': {
        'name': _('steradian'),
        'symbol': 'sr'
    },
    'stere': {
        'name': _('stere'),
        'symbol': 'st'
    },
    'stilb': {
        'name': _('stilb'),
        'symbol': 'sb'
    },
    'stokes': {
        'name': _('stokes'),
        'symbol': 'St'
    },
    'stone': {
        'name': _('stone'),
        'symbol': 'st.'
    },
    'survey_foot': {
        'name': _('survey foot'),
        'symbol': 'survey ft'
    },
    'survey_mile': {
        'name': _('survey mile'),
        'symbol': 'survey mile'
    },
    'svedberg': {
        'name': 'svedberg',
        'symbol': 'S'
    },
    'synodic_month': {
        'name': _('synodic month'),
        'symbol': _('synodic month')
    },
    'tablespoon': {
        'name': _('tablespoon'),
        'symbol': _('tablespoon')
    },
    'tansec': {
        'name': 'tansec',
        'symbol': 'tansec'
    },
    'teaspoon': {
        'name': _('teaspoon'),
        'symbol': _('teaspoon')
    },
    'technical_atmosphere': {
        'name': _('technical atmosphere'),
        'symbol': 'at'
    },
    'tesla': {
        'name': 'tesla',
        'symbol': 'T'
    },
    'tex': {
        'name': 'tex',
        'symbol': 'tex'
    },
    'tex_cicero': {
        'name': 'tex cicero',
        'symbol': 'tex cicero'
    },
    'tex_didot': {
        'name': 'tex didot',
        'symbol': 'tex didot'
    },
    'tex_pica': {
        'name': 'tex pica',
        'symbol': 'tex pica'
    },
    'tex_point': {
        'name': 'tex point',
        'symbol': 'tex point'
    },
    'therm': {
        'name': _('therm'),
        'symbol': 'Thm'
    },
    'thermochemical_british_thermal_unit': {
        'name': _('thermochemical Btu'),
        'symbol': 'thermochemical Btu'
    },
    'thomson_cross_section': {
        'name': _('Thomson cross section'),
        'symbol': 'Thomson cross section'
    },
    'thou': {
        'name': 'thou',
        'symbol': 'thou'
    },
    'ton': {
        'name': _('ton'),
        'symbol': 't'
    },
    'ton_TNT': {
        'name': _('ton of TNT'),
        'symbol': 'ton of TNT'
    },
    'tonne_of_oil_equivalent': {
        'name': _('ton of oil equivalent'),
        'symbol': _('toe')
    },
    'torr': {
        'name': 'torr',
        'symbol': 'torr'
    },
    'tropical_month': {
        'name': _('tropical month'),
        'symbol': _('tropical month')
    },
    'tropical_year': {
        'name': _('tropical year'),
        'symbol': _('tropical year')
    },
    'troy_ounce': {
        'name': _('troy ounce'),
        'symbol': _('troy ounce')
    },
    'troy_pound': {
        'name': _('troy pound'),
        'symbol': _('troy pound')
    },
    'turn': {
        'name': _('turn'),
        'symbol': _('turn')
    },
    'unified_atomic_mass_unit': {
        'name': _('unified atomic mass unit'),
        'symbol': _('unified atomic mass unit')
    },
    'unit_pole': {
        'name': _('unit pole'),
        'symbol': 'pole'
    },
    'vacuum_permeability': {
        'name': _('vacuum permeability'),
        'symbol': 'μ0'
    },
    'vacuum_permittivity': {
        'name': _('vacuum permittivity'),
        'symbol': 'ε0'
    },
    'volt': {
        'name': 'Volt',
        'symbol': 'V'
    },
    'volt_ampere': {
        'name': 'Volt Ampere',
        'symbol': 'VA'
    },
    'von_klitzing_constant': {
        'name': _('Von Klitzing constant'),
        'symbol': 'RK'
    },
    'water': {
        'name': _('Water volumic mass'),
        'symbol': 'g/m³'
    },
    'water_39F': {
        'name': _('Water volumic mass at 39F'),
        'symbol': 'g/m³'
    },
    'water_60F': {
        'name': _('Water volumic mass at 60F'),
        'symbol': 'g/m³'
    },
    'watt': {
        'name': 'Watt',
        'symbol': 'W'
    },
    'watt_hour': {
        'name': 'Watt',
        'symbol': 'Wh'
    },
    'weber': {
        'name': 'weber',
        'symbol': 'weber'
    },
    'week': {
        'name': 'week',
        'symbol': 'w'
    },
    'wien_frequency_displacement_law_constant': {
        'name': _('wien frequency displacement law constant'),
        'symbol': 'vpeak'
    },
    'wien_u': {
        'name': _('wien u'),
        'symbol': ''
    },
    'wien_wavelength_displacement_law_constant': {
        'name': _('wien displacement law constant'),
        'symbol': 'λpeak'
    },
    'wien_x': {
        'name': _('wien x'),
        'symbol': ''
    },
    'x_unit_Cu': {
        'name': _('Cu X-ray wavelength'),
        'symbol': ''
    },
    'x_unit_Mo': {
        'name': _('Mo X-ray wavelength'),
        'symbol': ''
    },
    'yard': {
        'name': _('yard'),
        'symbol': 'yd'
    },
    'year': {
        'name': _('year'),
        'symbol': _('year')
    },
    'zeta': {
        'name': _('zeta'),
        'symbol': ''
    },
    'decibelmilliwatt': {
        'name': _('decibelmilliwatt'),
        'symbol': 'dBmW'
    },
    'decibelmicrowatt': {
        'name': _('decibelmicrowatt'),
        'symbol': 'dBμW'
    },
    'eulers_number': {
        'name': _('Euler‘s number'),
        'symbol': 'e'
    },
    'octave': {
        'name': _('octave'),
        'symbol': ''
    },
    'sound_pressure_level': {
        'name': _('sound pressure level'),
        'symbol': ''
    },
    'meter_per_second': {
        'name': _('meter per second'),
        'symbol': 'm.s⁻¹'
    },
    'meter_per_square_second': {
        'name': _('meter per square second'),
        'symbol': 'm.s⁻²'
    },
    'square_meter': {
        'name': _('square meter'),
        'symbol': 'm²'
    },
    'cubic_meter': {
        'name': _('cubic meter'),
        'symbol': 'm³'
    },
    'milligram': {
        'name': _('milligram'),
        'symbol': 'mg'
    },
    'kilogram': {
        'name': _('kilogram'),
        'symbol': 'kg'
    },
    'kilometer': {
        'name': _('kilometer'),
        'symbol': 'km'
    },
    'centimeter': {
        'name': _('centimeter'),
        'symbol': 'cm'
    },
    'millimeter': {
        'name': _('millimeter'),
        'symbol': 'mm'
    },
    'centimeter_per_second': {
        'name': _('centimeter per second'),
        'symbol': 'cm.s⁻¹'
    },
}
