"""
Store Item Group Controller
================================================================================
Business logic for Store Item Group DocType

FEATURES:
- Auto-generate group codes
- Update statistics (item counts, child groups)
- Validate tree hierarchy
- Prevent deletion of groups with items
- Configuration inheritance from parent

RELATED FILES:
- DocType: setup/doctypes/StoreItemGroup.py
- Demo Data: setup/demo_data/store_item_group.py
================================================================================
"""

import frappe
from frappe import _
from frappe.utils import now, getdate
import re


class ItemGroupController:
	"""Controller for Store Item Group business logic"""
	
	def __init__(self, doc):
		"""Initialize with Store Item Group document"""
		self.doc = doc
	
	# ============================================================
	# EVENT HANDLERS
	# ============================================================
	
	def before_insert(self):
		"""Called before inserting a new item group"""
		# Generate group code if not provided
		if not self.doc.group_code:
			self.doc.group_code = self.generate_group_code()
		
		# Set created date
		self.doc.created_date = now()
		
		# Inherit configuration from parent if exists
		if self.doc.parent_item_group:
			self.inherit_from_parent()
		
		# Initialize statistics
		self.doc.item_count = 0
		self.doc.child_group_count = 0
		self.doc.total_item_count = 0
		self.doc.last_updated = now()
	
	def before_save(self):
		"""Called before saving the document"""
		# Update modified date
		self.doc.modified_date = now()
		
		# Validate group settings
		self.validate_group_settings()
		
		# Update last_updated timestamp
		self.doc.last_updated = now()
	
	def on_update(self):
		"""Called after document is saved"""
		# Update statistics for this group
		self.update_statistics()
		
		# Update parent group statistics if this has a parent
		if self.doc.parent_item_group:
			self.update_parent_statistics()
	
	def before_delete(self):
		"""Called before deleting the document"""
		# Prevent deletion if group has items
		if self.doc.item_count > 0:
			frappe.throw(
				_("Cannot delete Item Group '{0}' because it contains {1} item(s). Please move or delete the items first.").format(
					self.doc.item_group_name, self.doc.item_count
				)
			)
		
		# Prevent deletion if group has child groups
		if self.doc.child_group_count > 0:
			frappe.throw(
				_("Cannot delete Item Group '{0}' because it contains {1} sub-group(s). Please move or delete the sub-groups first.").format(
					self.doc.item_group_name, self.doc.child_group_count
				)
			)
	
	# ============================================================
	# CODE GENERATION
	# ============================================================
	
	def generate_group_code(self):
		"""
		Generate a unique group code
		
		Pattern:
		- Extract initials from group name
		- Add sequential number if needed
		
		Examples:
		- "Electronics" → "ELEC"
		- "Hand Tools" → "HTOOL"
		- "Office Supplies" → "OFFSUP"
		
		Returns:
			str: Generated group code
		"""
		name = self.doc.item_group_name
		
		# Extract initials or abbreviation
		words = name.split()
		if len(words) == 1:
			# Single word: take first 4-5 letters
			code_base = name[:5].upper()
		else:
			# Multiple words: take first letter of each word
			code_base = "".join([word[0] for word in words]).upper()
			
			# If too short, add more letters from first word
			if len(code_base) < 3:
				code_base = (name[:3] + "".join([word[0] for word in words[1:]])).upper()
		
		# Remove special characters
		code_base = re.sub(r'[^A-Z0-9]', '', code_base)
		
		# Check if code exists
		code = code_base
		counter = 1
		while frappe.db.exists("Store Item Group", {"group_code": code, "name": ["!=", self.doc.name]}):
			code = f"{code_base}{counter}"
			counter += 1
		
		return code
	
	# ============================================================
	# VALIDATION
	# ============================================================
	
	def validate_group_settings(self):
		"""Validate group configuration"""
		# If is_group is checked, ensure no items are directly assigned
		if self.doc.is_group:
			item_count = frappe.db.count("Store Item", {"item_group": self.doc.name})
			if item_count > 0:
				frappe.throw(
					_("Cannot mark '{0}' as Group because it has {1} item(s) assigned. Groups can only contain sub-groups, not items.").format(
						self.doc.item_group_name, item_count
					)
				)
		
		# Validate parent is a group
		if self.doc.parent_item_group:
			parent = frappe.get_doc("Store Item Group", self.doc.parent_item_group)
			if not parent.is_group:
				frappe.throw(
					_("Parent '{0}' must be marked as 'Is Group' to contain sub-groups").format(
						parent.item_group_name
					)
				)
		
		# Prevent circular reference
		if self.doc.parent_item_group:
			self.validate_no_circular_reference()
	
	def validate_no_circular_reference(self):
		"""Ensure no circular references in tree"""
		visited = set()
		current = self.doc.parent_item_group
		
		while current:
			if current == self.doc.name:
				frappe.throw(_("Circular reference detected: Cannot set parent to a descendant group"))
			
			if current in visited:
				# Circular reference in parent chain
				frappe.throw(_("Circular reference detected in parent hierarchy"))
			
			visited.add(current)
			parent_doc = frappe.get_value("Store Item Group", current, "parent_item_group")
			current = parent_doc
	
	# ============================================================
	# STATISTICS
	# ============================================================
	
	def update_statistics(self):
		"""Update all statistics for this group"""
		# Count direct items (items assigned to this group only)
		self.doc.item_count = frappe.db.count("Store Item", {"item_group": self.doc.name})
		
		# Count immediate child groups
		self.doc.child_group_count = frappe.db.count("Store Item Group", {"parent_item_group": self.doc.name})
		
		# Count total items recursively (including all sub-groups)
		self.doc.total_item_count = self.count_total_items_recursive()
		
		# Update timestamp
		self.doc.last_updated = now()
		
		# Save without triggering on_update again
		self.doc.db_update()
	
	def count_total_items_recursive(self):
		"""
		Count all items in this group and all sub-groups
		
		Returns:
			int: Total item count including all descendants
		"""
		# Start with direct items
		total = self.doc.item_count
		
		# Get all child groups
		children = frappe.get_all("Store Item Group", 
			filters={"parent_item_group": self.doc.name},
			fields=["name", "item_count", "total_item_count"]
		)
		
		# Add items from all children (use their total_item_count for efficiency)
		for child in children:
			# Get child's total count (includes their sub-groups)
			child_total = frappe.db.get_value("Store Item Group", child.name, "total_item_count") or 0
			child_direct = frappe.db.get_value("Store Item Group", child.name, "item_count") or 0
			
			# Add direct items from child plus their descendants
			total += child_direct + child_total
		
		return total
	
	def update_parent_statistics(self):
		"""Update statistics for parent group"""
		if not self.doc.parent_item_group:
			return
		
		try:
			parent = frappe.get_doc("Store Item Group", self.doc.parent_item_group)
			controller = ItemGroupController(parent)
			controller.update_statistics()
		except Exception as e:
			frappe.log_error(f"Error updating parent statistics: {str(e)}")
	
	# ============================================================
	# CONFIGURATION INHERITANCE
	# ============================================================
	
	def inherit_from_parent(self):
		"""Inherit configuration settings from parent group"""
		if not self.doc.parent_item_group:
			return
		
		try:
			parent = frappe.get_doc("Store Item Group", self.doc.parent_item_group)
			
			# Inherit default UOM if not set
			if not self.doc.default_uom and parent.default_uom:
				self.doc.default_uom = parent.default_uom
			
			# Inherit warehouse if not set
			if not self.doc.default_warehouse and parent.default_warehouse:
				self.doc.default_warehouse = parent.default_warehouse
			
			# Inherit tracking settings if not explicitly set
			# Note: Only inherit if current value is default (0)
			if not self.doc.has_serial_no and parent.has_serial_no:
				self.doc.has_serial_no = parent.has_serial_no
			
			if not self.doc.has_batch_no and parent.has_batch_no:
				self.doc.has_batch_no = parent.has_batch_no
			
			if not self.doc.allow_negative_stock and parent.allow_negative_stock:
				self.doc.allow_negative_stock = parent.allow_negative_stock
			
			if not self.doc.auto_create_bins and parent.auto_create_bins:
				self.doc.auto_create_bins = parent.auto_create_bins
		
		except Exception as e:
			frappe.log_error(f"Error inheriting from parent: {str(e)}")


# ============================================================
# EVENT FUNCTIONS (Called by hooks)
# ============================================================

def before_insert_event(doc, method=None):
	"""Hook: Called before inserting Store Item Group"""
	controller = ItemGroupController(doc)
	controller.before_insert()

def before_save_event(doc, method=None):
	"""Hook: Called before saving Store Item Group"""
	controller = ItemGroupController(doc)
	controller.before_save()

def on_update_event(doc, method=None):
	"""Hook: Called after Store Item Group is saved"""
	controller = ItemGroupController(doc)
	controller.on_update()

def before_delete_event(doc, method=None):
	"""Hook: Called before deleting Store Item Group"""
	controller = ItemGroupController(doc)
	controller.before_delete()


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def recalculate_all_statistics():
	"""
	Recalculate statistics for all item groups
	Useful for maintenance or after data migration
	
	Usage:
		bench execute technical_store_system.utils.controllers.item_group_controller.recalculate_all_statistics
	"""
	groups = frappe.get_all("Store Item Group", fields=["name"])
	
	frappe.msgprint(f"Recalculating statistics for {len(groups)} item groups...")
	
	for group_data in groups:
		try:
			doc = frappe.get_doc("Store Item Group", group_data.name)
			controller = ItemGroupController(doc)
			controller.update_statistics()
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Error recalculating stats for {group_data.name}: {str(e)}")
	
	frappe.msgprint("Statistics recalculation complete!")

def get_group_hierarchy(group_name):
	"""
	Get full hierarchy path for a group
	
	Args:
		group_name: Name of the Store Item Group
	
	Returns:
		list: List of group names from root to current group
	
	Example:
		>>> get_group_hierarchy("Laptops")
		['Electronics', 'Computers', 'Laptops']
	"""
	hierarchy = []
	current = group_name
	
	while current:
		doc = frappe.get_doc("Store Item Group", current)
		hierarchy.insert(0, doc.item_group_name)
		current = doc.parent_item_group
	
	return hierarchy

def get_group_children_recursive(group_name):
	"""
	Get all child groups recursively
	
	Args:
		group_name: Name of the Store Item Group
	
	Returns:
		list: List of all descendant group names
	"""
	children = []
	direct_children = frappe.get_all("Store Item Group", 
		filters={"parent_item_group": group_name},
		fields=["name"]
	)
	
	for child in direct_children:
		children.append(child.name)
		# Recursively get children of children
		children.extend(get_group_children_recursive(child.name))
	
	return children
