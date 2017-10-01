""" Element database management and handlers. 
"""

import os
import json

from astropy import units as u

class ElementDatabase(object):
	# Constants
	# Proton to Electron Mass Ratio
	data = None		
	
	def __init__(self, filename="element_default.json", validate=False,
				 use_isotope_name=True):
		"""
		Parameters
		----------
		filename: string
			A file containing the database

		validate: boolean
			Validate the database after loading
			Validate will warn on database key errors and missing 
			information.
		
		use_isotope_name: boolean
			Append -# to the name and symbol for isotopes.
			This information is redundant in a database context since
			you can uniquely identify each isotope by the isotope flag 
			and isotope number. 
		"""					
			 
		try:
			with open(filename) as infile:
				try:
					self.data = json.load(infile)
				except Exception as e:
					raise Exception("Error accessing element JSON database (%s)" % e)
		except Exception as e:
			raise Exception("Error accessing element JSON database filename (%s)" % filename)
					
		if validate:
			self.validate()
			
	def __getitem__(self, key):
		# Determine if key is an integer, a symbol, a name, or an 
		# isotope (denoted by name or symbol appended with -#
		if isinstance(key, int):
			# It's an integer, return the element corresponding to
			# that atomic number. 			
			for i in self.data["data"]:
				if i["atomic_number"] == key:
					return i
		
		# Check if it's an isotope
		if "-" in key:
			symb, mass_number = key.split("-")
			
			# Check if it's a symbol or a name			
			if len(symb) < 3:				
				# It's a symbol
				candidates = [x for x in self.data["data"] if x["symbol"] == symb]
			else:
				# It's a name
				candidates = [x for x in self.data["data"] if x["name"].lower() == symb.lower()]
						
			# Find the mass number			
			candidates = [x for x in candidates if x["mass_number"] == int(mass_number)]			
			
			if candidates:
				return candidates[0]
			else:
				raise KeyError("Key %s was not found in the database." % key)
				
		# Finally if it's a name or a symbol, just find it without
		# parsing the mass number (handle D and T which are noncompliant)
		candidates = [x for x in self.data["data"] if (not x["is_isotope"] 
		                                               or x["symbol"] in ["D", "T"])]
		
		if len(key) < 3:
			candidates = [x for x in candidates if x["symbol"] == key]
		else:
			candidates = [x for x in candidates if x["name"].lower() == key.lower()]
		
		if candidates:
			return candidates[0]
		else:
			raise KeyError("Key %s was not found in the database." % key)
		
	def write_database(self, filename, pretty=False):		
		with open(filename, 'w') as outfile:
			json.dump(filename, self.data)
			
	def write_database_csv(self, filename):
		# Unfortunately there is no way to use element_keys as 
		# a static method and still access keys from there. 
		csv_list = ["atomic_number", "symbol", "name", "atomic_mass", 
				    "is_isotope", "is_isotope_stable", "mass_number", 
				    "num_neutrons", "isotopic_abundance", "half_life"]
		with open(filename, 'w') as outfile:
			line = ",".join(csv_list) + "\n"
			outfile.write(line)
			for ele in self.data["data"]:
				line = ",".join([str(ele[key]) for key in csv_list]) + "\n"				
				outfile.write(line)

	def element_keys():
		""" Class method returns a dictionary containing all of the 
		keys used to describe each element. 
		"""
		keys = ["atomic_number", "symbol", "name", "atomic_mass", 
				"is_isotope", "is_isotope_stable", "mass_number", 
				"num_neutrons", "isotopic_abundance", "half_life"]
			   
		# Return an empty node containing these keys
		return dict.fromkeys(keys, None)
		
	def database_metadata_keys():
		""" Contains all of the metadata associated with the database.	
		
		citations - The full text of the material cited. Can be a list
				   or a string.
		author - The person who authored or compiled the database. 	
		compilation_date - Date the file was compiled
		data - The data itself (elements should be element_keys)		
		"""
		keys = ["citations", "author", "compilation_date", "data"]
		# Return an empty node containing these keys
		return dict.fromkeys(keys, None)
		
	def validate(self):
		pass

	
