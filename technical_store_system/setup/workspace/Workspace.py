"""
Technical Store System Workspace Definition
Simple workspace with welcome message - will grow as we add DocTypes
"""

import json

workspace = {
	"name": "Technical Store System",
	"label": "Technical Store System", 
	"title": "Technical Store System",
	"icon": "accounting",
	"module": "Technical Store System",
	"public": 1,
	"is_hidden": 0,
	"hide_custom": 0,
	
	"content": json.dumps([
		{
			"id": "getting_started_header",
			"type": "header",
			"data": {
				"text": '<span style="font-size: 18px;"><b>Getting Started</b></span>',
				"col": 12
			}
		},
		{
			"id": "getting_started_card",
			"type": "card",
			"data": {
				"card_name": "Getting Started",
				"col": 12
			}
		}
	]),
	
	"shortcuts": [],
	
	"links": [
		{
			"type": "Card Break",
			"label": "Masters",
			"description": "Store Items and Locations",
			"hidden": 0,
		},
		{
			"type": "Link",
			"link_type": "DocType",
			"link_to": "Store Item",
			"label": "Store Item",
			"description": "Manage store items",
			"hidden": 0,
		},
		{
			"type": "Link",
			"link_type": "DocType",
			"link_to": "Store Location",
			"label": "Store Location",
			"description": "Manage store locations",
			"hidden": 0,
		},
		{
			"type": "Link",
			"link_type": "DocType",
			"link_to": "Store UOM",
			"label": "Store UOM",
			"description": "Units of Measure (Each, Kg, Liter, etc.)",
			"hidden": 0,
		},
		{
			"type": "Link",
			"link_type": "DocType",
			"link_to": "Store Item Group",
			"label": "Store Item Group",
			"description": "Item categories and classifications (tree view)",
			"hidden": 0,
		},
		{
			"type": "Card Break",
			"label": "Settings",
			"description": "Configure your store system",
			"hidden": 0,
		},
		{
			"type": "Link",
			"link_type": "DocType",
			"link_to": "Store Settings",
			"label": "Store Settings",
			"description": "Configure store system settings",
			"hidden": 0,
		},
		{
			"type": "Card Break",
			"label": "Administration",
			"description": "Users and Roles",
			"hidden": 0,
		},
		{
			"type": "Link",
			"link_type": "DocType",
			"link_to": "User",
			"label": "User",
			"description": "Manage users and assign roles",
			"hidden": 0,
		},
		{
			"type": "Link",
			"link_type": "DocType", 
			"link_to": "Role",
			"label": "Role",
			"description": "Store Manager, Warehouse Staff, Inventory Admin, Store Viewer",
			"hidden": 0,
		},
	]
}
