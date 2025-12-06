"""
Store Item DocType Definition
Simple item master for testing
"""

doctype = {
	"doctype": "DocType",
	"name": "Store Item",
	"module": "Technical Store System",
	"custom": 1,
	"is_submittable": 0,
	"is_tree": 0,
	"editable_grid": 1,
	"track_changes": 1,
	"autoname": "field:item_name",
	"title_field": "item_name",
	"fields": [
		{
			"fieldname": "item_name",
			"label": "Item Name",
			"fieldtype": "Data",
			"reqd": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
		},
		{
			"fieldname": "description",
			"label": "Description",
			"fieldtype": "Text",
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
			"role": "Warehouse Staff",
			"read": 1,
			"write": 1,
			"create": 1,
		},
	]
}
