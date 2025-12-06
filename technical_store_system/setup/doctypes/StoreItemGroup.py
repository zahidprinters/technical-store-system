"""
Store Item Group DocType Definition
Hierarchical category/classification for items (tree structure)

Example: Electronics → Computers → Laptops
         Tools → Hand Tools → Screwdrivers
"""

import frappe


def on_doctype_install(force=False):
	"""
	Called automatically after Store Item Group DocType is created
	Creates default item groups if demo data is enabled or force=True
	"""
	try:
		# Skip check if force=True (called from button)
		if not force:
			install_demo = frappe.db.get_single_value("Store Settings", "install_demo_data")
			if not install_demo:
				print("    ℹ Demo data disabled - skipping default item groups")
				return
		
		print("    → Creating default item groups...")
		default_groups = get_default_item_groups()
		created_count = 0
		
		for group_data in default_groups:
			if not frappe.db.exists("Store Item Group", group_data["item_group_name"]):
				doc = frappe.new_doc("Store Item Group")
				for key, value in group_data.items():
					doc.set(key, value)
				doc.insert(ignore_permissions=True)
				created_count += 1
		
		if created_count > 0:
			print(f"    ✓ Created {created_count} demo item groups")
		else:
			print(f"    ℹ All demo item groups already exist")
		
		frappe.db.commit()
		
	except Exception as e:
			print(f"    ✗ Error creating default item groups: {str(e)}")


def get_default_item_groups():
	"""Returns list of default item groups (hierarchical)"""
	return [
		# Root groups
		{"item_group_name": "All Item Groups", "parent_item_group": "", "is_group": 1, "description": "Root group for all items"},
		
		# Main categories
		{"item_group_name": "Electronics", "parent_item_group": "All Item Groups", "is_group": 1, "description": "Electronic items and components"},
		{"item_group_name": "Tools", "parent_item_group": "All Item Groups", "is_group": 1, "description": "Hand tools and power tools"},
		{"item_group_name": "Consumables", "parent_item_group": "All Item Groups", "is_group": 1, "description": "Consumable items and supplies"},
		{"item_group_name": "Spare Parts", "parent_item_group": "All Item Groups", "is_group": 1, "description": "Replacement parts and spares"},
		{"item_group_name": "Safety Equipment", "parent_item_group": "All Item Groups", "is_group": 1, "description": "Safety gear and equipment"},
		{"item_group_name": "Office Supplies", "parent_item_group": "All Item Groups", "is_group": 1, "description": "Office and stationery items"},
		{"item_group_name": "Raw Materials", "parent_item_group": "All Item Groups", "is_group": 1, "description": "Raw materials for production"},
		
		# Electronics sub-groups
		{"item_group_name": "Computers", "parent_item_group": "Electronics", "is_group": 1, "description": "Computer hardware"},
		{"item_group_name": "Components", "parent_item_group": "Electronics", "is_group": 1, "description": "Electronic components"},
		{"item_group_name": "Cables & Connectors", "parent_item_group": "Electronics", "is_group": 0, "description": "Cables, wires, connectors"},
		
		# Tools sub-groups
		{"item_group_name": "Hand Tools", "parent_item_group": "Tools", "is_group": 1, "description": "Manual hand tools"},
		{"item_group_name": "Power Tools", "parent_item_group": "Tools", "is_group": 0, "description": "Electric and pneumatic tools"},
		{"item_group_name": "Measuring Tools", "parent_item_group": "Tools", "is_group": 0, "description": "Measurement instruments"},
		
		# Consumables sub-groups
		{"item_group_name": "Chemicals", "parent_item_group": "Consumables", "is_group": 0, "description": "Chemical supplies"},
		{"item_group_name": "Lubricants", "parent_item_group": "Consumables", "is_group": 0, "description": "Oils and lubricants"},
		{"item_group_name": "Cleaning Supplies", "parent_item_group": "Consumables", "is_group": 0, "description": "Cleaning materials"},
		
		# Safety Equipment sub-groups
		{"item_group_name": "Personal Protective Equipment", "parent_item_group": "Safety Equipment", "is_group": 1, "description": "PPE items"},
		{"item_group_name": "Fire Safety", "parent_item_group": "Safety Equipment", "is_group": 0, "description": "Fire extinguishers, alarms"},
	]


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
