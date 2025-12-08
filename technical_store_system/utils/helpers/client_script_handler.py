"""
Client Script Handler Helper
Handles installation, update, and uninstallation of Client Scripts

All logic for Client Script operations is centralized here.
setup/client_scripts_setup.py discovers files and delegates to this helper.
"""

import frappe
from frappe import _


def create_client_script(script_dict):
	"""
	Create a Client Script from dictionary definition
	
	Args:
		script_dict: Dictionary with Client Script configuration
		
	Returns:
		dict: {"success": bool, "message": str, "script_name": str}
	"""
	try:
		script_name = script_dict.get("name")
		
		# Check if Client Script already exists
		if frappe.db.exists("Client Script", script_name):
			return {
				"success": False,
				"message": f"Client Script '{script_name}' already exists",
				"script_name": script_name,
				"action": "skipped"
			}
		
		# Create Client Script
		doc = frappe.new_doc("Client Script")
		doc.name = script_dict.get("name")
		doc.dt = script_dict.get("dt")
		doc.script_type = script_dict.get("script_type", "Form")
		doc.enabled = script_dict.get("enabled", 1)
		doc.script = script_dict.get("script", "")
		
		# Insert Client Script
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": f"Client Script '{script_name}' created successfully",
			"script_name": script_name,
			"action": "created"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"Client Script Creation Failed: {script_name}")
		return {
			"success": False,
			"message": f"Error creating '{script_name}': {str(e)}",
			"script_name": script_name,
			"action": "failed"
		}


def update_client_script(script_dict):
	"""
	Update an existing Client Script
	
	Args:
		script_dict: Dictionary with Client Script configuration
		
	Returns:
		dict: {"success": bool, "message": str, "script_name": str}
	"""
	try:
		script_name = script_dict.get("name")
		
		# Check if Client Script exists
		if not frappe.db.exists("Client Script", script_name):
			return {
				"success": False,
				"message": f"Client Script '{script_name}' doesn't exist",
				"script_name": script_name,
				"action": "skipped"
			}
		
		# Get existing document
		doc = frappe.get_doc("Client Script", script_name)
		
		# Update fields
		doc.dt = script_dict.get("dt")
		doc.script_type = script_dict.get("script_type", "Form")
		doc.enabled = script_dict.get("enabled", 1)
		doc.script = script_dict.get("script", "")
		
		# Save changes
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": f"Client Script '{script_name}' updated successfully",
			"script_name": script_name,
			"action": "updated"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"Client Script Update Failed: {script_name}")
		return {
			"success": False,
			"message": f"Error updating '{script_name}': {str(e)}",
			"script_name": script_name,
			"action": "failed"
		}


def delete_client_script(script_name):
	"""
	Delete a Client Script
	
	Args:
		script_name: Name of the Client Script to delete
		
	Returns:
		dict: {"success": bool, "message": str, "script_name": str}
	"""
	try:
		# Check if Client Script exists
		if not frappe.db.exists("Client Script", script_name):
			return {
				"success": False,
				"message": f"Client Script '{script_name}' doesn't exist",
				"script_name": script_name,
				"action": "skipped"
			}
		
		# Delete Client Script
		frappe.delete_doc("Client Script", script_name, force=True, ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": f"Client Script '{script_name}' removed successfully",
			"script_name": script_name,
			"action": "deleted"
		}
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), f"Client Script Deletion Failed: {script_name}")
		return {
			"success": False,
			"message": f"Error deleting '{script_name}': {str(e)}",
			"script_name": script_name,
			"action": "failed"
		}
