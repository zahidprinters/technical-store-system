"""
Store Location Controller
=========================

Handles auto-generation of location codes and names with intelligent increment system.

Features:
- Auto-increments location names (Numeric, Alphabetic, Roman Numerals)
- Configurable prefixes via Store Settings
- Parent-aware naming (zones in WH-1 separate from WH-2)
- Full hierarchy display (e.g., "WH-1 - Z-A - R01 - S01 - B-1")

Architecture:
- location_code: Document name/primary key (e.g., "WH-1-Z-A-R01")
- location_name: Display name showing full hierarchy (e.g., "WH-1 - Z-A - R01")
- Name fields: Auto-generated per level (warehouse_name, zone_name, rack_name, shelf_name, bin)

Hierarchy: Warehouse → Zone → Rack → Shelf → Bin
"""

import frappe
from frappe.model.document import Document


# ============================================================================
# DOC EVENT HANDLERS
# ============================================================================

def before_insert_event(doc, method=None):
	"""
	Event handler for before_insert hook
	
	Validates and generates location_code (primary key) and location_name (display) 
	before the document is inserted into the database.
	
	Respects installer settings for validation and generation behavior.
	"""
	# Run validations
	validate_location(doc)
	
	# Generate location code
	generate_location_code(doc)
	
	if doc.location_code:
		doc.name = doc.location_code
	
	# Generate display name
	generate_location_name(doc)
	
	# Update system statistics
	update_system_stats(doc)


def before_save_event(doc, method=None):
	"""
	Event handler for before_save hook
	
	Updates location_name on save (location_code is immutable after insert)
	"""
	if not doc.is_new():
		generate_location_name(doc)


# ============================================================================
# LOCATION CODE GENERATION
# ============================================================================

def generate_location_code(doc):
	"""
	Generate unique location_code (primary key) with auto-increment
	
	Respects installer settings:
	- enable_auto_location_code: Enable/disable auto-generation
	- allow_manual_override: Allow manual location code entry
	- lock_naming_after_first_use: Prevent pattern changes after first use
	
	Strategy:
	1. Check installer settings for auto-generation
	2. Auto-generate name field if empty (warehouse_name, zone_name, etc.)
	3. Build hierarchical code by appending to parent code
	
	Examples:
		Warehouse: "WH-1"
		Zone: "WH-1-Z-A" (WH-1 + Z-A)
		Rack: "WH-1-Z-A-R01" (WH-1-Z-A + R01)
		Shelf: "WH-1-Z-A-R01-S01" (WH-1-Z-A-R01 + S01)
		Bin: "WH-1-Z-A-R01-S01-B-1" (WH-1-Z-A-R01-S01 + B-1)
	
	Args:
		doc: Store Location document
	"""
	# Get installer settings
	settings = frappe.get_single("Store Settings")
	
	# Check if auto-generation is enabled
	if not settings.get("enable_auto_location_code"):
		# Auto-generation disabled, require manual entry
		if not doc.location_code:
			frappe.throw("Auto-generation is disabled. Please enter location code manually.")
		return
	
	# Check if manual override is provided
	if doc.location_code and settings.get("allow_manual_override"):
		# Manual code provided and override allowed, skip auto-generation
		return
	
	location_type = doc.location_type
	
	if location_type == "Warehouse":
		if not doc.warehouse_name:
			doc.warehouse_name = get_next_location_name(None, "Warehouse")
		doc.location_code = doc.warehouse_name
	
	elif location_type == "Zone":
		if not doc.zone_name and doc.store:
			doc.zone_name = get_next_location_name(doc.store, "Zone")
		if doc.store and doc.zone_name:
			doc.location_code = f"{doc.store}-{doc.zone_name}"
	
	elif location_type == "Rack":
		if not doc.rack_name and doc.zone:
			doc.rack_name = get_next_location_name(doc.zone, "Rack")
		if doc.zone and doc.rack_name:
			doc.location_code = f"{doc.zone}-{doc.rack_name}"
	
	elif location_type == "Shelf":
		if not doc.shelf_name and doc.rack:
			doc.shelf_name = get_next_location_name(doc.rack, "Shelf")
		if doc.rack and doc.shelf_name:
			doc.location_code = f"{doc.rack}-{doc.shelf_name}"
	
	elif location_type == "Bin":
		if not doc.bin and doc.shelf:
			doc.bin = get_next_location_name(doc.shelf, "Bin")
		if doc.shelf and doc.bin:
			doc.location_code = f"{doc.shelf}-{doc.bin}"
	
	elif location_type in ["Transit", "Staging", "Other"]:
		if not doc.warehouse_name:
			doc.warehouse_name = location_type.upper()
		doc.location_code = doc.warehouse_name


# ============================================================================
# AUTO-INCREMENT SYSTEM
# ============================================================================

def get_next_location_name(parent_location, location_type):
	"""
	Calculate next available location name with auto-increment
	
	Features:
	- Parent-aware: Zones in WH-1 are separate from zones in WH-2
	- Pattern-based: Supports Numeric (1,2,3), Alphabetic (A,B,C), Roman (I,II,III)
	- Configurable: Reads patterns and prefixes from Store Settings
	
	Args:
		parent_location: Parent location code (None for Warehouse)
		location_type: Location type (Warehouse, Zone, Rack, Shelf, Bin)
	
	Returns:
		Next name with prefix (e.g., "WH-4", "Z-D", "R05", "S3", "B-10")
	
	Examples:
		Existing: WH-1, WH-2, WH-3 → Next: WH-4
		Existing: Z-A, Z-B → Next: Z-C
		Existing: R01, R02 → Next: R03
		Existing: I, II, III → Next: IV
	"""
	settings = frappe.get_single("Store Settings")
	
	# Get configuration for this location type
	pattern_field = f"{location_type.lower()}_naming_pattern"
	prefix_field = f"{location_type.lower()}_prefix"
	
	naming_pattern = getattr(settings, pattern_field, "Numeric")
	prefix = getattr(settings, prefix_field, location_type[0].upper())
	
	# Build filters for database query
	filters = {"location_type": location_type}
	
	if parent_location:
		# Filter by parent to make increment parent-aware
		parent_field_map = {
			"Zone": "store",
			"Rack": "zone",
			"Shelf": "rack",
			"Bin": "shelf"
		}
		parent_field = parent_field_map.get(location_type)
		if parent_field:
			filters[parent_field] = parent_location
	
	# Get name field for this location type
	field_map = {
		"Warehouse": "warehouse_name",
		"Zone": "zone_name",
		"Rack": "rack_name",
		"Shelf": "shelf_name",
		"Bin": "bin"
	}
	
	field_name = field_map.get(location_type)
	if not field_name:
		return f"{prefix}-1"
	
	# Query existing names
	existing = frappe.get_all(
		"Store Location",
		filters=filters,
		fields=[field_name],
		pluck=field_name
	)
	
	# Extract values (strip prefixes and separators)
	existing_values = []
	for name in existing:
		if name:
			value = name.replace(prefix, "").replace("-", "").strip()
			if value:
				existing_values.append(value)
	
	# Calculate next value
	next_value = get_next_value(existing_values, naming_pattern)
	
	# Format with prefix
	if naming_pattern == "Numeric":
		# Use padding for racks and shelves (R01, S01)
		if location_type in ["Rack", "Shelf"]:
			return f"{prefix}{next_value:02d}"
		else:
			return f"{prefix}-{next_value}"
	else:
		return f"{prefix}-{next_value}"


def get_next_value(existing_values, pattern):
	"""
	Calculate next sequential value based on naming pattern
	
	Supports three naming patterns:
	1. Numeric: 1, 2, 3, 4... → Next: 5
	2. Alphabetic: A, B, C... Z, AA, AB... → Next: increment letter
	3. Roman Numerals: I, II, III, IV, V... → Next: increment roman
	
	Args:
		existing_values: List of existing values (cleaned, no prefixes)
		pattern: Naming pattern ("Numeric", "Alphabetic", "Roman Numerals")
	
	Returns:
		Next value (int for Numeric, str for Alphabetic/Roman)
	"""
	import re
	
	if pattern == "Alphabetic":
		letters = [val.upper() for val in existing_values if val and val.isalpha()]
		
		if not letters:
			return "A"
		
		max_letter = max(letters)
		
		# Increment: A→B, Z→AA, AA→AB, AZ→BA
		if max_letter == "Z":
			return "AA"
		else:
			return chr(ord(max_letter) + 1)
	
	elif pattern == "Roman Numerals":
		numbers = []
		for val in existing_values:
			try:
				num = roman_to_int(val)
				numbers.append(num)
			except:
				pass
		
		next_num = max(numbers) + 1 if numbers else 1
		return int_to_roman(next_num)
	
	else:  # Numeric (default)
		numbers = []
		for val in existing_values:
			try:
				nums = re.findall(r'\d+', str(val))
				if nums:
					numbers.append(int(nums[0]))
			except:
				pass
		
		return max(numbers) + 1 if numbers else 1


# ============================================================================
# ROMAN NUMERAL UTILITIES
# ============================================================================

def roman_to_int(roman):
	"""
	Convert Roman numeral string to integer
	
	Examples:
		I → 1, IV → 4, IX → 9, XL → 40, XC → 90
	
	Args:
		roman: Roman numeral string (e.g., "XIV")
	
	Returns:
		Integer value (e.g., 14)
	"""
	roman_values = {
		'I': 1, 'V': 5, 'X': 10, 'L': 50,
		'C': 100, 'D': 500, 'M': 1000
	}
	
	total = 0
	prev_value = 0
	
	for char in reversed(roman.upper()):
		value = roman_values.get(char, 0)
		if value < prev_value:
			total -= value
		else:
			total += value
		prev_value = value
	
	return total


def int_to_roman(num):
	"""
	Convert integer to Roman numeral string
	
	Examples:
		1 → I, 4 → IV, 9 → IX, 40 → XL, 90 → XC
	
	Args:
		num: Integer (1-3999)
	
	Returns:
		Roman numeral string (e.g., "XIV" for 14)
	"""
	values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
	symbols = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
	
	roman = ''
	
	for i in range(len(values)):
		count = int(num / values[i])
		if count:
			roman += symbols[i] * count
			num -= values[i] * count
	
	return roman


# ============================================================================
# LOCATION NAME DISPLAY GENERATION
# ============================================================================

def generate_location_name(doc):
	"""
	Generate human-readable location_name showing full hierarchy
	
	Builds display name by fetching parent names and combining with current level.
	This provides clear visual hierarchy in lists and forms.
	
	Format: Components separated by " - "
	
	Examples:
		Warehouse: "WH-1"
		Zone: "WH-1 - Z-A"
		Rack: "WH-1 - Z-A - R01"
		Shelf: "WH-1 - Z-A - R01 - S01"
		Bin: "WH-1 - Z-A - R01 - S01 - B-1"
	
	Args:
		doc: Store Location document
	"""
	location_type = doc.location_type
	parts = []
	
	if location_type == "Warehouse":
		if doc.warehouse_name:
			parts.append(doc.warehouse_name)
	
	elif location_type == "Zone":
		if doc.store:
			parent_wh = frappe.get_value("Store Location", doc.store, "warehouse_name")
			if parent_wh:
				parts.append(parent_wh)
		if doc.zone_name:
			parts.append(doc.zone_name)
	
	elif location_type == "Rack":
		if doc.store:
			parent_wh = frappe.get_value("Store Location", doc.store, "warehouse_name")
			if parent_wh:
				parts.append(parent_wh)
		if doc.zone:
			parent_zone = frappe.get_value("Store Location", doc.zone, "zone_name")
			if parent_zone:
				parts.append(parent_zone)
		if doc.rack_name:
			parts.append(doc.rack_name)
	
	elif location_type == "Shelf":
		if doc.store:
			parent_wh = frappe.get_value("Store Location", doc.store, "warehouse_name")
			if parent_wh:
				parts.append(parent_wh)
		if doc.zone:
			parent_zone = frappe.get_value("Store Location", doc.zone, "zone_name")
			if parent_zone:
				parts.append(parent_zone)
		if doc.rack:
			parent_rack = frappe.get_value("Store Location", doc.rack, "rack_name")
			if parent_rack:
				parts.append(parent_rack)
		if doc.shelf_name:
			parts.append(doc.shelf_name)
	
	elif location_type == "Bin":
		if doc.store:
			parent_wh = frappe.get_value("Store Location", doc.store, "warehouse_name")
			if parent_wh:
				parts.append(parent_wh)
		if doc.zone:
			parent_zone = frappe.get_value("Store Location", doc.zone, "zone_name")
			if parent_zone:
				parts.append(parent_zone)
		if doc.rack:
			parent_rack = frappe.get_value("Store Location", doc.rack, "rack_name")
			if parent_rack:
				parts.append(parent_rack)
		if doc.shelf:
			parent_shelf = frappe.get_value("Store Location", doc.shelf, "shelf_name")
			if parent_shelf:
				parts.append(parent_shelf)
		if doc.bin:
			parts.append(doc.bin)
	
	# Set display name
	if parts:
		doc.location_name = " - ".join(parts)
	else:
		doc.location_name = doc.location_code or "New Location"


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_location(doc):
	"""
	Validate location document based on installer settings
	
	Validations:
	- Unique location names (if enforce_unique_names enabled)
	- Hierarchy validation (if enable_hierarchy_validation enabled)
	- Parent existence checks
	- Location type compatibility
	"""
	settings = frappe.get_single("Store Settings")
	
	# Validate unique names
	if settings.get("enforce_unique_names"):
		validate_unique_name(doc)
	
	# Validate hierarchy
	if settings.get("enable_hierarchy_validation"):
		validate_hierarchy(doc)


def validate_unique_name(doc):
	"""
	Ensure location_code is unique across the system
	"""
	if not doc.location_code:
		return
	
	existing = frappe.db.exists("Store Location", {
		"name": doc.location_code,
		"name": ["!=", doc.name]
	})
	
	if existing:
		frappe.throw(f"Location code '{doc.location_code}' already exists. Please use a different code.")


def validate_hierarchy(doc):
	"""
	Validate parent-child relationships in location hierarchy
	
	Rules:
	- Zone must have Warehouse parent
	- Rack must have Zone parent
	- Shelf must have Rack parent
	- Bin must have Shelf parent
	"""
	location_type = doc.location_type
	
	if location_type == "Zone":
		if not doc.store:
			frappe.throw("Zone must have a Warehouse (Store) parent")
		validate_parent_type(doc.store, "Warehouse", "Zone")
	
	elif location_type == "Rack":
		if not doc.zone:
			frappe.throw("Rack must have a Zone parent")
		validate_parent_type(doc.zone, "Zone", "Rack")
	
	elif location_type == "Shelf":
		if not doc.rack:
			frappe.throw("Shelf must have a Rack parent")
		validate_parent_type(doc.rack, "Rack", "Shelf")
	
	elif location_type == "Bin":
		if not doc.shelf:
			frappe.throw("Bin must have a Shelf parent")
		validate_parent_type(doc.shelf, "Shelf", "Bin")


def validate_parent_type(parent_name, expected_type, child_type):
	"""
	Validate that parent location has the correct type
	"""
	if not parent_name:
		return
	
	parent_type = frappe.db.get_value("Store Location", parent_name, "location_type")
	
	if not parent_type:
		frappe.throw(f"Parent location '{parent_name}' does not exist")
	
	if parent_type != expected_type:
		frappe.throw(f"{child_type} must have a {expected_type} parent. '{parent_name}' is a {parent_type}")


# ============================================================================
# SYSTEM STATISTICS
# ============================================================================

def update_system_stats(doc):
	"""
	Update system statistics in Store Settings
	
	Updates:
	- Total locations count
	- First location created date
	- System initialized flag
	- Last sync date
	"""
	try:
		settings = frappe.get_single("Store Settings")
		
		# Update total count
		location_count = frappe.db.count("Store Location")
		settings.total_locations_count = location_count + 1  # +1 for current doc
		
		# Set first location date if not set
		if not settings.first_location_created_date:
			from datetime import datetime
			settings.first_location_created_date = datetime.now()
			settings.system_initialized = 1
		
		# Update last sync
		from datetime import datetime
		settings.last_sync_date = datetime.now()
		
		# Save without triggering validation
		settings.flags.ignore_validate = True
		settings.save()
		frappe.db.commit()
	
	except Exception as e:
		# Don't fail location creation if stats update fails
		frappe.log_error(f"Failed to update system stats: {str(e)}", "Store Location Stats")
