"""
Store Item Group DocType Definition
Hierarchical category/classification for items (tree structure)

Example: Electronics → Computers → Laptops
         Tools → Hand Tools → Screwdrivers

Demo data stored in: setup/demo_data/store_item_group.py
Demo data installed via: utils/helpers/demo_data_handler.py
"""

import frappe


def on_doctype_install(force=False):
	"""
	Called automatically after Store Item Group DocType is created
	Creates default item groups if demo data is enabled or force=True
	"""
	try:
		from technical_store_system.utils.helpers.demo_data_handler import install_demo_data_for_doctype
		
		print("    → Installing Store Item Group demo data...")
		result = install_demo_data_for_doctype("Store Item Group", force=force)
		
		if result["success"]:
			if result["created"] > 0:
				print(f"    ✓ {result['message']}")
			else:
				print(f"    ℹ {result['message']}")
		else:
			print(f"    ℹ {result['message']}")
		
	except Exception as e:
		print(f"    ✗ Error installing Store Item Group demo data: {str(e)}")


doctype = {
	"name": "Store Item Group",
	"module": "Technical Store System",
	"custom": 1,
	"issingle": 0,
	"is_submittable": 0,
	"is_tree": 1,  # Enable tree/nested structure
	"editable_grid": 1,
	"track_changes": 1,
	"autoname": "field:item_group_name",
	"title_field": "item_group_name",
	"nsm_parent_field": "parent_item_group",  # Tree parent field
	
	"fields": [
		# Section: Basic Information
		{
			"fieldname": "item_group_name",
			"label": "Item Group Name",
			"fieldtype": "Data",
			"reqd": 1,
			"unique": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
			"bold": 1,
			"description": "Name of the item category/group"
		},
		{
			"fieldname": "parent_item_group",
			"label": "Parent Item Group",
			"fieldtype": "Link",
			"options": "Store Item Group",
			"in_list_view": 1,
			"in_standard_filter": 1,
			"description": "Parent category (leave blank for root)"
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "is_group",
			"label": "Is Group",
			"fieldtype": "Check",
			"default": 0,
			"in_list_view": 1,
			"description": "Check if this is a group (can have sub-groups)"
		},
		{
			"fieldname": "enabled",
			"label": "Enabled",
			"fieldtype": "Check",
			"default": 1,
			"in_standard_filter": 1
		},
		
		# Section: Details
		{
			"fieldname": "section_details",
			"fieldtype": "Section Break",
			"label": "Details"
		},
		{
			"fieldname": "description",
			"label": "Description",
			"fieldtype": "Text Editor",
			"description": "Detailed description of the item group"
		},
		{
			"fieldname": "column_break_2",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "image",
			"label": "Group Image",
			"fieldtype": "Attach Image",
			"description": "Representative image for this group"
		},
		
		# Section: Configuration
		{
			"fieldname": "section_config",
			"fieldtype": "Section Break",
			"label": "Configuration",
			"collapsible": 1
		},
		{
			"fieldname": "default_uom",
			"label": "Default UOM",
			"fieldtype": "Link",
			"options": "Store UOM",
			"description": "Default unit of measure for items in this group"
		},
		{
			"fieldname": "has_serial_no",
			"label": "Has Serial No",
			"fieldtype": "Check",
			"default": 0,
			"description": "Items in this group have serial numbers by default"
		},
		{
			"fieldname": "column_break_3",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "has_batch_no",
			"label": "Has Batch No",
			"fieldtype": "Check",
			"default": 0,
			"description": "Items in this group have batch numbers by default"
		},
		{
			"fieldname": "allow_negative_stock",
			"label": "Allow Negative Stock",
			"fieldtype": "Check",
			"default": 0,
			"description": "Allow negative stock for items in this group"
		},
		
		# Section: Statistics (read-only)
		{
			"fieldname": "section_stats",
			"fieldtype": "Section Break",
			"label": "Statistics",
			"collapsible": 1
		},
		{
			"fieldname": "item_count",
			"label": "Total Items",
			"fieldtype": "Int",
			"read_only": 1,
			"default": 0,
			"description": "Number of items in this group"
		},
		{
			"fieldname": "column_break_4",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "last_updated",
			"label": "Last Updated",
			"fieldtype": "Datetime",
			"read_only": 1,
			"description": "Last time statistics were updated"
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
