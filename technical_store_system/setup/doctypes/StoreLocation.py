"""
Store Location DocType Definition
Physical location tracking for inventory (warehouse, area, rack, shelf, bin, row, column)

Examples:
- Main Warehouse → Area A → Rack 1 → Shelf 2 → Bin 3
- Store Room → Section B → Row 5 → Column 3

Demo data: setup/demo_data/store_location.py
"""

doctype = {
	"name": "Store Location",
	"module": "Technical Store System",
	"custom": 1,
	"issingle": 0,
	"is_submittable": 0,
	"is_tree": 0,  # Not tree, but has parent_location
	"editable_grid": 1,
	"track_changes": 1,
	"autoname": "field:location_code",
	"title_field": "location_name",
	
	"fields": [
		# Section: Basic Information
		{
			"fieldname": "location_code",
			"label": "Location Code",
			"fieldtype": "Data",
			"reqd": 1,
			"unique": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
			"bold": 1,
			"description": "Unique code for location (e.g., WH-A-R01-S1)"
		},
		{
			"fieldname": "location_name",
			"label": "Location Name",
			"fieldtype": "Data",
			"reqd": 1,
			"in_list_view": 1,
			"description": "Descriptive name"
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "location_type",
			"label": "Location Type",
			"fieldtype": "Select",
			"options": "\nWarehouse\nStore Room\nArea\nZone\nRack\nShelf\nBin\nRow\nColumn\nCell\nBucket\nDrawer\nCabinet\nTransit\nStaging\nQuarantine\nReject\nOther",
			"reqd": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
			"description": "Type of location"
		},
		{
			"fieldname": "enabled",
			"label": "Enabled",
			"fieldtype": "Check",
			"default": 1,
			"in_standard_filter": 1
		},
		
		# Section: Hierarchy
		{
			"fieldname": "section_hierarchy",
			"fieldtype": "Section Break",
			"label": "Hierarchy & Address"
		},
		{
			"fieldname": "parent_location",
			"label": "Parent Location",
			"fieldtype": "Link",
			"options": "Store Location",
			"description": "Parent location in hierarchy"
		},
		{
			"fieldname": "is_group",
			"label": "Is Group Location",
			"fieldtype": "Check",
			"default": 0,
			"description": "Can contain sub-locations"
		},
		{
			"fieldname": "column_break_2",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "address",
			"label": "Physical Address",
			"fieldtype": "Text",
			"description": "Full physical address if applicable"
		},
		
		# Section: Physical Location Details
		{
			"fieldname": "section_physical",
			"fieldtype": "Section Break",
			"label": "Physical Location Details",
			"collapsible": 1
		},
		{
			"fieldname": "zone",
			"label": "Zone/Area",
			"fieldtype": "Data",
			"description": "Zone or area identifier (e.g., A, B, C)"
		},
		{
			"fieldname": "aisle",
			"label": "Aisle",
			"fieldtype": "Data",
			"description": "Aisle number or code"
		},
		{
			"fieldname": "rack",
			"label": "Rack",
			"fieldtype": "Data",
			"description": "Rack number or code"
		},
		{
			"fieldname": "column_break_3",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "shelf",
			"label": "Shelf/Level",
			"fieldtype": "Data",
			"description": "Shelf or level number"
		},
		{
			"fieldname": "row",
			"label": "Row",
			"fieldtype": "Data",
			"description": "Row number"
		},
		{
			"fieldname": "column",
			"label": "Column",
			"fieldtype": "Data",
			"description": "Column number"
		},
		{
			"fieldname": "column_break_4",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "bin",
			"label": "Bin",
			"fieldtype": "Data",
			"description": "Bin number"
		},
		{
			"fieldname": "cell",
			"label": "Cell",
			"fieldtype": "Data",
			"description": "Cell number or position"
		},
		{
			"fieldname": "bucket",
			"label": "Bucket/Container",
			"fieldtype": "Data",
			"description": "Bucket or container number"
		},
		
		# Section: Capacity & Dimensions
		{
			"fieldname": "section_capacity",
			"fieldtype": "Section Break",
			"label": "Capacity & Dimensions",
			"collapsible": 1
		},
		{
			"fieldname": "max_capacity",
			"label": "Max Capacity",
			"fieldtype": "Float",
			"precision": 2,
			"description": "Maximum storage capacity (quantity or volume)"
		},
		{
			"fieldname": "capacity_uom",
			"label": "Capacity UOM",
			"fieldtype": "Link",
			"options": "Store UOM",
			"description": "Unit of measure for capacity"
		},
		{
			"fieldname": "current_utilization",
			"label": "Current Utilization %",
			"fieldtype": "Percent",
			"read_only": 1,
			"description": "Current usage percentage"
		},
		{
			"fieldname": "column_break_5",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "length",
			"label": "Length",
			"fieldtype": "Float",
			"precision": 2,
			"description": "Length in meters"
		},
		{
			"fieldname": "width",
			"label": "Width",
			"fieldtype": "Float",
			"precision": 2,
			"description": "Width in meters"
		},
		{
			"fieldname": "height",
			"label": "Height",
			"fieldtype": "Float",
			"precision": 2,
			"description": "Height in meters"
		},
		
		# Section: Tracking & Identification
		{
			"fieldname": "section_tracking",
			"fieldtype": "Section Break",
			"label": "Tracking & Identification",
			"collapsible": 1
		},
		{
			"fieldname": "barcode",
			"label": "Barcode",
			"fieldtype": "Data",
			"unique": 1,
			"description": "Barcode for scanning"
		},
		{
			"fieldname": "qr_code",
			"label": "QR Code",
			"fieldtype": "Data",
			"unique": 1,
			"description": "QR code data"
		},
		{
			"fieldname": "column_break_6",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "rfid_tag",
			"label": "RFID Tag",
			"fieldtype": "Data",
			"description": "RFID tag identifier"
		},
		{
			"fieldname": "gps_coordinates",
			"label": "GPS Coordinates",
			"fieldtype": "Data",
			"description": "Latitude, Longitude"
		},
		
		# Section: Configuration
		{
			"fieldname": "section_config",
			"fieldtype": "Section Break",
			"label": "Configuration",
			"collapsible": 1
		},
		{
			"fieldname": "allow_negative_stock",
			"label": "Allow Negative Stock",
			"fieldtype": "Check",
			"default": 0,
			"description": "Allow stock to go negative"
		},
		{
			"fieldname": "is_bonded",
			"label": "Is Bonded Location",
			"fieldtype": "Check",
			"default": 0,
			"description": "Customs bonded warehouse"
		},
		{
			"fieldname": "column_break_7",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "temperature_controlled",
			"label": "Temperature Controlled",
			"fieldtype": "Check",
			"default": 0,
			"description": "Climate controlled storage"
		},
		{
			"fieldname": "hazardous_storage",
			"label": "Hazardous Storage",
			"fieldtype": "Check",
			"default": 0,
			"description": "For hazardous materials"
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
			"description": "Detailed description and notes"
		},
		{
			"fieldname": "column_break_8",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "image",
			"label": "Location Image",
			"fieldtype": "Attach Image",
			"description": "Photo of the location"
		},
		
		# Section: Contact & Management
		{
			"fieldname": "section_contact",
			"fieldtype": "Section Break",
			"label": "Contact & Management",
			"collapsible": 1
		},
		{
			"fieldname": "contact_person",
			"label": "Contact Person",
			"fieldtype": "Data",
			"description": "Person responsible for this location"
		},
		{
			"fieldname": "contact_phone",
			"label": "Contact Phone",
			"fieldtype": "Data"
		},
		{
			"fieldname": "column_break_9",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "contact_email",
			"label": "Contact Email",
			"fieldtype": "Data",
			"options": "Email"
		},
		{
			"fieldname": "manager",
			"label": "Manager",
			"fieldtype": "Link",
			"options": "User",
			"description": "User responsible for managing this location"
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
			"write": 1,
			"create": 1,
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
