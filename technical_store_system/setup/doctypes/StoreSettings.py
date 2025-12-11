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
		# Tab 1: General Settings
		{
			"fieldname": "general_tab",
			"label": "General Settings",
			"fieldtype": "Tab Break",
			"idx": 1,
		},
		{
			"fieldname": "general_settings",
			"label": "General Settings",
			"fieldtype": "Section Break",
			"idx": 2,
		},
		{
			"fieldname": "company_name",
			"label": "Company Name",
			"fieldtype": "Data",
			"description": "Company/store name."
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "default_currency",
			"label": "Default Currency",
			"fieldtype": "Link",
			"options": "Currency",
			"default": "USD",
			"description": "Currency for pricing and transactions."
		},
		
		# Tab 2: Stock Management
		{
			"fieldname": "stock_tab",
			"label": "Stock Management",
			"fieldtype": "Tab Break",
		},
		{
			"fieldname": "stock_settings",
			"label": "Stock Settings",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "allow_negative_stock",
			"label": "Allow Negative Stock",
			"fieldtype": "Check",
			"default": 0,
			"description": "Allow issuing items even when stock is zero (for backorders)."
		},
		{
			"fieldname": "stock_validation",
			"label": "Validate Stock Before Issue",
			"fieldtype": "Check",
			"default": 1,
			"description": "Check available quantity before allowing issue.",
			"depends_on": "eval:doc.allow_negative_stock==0",
		},
		{
			"fieldname": "auto_stock_reorder",
			"label": "Low Stock Alerts",
			"fieldtype": "Check",
			"default": 1,
			"description": "Send alerts when stock reaches minimum level."
		},
		{
			"fieldname": "column_break_2",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "enable_batch_tracking",
			"label": "Enable Batch Tracking",
			"fieldtype": "Check",
			"default": 0,
			"description": "Track items by batch numbers (manufacturing date, expiry, etc.)",
		},
		{
			"fieldname": "enable_serial_tracking",
			"label": "Enable Serial Number Tracking",
			"fieldtype": "Check",
			"default": 0,
			"description": "Track items by unique serial numbers (warranty, maintenance, etc.)",
		},
		{
			"fieldname": "auto_create_serial_no",
			"label": "Auto-Generate Serial Numbers",
			"fieldtype": "Check",
			"default": 0,
			"description": "Automatically create serial numbers (SN001, SN002, etc.)",
			"depends_on": "eval:doc.enable_serial_tracking==1",
		},
		
		# Tab 3: Integration
		{
			"fieldname": "integration_tab",
			"label": "Integration",
			"fieldtype": "Tab Break",
		},
		
		# Tab 4: Pricing & Tax
		{
			"fieldname": "pricing_tab",
			"label": "Pricing & Tax",
			"fieldtype": "Tab Break",
		},
		{
			"fieldname": "pricing_settings",
			"label": "Pricing Settings",
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
		
		
		# Tab 5: Notifications
		{
			"fieldname": "notifications_tab",
			"label": "Notifications",
			"fieldtype": "Tab Break",
		},
		{
			"fieldname": "notification_settings",
			"label": "Notification Settings",
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
		
		# Tab 6: Demo Data
		{
			"fieldname": "demo_data_tab",
			"label": "Demo Data",
			"fieldtype": "Tab Break",
		},
		{
			"fieldname": "demo_data_section",
			"label": "Demo/Test Data Management",
			"fieldtype": "Section Break",
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
			"label": "Items (Store Items)",
			"fieldtype": "Check",
			"default": 1,
			"description": "16 sample items: Tools, Safety, Electrical, Mechanical, etc.",
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
		
		# Tab 7: Advanced
		{
			"fieldname": "advanced_tab",
			"label": "Advanced",
			"fieldtype": "Tab Break",
		},
		{
			"fieldname": "advanced_settings",
			"label": "Advanced Settings",
			"fieldtype": "Section Break",
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
		
		# Tab: Installer Settings (Admin Only)
		{
			"fieldname": "installer_tab",
			"label": "Installer Settings",
			"fieldtype": "Tab Break",
			"description": "Administrator-only configuration for system setup and behavior",
		},
		{
			"fieldname": "installer_settings_section",
			"label": "System Configuration",
			"fieldtype": "Section Break",
			"collapsible": 0,
			"description": "⚠️ Administrator Only - These settings affect core system behavior",
		},
		{
			"fieldname": "installer_column_1",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "enable_auto_location_code",
			"label": "Enable Auto Location Code",
			"fieldtype": "Check",
			"default": 1,
			"description": "✅ ENABLED (Recommended): System automatically generates location codes (WH-1, WH-1-Z-A, etc.) based on patterns below. Users only select location type and parent.\n❌ DISABLED: Users must manually enter location codes (increases error risk and duplicates).",
		},
		{
			"fieldname": "allow_manual_override",
			"label": "Allow Manual Override",
			"fieldtype": "Check",
			"default": 0,
			"description": "⚠️ NOT RECOMMENDED: Allow users to manually type location codes even when auto-generation is enabled. This can lead to inconsistent naming and duplicates. Keep disabled unless you have a specific need.",
		},
		{
			"fieldname": "enforce_unique_names",
			"label": "Enforce Unique Names",
			"fieldtype": "Check",
			"default": 1,
			"description": "✅ ENABLED (Recommended): Prevents creating two locations with the same code (e.g., two WH-1). Ensures data integrity and prevents confusion.\n❌ DISABLED: Allows duplicate location codes (not recommended).",
		},
		{
			"fieldname": "installer_column_2",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "enable_hierarchy_validation",
			"label": "Enable Hierarchy Validation",
			"fieldtype": "Check",
			"default": 1,
			"description": "✅ ENABLED (Recommended): Enforces correct hierarchy rules (Zone must have Warehouse parent, Rack must have Zone parent, etc.). Prevents invalid location structures.\n❌ DISABLED: Allows any hierarchy (can create orphaned or incorrectly structured locations).",
		},
		{
			"fieldname": "auto_create_parents",
			"label": "Auto-Create Parents",
			"fieldtype": "Check",
			"default": 0,
			"description": "❌ DISABLED (Recommended): Users must manually create parent locations first (e.g., create Warehouse before Zone).\n✅ ENABLED: System automatically creates missing parents when creating child locations. Use with caution as it may create unintended locations.",
		},
		{
			"fieldname": "lock_naming_after_first_use",
			"label": "Lock Naming After First Use",
			"fieldtype": "Check",
			"default": 0,
			"description": "❌ DISABLED: Naming patterns can be changed anytime (existing locations keep their codes).\n✅ ENABLED: Once first location is created, naming patterns (Numeric/Alphabetic/Roman) and prefixes cannot be changed. Ensures naming consistency throughout system lifecycle.",
		},
		
		# Location Naming Configuration Section
		{
			"fieldname": "location_naming_section",
			"label": "Location Naming Configuration",
			"fieldtype": "Section Break",
			"collapsible": 1,
			"description": "Configure naming patterns and prefixes for each location type",
		},
		{
			"fieldname": "warehouse_naming_pattern",
			"label": "Warehouse Naming Pattern",
			"fieldtype": "Select",
			"options": "Numeric\nAlphabetic\nRoman Numerals",
			"default": "Numeric",
			"description": "Choose how warehouses are numbered:\n• Numeric: WH-1, WH-2, WH-3, WH-4...\n• Alphabetic: WH-A, WH-B, WH-C, WH-D...\n• Roman Numerals: WH-I, WH-II, WH-III, WH-IV...\nSystem automatically finds the next available number/letter.",
		},
		{
			"fieldname": "warehouse_prefix",
			"label": "Warehouse Prefix",
			"fieldtype": "Data",
			"default": "WH",
			"description": "Text that appears before the warehouse number. Examples:\n• 'WH' → WH-1, WH-2, WH-3\n• 'STORE' → STORE-1, STORE-2\n• 'WAREHOUSE' → WAREHOUSE-1\nKeep it short (2-4 characters) for easy reading.",
		},
		{
			"fieldname": "col_break_zone",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "zone_naming_pattern",
			"label": "Zone Naming Pattern",
			"fieldtype": "Select",
			"options": "Numeric\nAlphabetic\nRoman Numerals",
			"default": "Alphabetic",
			"description": "Choose how zones are numbered within each warehouse:\n• Numeric: Z-1, Z-2, Z-3...\n• Alphabetic: Z-A, Z-B, Z-C... (Default, recommended)\n• Roman Numerals: Z-I, Z-II, Z-III...\nEach warehouse has its own zone sequence (WH-1-Z-A, WH-2-Z-A are separate).",
		},
		{
			"fieldname": "zone_prefix",
			"label": "Zone Prefix",
			"fieldtype": "Data",
			"default": "Z",
			"description": "Text that appears before the zone identifier. Examples:\n• 'Z' → WH-1-Z-A, WH-1-Z-B (Default)\n• 'ZONE' → WH-1-ZONE-A, WH-1-ZONE-B\n• 'AREA' → WH-1-AREA-A, WH-1-AREA-B\nKeep it short (1-4 characters).",
		},
		{
			"fieldname": "sec_break_rack",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "rack_naming_pattern",
			"label": "Rack Naming Pattern",
			"fieldtype": "Select",
			"options": "Numeric\nAlphabetic\nRoman Numerals",
			"default": "Numeric",
			"description": "Choose how racks are numbered within each zone:\n• Numeric: R01, R02, R03... (Default, padded with zeros)\n• Alphabetic: R-A, R-B, R-C...\n• Roman Numerals: R-I, R-II, R-III...\nEach zone has its own rack sequence (WH-1-Z-A-R01 is separate from WH-1-Z-B-R01).",
		},
		{
			"fieldname": "rack_prefix",
			"label": "Rack Prefix",
			"fieldtype": "Data",
			"default": "R",
			"description": "Text that appears before the rack identifier. Examples:\n• 'R' → WH-1-Z-A-R01, WH-1-Z-A-R02 (Default)\n• 'RACK' → WH-1-Z-A-RACK01, WH-1-Z-A-RACK02\n• 'ROW' → WH-1-Z-A-ROW01\nKeep it short (1-4 characters).",
		},
		{
			"fieldname": "col_break_shelf",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "shelf_naming_pattern",
			"label": "Shelf Naming Pattern",
			"fieldtype": "Select",
			"options": "Numeric\nAlphabetic\nRoman Numerals",
			"default": "Numeric",
			"description": "Choose how shelves are numbered within each rack:\n• Numeric: S01, S02, S03... (Default, padded with zeros)\n• Alphabetic: S-A, S-B, S-C...\n• Roman Numerals: S-I, S-II, S-III...\nEach rack has its own shelf sequence (WH-1-Z-A-R01-S01 is separate from WH-1-Z-A-R02-S01).",
		},
		{
			"fieldname": "shelf_prefix",
			"label": "Shelf Prefix",
			"fieldtype": "Data",
			"default": "S",
			"description": "Text that appears before the shelf identifier. Examples:\n• 'S' → WH-1-Z-A-R01-S01, WH-1-Z-A-R01-S02 (Default)\n• 'SHELF' → WH-1-Z-A-R01-SHELF01\n• 'LEVEL' → WH-1-Z-A-R01-LEVEL01\nKeep it short (1-5 characters).",
		},
		{
			"fieldname": "sec_break_bin",
			"fieldtype": "Section Break",
		},
		{
			"fieldname": "bin_naming_pattern",
			"label": "Bin Naming Pattern",
			"fieldtype": "Select",
			"options": "Numeric\nAlphabetic\nRoman Numerals",
			"default": "Numeric",
			"description": "Choose how bins are numbered within each shelf:\n• Numeric: B01, B02, B03... (Default, padded with zeros)\n• Alphabetic: B-A, B-B, B-C...\n• Roman Numerals: B-I, B-II, B-III...\nEach shelf has its own bin sequence. This is the most granular storage unit.",
		},
		{
			"fieldname": "bin_prefix",
			"label": "Bin Prefix",
			"fieldtype": "Data",
			"default": "B",
			"description": "Text that appears before the bin identifier. Examples:\n• 'B' → WH-1-Z-A-R01-S01-B01 (Default)\n• 'BIN' → WH-1-Z-A-R01-S01-BIN01\n• 'BOX' → WH-1-Z-A-R01-S01-BOX01\nKeep it short (1-3 characters).",
		},
		
		{
			"fieldname": "installation_status_section",
			"label": "Installation Status",
			"fieldtype": "Section Break",
			"collapsible": 1,
		},
		{
			"fieldname": "first_location_created_date",
			"label": "First Location Created",
			"fieldtype": "Datetime",
			"read_only": 1,
			"description": "Automatically recorded when the first location is created. Used for system initialization tracking and audit. Cannot be manually modified.",
		},
		{
			"fieldname": "total_locations_count",
			"label": "Total Locations",
			"fieldtype": "Int",
			"read_only": 1,
			"default": 0,
			"description": "Live count of all locations in the system. Automatically updated when locations are created or deleted. Useful for monitoring system growth.",
		},
		{
			"fieldname": "installation_column_2",
			"fieldtype": "Column Break",
		},
		{
			"fieldname": "system_initialized",
			"label": "System Initialized",
			"fieldtype": "Check",
			"read_only": 1,
			"default": 0,
			"description": "Checked = System is fully initialized with locations created. Unchecked = System is in initial state, no locations exist yet. Automatically set after first location creation.",
		},
		{
			"fieldname": "last_sync_date",
			"label": "Last Sync",
			"fieldtype": "Datetime",
			"read_only": 1,
			"description": "Timestamp of last system statistics update. Updated automatically when locations are created/modified. Used for audit and troubleshooting.",
		},
		
		# ERPNext Integration Section
		{
			"fieldname": "erpnext_section",
			"label": "ERPNext Integration",
			"fieldtype": "Section Break",
			"collapsible": 1,
			"description": "Configure integration with ERPNext.",
		},
		{
			"fieldname": "erpnext_installed",
			"label": "ERPNext Status",
			"fieldtype": "Data",
			"read_only": 1,
			"default": "Not Installed",
			"description": "Shows whether ERPNext app is installed on this site. 'Installed' = ERPNext detected, integration can be enabled. 'Not Installed' = ERPNext not found, integration unavailable. System automatically detects ERPNext presence.",
		},
		{
			"fieldname": "enable_erpnext_integration",
			"label": "Enable ERPNext Integration",
			"fieldtype": "Check",
			"default": 0,
			"depends_on": "eval:doc.erpnext_installed=='Installed'",
			"description": "ENABLED: Sync Technical Store locations with ERPNext Warehouses. Store Items sync with ERPNext Items. Stock levels synchronized bi-directionally. DISABLED: Technical Store operates independently (no ERPNext sync). Only visible when ERPNext is installed.",
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
