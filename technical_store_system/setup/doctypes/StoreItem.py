"""
Store Item DocType Definition
Master data for inventory items in Technical Store
"""

doctype = {
	"doctype": "DocType",
	"name": "Store Item",
	"module": "Technical Store System",
	"custom": 1,
	"is_submittable": 0,
	"track_changes": 1,
	"autoname": "format:ITEM-{#####}",
	"title_field": "item_name",
	"fields": [
		# Core Identification Section
		{
			"fieldname": "item_details",
			"label": "Item Details",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Data",
			"reqd": 1,
			"unique": 1,
			"read_only": 1,
			"description": "Auto-generated: ITEM-#####",
		},
		{
			"fieldname": "item_name",
			"label": "Item Name",
			"fieldtype": "Data",
			"reqd": 1,
			"in_list_view": 1,
			"bold": 1,
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "item_group",
			"label": "Item Group",
			"fieldtype": "Link",
			"options": "Store Item Group",
			"reqd": 1,
			"in_list_view": 1,
		},
		{
			"fieldname": "technical_category",
			"label": "Technical Category",
			"fieldtype": "Link",
			"options": "Store Technical Category",
		},
		{
			"fieldname": "description_section",
			"label": "Description",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "description",
			"label": "Description",
			"fieldtype": "Text Editor",
		},
		{
			"fieldname": "column_break_2",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "image",
			"label": "Item Image",
			"fieldtype": "Attach Image",
		},
		
		# UOM Section
		{
			"fieldname": "uom_section",
			"label": "Unit of Measure",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "default_uom",
			"label": "Default UOM",
			"fieldtype": "Link",
			"options": "Store UOM",
			"reqd": 1,
			"in_list_view": 1,
		},
		{
			"fieldname": "allow_alternative_uom",
			"label": "Allow Alternative UOM",
			"fieldtype": "Check",
			"default": 0,
		},
		
		# Stock Control Section
		{
			"fieldname": "stock_control",
			"label": "Stock Control",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "maintain_stock",
			"label": "Maintain Stock",
			"fieldtype": "Check",
			"default": 1,
		},
		{
			"fieldname": "is_stock_item",
			"label": "Is Stock Item",
			"fieldtype": "Check",
			"default": 1,
		},
		{
			"fieldname": "allow_negative_stock",
			"label": "Allow Negative Stock",
			"fieldtype": "Check",
			"default": 0,
		},
		{
			"fieldname": "column_break_3",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "has_serial_no",
			"label": "Has Serial Number",
			"fieldtype": "Check",
			"default": 0,
			"description": "Track individual serial numbers for this item",
		},
		{
			"fieldname": "has_batch_no",
			"label": "Has Batch Number",
			"fieldtype": "Check",
			"default": 0,
			"description": "Track batch numbers for this item",
		},
		{
			"fieldname": "has_expiry_date",
			"label": "Has Expiry Date",
			"fieldtype": "Check",
			"default": 0,
			"description": "Item has expiry date (for batches)",
		},
		{
			"fieldname": "column_break_4",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "shelf_life_days",
			"label": "Shelf Life (Days)",
			"fieldtype": "Int",
			"depends_on": "eval:doc.has_expiry_date==1",
		},
		{
			"fieldname": "valuation_method",
			"label": "Valuation Method",
			"fieldtype": "Select",
			"options": "FIFO\nLIFO\nMoving Average",
			"default": "FIFO",
		},
		
		# Serial Numbers Section
		{
			"fieldname": "serial_numbers_section",
			"label": "Serial Numbers",
			"fieldtype": "Section Break",
			"depends_on": "eval:doc.has_serial_no==1",
			"collapsible": 1,
		},
		{
			"fieldname": "serial_numbers",
			"label": "Serial Numbers",
			"fieldtype": "Table",
			"options": "Store Item Serial Number",
		},
		
		# Batch Numbers Section
		{
			"fieldname": "batch_numbers_section",
			"label": "Batch Numbers",
			"fieldtype": "Section Break",
			"depends_on": "eval:doc.has_batch_no==1",
			"collapsible": 1,
		},
		{
			"fieldname": "batch_numbers",
			"label": "Batch Numbers",
			"fieldtype": "Table",
			"options": "Store Item Batch Number",
		},
		
		# Opening Stock Section
		{
			"fieldname": "opening_stock_section",
			"label": "Opening Stock",
			"fieldtype": "Section Break",
			"collapsible": 1,
		},
		{
			"fieldname": "opening_stock",
			"label": "Opening Stock Quantity",
			"fieldtype": "Float",
			"default": 0,
		},
		{
			"fieldname": "column_break_5",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "opening_valuation_rate",
			"label": "Opening Valuation Rate",
			"fieldtype": "Currency",
			"default": 0,
		},
		
		# Default Location Section
		{
			"fieldname": "location_section",
			"label": "Default Storage Location",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "default_location",
			"label": "Default Location",
			"fieldtype": "Link",
			"options": "Store Location",
			"description": "Default storage location (physical location details are in Store Location)",
		},
		
		# Reorder Management Section
		{
			"fieldname": "reorder_section",
			"label": "Reorder Management",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "minimum_level",
			"label": "Minimum Level",
			"fieldtype": "Float",
			"description": "Alert when stock falls below this level",
		},
		{
			"fieldname": "reorder_level",
			"label": "Reorder Level",
			"fieldtype": "Float",
			"description": "Trigger reorder at this level",
		},
		{
			"fieldname": "column_break_8",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "reorder_qty",
			"label": "Reorder Quantity",
			"fieldtype": "Float",
			"description": "Standard quantity to reorder",
		},
		{
			"fieldname": "maximum_level",
			"label": "Maximum Level",
			"fieldtype": "Float",
			"description": "Maximum stock allowed",
		},
		
		# Pricing Section
		{
			"fieldname": "pricing_section",
			"label": "Pricing",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "standard_rate",
			"label": "Standard Rate",
			"fieldtype": "Currency",
			"description": "Standard valuation rate",
		},
		{
			"fieldname": "column_break_9",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "last_purchase_rate",
			"label": "Last Purchase Rate",
			"fieldtype": "Currency",
			"read_only": 1,
		},
		
		# Technical Specifications Section
		{
			"fieldname": "specifications_section",
			"label": "Technical Specifications",
			"fieldtype": "Section Break",
			"collapsible": 1,
		},
		{
			"fieldname": "technical_specs",
			"label": "Technical Specifications",
			"fieldtype": "Text Editor",
		},
		{
			"fieldname": "column_break_10",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "specifications_json",
			"label": "Specifications (JSON)",
			"fieldtype": "JSON",
			"description": "Structured specifications data",
		},
		
		# Identification Section
		{
			"fieldname": "identification_section",
			"label": "Barcodes & Identification",
			"fieldtype": "Section Break",
			"collapsible": 1,
		},
		{
			"fieldname": "barcode",
			"label": "Barcode",
			"fieldtype": "Data",
			"unique": 1,
		},
		{
			"fieldname": "column_break_11",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "qr_code",
			"label": "QR Code",
			"fieldtype": "Data",
			"unique": 1,
		},
		
		# Item Type Flags Section
		{
			"fieldname": "item_type_section",
			"label": "Item Type",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "is_purchase_item",
			"label": "Is Purchase Item",
			"fieldtype": "Check",
			"default": 1,
			"description": "Can be purchased from suppliers",
		},
		{
			"fieldname": "is_returnable",
			"label": "Is Returnable",
			"fieldtype": "Check",
			"default": 1,
			"description": "Can be returned to purchase department",
		},
		{
			"fieldname": "column_break_12",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "is_restricted",
			"label": "Is Restricted",
			"fieldtype": "Check",
			"default": 0,
			"description": "Requires special authorization to issue",
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
			"delete": 1,
		},
		{
			"role": "Warehouse Staff",
			"read": 1,
			"write": 1,
			"create": 1,
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
