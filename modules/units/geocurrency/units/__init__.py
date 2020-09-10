from django.utils.translation import ugettext_lazy as _, pgettext_lazy

DIMENSION_COMMON_NAMES = {
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
    '1 / mole': _('density'),
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
    'gram / meter ** 3': _('volumic mass')
}

UNIT_EXTENDED_DEFINITION = {
    'K_alpha_Cu_d_220': {
        'name': _('Copper Kα'),
        'symbol': 'Cu Kα',
        'dimension': _('dimensionless')
    },
    'K_alpha_Mo_d_220': {
        'name': _('Molybdenum K-α'),
        'symbol': 'MO Kα',
        'dimension': _('dimensionless')
    },
    'K_alpha_W_d_220': {
        'name': _('Tungsten K-α'),
        'symbol': _('W Kα', ),
        'dimension': _('dimensionless')
    },
    'RKM': {
        'name': _('RKM'),
        'symbol': 'RKM',
        'obsolete': True,
        'dimension': _('absorption')
    },
    'UK_force_ton': {
        'name': _('long ton-force'),
        'symbol': 'long ton-force',
        'obsolete': True,
        'dimension': _('force')

    },
    'UK_hundredweight': {
        'name': 'long hundredweight',
        'symbol': 'long hundredweight',
        'obsolete': True,
        'dimension': _('mass')
    },
    'UK_ton': {
        'name': _('long ton'),
        'symbol': 'long ton',
        'obsolete': True,
        'dimension': _('mass')
    },
    'US_force_ton': {
        'name': _('short ton force'),
        'symbol': 'short ton-force',
        'obsolete': True,
        'dimension': _('force')
    },
    'US_hundredweight': {
        'name': _('short hundredweight'),
        'symbol': 'short hundredweight',
        'obsolete': True,
        'dimension': _('mass')
    },
    'US_ton': {
        'name': _('short ton'),
        'symbol': 'short ton',
        'obsolete': True,
        'dimension': _('mass')
    },
    'US_international_ampere': {
        'name': _('US International Ampere'),
        'symbol': 'US international A',
        'obsolete': True,
        'dimension': _('electric current')
    },
    'US_international_ohm': {
        'name': _('US international Ohm'),
        'symbol': 'US international Ω',
        'obsolete': True,
        'dimension': _('electric charge')
    },
    'US_international_volt': {
        'name': _('US international Volt'),
        'symbol': 'US international V',
        'obsolete': True,
        'dimension': _('electric potential difference')
    },
    'US_therm': {
        'name': _('US therm'),
        'symbol': 'thm',
        'dimension': _('heat energy')
    },
    'abampere': {
        'name': _('abampere'),
        'symbol': 'abA',
        'dimension': _('electric current')
    },
    'abcoulomb': {
        'name': _('abcoulomb'),
        'symbol': 'abC',
        'dimension': _('electromagnetic inductance')
    },
    'aberdeen': {
        'name': _('Aberdeen'),
        'symbol': 'aberdeen',
        'dimension': _('linear mass density')
    },
    'abfarad': {
        'name': _('abfarad'),
        'symbol': 'abF',
        'dimension': _('electrical capacitance')
    },
    'abhenry': {
        'name': _('abhenry'),
        'symbol': 'henry',
        'dimension': _('electrical inductance'),
    },
    'abohm': {
        'name': _('abohm'),
        'symbol': 'abohm',
        'dimension': _('electric charge')
    },
    'absiemens': {
        'name': _('absiemens'),
        'symbol': 'absiemens',
        'dimension': _('electrical conductance')
    },
    'abvolt': {
        'name': _('abvolt'),
        'symbol': 'abV',
        'dimension': _('electric potential difference')
    },
    'acre': {
        'name': _('acre'),
        'symbol': 'acre',
        'dimension': _('surface')
    },
    'acre_foot': {
        'name': _('acre-foot'),
        'symbol': 'acre-foot',
        'dimension': _('volume')
    },
    'ampere': {
        'name': _('ampere'),
        'symbol': 'A',
        'dimension': _('electric current'),
    },
    'ampere_turn': {
        'name': _('ampere-turn'),
        'symbol': 'At',
        'dimension': _('electric current'),
    },
    'angstrom': {
        'name': _('angstrom'),
        'symbol': 'Å',
        'dimension': _('length')
    },
    'angstrom_star': {
        'name': _('angstrom star'),
        'symbol': 'Å*',
        'dimension': _('length')
    },
    'apothecary_dram': {
        'name': _('apothecary dram'),
        'symbol': 'dr',
        'dimension': _('mass')
    },
    'apothecary_ounce': {
        'name': _('apothecary ounce'),
        'symbol': 'oz',
        'dimension': _('mass')
    },
    'apothecary_pound': {
        'name': _('apothecary pound'),
        'symbol': 'apothecary pound',
        'dimension': _('mass')
    }, 'arcminute': {
        'name': _('minute of arc'),
        'symbol': 'arcmin',
        'dimension': _('dimensionless')
    }, 'arcsecond': {
        'name': _('second of arc'),
        'symbol': 'arcsec',
        'dimension': _('dimensionless')
    }, 'are': {
        'name': _('are'),
        'symbol': 'are',
        'dimension': _('surface')
    }, 'astronomical_unit': {
        'name': _('astronomical unit'),
        'symbol': 'AU',
        'dimension': _('length')
    }, 'atmosphere_liter': {
        'name': _('atmosphere liter'),
        'symbol': 'atmosphere liter',
        'dimension': _('volume')
    }, 'atomic_mass_constant': {
        'name': _('atomic mass constant'),
        'symbol': 'Da',
        'dimension': _('constant')
    },
    'atomic_unit_of_current': {
        'name': _('atomic unit of current'),
        'symbol': '',
        'dimension': _('ampere')
    },
    'atomic_unit_of_electric_field': {
        'name': _('atomic unit of electric field'),
        'symbol': '',
        'dimension': _('electric field')
    }, 'atomic_unit_of_force': {
        'name': _('atomic unit of force'),
        'symbol': 'atomic unit of force',
        'dimension': _('force')
    }, 'atomic_unit_of_intensity': {
        'name': _('atomic unit of intensity'),
        'symbol': 'atomic unit of intensity',
        'dimension': _('intensity')
    }, 'atomic_unit_of_temperature': {
        'name': _('atomic unit of temperature'),
        'symbol': 'atomic unit of temperature',
        'dimension': _('temperature')
    }, 'atomic_unit_of_time': {
        'name': _('atomic unit of time'),
        'symbol': 'atomic unit of time',
        'dimension': _('time')
    }, 'avogadro_constant': {
        'name': _('Avogadro constant'),
        'symbol': 'L',
        'dimension': _('constant')
    }, 'avogadro_number': {
        'name': _('Avogadro number'),
        'symbol': '',
        'dimension': _('dimensionless'),
    }, 'bag': {
        'name': _('bag'),
        'symbol': 'bag',
        'dimension': _('quantity')
    }, 'bar': {
        'name': _('bar'),
        'symbol': 'bar',
        'dimension': _('pressure')
    }, 'barn': {
        'name': _('barn'),
        'symbol': 'b',
        'dimension': _('surface')
    }, 'barrel': {
        'name': _('barrel'),
        'symbol': 'barrel',
        'dimension': 'volume'
    }, 'barye': {
        'name': _('barrye'),
        'symbol': 'Ba',
        'dimension': _('pressure')
    },
    'baud': {
        'name': _('baud'),
        'symbol': 'Bd',
        'dimension': _('speed')
    },
    'becquerel': {
        'name': _('becquerel'),
        'symbol': 'Bq',
        'dimension': _('radioactivity')
    },
    'beer_barrel': {
        'name': _('beer barrel'),
        'symbol': 'beer barrel',
        'dimension': _('volume')
    },
    'bel': {
        'name': _('bel'),
        'symbol': 'B',
        'dimension': _('field quantity')
    },
    'biot': {
        'name': _('biot'),
        'symbol': 'biot',
        'dimension': _('dimensionless')
    },
    'biot_turn': {
        'name': _('biot turn'),
        'symbol': 'biot-turn',
        'dimension': _('dimensionless')
    },
    'bit': {
        'name': _('bit'),
        'symbol': 'bit',
        'dimension': _('quantity of information')
    },
    'bits_per_pixel': {
        'name': _('bits per pixel'),
        'symbol': 'bpp',
        'dimension': _('density of information')
    },
    'board_foot': {
        'name': _('board foot'),
        'symbol': 'board-foot',
        'dimension': _('volume')
    },
    'bohr': {
        'name': _('bohr'),
        'symbol': 'bohr',
        'dimension': _('length')
    },
    'bohr_magneton': {
        'name': _('bohr magneton'),
        'symbol': 'μB',
        'dimension': _('magnetic moment')
    },
    'boiler_horsepower': {
        'name': _('boiler horsepower'),
        'symbol': 'boiler hp',
        'dimension': _('power')
    },
    'boltzmann_constant': {
        'name': _('boltzmann constant'),
        'symbol': 'kB',
        'dimension': _('constant')
    },
    'british_thermal_unit': {
        'name': _('british thermal unit'),
        'symbol': 'Btu',
        'dimension': _('energy')
    },
    'buckingham': {
        'name': _('buckingham'),
        'symbol': 'B',
        'dimension': _('magnetic moment')
    },
    'bushel': {
        'name': _('bushel'),
        'symbol': 'bsh',
        'dimension': _('volume')
    },
    'byte': {
        'name': _('byte'),
        'symbol': 'byte',
        'dimension': _('quantity of information')
    },
    'cables_length': {
        'name': _('cable length'),
        'symbol': 'cable',
        'dimension': _('length')
    },
    'calorie': {
        'name': _('calorie'),
        'symbol': 'calorie',
        'dimension': _('energy')
    },
    'candela': {
        'name': _('candela'),
        'symbol': 'cd',
        'dimension': _('luminous intensity')
    },
    'carat': {
        'name': _('carat'),
        'symbol': 'ct',
        'dimension': _('mass')
    },
    'centimeter_H2O': {
        'name': _('centimeter H20'),
        'symbol': 'cm H2O',
        'dimension': _('pressure')
    },
    'centimeter_Hg': {
        'name': _('centimeter Hg'),
        'symbol': 'cm Hg',
        'dimension': _('pressure')
    },
    'century': {
        'name': _('century'),
        'symbol': 'c.',
        'dimension': _('time')
    },
    'chain': {
        'name': _('chain'),
        'symbol': 'chain',
        'dimension': _('length')
    },
    'cicero': {
        'name': _('cicero'),
        'symbol': 'cicero',
        'dimension': _('length')
    },
    'circular_mil': {
        'name': _('circular mil'),
        'symbol': 'mils',
        'dimension': _('surface')
    },
    'classical_electron_radius': {
        'name': _('classical electron radius'),
        'symbol': 're',
        'dimension': _('length')
    },
    'clausius': {
        'name': _('clausius'),
        'symbol': 'clausius',
        'dimension': _('energy')
    },
    'common_year': {
        'name': _('common year'),
        'symbol': '',
        'dimension': _('time')
    },
    'conductance_quantum': {
        'name': _('conductance quantum'),
        'symbol': 'G0',
        'dimension': _('electrical conductance')
    },
    'conventional_ampere_90': {
        'name': _('conventional ampere'),
        'symbol': 'A90',
        'dimension': _('electric current')
    },
    'conventional_coulomb_90': {
        'name': _('conventional coulomb'),
        'symbol': 'C90',
        'dimension': _('electromagnetic inductance')
    },
    'conventional_farad_90': {
        'name': _('conventional farad'),
        'symbol': 'F90',
        'dimension': _('eletrical capacitance')
    },
    'conventional_henry_90': {
        'name': _('conventional henry'),
        'symbol': 'H90',
        'dimension': _('electrical inductance'),
    },
    'conventional_josephson_constant': {
        'name': _('conventional josephson constant'),
        'symbol': 'KJ',
        'dimension': _('constant'),
    },
    'conventional_ohm_90': {
        'name': _('conventional ohm'),
        'symbol': 'Ω90',
        'dimension': _('electric charge')
    },
    'conventional_volt_90': {
        'name': _('conventional volt'),
        'symbol': 'V90',
        'dimension': _('electric potential difference')
    },
    'conventional_von_klitzing_constant': {
        'name': _('conventional Von Klitzing constant'),
        'symbol': 'RK',
        'dimension': _('constant'),
    },
    'conventional_watt_90': {
        'name': _('conventional Watt'),
        'symbol': 'W90',
        'dimension': _('power'),
    },
    'coulomb': {
        'name': _('coulomb'),
        'symbol': 'C',
        'dimension': _('electromagnetic inductance')
    }, 'coulomb_constant': {
        'name': _('coulomb constant'),
        'symbol': 'K',
        'dimension': _('constant')
    },
    'count': {
        'name': _('count'),
        'symbol': '',
        'dimension': _('dimensionless')
    },
    'counts_per_second': {
        'name': _('counts per second'),
        'symbol': 'counts/s',
        'dimension': _('frequency')
    },
    'css_pixel': {
        'name': _('CSS pixel'),
        'symbol': 'px',
        'dimension': _('length')
    },
    'cubic_centimeter': {
        'name': _('cubic centimeter'),
        'symbol': 'cm³',
        'dimension': _('volume')
    },
    'cubic_foot': {
        'name': _('cubic foot'),
        'symbol': 'cubic foot',
        'dimension': _('volume')
    },
    'cubic_inch': {
        'name': _('cubic inch'),
        'symbol': 'cubic inch',
        'dimension': _('volume')
    }, 'cubic_yard': {
        'name': _('cubic yard'),
        'symbol': 'cubic yard',
        'dimension': _('volume')
    }, 'cup': {
        'name': _('cup'),
        'symbol': 'cup',
        'dimension': _('volume')
    }, 'curie': {
        'name': _('curie'),
        'symbol': 'Ci',
        'dimension': _('frequency')
    }, 'dalton': {
        'name': _('dalton'),
        'symbol': 'Da',
        'dimension': _('mass')
    }, 'darcy': {
        'name': _('darcy'),
        'symbol': 'D',
        'dimension': _('permeability')
    }, 'day': {
        'name': _('day'),
        'symbol': pgettext_lazy('unit', 'day'),
        'dimension': _('time')
    }, 'debye': {
        'name': _('debye'),
        'symbol': 'D',
        'dimension': _('electric moment')
    }, 'decade': {
        'name': _('decade'),
        'symbol': pgettext_lazy('symbol', 'decade'),
        'dimension': _('time')
    }, 'degree': {
        'name': _('degree'),
        'symbol': '°',
        'dimension': _('dimensionless')
    }, 'degree_Celsius': {
        'name': _('degree Celsius'),
        'symbol': '°C',
        'dimension': _('temperature')
    }, 'degree_Fahrenheit': {
        'name': _('degree Fahrenheit'),
        'symbol': '°F',
        'dimension': _('temperature')
    }, 'degree_Rankine': {
        'name': _('degree Rankine'),
        'symbol': '°R',
        'dimension': _('temperature')
    }, 'degree_Reaumur': {
        'name': _('degree Reaumur'),
        'symbol': '°Re',
        'dimension': _('temperature')
    }, 'denier': {
        'name': _('denier'),
        'symbol': 'D',
        'dimension': _('linear mass density')
    }, 'didot': {
        'name': _('didot'),
        'symbol': 'didot',
        'dimension': _('length')
    }, 'dirac_constant': {
        'name': _('Dirac constant'),
        'symbol': 'ħ',
        'dimension': _('constant')
    }, 'dram': {
        'name': _('dram'),
        'symbol': 'dr',
        'dimension': _('mass')
    }, 'dry_barrel': {
        'name': _('dry barrel'),
        'symbol': 'dry barrel',
        'dimension': _('volume')
    }, 'dry_gallon': {
        'name': _('dry gallon'),
        'symbol': 'dry gallon',
        'dimension': _('volume')
    }, 'dry_pint': {
        'name': _('dry pint'),
        'symbol': 'dry pint',
        'dimension': _('volume')
    }, 'dry_quart': {
        'name': _('dry quart'),
        'symbol': 'dry quart',
        'dimension': _('volume')
    }, 'dtex': {
        'name': _('decitex'),
        'symbol': 'dtex',
        'dimension': _('linear mass density')
    }, 'dyne': {
        'name': _('dyne'),
        'symbol': 'dyn',
        'dimension': _('force')
    }, 'electrical_horsepower': {
        'name': _('eletcrical horsepower'),
        'symbol': 'HP',
        'dimension': _('power')
    }, 'electron_g_factor': {
        'name': _('electron G-factor'),
        'symbol': 'electron G-factor',
        'dimension': _('dimensionless')
    }, 'electron_mass': {
        'name': _('electron mass'),
        'symbol': 'me',
        'dimension': _('mass')
    }, 'electron_volt': {
        'name': _('electronvolt'),
        'symbol': 'eV',
        'dimension': _('electric potential difference')
    }, 'elementary_charge': {
        'name': _('elementary charge'),
        'symbol': 'e',
        'dimension': _('electromagnetic inductance')
    }, 'entropy_unit': {
        'name': _('entropy unit'),
        'symbol': 'S',
        'dimension': _('energy by temperature')
    }, 'enzyme_unit': {
        'name': _('enzyme unit'),
        'symbol': 'U',
        'dimension': _('catalytic activity')
    }, 'eon': {
        'name': _('eon'),
        'symbol': 'eon',
        'dimension': _('time')
    }, 'erg': {
        'name': _('erg'),
        'symbol': 'erg',
        'dimension': _('energy')
    }, 'farad': {
        'name': _('farad'),
        'symbol': 'F',
        'dimension': _('electrical capacitance')
    }, 'faraday': {
        'name': _('faraday'),
        'symbol': 'faraday',
        'dimension': _('electric charge'),
    }, 'faraday_constant': {
        'name': _('faraday constant'),
        'symbol': 'F',
        'dimension': _('constant'),
    }, 'fathom': {
        'name': _('fathom'),
        'symbol': 'fathom',
        'dimension': _('length'),
    }, 'fermi': {
        'name': _('fermi'),
        'symbol': 'fm',
        'dimension': _('length'),
    }, 'fifteen_degree_calorie': {
        'name': _('fifteen degree calorie'),
        'symbol': 'fifteen degree calorie',
        'dimension': _('energy'),
    }, 'fifth': {
        'name': _('fifth'),
        'symbol': 'fifth',
        'dimension': _('volume'),
    }, 'fine_structure_constant': {
        'name': _('fine structure constant'),
        'symbol': 'α',
        'dimension': _('constant'),
    }, 'first_radiation_constant': {
        'name': _('first radiation constant'),
        'symbol': 'c1',
        'dimension': _('constant'),
    }, 'fluid_dram': {
        'name': _('fluid dram'),
        'symbol': 'fluid dr',
        'dimension': _('mass')
    }, 'fluid_ounce': {
        'name': _('fluid ounce'),
        'symbol': 'fluid ounce',
        'dimension': _('mass')
    }, 'foot': {
        'name': _('foot'),
        'symbol': 'foot',
        'dimension': _('length')
    }, 'foot_H2O': {
        'name': _('foot H2O'),
        'symbol': 'foot H2O',
        'dimension': _('pressure')
    }, 'foot_per_second': {
        'name': _('foot per second'),
        'symbol': 'foot per second',
        'dimension': _('speed')
    }, 'foot_pound': {
        'name': _('foot pound'),
        'symbol': 'foot pound',
        'dimension': _('energy')
    }, 'force_gram': {
        'name': _('gram-force'),
        'symbol': 'gram-force',
        'obsolete': True,
        'dimension': _('force')
    }, 'force_kilogram': {
        'name': _('kilogram-force'),
        'symbol': 'kg-force',
        'obsolete': True,
        'dimension': _('force')
    }, 'force_long_ton': {
        'name': _('long ton-force'),
        'symbol': 'long ton-force',
        'obsolete': True,
        'dimension': _('force')
    }, 'force_metric_ton': {
        'name': _('tonne-force'),
        'symbol': 'tf',
        'obsolete': True,
        'dimension': _('force')
    }, 'force_ounce': {
        'name': _('ounce-force'),
        'symbol': 'ounce force',
        'obsolete': True,
        'dimension': _('force')
    }, 'force_pound': {
        'name': _('pound-force'),
        'symbol': 'pound force',
        'obsolete': True,
        'dimension': _('force')
    }, 'force_ton': {
        'name': _('tonne-force'),
        'symbol': 'tf',
        'obsolete': True,
        'dimension': _('force')
    }, 'fortnight': {
        'name': _('fortnight'),
        'symbol': 'fortnight',
        'dimension': _('time')
    }, 'franklin': {
        'name': _('franklin'),
        'symbol': 'Fr',
        'dimension': _('electrostatic unit of charge')
    }, 'furlong': {
        'name': _('furlong'),
        'symbol': 'furlong',
        'dimension': _('length')
    }, 'galileo': {
        'name': _('galileo'),
        'symbol': 'Gal',
        'dimension': _('acceleration')
    }, 'gallon': {
        'name': _('gallon'),
        'symbol': 'gal',
        'dimension': _('volume')
    }, 'gamma': {
        'name': _('gamma'),
        'symbol': 'γ',
        'dimension': _('constant')
    }, 'gamma_mass': {
        'name': _('gamma'),
        'symbol': 'γ',
        'dimension': _('mass')
    }, 'gauss': {
        'name': _('gauss'),
        'symbol': 'G',
        'dimension': _('magnetic induction')
    }, 'gilbert': {
        'name': _('gilbert'),
        'symbol': 'Gb',
        'dimension': _('electric current'),
    }, 'gill': {
        'name': _('gill'),
        'symbol': 'gill',
        'dimension': _('volume'),
    }, 'grade': {
        'name': _('grade'),
        'symbol': 'gr',
        'dimension': _('angle'),
    }, 'grain': {
        'name': _('grain'),
        'symbol': 'grain',
        'dimension': _('mass'),
    }, 'gram': {
        'name': _('gram'),
        'symbol': 'g',
        'dimension': _('mass'),
    }, 'gray': {
        'name': _('gray'),
        'symbol': 'Gy',
        'dimension': _('absorption'),
    }, 'gregorian_year': {
        'name': _('gregorian year'),
        'symbol': pgettext_lazy('unit', 'gregorian year'),
        'dimension': _('time')
    }, 'hand': {
        'name': _('hand'),
        'symbol': 'hand',
        'dimension': _('length'),
    }, 'hartree': {
        'name': _('hartree'),
        'symbol': 'Eh',
        'dimension': _('energy'),
    }, 'hectare': {
        'name': _('hectare'),
        'symbol': 'ha',
        'dimension': _('surface'),
    }, 'henry': {
        'name': _('henry'),
        'symbol': 'henry',
        'dimension': _('electrical inductance'),
    }, 'hertz': {
        'name': _('hertz'),
        'symbol': 'Hz',
        'dimension': _('frequency'),
    }, 'hogshead': {
        'name': _('hogshead'),
        'symbol': 'hhd',
        'dimension': _('volume'),
    }, 'horsepower': {
        'name': _('horsepower'),
        'symbol': 'HP',
        'dimension': _('power'),
    }, 'hour': {
        'name': _('hour'),
        'symbol': 'h',
        'dimension': _('time'),
    }, 'hundredweight': {
        'name': _('hundredweight'),
        'symbol': 'cwt',
        'dimension': _('mass'),
    }, 'impedance_of_free_space': {
        'name': _('impedance of free space'),
        'symbol': 'Z0',
        'dimension': _('electromagnetic resistance'),
    }, 'imperial_barrel': {
        'name': _('imperial barrel'),
        'symbol': 'imperial barrel',
        'dimension': _('volume'),
    }, 'imperial_bushel': {
        'name': _('imperial bushel'),
        'symbol': 'bsh',
        'dimension': _('volume'),
    }, 'imperial_cup': {
        'name': _('imperial cup'),
        'symbol': 'imperial cup',
        'dimension': _('volume'),
    }, 'imperial_fluid_drachm': {
        'name': _('imperial fluid drachm'),
        'symbol': 'ʒ',
        'dimension': _('mass'),
    }, 'imperial_fluid_ounce': {
        'name': _('imperial fluid ounce'),
        'symbol': 'fl oz',
        'dimension': _('volume'),
    }, 'imperial_fluid_scruple': {
        'name': _('imperial fluid scruple'),
        'symbol': '℈',
        'dimension': _('volume'),
    }, 'imperial_gallon': {
        'name': _('imperial gallon'),
        'symbol': 'imperial gallon',
        'dimension': _('volume'),
    }, 'imperial_gill': {
        'name': _('imperial gill'),
        'symbol': 'imperial gill',
        'dimension': _('volume'),
    }, 'imperial_minim': {
        'name': _('imperial minim'),
        'symbol': 'min',
        'dimension': _('volume'),
    }, 'imperial_peck': {
        'name': _('imperial peck'),
        'symbol': 'peck',
        'dimension': _('volume')
    }, 'imperial_pint': {
        'name': _('imperial pint'),
        'symbol': 'imperial pint',
        'dimension': _('volume')
    }, 'imperial_quart': {
        'name': _('imperial quart'),
        'symbol': 'imperial quart',
        'dimension': _('volume')
    }, 'inch': {
        'name': _('inch'),
        'symbol': 'inch',
        'dimension': _('length')
    }, 'inch_H2O_39F': {
        'name': _('inch H20 39F'),
        'symbol': 'inch H20 39F',
        'dimension': _('pressure')
    }, 'inch_H2O_60F': {
        'name': _('inch H20 60F'),
        'symbol': 'inch H20 60F',
        'dimension': _('pressure')
    }, 'inch_Hg': {
        'name': _('inch Hg'),
        'symbol': 'inch Hg',
        'dimension': _('pressure')
    }, 'inch_Hg_60F': {
        'name': _('inch Hg 60F'),
        'symbol': 'inch Hg 60F',
        'dimension': _('pressure')
    }, 'international_british_thermal_unit': {
        'name': _('international Btu'),
        'symbol': 'international Btu',
        'dimension': _('energy')
    }, 'international_calorie': {
        'name': _('international calorie'),
        'symbol': 'international calorie',
        'dimension': _('energy')
    }, 'josephson_constant': {
        'name': _('Josephson constant'),
        'symbol': 'KJ',
        'dimension': _('constant'),
    }, 'joule': {
        'name': _('Joule'),
        'symbol': 'J',
        'dimension': _('energy'),
    }, 'jute': {
        'name': _('jute'),
        'symbol': 'jute',
        'dimension': _('volume'),
    }, 'katal': {
        'name': _('katal'),
        'symbol': 'kat',
        'dimension': _('catalytic activity'),
    }, 'kelvin': {
        'name': _('kelvin'),
        'symbol': 'K',
        'dimension': _('temperature'),
    }, 'kilometer_per_hour': {
        'name': _('kilometer per hour'),
        'symbol': 'km/hour',
        'dimension': _('speed'),
    }, 'kilometer_per_second': {
        'name': _('kilometer per second'),
        'symbol': 'km/second',
        'dimension': _('speed'),
    }, 'kip': {
        'name': _('kip'),
        'symbol': 'kip',
        'dimension': _('force'),
    }, 'kip_per_square_inch': {
        'name': _('kip per square inch'),
        'symbol': 'kip / sq inch',
        'dimension': _('pressure')
    }, 'knot': {
        'name': _('knot'),
        'symbol': 'kt',
        'dimension': _('speed')
    }, 'lambda': {
        'name': _('lambda'),
        'symbol': 'λ',
        'dimension': _('volume')
    }, 'lambert': {
        'name': _('lambert'),
        'symbol': 'L',
        'dimension': _('luminance')
    }, 'langley': {
        'name': _('langley'),
        'symbol': 'Ly',
        'dimension': _('radiation')
    }, 'lattice_spacing_of_Si': {
        'name': _('lattice constant'),
        'symbol': 'Ly',
        'dimension': _('constant')
    }, 'league': {
        'name': _('league'),
        'symbol': 'league',
        'obsolete': True,
        'dimension': _('length')
    }, 'leap_year': {
        'name': _('leap year'),
        'symbol': _('year'),
        'dimension': _('time')
    }, 'light_year': {
        'name': _('light year'),
        'symbol': _('ly'),
        'dimension': _('length')
    }, 'link': {
        'name': _('link'),
        'symbol': _('li'),
        'dimension': _('length')
    }, 'liter': {
        'name': _('liter'),
        'symbol': _('L'),
        'dimension': _('volume')
    }, 'ln10': {
        'name': _('log 10'),
        'symbol': _('ln10'),
        'dimension': _('dimesionless')
    }, 'long_hundredweight': {
        'name': _('long hundredweight'),
        'symbol': 'long hundredweight',
        'obsolete': True,
        'dimension': _('mass')
    }, 'long_ton': {
        'name': _('long ton'),
        'symbol': 'long ton',
        'obsolete': True,
        'dimension': _('length')
    }, 'lumen': {
        'name': _('lumen'),
        'symbol': 'lm',
        'dimension': _('luminous flux')
    }, 'lux': {
        'name': _('lux'),
        'symbol': 'lx',
        'dimension': _('illuminance')
    }, 'magnetic_flux_quantum': {
        'name': _('magnetic flux quantum'),
        'symbol': 'Φ',
        'dimension': _('magnetic flux quantum')
    }, 'maxwell': {
        'name': _('maxwell'),
        'symbol': 'Mx',
        'dimension': _('electrostatic unit of charge')
    }, 'mean_international_ampere': {
        'name': _('mean international ampere'),
        'symbol': 'mean international A',
        'dimension': _('electric current')
    }, 'mean_international_ohm': {
        'name': _('mean international Ohm'),
        'symbol': 'mean international Ω',
        'dimension': _('electric charge')
    }, 'mean_international_volt': {
        'name': _('mean international Volt'),
        'symbol': 'mean international V',
        'dimension': _('electric potential difference')
    }, 'mercury': {

    }, 'mercury_60F': {

    }, 'meter': {
        'name': _('meter'),
        'symbol': 'm',
        'dimension': _('length')
    }, 'meter_per_second': {
        'name': _('meter per second'),
        'symbol': 'm/s',
        'dimension': _('speed')
    }, 'metric_horsepower': {
        'name': _('metric horsepower'),
        'symbol': 'hp',
        'dimension': _('power')
    }, 'metric_ton': {
        'name': _('metric ton'),
        'symbol': 't',
        'dimension': _('mass')
    }, 'micron': {
        'name': _('micron'),
        'symbol': 'μm',
        'dimension': _('length')
    }, 'mil': {
        'name': _('mil'),
        'symbol': 'ml',
        'dimension': _('volume')
    }, 'mile': {
        'name': _('mile'),
        'symbol': 'mile',
        'dimension': _('length')
    }, 'mile_per_hour': {
        'name': _('mile per hour'),
        'symbol': 'mph',
        'dimension': _('speed')
    }, 'millennium': {
        'name': _('millenium'),
        'symbol': _('millenium'),
        'dimension': _('time')
    }, 'milliarcsecond': {
        'name': _('milliarcsecond'),
        'symbol': 'mas',
        'dimension': _('angle')
    }, 'millimeter_Hg': {
        'name': _('Hg millimeter'),
        'symbol': 'mmHg',
        'dimension': _('pressure')
    }, 'minim': {
        'name': _('minim'),
        'symbol': 'min',
        'dimension': _('volume')
    }, 'minute': {
        'name': _('minute'),
        'symbol': 'min',
        'dimension': _('time')
    }, 'molar': {
        'name': _('molar'),
        'symbol': 'M',
        'dimension': _('concentration')
    }, 'molar_gas_constant': {
        'name': _('molar gas constant'),
        'symbol': 'R',
        'dimension': _('constant')
    }, 'mole': {
        'name': _('mole'),
        'symbol': 'mol',
        'dimension': _('amount of substance'),
    }, 'month': {
        'name': _('month'),
        'symbol': 'm',
        'dimension': _('time')
    }, 'nautical_mile': {
        'name': _('nautical mile'),
        'symbol': _('nm'),
        'dimension': _('length')
    }, 'neper': {
        'name': _('neper'),
        'symbol': _('Np'),
        'dimension': _('neper')
    }, 'neutron_mass': {
        'name': _('neutron mass'),
        'symbol': 'mN',
        'dimension': _('constant')
    }, 'newton': {
        'name': _('newton'),
        'symbol': 'N',
        'dimension': _('force')
    }, 'newtonian_constant_of_gravitation': {
        'name': _('newtonian constant of gravitation'),
        'symbol': 'N',
        'dimension': _('constant')
    }, 'nit': {
        'name': _('nit'),
        'symbol': 'cd/m²',
        'dimension': _('luminance')
    }, 'nuclear_magneton': {
        'name': _('nuclear magneton'),
        'symbol': 'μN',
        'dimension': _('magnetic moment')
    }, 'number_english': {
        'name': _('number english'),
        'symbol': 'm/g',
        'dimension': _('meter per gram')
    }, 'number_meter': {
        'name': _('number meter'),
        'symbol': 'm/g',
        'dimension': _('meter per gram')
    }, 'oersted': {
        'name': _('oersted'),
        'symbol': 'Oe',
        'dimension': _('H-field')
    }, 'ohm': {
        'name': _('ohm'),
        'symbol': 'Ω',
        'dimension': _('electric charge')
    }, 'oil_barrel': {
        'name': _('oil barrel'),
        'symbol': 'oil barrel',
        'dimension': 'volume'
    }, 'ounce': {
        'name': _('ounce'),
        'symbol': 'oz t',
        'dimension': _('mass')
    }, 'parsec': {
        'name': _('parsec'),
        'symbol': 'pc',
        'dimension': _('length')
    }, 'particle': {
        'name': _('particle'),
        'symbol': 'particle',
        'dimension': _('amount of substance')
    }, 'pascal': {
        'name': _('pascal'),
        'symbol': 'Pa',
        'dimension': _('pressure')
    }, 'peak_sun_hour': {
        'name': _('peak sun hour'),
        'symbol': 'peak sun hour',
        'dimension': _('time')
    }, 'peck': {
        'name': _('peck'),
        'symbol': 'peck',
        'dimension': _('volume')
    }, 'pennyweight': {
        'name': _('pennyweight'),
        'symbol': 'dwt',
        'dimension': _('mass')
    }, 'pi': {
        'name': 'pi',
        'symbol': 'π',
        'dimension': _('constant')
    }, 'pica': {
        'name': _('pica'),
        'symbol': 'pica',
        'dimension': _('length')
    }, 'pint': {
        'name': _('pint'),
        'symbol': 'pt',
        'dimension': _('volume')
    }, 'pixel': {
        'name': _('pixel'),
        'symbol': 'px',
        'dimension': _('unit')
    }, 'pixels_per_centimeter': {
        'name': _('pixel per centimeter'),
        'symbol': 'ppcm',
        'dimension': _('density')
    }, 'pixels_per_inch': {
        'name': _('pixel per inch'),
        'symbol': 'ppi',
        'dimension': _('density')
    }, 'planck_constant': {
        'name': _('Planck constant'),
        'symbol': 'h',
        'dimension': _('constant')
    }, 'planck_current': {
        'name': _('Planck current'),
        'symbol': _('qP'),
        'dimension': _('electric current')
    }, 'planck_length': {
        'name': _('Planck current'),
        'symbol': _('lP'),
        'dimension': _('length')
    }, 'planck_mass': {
        'name': _('Planck mass'),
        'symbol': _('mP'),
        'dimension': _('mass')
    }, 'planck_temperature': {
        'name': _('Planck temperature'),
        'symbol': _('TP'),
        'dimension': _('temperature')
    }, 'planck_time': {
        'name': _('Planck time'),
        'symbol': _('tP'),
        'dimension': _('time')
    }, 'point': {
        'name': _('point'),
        'symbol': 'pt',
        'dimension': _('length')
    }, 'poise': {
        'name': _('poise'),
        'symbol': 'P',
        'dimension': _('viscosity')
    }, 'pound': {
        'name': _('pound'),
        'symbol': 'lb',
        'dimension': _('mass')
    }, 'pound_force_per_square_inch': {
        'name': _('pound force per square inch'),
        'symbol': 'lb-force/inch²',
        'dimension': _('pressure')
    }, 'poundal': {
        'name': _('poundal'),
        'symbol': 'pdl',
        'dimension': _('force')
    }, 'proton_mass': {
        'name': _('proton mass'),
        'symbol': 'mP',
        'dimension': _('constant')
    }, 'quadrillion_Btu': {
        'name': _('quadrillion Btu'),
        'symbol': 'quadrillion Btu',
        'dimension': _('energy')
    }, 'quart': {
        'name': _('quart'),
        'symbol': 'qt',
        'dimension': _('volume')
    }, 'quarter': {
        'name': _('quarter'),
        'symbol': 'qr',
        'dimension': _('length')
    }, 'radian': {
        'name': _('radian'),
        'symbol': 'rad',
        'dimension': _('angle')
    }, 'rads': {
        'name': _('rads'),
        'symbol': 'rads',
        'dimension': _('absorption')
    }, 'reciprocal_centimeter': {
        'name': _('reciprocal centimeter'),
        'symbol': 'cm⁻¹',
        'dimension': _('reciprocal length')
    }, 'refrigeration_ton': {
        'name': _('refrigeration ton'),
        'symbol': 'TR',
        'dimension': _('power')
    }, 'rem': {
        'name': _('roentgen equivalent man'),
        'symbol': 'rem',
        'dimension': _('absorption')
    }, 'revolutions_per_minute': {
        'name': _('revolutions per minute'),
        'symbol': _('rpm'),
        'dimension': _('angular speed')
    }, 'revolutions_per_second': {
        'name': _('revolutions per second'),
        'symbol': _('rps'),
        'dimension': _('angular speed')
    }, 'reyn': {
        'name': _('reyn'),
        'symbol': _('reyn'),
        'dimension': _('viscosity')
    }, 'rhe': {
        'name': _('reciprocal poise'),
        'symbol': 'P⁻¹',
        'dimension': _('reciprocal viscosity')
    }, 'rod': {
        'name': _('rod'),
        'symbol': 'rod',
        'dimension': _('length')
    }, 'roentgen': {
        'name': _('roentgen'),
        'symbol': 'R',
        'dimension': _('radiation exposure')
    }, 'rutherford': {
        'name': _('rutherford'),
        'symbol': 'Rd',
        'dimension': _('frequency')
    }, 'rydberg': {
        'name': _('rydberg'),
        'symbol': 'Ry',
        'dimension': _('energy')
    }, 'rydberg_constant': {
        'name': _('rydberg constant'),
        'symbol': 'R∞',
        'dimension': _('constant')
    }, 'scaled_point': {
        'name': _('scaled point'),
        'symbol': 'Pt',
        'dimension': _('length')
    }, 'scruple': {
        'name': _('scruple'),
        'symbol': '℈',
        'dimension': _('volume'),
    }, 'second': {
        'name': _('second'),
        'symbol': 's',
        'dimension': _('time'),
    }, 'second_radiation_constant': {
        'name': _('second radiation constant'),
        'symbol': 'c2',
        'dimension': _('constant'),
    }, 'shake': {
        'name': _('shake'),
        'symbol': 'shake',
        'dimension': _('time'),
    }, 'shot': {
        'name': _('shot'),
        'symbol': 'shot',
        'dimension': _('length'),
    }, 'sidereal_day': {
        'name': _('sidereal day'),
        'symbol': pgettext_lazy('unit', 'sidereal day'),
        'dimension': _('time')
    }, 'sidereal_month': {
        'name': _('sidereal month'),
        'symbol': pgettext_lazy('unit', 'sidereal month'),
        'dimension': _('time')
    }, 'sidereal_year': {
        'name': _('sidereal year'),
        'symbol': pgettext_lazy('unit', 'sidereal year'),
        'dimension': _('time')
    }, 'siemens': {
        'name': _('siemens'),
        'symbol': 'S',
        'dimension': _('electrical conductance')
    }, 'sievert': {
        'name': _('sievert'),
        'symbol': 'Sv',
        'dimension': _('absorption')
    }, 'slinch': {
        'name': _('slinch'),
        'symbol': 'slinch',
        'dimension': _('mass')
    }, 'slug': {
        'name': _('slug'),
        'symbol': 'slug',
        'dimension': _('mass')
    }, 'speed_of_light': {
        'name': _('speed of light'),
        'symbol': 'c',
        'dimension': _('speed')
    }, 'square_degree': {
        'name': _('square degree'),
        'symbol': '(°)²',
        'dimension': _('solid angle')
    }, 'square_foot': {
        'name': _('square foot'),
        'symbol': 'sq ft',
        'dimension': _('surface')
    }, 'square_inch': {
        'name': _('square inch'),
        'symbol': 'sq in',
        'dimension': _('surface')
    }, 'square_league': {
        'name': _('square league'),
        'symbol': 'sq league',
        'dimension': _('surface')
    }, 'square_mile': {
        'name': _('square mile'),
        'symbol': 'sq mile',
        'dimension': _('surface')
    }, 'square_rod': {
        'name': _('square rod'),
        'symbol': 'sq rod',
        'dimension': _('surface')
    }, 'square_survey_mile': {
        'name': _('square survey mile'),
        'symbol': 'sq survey mile',
        'dimension': _('surface')
    }, 'square_yard': {
        'name': _('square yard'),
        'symbol': 'sq yd',
        'dimension': _('surface')
    }, 'standard_atmosphere': {
        'name': _('standard atmosphere'),
        'symbol': 'atm',
        'dimension': _('pressure')
    }, 'standard_gravity': {
        'name': _('standard gravity'),
        'symbol': 'g0',
        'dimension': _('constant')
    }, 'standard_liter_per_minute': {
        'name': _('standard liter per minute'),
        'symbol': 'SLM',
        'dimension': _('volumetric flow rate')
    }, 'statampere': {
        'name': 'statampere',
        'symbol': 'statA',
        'dimension': _('electric current')
    }, 'statfarad': {
        'name': 'statfarad',
        'symbol': 'statF',
        'dimension': _('electrical capacitance')
    }, 'stathenry': {
        'name': 'stathenry',
        'symbol': 'stathenry',
        'dimension': _('electrical inductance'),
    }, 'statmho': {
        'name': 'statmho',
        'symbol': 'statmho',
        'dimension': _('electrical conductance')
    }, 'statohm': {
        'name': 'statohm',
        'symbol': 'statohm',
        'dimension': _('electrical resistance')
    }, 'stattesla': {
        'name': 'stattesla',
        'symbol': 'stattesla',
        'dimension': _('magnetic field')
    }, 'statvolt': {
        'name': 'statvolt',
        'symbol': 'statvolt',
        'dimension': _('electric potential difference')
    }, 'statweber': {
        'name': 'statweber',
        'symbol': 'statweber',
        'dimension': _('flux density')
    }, 'stefan_boltzmann_constant': {
        'name': _('Stefan-Boltzmann constant'),
        'symbol': 'σ',
        'dimension': _('constant')
    }, 'steradian': {
        'name': _('steradian'),
        'symbol': 'sr',
        'dimension': _('solid angle')
    }, 'stere': {
        'name': _('stere'),
        'symbol': 'st',
        'dimension': _('volume')
    }, 'stilb': {
        'name': _('stilb'),
        'symbol': 'sb',
        'dimension': _('luminance')
    }, 'stokes': {
        'name': _('stokes'),
        'symbol': 'St',
        'dimension': _('viscosity')
    }, 'stone': {
        'name': _('stone'),
        'symbol': 'st.',
        'dimension': _('mass')
    }, 'survey_foot': {
        'name': _('survey foot'),
        'symbol': 'survey ft',
        'dimension': _('length')
    }, 'survey_mile': {
        'name': _('survey mile'),
        'symbol': 'survey mile',
        'dimension': _('length')
    }, 'svedberg': {
        'name': 'svedberg',
        'symbol': 'S',
        'dimension': _('time')
    }, 'synodic_month': {
        'name': _('synodic month'),
        'symbol': _('synodic month'),
        'dimension': _('time')
    }, 'tablespoon': {
        'name': _('tablespoon'),
        'symbol': _('tablespoon'),
        'dimension': _('volume')
    }, 'tansec': {
        'name': 'tansec',
        'symbol': 'tansec',
        'dimension': _('constant')
    }, 'teaspoon': {
        'name': _('teaspoon'),
        'symbol': _('teaspoon'),
        'dimension': _('volume')
    }, 'technical_atmosphere': {
        'name': _('technical atmosphere'),
        'symbol': 'at',
        'dimension': _('pressure')
    }, 'tesla': {
        'name': 'tesla',
        'symbol': 'T',
        'dimension': _('magnetic field')
    }, 'tex': {
        'name': 'tex',
        'symbol': 'tex',
        'dimension': _('linear mass density')
    }, 'tex_cicero': {
        'name': 'tex cicero',
        'symbol': 'tex cicero',
        'dimension': _('length')
    }, 'tex_didot': {
        'name': 'tex didot',
        'symbol': 'tex didot',
        'dimension': _('length')
    }, 'tex_pica': {
        'name': 'tex pica',
        'symbol': 'tex pica',
        'dimension': _('length')
    }, 'tex_point': {
        'name': 'tex point',
        'symbol': 'tex point',
        'dimension': _('length')
    }, 'therm': {
        'name': _('therm'),
        'symbol': 'Thm',
        'dimension': _('energy')
    }, 'thermochemical_british_thermal_unit': {
        'name': _('thermochemical Btu'),
        'symbol': 'thermochemical Btu',
        'dimension': _('energy')
    }, 'thomson_cross_section': {
        'name': _('Thomson cross section'),
        'symbol': 'Thomson cross section',
        'dimension': _('surface')
    }, 'thou': {
        'name': 'thou',
        'symbol': 'thou',
        'dimension': _('length')
    }, 'ton': {
        'name': _('ton'),
        'symbol': 't',
        'dimension': _('mass')
    }, 'ton_TNT': {
        'name': _('ton of TNT'),
        'symbol': 'ton of TNT',
        'dimension': _('energy')
    }, 'tonne_of_oil_equivalent': {
        'name': _('ton of oil equivalent'),
        'symbol': _('toe'),
        'dimension': _('energy')
    }, 'torr': {
        'name': 'torr',
        'symbol': 'torr',
        'dimension': _('pressure')
    }, 'tropical_month': {
        'name': _('tropical month'),
        'symbol': _('tropical month'),
        'dimension': _('time')
    }, 'tropical_year': {
        'name': _('tropical year'),
        'symbol': _('tropical year'),
        'dimension': _('time')
    }, 'troy_ounce': {
        'name': _('troy ounce'),
        'symbol': _('troy ounce'),
        'dimension': _('mass')
    }, 'troy_pound': {
        'name': _('troy pound'),
        'symbol': _('troy pound'),
        'dimension': _('mass')
    }, 'turn': {
        'name': _('turn'),
        'symbol': _('turn'),
        'dimension': _('angle')
    }, 'unified_atomic_mass_unit': {
        'name': _('unified atomic mass unit'),
        'symbol': _('unified atomic mass unit'),
        'dimension': _('mass')
    }, 'unit_pole': {
        'name': _('unit pole'),
        'symbol': 'pole',
        'dimension': _('length')
    }, 'vacuum_permeability': {
        'name': _('vacuum permeability'),
        'symbol': 'μ0',
        'dimension': _('constant')
    }, 'vacuum_permittivity': {
        'name': _('vacuum permittivity'),
        'symbol': 'ε0',
        'dimension': _('constant')
    }, 'volt': {
        'name': 'Volt',
        'symbol': 'V',
        'dimension': _('electric potential difference')
    }, 'volt_ampere': {
        'name': 'Volt Ampere',
        'symbol': 'VA',
        'dimension': _('power')
    }, 'von_klitzing_constant': {
        'name': _('Von Klitzing constant'),
        'symbol': 'RK',
        'dimension': _('constant'),
    }, 'water': {
        'name': _('Water volumic mass'),
        'symbol': 'g/m³',
        'dimension': _('constant'),
    }, 'water_39F': {
        'name': _('Water volumic mass at 39F'),
        'symbol': 'g/m³',
        'dimension': _('constant'),
    }, 'water_60F': {
        'name': _('Water volumic mass at 60F'),
        'symbol': 'g/m³',
        'dimension': _('constant'),
    }, 'watt': {
        'name': 'Watt',
        'symbol': 'W',
        'dimension': _('power'),
    }, 'watt_hour': {
        'name': 'Watt',
        'symbol': 'Wh',
        'dimension': _('energy'),
    }, 'weber': {
        'name': 'weber',
        'symbol': 'weber',
        'dimension': _('flux density')
    }, 'week': {
        'name': 'week',
        'symbol': 'w',
        'dimension': _('time'),
    }, 'wien_frequency_displacement_law_constant': {
        'name': _('wien frequency displacement law constant'),
        'symbol': 'vpeak',
        'dimension': _('constant')
    }, 'wien_u': {
        'name': _('wien u'),
        'symbol': '',
        'dimension': _('constant')
    }, 'wien_wavelength_displacement_law_constant': {
        'name': _('wien displacement law constant'),
        'symbol': 'λpeak',
        'dimension': _('constant')
    }, 'wien_x': {
        'name': _('wien x'),
        'symbol': '',
        'dimension': _('constant')
    }, 'x_unit_Cu': {
        'name': _('Cu X-ray wavelength'),
        'symbol': '',
        'dimension': _('constant')
    }, 'x_unit_Mo': {
        'name': _('Mo X-ray wavelength'),
        'symbol': '',
        'dimension': _('constant')
    }, 'yard': {
        'name': 'yard',
        'symbol': 'yd',
        'dimension': _('length')
    }, 'year': {
        'name': _('year'),
        'symbol': _('year'),
        'dimension': _('time')
    }, 'zeta': {
        'name': 'zeta',
        'symbol': '',
        'dimension': _('constant')
    }

}
