"""
Store Settings DocType Definition
Single DocType for app configuration and settings
"""

doctype = {
	"doctype": "DocType",
	"name": "Store Settings",
	"module": "Technical Store System",
	"custom": 1,
	"is_submittable": 0,
	"is_single": 1,
	"issingle": 1,
	"editable_grid": 0,
	"track_changes": 1,
	"fields": [
		# General Settings Section
		{
			"fieldname": "general_settings",
			"label": "General Settings",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "company_name",
			"label": "Company Name",
			"fieldtype": "Data",
			"description": "Your company/store name",
		},
		{
			"fieldname": "default_currency",
			"label": "Default Currency",
			"fieldtype": "Link",
			"options": "Currency",
			"default": "USD",
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "allow_negative_stock",
			"label": "Allow Negative Stock",
			"fieldtype": "Check",
			"default": 0,
			"description": "Allow stock to go below zero",
		},
		{
			"fieldname": "auto_create_serial_no",
			"label": "Auto Create Serial Numbers",
			"fieldtype": "Check",
			"default": 0,
		},
		
		# Stock Settings Section
		{
			"fieldname": "stock_settings",
			"label": "Stock Management",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "enable_batch_tracking",
			"label": "Enable Batch Tracking",
			"fieldtype": "Check",
			"default": 0,
			"description": "Track items by batch numbers",
		},
		{
			"fieldname": "enable_serial_tracking",
			"label": "Enable Serial Number Tracking",
			"fieldtype": "Check",
			"default": 0,
			"description": "Track items by serial numbers",
		},
		{
			"fieldname": "column_break_2",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "stock_validation",
			"label": "Stock Validation on Entry",
			"fieldtype": "Check",
			"default": 1,
			"description": "Validate stock before creating entries",
		},
		{
			"fieldname": "auto_stock_reorder",
			"label": "Auto Stock Reorder Alert",
			"fieldtype": "Check",
			"default": 1,
			"description": "Send alerts when stock reaches reorder level",
		},
		
		# Pricing Settings
		{
			"fieldname": "pricing_settings",
			"label": "Pricing & Tax",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "default_price_list",
			"label": "Default Price List",
			"fieldtype": "Data",
			"description": "Default price list for items",
		},
		{
			"fieldname": "include_tax_in_price",
			"label": "Include Tax in Item Price",
			"fieldtype": "Check",
			"default": 0,
		},
		{
			"fieldname": "column_break_3",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "default_tax_rate",
			"label": "Default Tax Rate (%)",
			"fieldtype": "Float",
			"default": 0,
			"description": "Default tax percentage",
		},
		{
			"fieldname": "round_off_amount",
			"label": "Round Off Amount",
			"fieldtype": "Check",
			"default": 1,
		},
		
		# ERPNext Integration
		{
			"fieldname": "erpnext_integration",
			"label": "ERPNext Integration (Optional)",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "enable_erpnext_sync",
			"label": "Enable ERPNext Sync",
			"fieldtype": "Check",
			"default": 0,
			"description": "Sync with ERPNext if installed",
		},
		{
			"fieldname": "auto_sync_items",
			"label": "Auto Sync Items",
			"fieldtype": "Check",
			"default": 0,
			"depends_on": "eval:doc.enable_erpnext_sync==1",
		},
		{
			"fieldname": "column_break_4",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "sync_frequency",
			"label": "Sync Frequency",
			"fieldtype": "Select",
			"options": "Hourly\nDaily\nWeekly\nManual",
			"default": "Manual",
			"depends_on": "eval:doc.enable_erpnext_sync==1",
		},
		{
			"fieldname": "last_sync_time",
			"label": "Last Sync Time",
			"fieldtype": "Datetime",
			"read_only": 1,
			"depends_on": "eval:doc.enable_erpnext_sync==1",
		},
		
		# Notifications
		{
			"fieldname": "notification_settings",
			"label": "Notifications",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "enable_email_notifications",
			"label": "Enable Email Notifications",
			"fieldtype": "Check",
			"default": 0,
		},
		{
			"fieldname": "notification_email",
			"label": "Notification Email",
			"fieldtype": "Data",
			"depends_on": "eval:doc.enable_email_notifications==1",
		},
		{
			"fieldname": "column_break_5",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "low_stock_alert",
			"label": "Low Stock Alert",
			"fieldtype": "Check",
			"default": 1,
		},
		{
			"fieldname": "stock_expiry_alert",
			"label": "Stock Expiry Alert",
			"fieldtype": "Check",
			"default": 1,
		},
		
		# Demo/Test Data Management
		{
			"fieldname": "demo_data_section",
			"label": "Demo/Test Data Management",
			"fieldtype": "Section Break",
			"collapsible": 1,
		},
		{
			"fieldname": "demo_data_info",
			"label": "",
			"fieldtype": "HTML",
			"options": '<p style="color: #666;">Install sample data for testing and training purposes. Select which data types to install below.</p>',
		},
		{
			"fieldname": "install_demo_uoms",
			"label": "UOMs (Units of Measure)",
			"fieldtype": "Check",
			"default": 1,
			"description": "27 units: Each, Kg, Liter, Meter, Box, etc.",
		},
		{
			"fieldname": "install_demo_item_groups",
			"label": "Item Groups (Categories)",
			"fieldtype": "Check",
			"default": 1,
			"description": "19 categories: Electronics, Tools, Consumables, etc.",
		},
		{
			"fieldname": "column_break_demo",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "install_demo_locations",
			"label": "Locations (Warehouse Structure)",
			"fieldtype": "Check",
			"default": 1,
			"description": "11 locations: Warehouses, Areas, Racks, Shelves, etc.",
		},
		{
			"fieldname": "install_demo_items",
			"label": "Items (Products)",
			"fieldtype": "Check",
			"default": 0,
			"description": "Sample items (future feature)",
		},
		{
			"fieldname": "column_break_demo",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "install_demo_data_btn",
			"label": "Install Selected Demo Data",
			"fieldtype": "Button",
			"description": "Create selected demo data types",
		},
		{
			"fieldname": "uninstall_demo_data_btn",
			"label": "Remove All Demo Data",
			"fieldtype": "Button",
			"description": "Delete all demo/test data (only works if no transactions exist)",
		},
		{
			"fieldname": "demo_data_status",
			"label": "Demo Data Status",
			"fieldtype": "HTML",
			"read_only": 1,
		},
		
		# Advanced Settings
		{
			"fieldname": "advanced_settings",
			"label": "Advanced Settings",
			"fieldtype": "Section Break",
			"collapsible": 1,
		},
		{
			"fieldname": "enable_audit_trail",
			"label": "Enable Audit Trail",
			"fieldtype": "Check",
			"default": 1,
			"description": "Track all changes in system",
		},
		{
			"fieldname": "enable_barcode_scanning",
			"label": "Enable Barcode Scanning",
			"fieldtype": "Check",
			"default": 0,
		},
		{
			"fieldname": "column_break_6",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "enable_mobile_app",
			"label": "Enable Mobile App Access",
			"fieldtype": "Check",
			"default": 0,
		},
		{
			"fieldname": "enable_api_access",
			"label": "Enable API Access",
			"fieldtype": "Check",
			"default": 0,
		},
	],
	"permissions": [
		{
			"role": "Store Manager",
			"read": 1,
			"write": 1,
			"create": 1,
		},
		{
			"role": "System Manager",
			"read": 1,
			"write": 1,
			"create": 1,
		},
	]
}
