"""Structures containing atomic data"""

import os
from astropy import units as u, constants as const
from .elementdatabase import ElementDatabase

atomic_symbols = {}
atomic_symbols_dict = {}
Elements = {}

def load_database(fname):
	""" This function replaces the hardcoded element data with 
	an ElementDatabase scan for compatibility purposes. 
	Future implementation should use the ElementDatabase as it provides
	access to the data directly without declaring multiple copies of 
	the data. 
	"""
	
	# Parse into atomic_symbols
	ed = ElementDatabase(fname)
	
	# Get the range of atomic numbers (optimistically)
	max_no = max([x["atomic_number"] for x in ed.data["data"]])
	
	# Update the atomic symbols	
	for i in range(max_no):
		atomic_symbols[i+1] = ed[i+1]
	
	# Update atomic symbols dict	
	for i in range(max_no):
		name = ed[i+1]["name"]
		atomic_symbols_dict[name] = ed[i+1]["symbol"]
		
	# Update elements	
	for i in range(max_no):
		symbol = ed[i+1]["symbol"]
		Elements[symbol] = {}
		Elements[symbol]["atomic_number"] = i+1		
		if ed[i+1]["atomic_mass"]:
			Elements[symbol]["atomic_mass"] = u.Unit(ed[i+1]["atomic_mass"])
		Elements[symbol]["symbol"] = ed[i+1]["symbol"]
		Elements[symbol]["name"] = ed[i+1]["name"]
	
default_file_loc = os.path.split(__file__)[0] + "/element_default.json"
load_database(os.path.join(default_file_loc))
