"""
Store Item Serial Number Child Table
Tracks serial numbers for items with serial tracking
"""

doctype = {
	"doctype": "DocType",
	"name": "Store Item Serial Number",
	"module": "Technical Store System",
	"custom": 1,
	"istable": 1,  # Child table
	"editable_grid": 1,
	"fields": [
		{
			"fieldname": "serial_no",
			"label": "Serial Number",
			"fieldtype": "Data",
			"reqd": 1,
			"in_list_view": 1,
			"unique": 1,
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Select",
			"options": "Available\nIssued\nIn Transit\nDamaged\nReturned",
			"default": "Available",
			"in_list_view": 1,
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "purchase_date",
			"label": "Purchase Date",
			"fieldtype": "Date",
		},
		{
			"fieldname": "warranty_expiry",
			"label": "Warranty Expiry",
			"fieldtype": "Date",
		},
	],
	"permissions": []  # Inherits from parent
}
