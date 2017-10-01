"""Sets up a dictionary containing basic data about isotopes."""

import os
from numpy import inf, nan
from astropy import units
from .elementdatabase import ElementDatabase

Isotopes = {}

def Iso(symbol, name, atomic_number, mass_number, relative_atomic_mass,
        is_stable, isotopic_abundance=None, half_life=None):
    """Create a dictionary containing isotope information."""
    Isotope = {'name': name,
               'atomic_number': atomic_number,
               'mass_number': mass_number,
               'atomic_mass': units.Unit(relative_atomic_mass),
               'is_stable': is_stable}

    if isotopic_abundance is not None:
        assert isotopic_abundance <= 1
        Isotope['isotopic_abundance'] = isotopic_abundance
    if half_life is not None:		
        Isotope['half_life'] = units.Unit(half_life)

    return Isotope


def load_database(fname):
	""" This function replaces the hardcoded isotope data with 
	an ElementDatabase scan for compatibility purposes. 
	Future implementation should use the ElementDatabase as it provides
	access to the data directly without declaring multiple copies of 
	the data. 
	"""
	
	# Parse into atomic_symbols	
	ed = ElementDatabase(fname)
	isotopes = [x for x in ed.data["data"] if x["is_isotope"]]
	for iso in isotopes:
		if iso["symbol"] in ["n", "D", "T"]:
			symbol = iso["symbol"]
			name = iso["name"]
		else:
			symbol = iso["symbol"] + "-" + str(iso["mass_number"])
			name = iso["name"] + "-" + str(iso["mass_number"])
		Isotopes[symbol] = Iso(symbol,
							   name, 
							   iso["atomic_number"],
							   iso["mass_number"],
							   iso["atomic_mass"],
							   iso["is_stable"],
							   iso["isotopic_abundance"],
							   iso["half_life"])
			
default_file_loc = os.path.split(__file__)[0] + "/element_default.json"
load_database(os.path.join(default_file_loc))
