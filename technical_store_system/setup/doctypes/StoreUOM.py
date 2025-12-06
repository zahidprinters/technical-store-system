"""
Store UOM (Unit of Measure) DocType Definition
Foundation master for all quantity measurements

After this DocType is created, default UOMs are auto-installed via on_doctype_install hook
"""

import frappe


def on_doctype_install(force=False):
	"""
	Called automatically after Store UOM DocType is created
	Creates default UOMs if demo data is enabled or force=True
	"""
	try:
		# Skip check if force=True (called from button)
		if not force:
			install_demo = frappe.db.get_single_value("Store Settings", "install_demo_data")
			if not install_demo:
				print("    ℹ Demo data disabled - skipping default UOMs")
				return
		
		print("    → Creating default UOMs...")
		default_uoms = get_default_uoms()
		created_count = 0
		
		for uom_data in default_uoms:
			if not frappe.db.exists("Store UOM", uom_data["uom_name"]):
				doc = frappe.new_doc("Store UOM")
				for key, value in uom_data.items():
					doc.set(key, value)
				doc.insert(ignore_permissions=True)
				created_count += 1
		
		if created_count > 0:
			print(f"    ✓ Created {created_count} demo UOMs")
		else:
			print(f"    ℹ All demo UOMs already exist")
		
		frappe.db.commit()
		
	except Exception as e:
		print(f"    ✗ Error creating default UOMs: {str(e)}")


def get_default_uoms():
	"""Returns list of default UOMs to create"""
	return [
		# Quantity-based (whole numbers)
		{"uom_name": "Each", "uom_symbol": "Ea", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "is_default": 1, "description": "Individual items, pieces, units"},
		{"uom_name": "Nos", "uom_symbol": "Nos", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Numbers (same as Each)"},
		{"uom_name": "Piece", "uom_symbol": "Pc", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Individual pieces"},
		{"uom_name": "Pair", "uom_symbol": "Pr", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Pair of items (2 pieces)"},
		{"uom_name": "Set", "uom_symbol": "Set", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Set of items"},
		{"uom_name": "Dozen", "uom_symbol": "Dz", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "12 pieces"},
		{"uom_name": "Box", "uom_symbol": "Box", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Boxed items"},
		{"uom_name": "Pack", "uom_symbol": "Pk", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Package of items"},
		{"uom_name": "Bundle", "uom_symbol": "Bdl", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Bundle of items"},
		{"uom_name": "Carton", "uom_symbol": "Ctn", "uom_type": "Quantity", "must_be_whole_number": 1, "enabled": 1, "description": "Carton box"},
		# Weight
		{"uom_name": "Kilogram", "uom_symbol": "Kg", "uom_type": "Weight", "must_be_whole_number": 0, "enabled": 1, "description": "Weight in kilograms"},
		{"uom_name": "Gram", "uom_symbol": "g", "uom_type": "Weight", "must_be_whole_number": 0, "enabled": 1, "description": "Weight in grams"},
		{"uom_name": "Ton", "uom_symbol": "t", "uom_type": "Weight", "must_be_whole_number": 0, "enabled": 1, "description": "Weight in metric tons"},
		# Volume
		{"uom_name": "Liter", "uom_symbol": "L", "uom_type": "Volume", "must_be_whole_number": 0, "enabled": 1, "description": "Volume in liters"},
		{"uom_name": "Milliliter", "uom_symbol": "mL", "uom_type": "Volume", "must_be_whole_number": 0, "enabled": 1, "description": "Volume in milliliters"},
		{"uom_name": "Cubic Meter", "uom_symbol": "m³", "uom_type": "Volume", "must_be_whole_number": 0, "enabled": 1, "description": "Volume in cubic meters"},
		# Length
		{"uom_name": "Meter", "uom_symbol": "m", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in meters"},
		{"uom_name": "Centimeter", "uom_symbol": "cm", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in centimeters"},
		{"uom_name": "Millimeter", "uom_symbol": "mm", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in millimeters"},
		{"uom_name": "Kilometer", "uom_symbol": "km", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in kilometers"},
		{"uom_name": "Inch", "uom_symbol": "in", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in inches"},
		{"uom_name": "Foot", "uom_symbol": "ft", "uom_type": "Length", "must_be_whole_number": 0, "enabled": 1, "description": "Length in feet"},
		# Area
		{"uom_name": "Square Meter", "uom_symbol": "m²", "uom_type": "Area", "must_be_whole_number": 0, "enabled": 1, "description": "Area in square meters"},
		{"uom_name": "Square Foot", "uom_symbol": "ft²", "uom_type": "Area", "must_be_whole_number": 0, "enabled": 1, "description": "Area in square feet"},
		# Special
		{"uom_name": "Roll", "uom_symbol": "Roll", "uom_type": "Other", "must_be_whole_number": 1, "enabled": 1, "description": "Roll (cables, wires, fabrics)"},
		{"uom_name": "Sheet", "uom_symbol": "Sht", "uom_type": "Other", "must_be_whole_number": 1, "enabled": 1, "description": "Sheet (paper, metal sheets)"},
		{"uom_name": "Hour", "uom_symbol": "Hr", "uom_type": "Time", "must_be_whole_number": 0, "enabled": 1, "description": "Time in hours (services)"},
	]


doctype = {
	"name": "Store UOM",
	"module": "Technical Store System",
	"custom": 1,
	"issingle": 0,
	"is_submittable": 0,
	"is_tree": 0,
	"editable_grid": 1,
	"track_changes": 1,
	"autoname": "field:uom_name",
	"title_field": "uom_name",
	
	"fields": [
		# Section: Basic Information
		{
			"fieldname": "uom_name",
			"label": "UOM Name",
			"fieldtype": "Data",
			"reqd": 1,
			"unique": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
			"bold": 1,
			"description": "Unit of Measure name (e.g., Each, Kg, Liter)"
		},
		{
			"fieldname": "uom_symbol",
			"label": "Symbol",
			"fieldtype": "Data",
			"in_list_view": 1,
			"description": "Short symbol (e.g., Ea, kg, L)"
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "enabled",
			"label": "Enabled",
			"fieldtype": "Check",
			"default": 1,
			"in_list_view": 1,
			"in_standard_filter": 1
		},
		{
			"fieldname": "is_default",
			"label": "Is Default UOM",
			"fieldtype": "Check",
			"default": 0,
			"description": "Set as default UOM for new items"
		},
		
		# Section: Classification
		{
			"fieldname": "section_classification",
			"fieldtype": "Section Break",
			"label": "Classification"
		},
		{
			"fieldname": "uom_type",
			"label": "UOM Type",
			"fieldtype": "Select",
			"options": "\nQuantity\nWeight\nVolume\nLength\nArea\nTime\nOther",
			"default": "Quantity",
			"in_list_view": 1,
			"in_standard_filter": 1
		},
		{
			"fieldname": "must_be_whole_number",
			"label": "Must Be Whole Number",
			"fieldtype": "Check",
			"default": 1,
			"description": "Quantities must be integers (e.g., Each, Box)"
		},
		
		# Section: Conversion
		{
			"fieldname": "section_conversion",
			"fieldtype": "Section Break",
			"label": "Conversion Details",
			"collapsible": 1
		},
		{
			"fieldname": "has_conversion",
			"label": "Has Conversion",
			"fieldtype": "Check",
			"default": 0,
			"description": "Can convert to other UOMs (future enhancement)"
		},
		{
			"fieldname": "base_uom",
			"label": "Base UOM",
			"fieldtype": "Link",
			"options": "Store UOM",
			"depends_on": "eval:doc.has_conversion==1",
			"description": "Reference UOM for conversion"
		},
		{
			"fieldname": "column_break_2",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "conversion_factor",
			"label": "Conversion Factor",
			"fieldtype": "Float",
			"depends_on": "eval:doc.has_conversion==1",
			"precision": 6,
			"description": "1 [This UOM] = X [Base UOM]"
		},
		
		# Section: Additional Information
		{
			"fieldname": "section_additional",
			"fieldtype": "Section Break",
			"label": "Additional Information",
			"collapsible": 1
		},
		{
			"fieldname": "description",
			"label": "Description",
			"fieldtype": "Text Editor",
			"description": "Detailed description and usage notes"
		}
	],
	
	"permissions": [
		{
			"role": "Store Manager",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"select": 1,
			"report": 1,
			"export": 1
		},
		{
			"role": "Inventory Admin",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
			"select": 1,
			"report": 1,
			"export": 1
		},
		{
			"role": "Warehouse Staff",
			"read": 1,
			"select": 1,
			"report": 1
		},
		{
			"role": "Store Viewer",
			"read": 1,
			"select": 1,
			"report": 1
		}
	]
}
