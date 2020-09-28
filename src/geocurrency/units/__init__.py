from django.utils.translation import ugettext_lazy as _, pgettext_lazy

DIMENSION_FAMILIES = {
    'dimensionless': _('dimensionless'),
    'meter': _('length'),
    'meter ** 2': _('surface'),
    'meter ** 3': _('volume'),
    'second': _('time'),
    'gram': _('mass'),
    'meter / second': _('speed'),
    'meter / second ** 2': _('acceleration'),
    'meter / gram': _('meter per gram'),
    'meter ** 2 / second ** 2': _('absorption'),
    'gram * meter / second ** 2': _('force'),
    'gram * meter ** 2 / second ** 2': _('energy'),
    'ampere': _('electric current'),
    'ampere * second': _('electric charge'),
    'ampere * second / mole': _('elementary charge'),
    'gram * meter ** 2 / ampere ** 2 / second ** 2': _('electromagnetic inductance'),
    'gram * meter ** 2 / ampere ** 2 / second ** 3': _('electromagnetic resistance'),
    'ampere ** 2 * second ** 3 / gram / meter ** 2': _('electrical conductance'),
    'gram * meter ** 2 / ampere / second ** 3': _('electric potential difference'),
    'gram * meter / ampere / second ** 3': _('electric field'),
    'gram / meter': _('linear mass density'),
    'gram / second ** 3': _('intensity'),
    'kelvin': _('temperature'),
    'mole': _('amount of substance'),
    '1 / mole': _('density of particle'),
    'mole / second': _('catalytic activity'),
    'bit': _('quantity of information'),
    'bit / pixel': _('density of information'),
    'ampere * meter ** 2': _('magnetic moment'),
    'ampere * meter * second': _('electric moment'),
    'gram * meter ** 2 / kelvin / second ** 2': _('energy'),
    'ampere * meter ** 2 * second': _('magnetic moment'),
    'candela': _('luminous intensity'),
    'ampere ** 2 * second ** 4 / gram / meter ** 2': _('electrical capacitance'),
    'gram * meter ** 3 / ampere ** 2 / second ** 4': _('electric force'),
    'count / second': _('frequency'),
    'gram * meter ** 2 / second': _('electromagnetic action'),
    'gram * meter ** 4 / second ** 3': _('power per unit per wavelength interval'),
    'gram ** 0.5 * meter ** 1.5 / second': _('electrostatic unit of charge'),
    'gram ** 0.5 / meter ** 0.5 / second': _('magnetic induction'),
    'radian': _('angle'),
    'candela / meter ** 2': _('luminance'),
    'gram / second ** 2': _('radiation'),
    'candela * radian ** 2': _('luminous flux'),
    'candela * radian ** 2 / meter ** 2': _('illuminance'),
    'gram * meter ** 2 / ampere / second ** 2': _('magnetic flux quantum'),
    'mole / meter ** 3': _('concentration'),
    'gram * meter ** 2 / kelvin / mole / second ** 2': _('energy per temperature increment per mole'),
    'neper': _('neper'),
    'meter ** 3 / gram / second ** 2': _('newtonian constant of gravitation'),
    'gram / meter / second': _('viscosity'),
    'gram / meter / second ** 2': _('pressure'),
    '1 / meter': _('reciprocal length'),
    'radian / second': _('angular speed'),
    'meter * second / gram': _('reciprocal viscosity'),
    'ampere * second / gram': _('radiation exposure'),
    'radian ** 2': _('solid degree'),
    'gram * meter ** 2 / second ** 3': _('volumetric flow rate'),
    'gram / ampere / second ** 2': _('magnetic field'),
    'gram / meter ** 3': _('mass density')
}

UNIT_EXTENDED_DEFINITION = {
    'K_alpha_Cu_d_220': {
        'name': _('Copper Kα'),
        'symbol': 'Cu Kα',
        'family': _('dimensionless')
    },
    'K_alpha_Mo_d_220': {
        'name': _('Molybdenum K-α'),
        'symbol': 'MO Kα',
        'family': _('dimensionless')
    },
    'K_alpha_W_d_220': {
        'name': _('Tungsten K-α'),
        'symbol': _('W Kα', ),
        'family': _('dimensionless')
    },
    'RKM': {
        'name': _('RKM'),
        'symbol': 'RKM',
        'obsolete': True,
        'family': _('absorption')
    },
    'UK_force_ton': {
        'name': _('long ton-force'),
        'symbol': 'long ton-force',
        'obsolete': True,
        'family': _('force')

    },
    'UK_hundredweight': {
        'name': 'long hundredweight',
        'symbol': 'long hundredweight',
        'obsolete': True,
        'family': _('mass')
    },
    'UK_ton': {
        'name': _('long ton'),
        'symbol': 'long ton',
        'obsolete': True,
        'family': _('mass')
    },
    'US_force_ton': {
        'name': _('short ton force'),
        'symbol': 'short ton-force',
        'obsolete': True,
        'family': _('force')
    },
    'US_hundredweight': {
        'name': _('short hundredweight'),
        'symbol': 'short hundredweight',
        'obsolete': True,
        'family': _('mass')
    },
    'US_ton': {
        'name': _('short ton'),
        'symbol': 'short ton',
        'obsolete': True,
        'family': _('mass')
    },
    'US_international_ampere': {
        'name': _('US International Ampere'),
        'symbol': 'US international A',
        'obsolete': True,
        'family': _('electric current')
    },
    'US_international_ohm': {
        'name': _('US international Ohm'),
        'symbol': 'US international Ω',
        'obsolete': True,
        'family': _('electric charge')
    },
    'US_international_volt': {
        'name': _('US international Volt'),
        'symbol': 'US international V',
        'obsolete': True,
        'family': _('electric potential difference')
    },
    'US_therm': {
        'name': _('US therm'),
        'symbol': 'thm',
        'family': _('heat energy')
    },
    'abampere': {
        'name': _('abampere'),
        'symbol': 'abA',
        'family': _('electric current')
    },
    'abcoulomb': {
        'name': _('abcoulomb'),
        'symbol': 'abC',
        'family': _('electromagnetic inductance')
    },
    'aberdeen': {
        'name': _('Aberdeen'),
        'symbol': 'aberdeen',
        'family': _('linear mass density')
    },
    'abfarad': {
        'name': _('abfarad'),
        'symbol': 'abF',
        'family': _('electrical capacitance')
    },
    'abhenry': {
        'name': _('abhenry'),
        'symbol': 'henry',
        'family': _('electrical inductance'),
    },
    'abohm': {
        'name': _('abohm'),
        'symbol': 'abohm',
        'family': _('electric charge')
    },
    'absiemens': {
        'name': _('absiemens'),
        'symbol': 'absiemens',
        'family': _('electrical conductance')
    },
    'abvolt': {
        'name': _('abvolt'),
        'symbol': 'abV',
        'family': _('electric potential difference')
    },
    'acre': {
        'name': _('acre'),
        'symbol': 'acre',
        'family': _('surface')
    },
    'acre_foot': {
        'name': _('acre-foot'),
        'symbol': 'acre-foot',
        'family': _('volume')
    },
    'ampere': {
        'name': _('ampere'),
        'symbol': 'A',
        'family': _('electric current'),
    },
    'ampere_turn': {
        'name': _('ampere-turn'),
        'symbol': 'At',
        'family': _('electric current'),
    },
    'angstrom': {
        'name': _('angstrom'),
        'symbol': 'Å',
        'family': _('length')
    },
    'angstrom_star': {
        'name': _('angstrom star'),
        'symbol': 'Å*',
        'family': _('length')
    },
    'apothecary_dram': {
        'name': _('apothecary dram'),
        'symbol': 'dr',
        'family': _('mass')
    },
    'apothecary_ounce': {
        'name': _('apothecary ounce'),
        'symbol': 'oz',
        'family': _('mass')
    },
    'apothecary_pound': {
        'name': _('apothecary pound'),
        'symbol': 'apothecary pound',
        'family': _('mass')
    }, 'arcminute': {
        'name': _('minute of arc'),
        'symbol': 'arcmin',
        'family': _('dimensionless')
    }, 'arcsecond': {
        'name': _('second of arc'),
        'symbol': 'arcsec',
        'family': _('dimensionless')
    }, 'are': {
        'name': _('are'),
        'symbol': 'are',
        'family': _('surface')
    }, 'astronomical_unit': {
        'name': _('astronomical unit'),
        'symbol': 'AU',
        'family': _('length')
    }, 'atmosphere_liter': {
        'name': _('atmosphere liter'),
        'symbol': 'atmosphere liter',
        'family': _('volume')
    }, 'atomic_mass_constant': {
        'name': _('atomic mass constant'),
        'symbol': 'Da',
        'family': _('constant')
    },
    'atomic_unit_of_current': {
        'name': _('atomic unit of current'),
        'symbol': '',
        'family': _('ampere')
    },
    'atomic_unit_of_electric_field': {
        'name': _('atomic unit of electric field'),
        'symbol': '',
        'family': _('electric field')
    }, 'atomic_unit_of_force': {
        'name': _('atomic unit of force'),
        'symbol': 'atomic unit of force',
        'family': _('force')
    }, 'atomic_unit_of_intensity': {
        'name': _('atomic unit of intensity'),
        'symbol': 'atomic unit of intensity',
        'family': _('intensity')
    }, 'atomic_unit_of_temperature': {
        'name': _('atomic unit of temperature'),
        'symbol': 'atomic unit of temperature',
        'family': _('temperature')
    }, 'atomic_unit_of_time': {
        'name': _('atomic unit of time'),
        'symbol': 'atomic unit of time',
        'family': _('time')
    }, 'avogadro_constant': {
        'name': _('Avogadro constant'),
        'symbol': 'L',
        'family': _('constant')
    }, 'avogadro_number': {
        'name': _('Avogadro number'),
        'symbol': '',
        'family': _('dimensionless'),
    }, 'bag': {
        'name': _('bag'),
        'symbol': 'bag',
        'family': _('quantity')
    }, 'bar': {
        'name': _('bar'),
        'symbol': 'bar',
        'family': _('pressure')
    }, 'barn': {
        'name': _('barn'),
        'symbol': 'b',
        'family': _('surface')
    }, 'barrel': {
        'name': _('barrel'),
        'symbol': 'barrel',
        'family': 'volume'
    }, 'barye': {
        'name': _('barrye'),
        'symbol': 'Ba',
        'family': _('pressure')
    },
    'baud': {
        'name': _('baud'),
        'symbol': 'Bd',
        'family': _('speed')
    },
    'becquerel': {
        'name': _('becquerel'),
        'symbol': 'Bq',
        'family': _('radioactivity')
    },
    'beer_barrel': {
        'name': _('beer barrel'),
        'symbol': 'beer barrel',
        'family': _('volume')
    },
    'bel': {
        'name': _('bel'),
        'symbol': 'B',
        'family': _('field quantity')
    },
    'biot': {
        'name': _('biot'),
        'symbol': 'biot',
        'family': _('dimensionless')
    },
    'biot_turn': {
        'name': _('biot turn'),
        'symbol': 'biot-turn',
        'family': _('dimensionless')
    },
    'bit': {
        'name': _('bit'),
        'symbol': 'bit',
        'family': _('quantity of information')
    },
    'bits_per_pixel': {
        'name': _('bits per pixel'),
        'symbol': 'bpp',
        'family': _('density of information')
    },
    'board_foot': {
        'name': _('board foot'),
        'symbol': 'board-foot',
        'family': _('volume')
    },
    'bohr': {
        'name': _('bohr'),
        'symbol': 'bohr',
        'family': _('length')
    },
    'bohr_magneton': {
        'name': _('bohr magneton'),
        'symbol': 'μB',
        'family': _('magnetic moment')
    },
    'boiler_horsepower': {
        'name': _('boiler horsepower'),
        'symbol': 'boiler hp',
        'family': _('power')
    },
    'boltzmann_constant': {
        'name': _('boltzmann constant'),
        'symbol': 'kB',
        'family': _('constant')
    },
    'british_thermal_unit': {
        'name': _('british thermal unit'),
        'symbol': 'Btu',
        'family': _('energy')
    },
    'buckingham': {
        'name': _('buckingham'),
        'symbol': 'B',
        'family': _('magnetic moment')
    },
    'bushel': {
        'name': _('bushel'),
        'symbol': 'bsh',
        'family': _('volume')
    },
    'byte': {
        'name': _('byte'),
        'symbol': 'byte',
        'family': _('quantity of information')
    },
    'cables_length': {
        'name': _('cable length'),
        'symbol': 'cable',
        'family': _('length')
    },
    'calorie': {
        'name': _('calorie'),
        'symbol': 'calorie',
        'family': _('energy')
    },
    'candela': {
        'name': _('candela'),
        'symbol': 'cd',
        'family': _('luminous intensity')
    },
    'carat': {
        'name': _('carat'),
        'symbol': 'ct',
        'family': _('mass')
    },
    'centimeter_H2O': {
        'name': _('centimeter H20'),
        'symbol': 'cm H2O',
        'family': _('pressure')
    },
    'centimeter_Hg': {
        'name': _('centimeter Hg'),
        'symbol': 'cm Hg',
        'family': _('pressure')
    },
    'century': {
        'name': _('century'),
        'symbol': 'c.',
        'family': _('time')
    },
    'chain': {
        'name': _('chain'),
        'symbol': 'chain',
        'family': _('length')
    },
    'cicero': {
        'name': _('cicero'),
        'symbol': 'cicero',
        'family': _('length')
    },
    'circular_mil': {
        'name': _('circular mil'),
        'symbol': 'mils',
        'family': _('surface')
    },
    'classical_electron_radius': {
        'name': _('classical electron radius'),
        'symbol': 're',
        'family': _('length')
    },
    'clausius': {
        'name': _('clausius'),
        'symbol': 'clausius',
        'family': _('energy')
    },
    'common_year': {
        'name': _('common year'),
        'symbol': '',
        'family': _('time')
    },
    'conductance_quantum': {
        'name': _('conductance quantum'),
        'symbol': 'G0',
        'family': _('electrical conductance')
    },
    'conventional_ampere_90': {
        'name': _('conventional ampere'),
        'symbol': 'A90',
        'family': _('electric current')
    },
    'conventional_coulomb_90': {
        'name': _('conventional coulomb'),
        'symbol': 'C90',
        'family': _('electromagnetic inductance')
    },
    'conventional_farad_90': {
        'name': _('conventional farad'),
        'symbol': 'F90',
        'family': _('eletrical capacitance')
    },
    'conventional_henry_90': {
        'name': _('conventional henry'),
        'symbol': 'H90',
        'family': _('electrical inductance'),
    },
    'conventional_josephson_constant': {
        'name': _('conventional josephson constant'),
        'symbol': 'KJ',
        'family': _('constant'),
    },
    'conventional_ohm_90': {
        'name': _('conventional ohm'),
        'symbol': 'Ω90',
        'family': _('electric charge')
    },
    'conventional_volt_90': {
        'name': _('conventional volt'),
        'symbol': 'V90',
        'family': _('electric potential difference')
    },
    'conventional_von_klitzing_constant': {
        'name': _('conventional Von Klitzing constant'),
        'symbol': 'RK',
        'family': _('constant'),
    },
    'conventional_watt_90': {
        'name': _('conventional Watt'),
        'symbol': 'W90',
        'family': _('power'),
    },
    'coulomb': {
        'name': _('coulomb'),
        'symbol': 'C',
        'family': _('electromagnetic inductance')
    }, 'coulomb_constant': {
        'name': _('coulomb constant'),
        'symbol': 'K',
        'family': _('constant')
    },
    'count': {
        'name': _('count'),
        'symbol': '',
        'family': _('dimensionless')
    },
    'counts_per_second': {
        'name': _('counts per second'),
        'symbol': 'counts/s',
        'family': _('frequency')
    },
    'css_pixel': {
        'name': _('CSS pixel'),
        'symbol': 'px',
        'family': _('length')
    },
    'cubic_centimeter': {
        'name': _('cubic centimeter'),
        'symbol': 'cm³',
        'family': _('volume')
    },
    'cubic_foot': {
        'name': _('cubic foot'),
        'symbol': 'cubic foot',
        'family': _('volume')
    },
    'cubic_inch': {
        'name': _('cubic inch'),
        'symbol': 'cubic inch',
        'family': _('volume')
    }, 'cubic_yard': {
        'name': _('cubic yard'),
        'symbol': 'cubic yard',
        'family': _('volume')
    }, 'cup': {
        'name': _('cup'),
        'symbol': 'cup',
        'family': _('volume')
    }, 'curie': {
        'name': _('curie'),
        'symbol': 'Ci',
        'family': _('frequency')
    }, 'dalton': {
        'name': _('dalton'),
        'symbol': 'Da',
        'family': _('mass')
    }, 'darcy': {
        'name': _('darcy'),
        'symbol': 'D',
        'family': _('permeability')
    }, 'day': {
        'name': _('day'),
        'symbol': pgettext_lazy('unit', 'day'),
        'family': _('time')
    }, 'debye': {
        'name': _('debye'),
        'symbol': 'D',
        'family': _('electric moment')
    }, 'decade': {
        'name': _('decade'),
        'symbol': pgettext_lazy('symbol', 'decade'),
        'family': _('time')
    }, 'decibel': {
        'name': _('decibel'),
        'symbol': 'dB',
        'family': _('field quantity')
    },'degree': {
        'name': _('degree'),
        'symbol': '°',
        'family': _('dimensionless')
    }, 'degree_Celsius': {
        'name': _('degree Celsius'),
        'symbol': '°C',
        'family': _('temperature')
    }, 'degree_Fahrenheit': {
        'name': _('degree Fahrenheit'),
        'symbol': '°F',
        'family': _('temperature')
    }, 'degree_Rankine': {
        'name': _('degree Rankine'),
        'symbol': '°R',
        'family': _('temperature')
    }, 'degree_Reaumur': {
        'name': _('degree Reaumur'),
        'symbol': '°Re',
        'family': _('temperature')
    }, 'denier': {
        'name': _('denier'),
        'symbol': 'D',
        'family': _('linear mass density')
    }, 'didot': {
        'name': _('didot'),
        'symbol': 'didot',
        'family': _('length')
    }, 'dirac_constant': {
        'name': _('Dirac constant'),
        'symbol': 'ħ',
        'family': _('constant')
    }, 'dram': {
        'name': _('dram'),
        'symbol': 'dr',
        'family': _('mass')
    }, 'dry_barrel': {
        'name': _('dry barrel'),
        'symbol': 'dry barrel',
        'family': _('volume')
    }, 'dry_gallon': {
        'name': _('dry gallon'),
        'symbol': 'dry gallon',
        'family': _('volume')
    }, 'dry_pint': {
        'name': _('dry pint'),
        'symbol': 'dry pint',
        'family': _('volume')
    }, 'dry_quart': {
        'name': _('dry quart'),
        'symbol': 'dry quart',
        'family': _('volume')
    }, 'dtex': {
        'name': _('decitex'),
        'symbol': 'dtex',
        'family': _('linear mass density')
    }, 'dyne': {
        'name': _('dyne'),
        'symbol': 'dyn',
        'family': _('force')
    }, 'electrical_horsepower': {
        'name': _('eletcrical horsepower'),
        'symbol': 'HP',
        'family': _('power')
    }, 'electron_g_factor': {
        'name': _('electron G-factor'),
        'symbol': 'electron G-factor',
        'family': _('dimensionless')
    }, 'electron_mass': {
        'name': _('electron mass'),
        'symbol': 'me',
        'family': _('mass')
    }, 'electron_volt': {
        'name': _('electronvolt'),
        'symbol': 'eV',
        'family': _('electric potential difference')
    }, 'elementary_charge': {
        'name': _('elementary charge'),
        'symbol': 'e',
        'family': _('electromagnetic inductance')
    }, 'entropy_unit': {
        'name': _('entropy unit'),
        'symbol': 'S',
        'family': _('energy by temperature')
    }, 'enzyme_unit': {
        'name': _('enzyme unit'),
        'symbol': 'U',
        'family': _('catalytic activity')
    }, 'eon': {
        'name': _('eon'),
        'symbol': 'eon',
        'family': _('time')
    }, 'erg': {
        'name': _('erg'),
        'symbol': 'erg',
        'family': _('energy')
    }, 'farad': {
        'name': _('farad'),
        'symbol': 'F',
        'family': _('electrical capacitance')
    }, 'faraday': {
        'name': _('faraday'),
        'symbol': 'faraday',
        'family': _('electric charge'),
    }, 'faraday_constant': {
        'name': _('faraday constant'),
        'symbol': 'F',
        'family': _('constant'),
    }, 'fathom': {
        'name': _('fathom'),
        'symbol': 'fathom',
        'family': _('length'),
    }, 'fermi': {
        'name': _('fermi'),
        'symbol': 'fm',
        'family': _('length'),
    }, 'fifteen_degree_calorie': {
        'name': _('fifteen degree calorie'),
        'symbol': 'fifteen degree calorie',
        'family': _('energy'),
    }, 'fifth': {
        'name': _('fifth'),
        'symbol': 'fifth',
        'family': _('volume'),
    }, 'fine_structure_constant': {
        'name': _('fine structure constant'),
        'symbol': 'α',
        'family': _('constant'),
    }, 'first_radiation_constant': {
        'name': _('first radiation constant'),
        'symbol': 'c1',
        'family': _('constant'),
    }, 'fluid_dram': {
        'name': _('fluid dram'),
        'symbol': 'fluid dr',
        'family': _('mass')
    }, 'fluid_ounce': {
        'name': _('fluid ounce'),
        'symbol': 'fluid ounce',
        'family': _('mass')
    }, 'foot': {
        'name': _('foot'),
        'symbol': 'foot',
        'family': _('length')
    }, 'foot_H2O': {
        'name': _('foot H2O'),
        'symbol': 'foot H2O',
        'family': _('pressure')
    }, 'foot_per_second': {
        'name': _('foot per second'),
        'symbol': 'foot per second',
        'family': _('speed')
    }, 'foot_pound': {
        'name': _('foot pound'),
        'symbol': 'foot pound',
        'family': _('energy')
    }, 'force_gram': {
        'name': _('gram-force'),
        'symbol': 'gram-force',
        'obsolete': True,
        'family': _('force')
    }, 'force_kilogram': {
        'name': _('kilogram-force'),
        'symbol': 'kg-force',
        'obsolete': True,
        'family': _('force')
    }, 'force_long_ton': {
        'name': _('long ton-force'),
        'symbol': 'long ton-force',
        'obsolete': True,
        'family': _('force')
    }, 'force_metric_ton': {
        'name': _('tonne-force'),
        'symbol': 'tf',
        'obsolete': True,
        'family': _('force')
    }, 'force_ounce': {
        'name': _('ounce-force'),
        'symbol': 'ounce force',
        'obsolete': True,
        'family': _('force')
    }, 'force_pound': {
        'name': _('pound-force'),
        'symbol': 'pound force',
        'obsolete': True,
        'family': _('force')
    }, 'force_ton': {
        'name': _('tonne-force'),
        'symbol': 'tf',
        'obsolete': True,
        'family': _('force')
    }, 'fortnight': {
        'name': _('fortnight'),
        'symbol': 'fortnight',
        'family': _('time')
    }, 'franklin': {
        'name': _('franklin'),
        'symbol': 'Fr',
        'family': _('electrostatic unit of charge')
    }, 'furlong': {
        'name': _('furlong'),
        'symbol': 'furlong',
        'family': _('length')
    }, 'galileo': {
        'name': _('galileo'),
        'symbol': 'Gal',
        'family': _('acceleration')
    }, 'gallon': {
        'name': _('gallon'),
        'symbol': 'gal',
        'family': _('volume')
    }, 'gamma': {
        'name': _('gamma'),
        'symbol': 'γ',
        'family': _('constant')
    }, 'gamma_mass': {
        'name': _('gamma'),
        'symbol': 'γ',
        'family': _('mass')
    }, 'gauss': {
        'name': _('gauss'),
        'symbol': 'G',
        'family': _('magnetic induction')
    }, 'gilbert': {
        'name': _('gilbert'),
        'symbol': 'Gb',
        'family': _('electric current'),
    }, 'gill': {
        'name': _('gill'),
        'symbol': 'gill',
        'family': _('volume'),
    }, 'grade': {
        'name': _('grade'),
        'symbol': 'gr',
        'family': _('angle'),
    }, 'grain': {
        'name': _('grain'),
        'symbol': 'grain',
        'family': _('mass'),
    }, 'gram': {
        'name': _('gram'),
        'symbol': 'g',
        'family': _('mass'),
    }, 'gray': {
        'name': _('gray'),
        'symbol': 'Gy',
        'family': _('absorption'),
    }, 'gregorian_year': {
        'name': _('gregorian year'),
        'symbol': pgettext_lazy('unit', 'gregorian year'),
        'family': _('time')
    }, 'hand': {
        'name': _('hand'),
        'symbol': 'hand',
        'family': _('length'),
    }, 'hartree': {
        'name': _('hartree'),
        'symbol': 'Eh',
        'family': _('energy'),
    }, 'hectare': {
        'name': _('hectare'),
        'symbol': 'ha',
        'family': _('surface'),
    }, 'henry': {
        'name': _('henry'),
        'symbol': 'henry',
        'family': _('electrical inductance'),
    }, 'hertz': {
        'name': _('hertz'),
        'symbol': 'Hz',
        'family': _('frequency'),
    }, 'hogshead': {
        'name': _('hogshead'),
        'symbol': 'hhd',
        'family': _('volume'),
    }, 'horsepower': {
        'name': _('horsepower'),
        'symbol': 'HP',
        'family': _('power'),
    }, 'hour': {
        'name': _('hour'),
        'symbol': 'h',
        'family': _('time'),
    }, 'hundredweight': {
        'name': _('hundredweight'),
        'symbol': 'cwt',
        'family': _('mass'),
    }, 'impedance_of_free_space': {
        'name': _('impedance of free space'),
        'symbol': 'Z0',
        'family': _('electromagnetic resistance'),
    }, 'imperial_barrel': {
        'name': _('imperial barrel'),
        'symbol': 'imperial barrel',
        'family': _('volume'),
    }, 'imperial_bushel': {
        'name': _('imperial bushel'),
        'symbol': 'bsh',
        'family': _('volume'),
    }, 'imperial_cup': {
        'name': _('imperial cup'),
        'symbol': 'imperial cup',
        'family': _('volume'),
    }, 'imperial_fluid_drachm': {
        'name': _('imperial fluid drachm'),
        'symbol': 'ʒ',
        'family': _('mass'),
    }, 'imperial_fluid_ounce': {
        'name': _('imperial fluid ounce'),
        'symbol': 'fl oz',
        'family': _('volume'),
    }, 'imperial_fluid_scruple': {
        'name': _('imperial fluid scruple'),
        'symbol': '℈',
        'family': _('volume'),
    }, 'imperial_gallon': {
        'name': _('imperial gallon'),
        'symbol': 'imperial gallon',
        'family': _('volume'),
    }, 'imperial_gill': {
        'name': _('imperial gill'),
        'symbol': 'imperial gill',
        'family': _('volume'),
    }, 'imperial_minim': {
        'name': _('imperial minim'),
        'symbol': 'min',
        'family': _('volume'),
    }, 'imperial_peck': {
        'name': _('imperial peck'),
        'symbol': 'peck',
        'family': _('volume')
    }, 'imperial_pint': {
        'name': _('imperial pint'),
        'symbol': 'imperial pint',
        'family': _('volume')
    }, 'imperial_quart': {
        'name': _('imperial quart'),
        'symbol': 'imperial quart',
        'family': _('volume')
    }, 'inch': {
        'name': _('inch'),
        'symbol': 'inch',
        'family': _('length')
    }, 'inch_H2O_39F': {
        'name': _('inch H20 39F'),
        'symbol': 'inch H20 39F',
        'family': _('pressure')
    }, 'inch_H2O_60F': {
        'name': _('inch H20 60F'),
        'symbol': 'inch H20 60F',
        'family': _('pressure')
    }, 'inch_Hg': {
        'name': _('inch Hg'),
        'symbol': 'inch Hg',
        'family': _('pressure')
    }, 'inch_Hg_60F': {
        'name': _('inch Hg 60F'),
        'symbol': 'inch Hg 60F',
        'family': _('pressure')
    }, 'international_british_thermal_unit': {
        'name': _('international Btu'),
        'symbol': 'international Btu',
        'family': _('energy')
    }, 'international_calorie': {
        'name': _('international calorie'),
        'symbol': 'international calorie',
        'family': _('energy')
    }, 'josephson_constant': {
        'name': _('Josephson constant'),
        'symbol': 'KJ',
        'family': _('constant'),
    }, 'joule': {
        'name': _('Joule'),
        'symbol': 'J',
        'family': _('energy'),
    }, 'jute': {
        'name': _('jute'),
        'symbol': 'jute',
        'family': _('volume'),
    }, 'katal': {
        'name': _('katal'),
        'symbol': 'kat',
        'family': _('catalytic activity'),
    }, 'kelvin': {
        'name': _('kelvin'),
        'symbol': 'K',
        'family': _('temperature'),
    }, 'kilometer_per_hour': {
        'name': _('kilometer per hour'),
        'symbol': 'km/hour',
        'family': _('speed'),
    }, 'kilometer_per_second': {
        'name': _('kilometer per second'),
        'symbol': 'km/second',
        'family': _('speed'),
    }, 'kip': {
        'name': _('kip'),
        'symbol': 'kip',
        'family': _('force'),
    }, 'kip_per_square_inch': {
        'name': _('kip per square inch'),
        'symbol': 'kip / sq inch',
        'family': _('pressure')
    }, 'knot': {
        'name': _('knot'),
        'symbol': 'kt',
        'family': _('speed')
    }, 'lambda': {
        'name': _('lambda'),
        'symbol': 'λ',
        'family': _('volume')
    }, 'lambert': {
        'name': _('lambert'),
        'symbol': 'L',
        'family': _('luminance')
    }, 'langley': {
        'name': _('langley'),
        'symbol': 'Ly',
        'family': _('radiation')
    }, 'lattice_spacing_of_Si': {
        'name': _('lattice constant'),
        'symbol': 'Ly',
        'family': _('constant')
    }, 'league': {
        'name': _('league'),
        'symbol': 'league',
        'obsolete': True,
        'family': _('length')
    }, 'leap_year': {
        'name': _('leap year'),
        'symbol': _('year'),
        'family': _('time')
    }, 'light_year': {
        'name': _('light year'),
        'symbol': _('ly'),
        'family': _('length')
    }, 'link': {
        'name': _('link'),
        'symbol': _('li'),
        'family': _('length')
    }, 'liter': {
        'name': _('liter'),
        'symbol': _('L'),
        'family': _('volume')
    }, 'ln10': {
        'name': _('log 10'),
        'symbol': _('ln10'),
        'family': _('dimesionless')
    }, 'long_hundredweight': {
        'name': _('long hundredweight'),
        'symbol': 'long hundredweight',
        'obsolete': True,
        'family': _('mass')
    }, 'long_ton': {
        'name': _('long ton'),
        'symbol': 'long ton',
        'obsolete': True,
        'family': _('length')
    }, 'lumen': {
        'name': _('lumen'),
        'symbol': 'lm',
        'family': _('luminous flux')
    }, 'lux': {
        'name': _('lux'),
        'symbol': 'lx',
        'family': _('illuminance')
    }, 'magnetic_flux_quantum': {
        'name': _('magnetic flux quantum'),
        'symbol': 'Φ',
        'family': _('magnetic flux quantum')
    }, 'maxwell': {
        'name': _('maxwell'),
        'symbol': 'Mx',
        'family': _('electrostatic unit of charge')
    }, 'mean_international_ampere': {
        'name': _('mean international ampere'),
        'symbol': 'mean international A',
        'family': _('electric current')
    }, 'mean_international_ohm': {
        'name': _('mean international Ohm'),
        'symbol': 'mean international Ω',
        'family': _('electric charge')
    }, 'mean_international_volt': {
        'name': _('mean international Volt'),
        'symbol': 'mean international V',
        'family': _('electric potential difference')
    }, 'mercury': {
        'name': _('density of mercury'),
        'symbol': '',
        'family': _('constant')
    }, 'mercury_60F': {
        'name': _('density of mercury 60F'),
        'symbol': '',
        'family': _('constant')
    }, 'meter': {
        'name': _('meter'),
        'symbol': 'm',
        'family': _('length')
    }, 'meter_per_second': {
        'name': _('meter per second'),
        'symbol': 'm/s',
        'family': _('speed')
    }, 'metric_horsepower': {
        'name': _('metric horsepower'),
        'symbol': 'hp',
        'family': _('power')
    }, 'metric_ton': {
        'name': _('metric ton'),
        'symbol': 't',
        'family': _('mass')
    }, 'micron': {
        'name': _('micron'),
        'symbol': 'μm',
        'family': _('length')
    }, 'mil': {
        'name': _('mil'),
        'symbol': 'ml',
        'family': _('volume')
    }, 'mile': {
        'name': _('mile'),
        'symbol': 'mile',
        'family': _('length')
    }, 'mile_per_hour': {
        'name': _('mile per hour'),
        'symbol': 'mph',
        'family': _('speed')
    }, 'millennium': {
        'name': _('millenium'),
        'symbol': _('millenium'),
        'family': _('time')
    }, 'milliarcsecond': {
        'name': _('milliarcsecond'),
        'symbol': 'mas',
        'family': _('angle')
    }, 'millimeter_Hg': {
        'name': _('Hg millimeter'),
        'symbol': 'mmHg',
        'family': _('pressure')
    }, 'minim': {
        'name': _('minim'),
        'symbol': 'min',
        'family': _('volume')
    }, 'minute': {
        'name': _('minute'),
        'symbol': 'min',
        'family': _('time')
    }, 'molar': {
        'name': _('molar'),
        'symbol': 'M',
        'family': _('concentration')
    }, 'molar_gas_constant': {
        'name': _('molar gas constant'),
        'symbol': 'R',
        'family': _('constant')
    }, 'mole': {
        'name': _('mole'),
        'symbol': 'mol',
        'family': _('amount of substance'),
    }, 'month': {
        'name': _('month'),
        'symbol': 'm',
        'family': _('time')
    }, 'nautical_mile': {
        'name': _('nautical mile'),
        'symbol': _('nm'),
        'family': _('length')
    }, 'neper': {
        'name': _('neper'),
        'symbol': _('Np'),
        'family': _('neper')
    }, 'neutron_mass': {
        'name': _('neutron mass'),
        'symbol': 'mN',
        'family': _('constant')
    }, 'newton': {
        'name': _('newton'),
        'symbol': 'N',
        'family': _('force')
    }, 'newtonian_constant_of_gravitation': {
        'name': _('newtonian constant of gravitation'),
        'symbol': 'N',
        'family': _('constant')
    }, 'nit': {
        'name': _('nit'),
        'symbol': 'cd/m²',
        'family': _('luminance')
    }, 'nuclear_magneton': {
        'name': _('nuclear magneton'),
        'symbol': 'μN',
        'family': _('magnetic moment')
    }, 'number_english': {
        'name': _('number english'),
        'symbol': 'm/g',
        'family': _('meter per gram')
    }, 'number_meter': {
        'name': _('number meter'),
        'symbol': 'm/g',
        'family': _('meter per gram')
    }, 'oersted': {
        'name': _('oersted'),
        'symbol': 'Oe',
        'family': _('H-field')
    }, 'ohm': {
        'name': _('ohm'),
        'symbol': 'Ω',
        'family': _('electric charge')
    }, 'oil_barrel': {
        'name': _('oil barrel'),
        'symbol': 'oil barrel',
        'family': 'volume'
    }, 'ounce': {
        'name': _('ounce'),
        'symbol': 'oz t',
        'family': _('mass')
    }, 'parsec': {
        'name': _('parsec'),
        'symbol': 'pc',
        'family': _('length')
    }, 'particle': {
        'name': _('particle'),
        'symbol': 'particle',
        'family': _('amount of substance')
    }, 'pascal': {
        'name': _('pascal'),
        'symbol': 'Pa',
        'family': _('pressure')
    }, 'peak_sun_hour': {
        'name': _('peak sun hour'),
        'symbol': 'peak sun hour',
        'family': _('time')
    }, 'peck': {
        'name': _('peck'),
        'symbol': 'peck',
        'family': _('volume')
    }, 'pennyweight': {
        'name': _('pennyweight'),
        'symbol': 'dwt',
        'family': _('mass')
    }, 'pi': {
        'name': 'pi',
        'symbol': 'π',
        'family': _('constant')
    }, 'pica': {
        'name': _('pica'),
        'symbol': 'pica',
        'family': _('length')
    }, 'pint': {
        'name': _('pint'),
        'symbol': 'pt',
        'family': _('volume')
    }, 'pixel': {
        'name': _('pixel'),
        'symbol': 'px',
        'family': _('unit')
    }, 'pixels_per_centimeter': {
        'name': _('pixel per centimeter'),
        'symbol': 'ppcm',
        'family': _('density of information')
    }, 'pixels_per_inch': {
        'name': _('pixel per inch'),
        'symbol': 'ppi',
        'family': _('density of information')
    }, 'planck_constant': {
        'name': _('Planck constant'),
        'symbol': 'h',
        'family': _('constant')
    }, 'planck_current': {
        'name': _('Planck current'),
        'symbol': _('qP'),
        'family': _('electric current')
    }, 'planck_length': {
        'name': _('Planck current'),
        'symbol': _('lP'),
        'family': _('length')
    }, 'planck_mass': {
        'name': _('Planck mass'),
        'symbol': _('mP'),
        'family': _('mass')
    }, 'planck_temperature': {
        'name': _('Planck temperature'),
        'symbol': _('TP'),
        'family': _('temperature')
    }, 'planck_time': {
        'name': _('Planck time'),
        'symbol': _('tP'),
        'family': _('time')
    }, 'point': {
        'name': _('point'),
        'symbol': 'pt',
        'family': _('length')
    }, 'poise': {
        'name': _('poise'),
        'symbol': 'P',
        'family': _('viscosity')
    }, 'pound': {
        'name': _('pound'),
        'symbol': 'lb',
        'family': _('mass')
    }, 'pound_force_per_square_inch': {
        'name': _('pound force per square inch'),
        'symbol': 'lb-force/inch²',
        'family': _('pressure')
    }, 'poundal': {
        'name': _('poundal'),
        'symbol': 'pdl',
        'family': _('force')
    }, 'proton_mass': {
        'name': _('proton mass'),
        'symbol': 'mP',
        'family': _('constant')
    }, 'quadrillion_Btu': {
        'name': _('quadrillion Btu'),
        'symbol': 'quadrillion Btu',
        'family': _('energy')
    }, 'quart': {
        'name': _('quart'),
        'symbol': 'qt',
        'family': _('volume')
    }, 'quarter': {
        'name': _('quarter'),
        'symbol': 'qr',
        'family': _('length')
    }, 'radian': {
        'name': _('radian'),
        'symbol': 'rad',
        'family': _('angle')
    }, 'rads': {
        'name': _('rads'),
        'symbol': 'rads',
        'family': _('absorption')
    }, 'reciprocal_centimeter': {
        'name': _('reciprocal centimeter'),
        'symbol': 'cm⁻¹',
        'family': _('reciprocal length')
    }, 'refrigeration_ton': {
        'name': _('refrigeration ton'),
        'symbol': 'TR',
        'family': _('power')
    }, 'rem': {
        'name': _('roentgen equivalent man'),
        'symbol': 'rem',
        'family': _('absorption')
    }, 'revolutions_per_minute': {
        'name': _('revolutions per minute'),
        'symbol': _('rpm'),
        'family': _('angular speed')
    }, 'revolutions_per_second': {
        'name': _('revolutions per second'),
        'symbol': _('rps'),
        'family': _('angular speed')
    }, 'reyn': {
        'name': _('reyn'),
        'symbol': _('reyn'),
        'family': _('viscosity')
    }, 'rhe': {
        'name': _('reciprocal poise'),
        'symbol': 'P⁻¹',
        'family': _('reciprocal viscosity')
    }, 'rod': {
        'name': _('rod'),
        'symbol': 'rod',
        'family': _('length')
    }, 'roentgen': {
        'name': _('roentgen'),
        'symbol': 'R',
        'family': _('radiation exposure')
    }, 'rutherford': {
        'name': _('rutherford'),
        'symbol': 'Rd',
        'family': _('frequency')
    }, 'rydberg': {
        'name': _('rydberg'),
        'symbol': 'Ry',
        'family': _('energy')
    }, 'rydberg_constant': {
        'name': _('rydberg constant'),
        'symbol': 'R∞',
        'family': _('constant')
    }, 'scaled_point': {
        'name': _('scaled point'),
        'symbol': 'Pt',
        'family': _('length')
    }, 'scruple': {
        'name': _('scruple'),
        'symbol': '℈',
        'family': _('volume'),
    }, 'second': {
        'name': _('second'),
        'symbol': 's',
        'family': _('time'),
    }, 'second_radiation_constant': {
        'name': _('second radiation constant'),
        'symbol': 'c2',
        'family': _('constant'),
    }, 'shake': {
        'name': _('shake'),
        'symbol': 'shake',
        'family': _('time'),
    }, 'shot': {
        'name': _('shot'),
        'symbol': 'shot',
        'family': _('length'),
    }, 'sidereal_day': {
        'name': _('sidereal day'),
        'symbol': pgettext_lazy('unit', 'sidereal day'),
        'family': _('time')
    }, 'sidereal_month': {
        'name': _('sidereal month'),
        'symbol': pgettext_lazy('unit', 'sidereal month'),
        'family': _('time')
    }, 'sidereal_year': {
        'name': _('sidereal year'),
        'symbol': pgettext_lazy('unit', 'sidereal year'),
        'family': _('time')
    }, 'siemens': {
        'name': _('siemens'),
        'symbol': 'S',
        'family': _('electrical conductance')
    }, 'sievert': {
        'name': _('sievert'),
        'symbol': 'Sv',
        'family': _('absorption')
    }, 'slinch': {
        'name': _('slinch'),
        'symbol': 'slinch',
        'family': _('mass')
    }, 'slug': {
        'name': _('slug'),
        'symbol': 'slug',
        'family': _('mass')
    }, 'speed_of_light': {
        'name': _('speed of light'),
        'symbol': 'c',
        'family': _('speed')
    }, 'square_degree': {
        'name': _('square degree'),
        'symbol': '(°)²',
        'family': _('solid angle')
    }, 'square_foot': {
        'name': _('square foot'),
        'symbol': 'sq ft',
        'family': _('surface')
    }, 'square_inch': {
        'name': _('square inch'),
        'symbol': 'sq in',
        'family': _('surface')
    }, 'square_league': {
        'name': _('square league'),
        'symbol': 'sq league',
        'family': _('surface')
    }, 'square_mile': {
        'name': _('square mile'),
        'symbol': 'sq mile',
        'family': _('surface')
    }, 'square_rod': {
        'name': _('square rod'),
        'symbol': 'sq rod',
        'family': _('surface')
    }, 'square_survey_mile': {
        'name': _('square survey mile'),
        'symbol': 'sq survey mile',
        'family': _('surface')
    }, 'square_yard': {
        'name': _('square yard'),
        'symbol': 'sq yd',
        'family': _('surface')
    }, 'standard_atmosphere': {
        'name': _('standard atmosphere'),
        'symbol': 'atm',
        'family': _('pressure')
    }, 'standard_gravity': {
        'name': _('standard gravity'),
        'symbol': 'g0',
        'family': _('constant')
    }, 'standard_liter_per_minute': {
        'name': _('standard liter per minute'),
        'symbol': 'SLM',
        'family': _('volumetric flow rate')
    }, 'statampere': {
        'name': 'statampere',
        'symbol': 'statA',
        'family': _('electric current')
    }, 'statfarad': {
        'name': 'statfarad',
        'symbol': 'statF',
        'family': _('electrical capacitance')
    }, 'stathenry': {
        'name': 'stathenry',
        'symbol': 'stathenry',
        'family': _('electrical inductance'),
    }, 'statmho': {
        'name': 'statmho',
        'symbol': 'statmho',
        'family': _('electrical conductance')
    }, 'statohm': {
        'name': 'statohm',
        'symbol': 'statohm',
        'family': _('electrical resistance')
    }, 'stattesla': {
        'name': 'stattesla',
        'symbol': 'stattesla',
        'family': _('magnetic field')
    }, 'statvolt': {
        'name': 'statvolt',
        'symbol': 'statvolt',
        'family': _('electric potential difference')
    }, 'statweber': {
        'name': 'statweber',
        'symbol': 'statweber',
        'family': _('flux density')
    }, 'stefan_boltzmann_constant': {
        'name': _('Stefan-Boltzmann constant'),
        'symbol': 'σ',
        'family': _('constant')
    }, 'steradian': {
        'name': _('steradian'),
        'symbol': 'sr',
        'family': _('solid angle')
    }, 'stere': {
        'name': _('stere'),
        'symbol': 'st',
        'family': _('volume')
    }, 'stilb': {
        'name': _('stilb'),
        'symbol': 'sb',
        'family': _('luminance')
    }, 'stokes': {
        'name': _('stokes'),
        'symbol': 'St',
        'family': _('viscosity')
    }, 'stone': {
        'name': _('stone'),
        'symbol': 'st.',
        'family': _('mass')
    }, 'survey_foot': {
        'name': _('survey foot'),
        'symbol': 'survey ft',
        'family': _('length')
    }, 'survey_mile': {
        'name': _('survey mile'),
        'symbol': 'survey mile',
        'family': _('length')
    }, 'svedberg': {
        'name': 'svedberg',
        'symbol': 'S',
        'family': _('time')
    }, 'synodic_month': {
        'name': _('synodic month'),
        'symbol': _('synodic month'),
        'family': _('time')
    }, 'tablespoon': {
        'name': _('tablespoon'),
        'symbol': _('tablespoon'),
        'family': _('volume')
    }, 'tansec': {
        'name': 'tansec',
        'symbol': 'tansec',
        'family': _('constant')
    }, 'teaspoon': {
        'name': _('teaspoon'),
        'symbol': _('teaspoon'),
        'family': _('volume')
    }, 'technical_atmosphere': {
        'name': _('technical atmosphere'),
        'symbol': 'at',
        'family': _('pressure')
    }, 'tesla': {
        'name': 'tesla',
        'symbol': 'T',
        'family': _('magnetic field')
    }, 'tex': {
        'name': 'tex',
        'symbol': 'tex',
        'family': _('linear mass density')
    }, 'tex_cicero': {
        'name': 'tex cicero',
        'symbol': 'tex cicero',
        'family': _('length')
    }, 'tex_didot': {
        'name': 'tex didot',
        'symbol': 'tex didot',
        'family': _('length')
    }, 'tex_pica': {
        'name': 'tex pica',
        'symbol': 'tex pica',
        'family': _('length')
    }, 'tex_point': {
        'name': 'tex point',
        'symbol': 'tex point',
        'family': _('length')
    }, 'therm': {
        'name': _('therm'),
        'symbol': 'Thm',
        'family': _('energy')
    }, 'thermochemical_british_thermal_unit': {
        'name': _('thermochemical Btu'),
        'symbol': 'thermochemical Btu',
        'family': _('energy')
    }, 'thomson_cross_section': {
        'name': _('Thomson cross section'),
        'symbol': 'Thomson cross section',
        'family': _('surface')
    }, 'thou': {
        'name': 'thou',
        'symbol': 'thou',
        'family': _('length')
    }, 'ton': {
        'name': _('ton'),
        'symbol': 't',
        'family': _('mass')
    }, 'ton_TNT': {
        'name': _('ton of TNT'),
        'symbol': 'ton of TNT',
        'family': _('energy')
    }, 'tonne_of_oil_equivalent': {
        'name': _('ton of oil equivalent'),
        'symbol': _('toe'),
        'family': _('energy')
    }, 'torr': {
        'name': 'torr',
        'symbol': 'torr',
        'family': _('pressure')
    }, 'tropical_month': {
        'name': _('tropical month'),
        'symbol': _('tropical month'),
        'family': _('time')
    }, 'tropical_year': {
        'name': _('tropical year'),
        'symbol': _('tropical year'),
        'family': _('time')
    }, 'troy_ounce': {
        'name': _('troy ounce'),
        'symbol': _('troy ounce'),
        'family': _('mass')
    }, 'troy_pound': {
        'name': _('troy pound'),
        'symbol': _('troy pound'),
        'family': _('mass')
    }, 'turn': {
        'name': _('turn'),
        'symbol': _('turn'),
        'family': _('angle')
    }, 'unified_atomic_mass_unit': {
        'name': _('unified atomic mass unit'),
        'symbol': _('unified atomic mass unit'),
        'family': _('mass')
    }, 'unit_pole': {
        'name': _('unit pole'),
        'symbol': 'pole',
        'family': _('length')
    }, 'vacuum_permeability': {
        'name': _('vacuum permeability'),
        'symbol': 'μ0',
        'family': _('constant')
    }, 'vacuum_permittivity': {
        'name': _('vacuum permittivity'),
        'symbol': 'ε0',
        'family': _('constant')
    }, 'volt': {
        'name': 'Volt',
        'symbol': 'V',
        'family': _('electric potential difference')
    }, 'volt_ampere': {
        'name': 'Volt Ampere',
        'symbol': 'VA',
        'family': _('power')
    }, 'von_klitzing_constant': {
        'name': _('Von Klitzing constant'),
        'symbol': 'RK',
        'family': _('constant'),
    }, 'water': {
        'name': _('Water volumic mass'),
        'symbol': 'g/m³',
        'family': _('constant'),
    }, 'water_39F': {
        'name': _('Water volumic mass at 39F'),
        'symbol': 'g/m³',
        'family': _('constant'),
    }, 'water_60F': {
        'name': _('Water volumic mass at 60F'),
        'symbol': 'g/m³',
        'family': _('constant'),
    }, 'watt': {
        'name': 'Watt',
        'symbol': 'W',
        'family': _('power'),
    }, 'watt_hour': {
        'name': 'Watt',
        'symbol': 'Wh',
        'family': _('energy'),
    }, 'weber': {
        'name': 'weber',
        'symbol': 'weber',
        'family': _('flux density')
    }, 'week': {
        'name': 'week',
        'symbol': 'w',
        'family': _('time'),
    }, 'wien_frequency_displacement_law_constant': {
        'name': _('wien frequency displacement law constant'),
        'symbol': 'vpeak',
        'family': _('constant')
    }, 'wien_u': {
        'name': _('wien u'),
        'symbol': '',
        'family': _('constant')
    }, 'wien_wavelength_displacement_law_constant': {
        'name': _('wien displacement law constant'),
        'symbol': 'λpeak',
        'family': _('constant')
    }, 'wien_x': {
        'name': _('wien x'),
        'symbol': '',
        'family': _('constant')
    }, 'x_unit_Cu': {
        'name': _('Cu X-ray wavelength'),
        'symbol': '',
        'family': _('constant')
    }, 'x_unit_Mo': {
        'name': _('Mo X-ray wavelength'),
        'symbol': '',
        'family': _('constant')
    }, 'yard': {
        'name': 'yard',
        'symbol': 'yd',
        'family': _('length')
    }, 'year': {
        'name': _('year'),
        'symbol': _('year'),
        'family': _('time')
    }, 'zeta': {
        'name': 'zeta',
        'symbol': '',
        'family': _('constant')
    }

}
