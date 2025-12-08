"""
Store Location Demo Data
11 hierarchical warehouse locations for testing and initial setup
"""

DEMO_LOCATIONS = [
	# Main Warehouse
	{"location_code": "WH-MAIN", "location_name": "Main Warehouse", "location_type": "Warehouse", "is_group": 0, "enabled": 1},
	{"location_code": "WH-MAIN-A", "location_name": "Area A", "location_type": "Area", "parent_location": "WH-MAIN", "zone": "A", "enabled": 1},
	{"location_code": "WH-MAIN-A-R01", "location_name": "Rack A-01", "location_type": "Rack", "parent_location": "WH-MAIN-A", "zone": "A", "rack": "01", "enabled": 1},
	{"location_code": "WH-MAIN-A-R01-S1", "location_name": "Shelf 1", "location_type": "Shelf", "parent_location": "WH-MAIN-A-R01", "rack": "01", "shelf": "1", "enabled": 1},
	{"location_code": "WH-MAIN-A-R01-S2", "location_name": "Shelf 2", "location_type": "Shelf", "parent_location": "WH-MAIN-A-R01", "rack": "01", "shelf": "2", "enabled": 1},
	
	# Store Room
	{"location_code": "STORE-01", "location_name": "Store Room 1", "location_type": "Store Room", "is_group": 0, "enabled": 1},
	{"location_code": "STORE-01-R1", "location_name": "Row 1", "location_type": "Row", "parent_location": "STORE-01", "row": "1", "enabled": 1},
	{"location_code": "STORE-01-R1-C1", "location_name": "Column 1", "location_type": "Bin", "parent_location": "STORE-01-R1", "row": "1", "column": "1", "enabled": 1},
	{"location_code": "STORE-01-R1-C2", "location_name": "Column 2", "location_type": "Bin", "parent_location": "STORE-01-R1", "row": "1", "column": "2", "enabled": 1},
	
	# Transit/Staging
	{"location_code": "TRANSIT", "location_name": "In Transit", "location_type": "Transit", "is_group": 0, "enabled": 1, "description": "Items in transit between locations"},
	{"location_code": "STAGING", "location_name": "Staging Area", "location_type": "Staging", "is_group": 0, "enabled": 1, "description": "Temporary staging for receiving/dispatch"},
]
