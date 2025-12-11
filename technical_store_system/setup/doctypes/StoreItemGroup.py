"""
Store Item Group DocType Definition
================================================================================
Hierarchical category/classification system for inventory items

PURPOSE:
- Organize items into logical categories
- Support unlimited nesting (tree structure)
- Apply default settings to all items in group
- Track statistics per category

STRUCTURE:
- Tree-based hierarchy (nested set model)
- Parent-child relationships
- Group vs. Item classification

EXAMPLES:
├── Electronics (Group)
│   ├── Computers (Group)
│   │   ├── Laptops (Group)
│   │   ├── Desktops (Group)
│   │   └── Accessories (Items allowed)
│   └── Mobile Devices (Group)
├── Tools (Group)
│   ├── Hand Tools (Group)
│   │   ├── Screwdrivers (Items allowed)
│   │   └── Hammers (Items allowed)
│   └── Power Tools (Group)
└── Office Supplies (Items allowed)

FEATURES:
- Auto-generated group codes (optional)
- Default UOM inheritance
- Serial/Batch tracking defaults
- Item count statistics
- Image support per group

RELATED FILES:
- Demo Data: setup/demo_data/store_item_group.py
- Controller: utils/controllers/item_group_controller.py
================================================================================
"""

doctype = {
	"name": "Store Item Group",
	"module": "Technical Store System",
	"custom": 1,
	"issingle": 0,
	"is_submittable": 0,
	"is_tree": 1,  # Enable tree/nested structure
	"editable_grid": 1,
	"track_changes": 1,
	"autoname": "field:item_group_name",
	"title_field": "item_group_name",
	"nsm_parent_field": "parent_item_group",  # Tree parent field
	
	"fields": [
		# Tab 1: Basic Information
		{
			"fieldname": "basic_info_tab",
			"label": "Basic Information",
			"fieldtype": "Tab Break",
		},
		{
			"fieldname": "group_code",
			"label": "Group Code",
			"fieldtype": "Data",
			"reqd": 0,
			"unique": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
			"description": "Short code for quick identification (e.g., ELEC, TOOLS, OFF)"
		},
		{
			"fieldname": "item_group_name",
			"label": "Item Group Name",
			"fieldtype": "Data",
			"reqd": 1,
			"unique": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
			"bold": 1,
			"description": "Full descriptive name of the category (e.g., Electronics, Hand Tools, Office Supplies)"
		},
		{
			"fieldname": "parent_item_group",
			"label": "Parent Item Group",
			"fieldtype": "Link",
			"options": "Store Item Group",
			"in_list_view": 1,
			"in_standard_filter": 1,
			"description": "Parent category for creating nested hierarchy. Leave blank for top-level groups."
		},
		{
			"fieldname": "is_group",
			"label": "Is Group",
			"fieldtype": "Check",
			"default": 0,
			"in_list_view": 1,
			"description": "Group: Can contain sub-categories (no items directly). Leaf: Can contain items (no sub-categories)."
		},
		{
			"fieldname": "enabled",
			"label": "Enabled",
			"fieldtype": "Check",
			"default": 1,
			"in_list_view": 1,
			"in_standard_filter": 1,
			"description": "Active groups appear in dropdowns and reports. Disabled groups are hidden."
		},
		{
			"fieldname": "sort_order",
			"label": "Sort Order",
			"fieldtype": "Int",
			"default": 0,
			"description": "Display order for this group (lower numbers appear first in lists)"
		},
		
		# Section: Details
		{
			"fieldname": "section_details",
			"fieldtype": "Section Break",
			"label": "Details"
		},
		{
			"fieldname": "description",
			"label": "Description",
			"fieldtype": "Text Editor",
			"description": "Detailed description of this category and what items belong here."
		},
		{
			"fieldname": "column_break_1",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "image",
			"label": "Group Image",
			"fieldtype": "Attach Image",
			"description": "Icon or image representing this category."
		},
		
		# Tab 2: Configuration
		{
			"fieldname": "config_tab",
			"label": "Configuration",
			"fieldtype": "Tab Break",
		},
		{
			"fieldname": "section_defaults",
			"fieldtype": "Section Break",
			"label": "Default Settings"
		},
		{
			"fieldname": "default_uom",
			"label": "Default UOM",
			"fieldtype": "Link",
			"options": "Store UOM",
			"description": "Default unit of measure inherited by new items in this group (e.g., Pcs, Kg, Meter, Liter)."
		},
		{
			"fieldname": "column_break_2",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "default_warehouse",
			"label": "Default Warehouse",
			"fieldtype": "Link",
			"options": "Store Location",
			"description": "Default storage location for items in this group."
		},
		
		# Section: Tracking Options
		{
			"fieldname": "section_tracking",
			"fieldtype": "Section Break",
			"label": "Tracking Options",
			"description": "Configure how items in this group are tracked."
		},
		{
			"fieldname": "has_serial_no",
			"label": "Has Serial No",
			"fieldtype": "Check",
			"default": 0,
			"description": "Track each item individually with unique serial numbers. Use for laptops, phones, equipment with warranties, high-value assets."
		},
		{
			"fieldname": "has_batch_no",
			"label": "Has Batch No",
			"fieldtype": "Check",
			"default": 0,
			"description": "Track items by production batch or lot number. Use for chemicals, medicines, food items with expiry dates, manufactured goods."
		},
		{
			"fieldname": "column_break_3",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "allow_negative_stock",
			"label": "Allow Negative Stock",
			"fieldtype": "Check",
			"default": 0,
			"description": "Allow issuing items even when stock quantity is zero or negative. Useful for back-order scenarios, quick transactions. Risk: Inaccurate inventory if not managed properly."
		},
		{
			"fieldname": "auto_create_bins",
			"label": "Auto Create Bins",
			"fieldtype": "Check",
			"default": 0,
			"description": "Automatically create storage bins when items are added to warehouse locations."
		},
		
		# Tab 3: Statistics
		{
			"fieldname": "stats_tab",
			"label": "Statistics",
			"fieldtype": "Tab Break",
		},
		{
			"fieldname": "section_statistics",
			"fieldtype": "Section Break",
			"label": "Group Statistics",
			"description": "Real-time statistics for this category."
		},
		{
			"fieldname": "item_count",
			"label": "Direct Items",
			"fieldtype": "Int",
			"read_only": 1,
			"default": 0,
			"in_list_view": 1,
			"description": "Number of items directly assigned to this group (excludes sub-groups). Auto-updated."
		},
		{
			"fieldname": "child_group_count",
			"label": "Sub-Groups",
			"fieldtype": "Int",
			"read_only": 1,
			"default": 0,
			"in_list_view": 1,
			"description": "Number of immediate child groups under this group. Auto-updated."
		},
		{
			"fieldname": "column_break_4",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "total_item_count",
			"label": "Total Items (Recursive)",
			"fieldtype": "Int",
			"read_only": 1,
			"default": 0,
			"description": "Total count of all items including all sub-groups (entire tree branch). Auto-updated."
		},
		{
			"fieldname": "last_updated",
			"label": "Last Updated",
			"fieldtype": "Datetime",
			"read_only": 1,
			"description": "Last time statistics were recalculated. Auto-updated."
		},
		
		# Section: Creation Info
		{
			"fieldname": "section_meta",
			"fieldtype": "Section Break",
			"label": "Metadata",
			"collapsible": 1
		},
		{
			"fieldname": "created_date",
			"label": "Created Date",
			"fieldtype": "Datetime",
			"read_only": 1,
			"description": "When this group was first created."
		},
		{
			"fieldname": "column_break_5",
			"fieldtype": "Column Break"
		},
		{
			"fieldname": "modified_date",
			"label": "Modified Date",
			"fieldtype": "Datetime",
			"read_only": 1,
			"description": "Last time this group was modified."
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
