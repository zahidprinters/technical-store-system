"""
Store UOM (Unit of Measure) DocType Definition
Foundation master for all quantity measurements

Demo data stored in: setup/demo_data/store_uom.py
Demo data installed via: utils/helpers/demo_data_handler.py
"""

import frappe


def on_doctype_install(force=False):
	"""
	Called automatically after Store UOM DocType is created
	Creates default UOMs if demo data is enabled or force=True
	"""
	try:
		from technical_store_system.utils.helpers.demo_data_handler import install_demo_data_for_doctype
		
		print("    → Installing Store UOM demo data...")
		result = install_demo_data_for_doctype("Store UOM", force=force)
		
		if result["success"]:
			if result["created"] > 0:
				print(f"    ✓ {result['message']}")
			else:
				print(f"    ℹ {result['message']}")
		else:
			print(f"    ℹ {result['message']}")
		
	except Exception as e:
		print(f"    ✗ Error installing Store UOM demo data: {str(e)}")


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
