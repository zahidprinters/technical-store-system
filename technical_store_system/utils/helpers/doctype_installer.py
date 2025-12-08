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
	Update an existing DocType
	
	Args:
		doctype_dict: Dictionary with DocType configuration
		
	Returns:
		dict: {"success": bool, "message": str, "doctype_name": str}
	"""
	try:
		doctype_name = doctype_dict.get("name")
		
		# Check if DocType exists
		if not frappe.db.exists("DocType", doctype_name):
			return {
				"success": False,
				"message": f"DocType '{doctype_name}' doesn't exist",
				"doctype_name": doctype_name,
				"action": "skipped"
			}
		
		# For now, just log that DocType exists
		# Full update logic can be added when needed
		return {
			"success": True,
			"message": f"DocType '{doctype_name}' exists (update logic can be added)",
			"doctype_name": doctype_name,
			"action": "checked"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"DocType Update Failed: {doctype_name}")
		return {
			"success": False,
			"message": f"Error updating '{doctype_name}': {str(e)}",
			"doctype_name": doctype_name,
			"action": "failed"
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
