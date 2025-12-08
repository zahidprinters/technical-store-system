"""
Store Item Group Demo Data
19 hierarchical item groups for testing and initial setup
"""

DEMO_ITEM_GROUPS = [
	# Root group
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
