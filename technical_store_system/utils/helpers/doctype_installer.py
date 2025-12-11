"""
DocType Installer Helper
Handles installation, update, and uninstallation of DocTypes

All logic for DocType operations is centralized here.
setup/doctypes_setup.py discovers files and delegates to this helper.
"""

import frappe
from frappe import _


def create_doctype(doctype_dict):
	"""
	Create a DocType from dictionary definition
	
	Args:
		doctype_dict: Dictionary with DocType configuration
		
	Returns:
		dict: {"success": bool, "message": str, "doctype_name": str}
	"""
	try:
		doctype_name = doctype_dict.get("name")
		
		# Check if DocType already exists
		if frappe.db.exists("DocType", doctype_name):
			return {
				"success": False,
				"message": f"DocType '{doctype_name}' already exists",
				"doctype_name": doctype_name,
				"action": "skipped"
			}
		
		# Create DocType
		doc = frappe.new_doc("DocType")
		
		# Set basic properties
		doc.name = doctype_dict.get("name")
		doc.module = doctype_dict.get("module", "Technical Store System")
		doc.custom = doctype_dict.get("custom", 0)
		doc.issingle = doctype_dict.get("issingle", 0) or doctype_dict.get("is_single", 0)
		doc.istable = doctype_dict.get("istable", 0)  # Child table flag
		doc.is_submittable = doctype_dict.get("is_submittable", 0)
		doc.is_tree = doctype_dict.get("is_tree", 0)
		doc.editable_grid = doctype_dict.get("editable_grid", 1)
		doc.track_changes = doctype_dict.get("track_changes", 1)
		doc.autoname = doctype_dict.get("autoname", "hash")
		doc.title_field = doctype_dict.get("title_field", "")
		doc.nsm_parent_field = doctype_dict.get("nsm_parent_field", "")
		
		# Add fields
		for field in doctype_dict.get("fields", []):
			doc.append("fields", field)
		
		# Add permissions
		for perm in doctype_dict.get("permissions", []):
			doc.append("permissions", perm)
		
		# Insert DocType
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": f"DocType '{doctype_name}' created successfully",
			"doctype_name": doctype_name,
			"action": "created"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"DocType Creation Failed: {doctype_name}")
		return {
			"success": False,
			"message": f"Error creating '{doctype_name}': {str(e)}",
			"doctype_name": doctype_name,
			"action": "failed"
		}


def update_doctype(doctype_dict):
	"""
	Update an existing DocType with new field definitions
	Compares existing fields with new definition and adds missing fields
	
	Args:
		doctype_dict: Dictionary with DocType configuration
		
	Returns:
		dict: {"success": bool, "message": str, "doctype_name": str, "changes": dict}
	"""
	try:
		doctype_name = doctype_dict.get("name")
		
		# Check if DocType exists
		if not frappe.db.exists("DocType", doctype_name):
			return {
				"success": False,
				"message": f"DocType '{doctype_name}' doesn't exist",
				"doctype_name": doctype_name,
				"action": "skipped",
				"changes": {}
			}
		
		# Get existing DocType
		doc = frappe.get_doc("DocType", doctype_name)
		
		# Build map of existing fields by fieldname
		existing_fields = {field.fieldname: field for field in doc.fields if field.fieldname}
		
		# Track changes
		changes = {
			"fields_added": [],
			"fields_updated": [],
			"properties_updated": []
		}
		
		# Process new field definitions
		new_fields = doctype_dict.get("fields", [])
		
		for new_field in new_fields:
			fieldname = new_field.get("fieldname")
			
			# Skip if no fieldname (section breaks, column breaks, etc. without fieldname)
			if not fieldname:
				# Check if this non-fieldname item exists by comparing label and fieldtype
				exists = False
				for existing in doc.fields:
					if (existing.fieldtype == new_field.get("fieldtype") and 
						existing.label == new_field.get("label")):
						exists = True
						break
				
				if not exists:
					# Add new section break, column break, etc.
					doc.append("fields", new_field)
					changes["fields_added"].append(f"{new_field.get('fieldtype')} - {new_field.get('label', 'No Label')}")
				continue
			
			# Check if field exists
			if fieldname in existing_fields:
				# Field exists - check if properties need updating
				existing = existing_fields[fieldname]
				updated_props = []
				
				# Compare important properties
				props_to_check = ["label", "fieldtype", "options", "reqd", "default", 
								 "description", "read_only", "hidden", "in_list_view"]
				
				for prop in props_to_check:
					new_value = new_field.get(prop)
					existing_value = getattr(existing, prop, None)
					
					# Normalize for comparison (handle int/bool vs string)
					def normalize_value(val):
						if val is None:
							return None
						# Convert to string for comparison
						return str(val) if not isinstance(val, str) else val
					
					# Update if different and new_value is not None
					if new_value is not None:
						norm_new = normalize_value(new_value)
						norm_existing = normalize_value(existing_value)
						
						if norm_new != norm_existing:
							setattr(existing, prop, new_value)
							updated_props.append(f"{prop}: {existing_value} → {new_value}")
				
				if updated_props:
					changes["fields_updated"].append(f"{fieldname} ({', '.join(updated_props)})")
			else:
				# Field doesn't exist - add it
				doc.append("fields", new_field)
				changes["fields_added"].append(fieldname)
		
		# Update basic DocType properties if provided
		basic_props = ["module", "is_submittable", "is_tree", "track_changes", 
					   "editable_grid", "title_field", "nsm_parent_field"]
		
		for prop in basic_props:
			new_value = doctype_dict.get(prop)
			if new_value is not None and new_value != getattr(doc, prop, None):
				old_value = getattr(doc, prop, None)
				setattr(doc, prop, new_value)
				changes["properties_updated"].append(f"{prop}: {old_value} → {new_value}")
		
		# Check if any changes were made
		has_changes = (changes["fields_added"] or changes["fields_updated"] or changes["properties_updated"])
		
		if has_changes:
			# Save changes
			doc.save()
			frappe.db.commit()
			
			# Build summary message
			summary = []
			if changes["fields_added"]:
				summary.append(f"{len(changes['fields_added'])} fields added")
			if changes["fields_updated"]:
				summary.append(f"{len(changes['fields_updated'])} fields updated")
			if changes["properties_updated"]:
				summary.append(f"{len(changes['properties_updated'])} properties updated")
			
			return {
				"success": True,
				"message": f"DocType '{doctype_name}' updated: {', '.join(summary)}",
				"doctype_name": doctype_name,
				"action": "updated",
				"changes": changes
			}
		else:
			return {
				"success": True,
				"message": f"DocType '{doctype_name}' is up to date (no changes needed)",
				"doctype_name": doctype_name,
				"action": "unchanged",
				"changes": changes
			}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"DocType Update Failed: {doctype_name}")
		return {
			"success": False,
			"message": f"Error updating '{doctype_name}': {str(e)}",
			"doctype_name": doctype_name,
			"action": "failed",
			"changes": {}
		}


def delete_doctype(doctype_name):
	"""
	Delete a DocType
	
	Args:
		doctype_name: Name of the DocType to delete
		
	Returns:
		dict: {"success": bool, "message": str, "doctype_name": str}
	"""
	try:
		# Check if DocType exists
		if not frappe.db.exists("DocType", doctype_name):
			return {
				"success": False,
				"message": f"DocType '{doctype_name}' doesn't exist",
				"doctype_name": doctype_name,
				"action": "skipped"
			}
		
		# Delete DocType
		frappe.delete_doc("DocType", doctype_name, force=True, ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": f"DocType '{doctype_name}' removed successfully",
			"doctype_name": doctype_name,
			"action": "deleted"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"DocType Deletion Failed: {doctype_name}")
		return {
			"success": False,
			"message": f"Error deleting '{doctype_name}': {str(e)}",
			"doctype_name": doctype_name,
			"action": "failed"
		}


def install_demo_data_for_doctype_if_enabled(doctype_name, force=False):
	"""
	Install demo data for a DocType after it's created
	Only if demo data is enabled or force=True
	
	Args:
		doctype_name: Name of the DocType
		force: If True, bypass flag check
		
	Returns:
		dict: Result from demo_data_handler
	"""
	try:
		from technical_store_system.utils.helpers.demo_data_handler import install_demo_data_for_doctype
		
		result = install_demo_data_for_doctype(doctype_name, force=force)
		return result
		
	except Exception as e:
		return {
			"success": False,
			"created": 0,
			"message": f"Error installing demo data: {str(e)}"
		}
