"""
Store Item Batch Number Child Table
Tracks batch numbers for items with batch tracking
"""

doctype = {
	"doctype": "DocType",
	"name": "Store Item Batch Number",
	"module": "Technical Store System",
	"custom": 1,
	"istable": 1,  # Child table
	"editable_grid": 1,
	"fields": [
		{
			"fieldname": "batch_no",
			"label": "Batch Number",
			"fieldtype": "Data",
			"reqd": 1,
			"in_list_view": 1,
		},
		{
			"fieldname": "quantity",
			"label": "Quantity",
			"fieldtype": "Float",
			"reqd": 1,
			"in_list_view": 1,
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "manufacturing_date",
			"label": "Manufacturing Date",
			"fieldtype": "Date",
			"in_list_view": 1,
		},
		{
			"fieldname": "expiry_date",
			"label": "Expiry Date",
			"fieldtype": "Date",
			"in_list_view": 1,
		},
	],
	"permissions": []  # Inherits from parent
}
