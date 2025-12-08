"""
Store Technical Category DocType Definition
Classification of items by technical category (Electrical, Mechanical, etc.)
"""

doctype = {
	"doctype": "DocType",
	"name": "Store Technical Category",
	"module": "Technical Store System",
	"custom": 1,
	"is_submittable": 0,
	"track_changes": 1,
	"autoname": "field:category_name",
	"fields": [
		{
			"fieldname": "category_name",
			"label": "Category Name",
			"fieldtype": "Data",
			"reqd": 1,
			"unique": 1,
			"in_list_view": 1,
		},
		{
			"fieldname": "description",
			"label": "Description",
			"fieldtype": "Text",
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "enabled",
			"label": "Enabled",
			"fieldtype": "Check",
			"default": 1,
		},
	],
	"permissions": [
		{
			"role": "Store Manager",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
		},
		{
			"role": "Inventory Admin",
			"read": 1,
			"write": 1,
			"create": 1,
		},
		{
			"role": "Warehouse Staff",
			"read": 1,
		},
		{
			"role": "Store Viewer",
			"read": 1,
		},
		{
			"role": "System Manager",
			"read": 1,
			"write": 1,
			"create": 1,
			"delete": 1,
		},
	]
}


def on_doctype_install():
	"""Create default technical categories"""
	import frappe
	
	categories = [
		{"category_name": "Electrical", "description": "Electrical components, cables, and equipment"},
		{"category_name": "Mechanical", "description": "Mechanical parts, tools, and equipment"},
		{"category_name": "Electronic", "description": "Electronic components and devices"},
		{"category_name": "Consumable", "description": "Consumable items and supplies"},
		{"category_name": "Chemical", "description": "Chemicals and hazardous materials"},
		{"category_name": "Hardware", "description": "Hardware items, fasteners, fittings"},
		{"category_name": "Tool", "description": "Tools and equipment"},
		{"category_name": "Safety", "description": "Safety equipment and PPE"},
		{"category_name": "Office", "description": "Office supplies and stationery"},
		{"category_name": "IT", "description": "IT equipment and accessories"},
		{"category_name": "Spare Part", "description": "Spare parts and replacements"},
		{"category_name": "Raw Material", "description": "Raw materials for production"},
	]
	
	created = 0
	for cat in categories:
		if not frappe.db.exists("Store Technical Category", cat["category_name"]):
			doc = frappe.get_doc({
				"doctype": "Store Technical Category",
				"category_name": cat["category_name"],
				"description": cat["description"],
				"enabled": 1
			})
			doc.insert(ignore_permissions=True)
			created += 1
	
	if created > 0:
		frappe.db.commit()
	
	return created
