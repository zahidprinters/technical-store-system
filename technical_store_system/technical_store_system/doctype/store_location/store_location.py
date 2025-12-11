"""
Store Location Controller
Auto-generates location_code and location_name from hierarchical components
"""

import frappe
from frappe.model.document import Document


class StoreLocation(Document):
	"""Controller for Store Location DocType"""
	
	def autoname(self):
		"""Auto-generate location code before naming"""
		self.generate_location_code()
		# Set name from location_code for Frappe's naming system
		if self.location_code:
			self.name = self.location_code
	
	def before_save(self):
		"""Generate location name before save"""
		self.generate_location_name()
	
	def validate(self):
		"""Validate location code and name"""
		if not self.location_code:
			self.generate_location_code()
		self.generate_location_name()
	
	def generate_location_code(self):
		"""
		Auto-generate location_code from hierarchy + name fields
		
		Examples:
		- Warehouse: warehouse_name = 'WH-1' → location_code = 'WH-1'
		- Zone: store = 'WH-1', zone_name = 'A' → location_code = 'WH-1-A'
		- Rack: zone = 'WH-1-A', rack_name = 'R01' → location_code = 'WH-1-A-R01'
		- Shelf: rack = 'WH-1-A-R01', shelf_name = 'S1' → location_code = 'WH-1-A-R01-S1'
		- Bin: shelf = 'WH-1-A-R01-S1', bin = 'B1' → location_code = 'WH-1-A-R01-S1-B1'
		"""
		
		location_type = self.location_type
		
		if location_type == "Warehouse":
			# Warehouse: use warehouse_name directly
			if self.warehouse_name:
				self.location_code = self.warehouse_name
		
		elif location_type == "Zone":
			# Zone: store + zone_name
			if self.store and self.zone_name:
				self.location_code = f"{self.store}-{self.zone_name}"
		
		elif location_type == "Rack":
			# Rack: zone + rack_name
			if self.zone and self.rack_name:
				self.location_code = f"{self.zone}-{self.rack_name}"
		
		elif location_type == "Shelf":
			# Shelf: rack + shelf_name
			if self.rack and self.shelf_name:
				self.location_code = f"{self.rack}-{self.shelf_name}"
		
		elif location_type == "Bin":
			# Bin: shelf + bin name
			if self.shelf and self.bin:
				self.location_code = f"{self.shelf}-{self.bin}"
		
		elif location_type in ["Transit", "Staging", "Other"]:
			# Special locations: use warehouse_name if provided
			if self.warehouse_name:
				self.location_code = self.warehouse_name
	
	def generate_location_name(self):
		"""
		Auto-generate location_name from hierarchical components
		Hierarchy: Store → Zone → Rack → Shelf → Bin
		
		Examples:
		- Store: "STORE-01" (just code)
		- Zone in STORE-01: "STORE-01-A" (store + zone)
		- Rack in Zone A: "STORE-01-A-R01" (store + zone + rack)
		- Shelf in Rack R01: "STORE-01-A-R01-S1" (store + zone + rack + shelf)
		- Bin in Shelf S1: "STORE-01-A-R01-S1-B1" (full hierarchy)
		
		Physical Components (for bins):
		- Rack: R01, R02, R03
		- Shelf: S1, S2, S3
		- Bin: B1, B2, B3
		"""
		
		location_type = self.location_type
		
		# Build name based on hierarchy
		parts = []
		
		# Store is always first (if set)
		if self.store:
			parts.append(self.store)
		
		# Zone second
		if self.zone and location_type in ["Zone", "Rack", "Shelf", "Bin"]:
			# Extract just the zone part (last segment after '-')
			zone_part = self.zone.split('-')[-1] if '-' in self.zone else self.zone
			parts.append(zone_part)
		
		# Rack third
		if self.rack and location_type in ["Rack", "Shelf", "Bin"]:
			rack_part = self.rack.split('-')[-1] if '-' in self.rack else self.rack
			parts.append(rack_part)
		
		# Shelf fourth
		if self.shelf and location_type in ["Shelf", "Bin"]:
			shelf_part = self.shelf.split('-')[-1] if '-' in self.shelf else self.shelf
			parts.append(shelf_part)
		
		# Bin last
		if self.bin and location_type == "Bin":
			parts.append(self.bin)
		
		# Join all parts with ' - '
		if parts:
			self.location_name = " - ".join(parts)
		else:
			# Fallback to location_code if no hierarchy
			self.location_name = self.location_code or "New Location"
