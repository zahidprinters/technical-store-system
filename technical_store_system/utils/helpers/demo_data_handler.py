"""
Demo Data Handler
Central manager for all demo/test data operations

This module provides generic functions to install/uninstall demo data for any DocType.
All demo data is stored in setup/demo_data/*.py files as pure data.
"""

import frappe
from frappe import _


# Demo data registry - maps DocType names to their demo data modules
DEMO_DATA_REGISTRY = {
	"Store UOM": {
		"module": "technical_store_system.setup.demo_data.store_uom",
		"data_var": "DEMO_UOMS",
		"name_field": "uom_name",
		"count": 27
	},
	"Store Item Group": {
		"module": "technical_store_system.setup.demo_data.store_item_group",
		"data_var": "DEMO_ITEM_GROUPS",
		"name_field": "item_group_name",
		"count": 19
	},
	"Store Location": {
		"module": "technical_store_system.setup.demo_data.store_location",
		"data_var": "DEMO_LOCATIONS",
		"name_field": "location_code",
		"count": 11
	}
}


def get_demo_data(doctype_name):
	"""
	Get demo data for a specific DocType
	
	Args:
		doctype_name: Name of the DocType
		
	Returns:
		list: List of dictionaries containing demo data records
		
	Raises:
		ValueError: If DocType is not registered in DEMO_DATA_REGISTRY
	"""
	if doctype_name not in DEMO_DATA_REGISTRY:
		raise ValueError(f"DocType '{doctype_name}' not registered in demo data registry")
	
	config = DEMO_DATA_REGISTRY[doctype_name]
	
	# Dynamically import the demo data module
	module = __import__(config["module"], fromlist=[config["data_var"]])
	demo_data = getattr(module, config["data_var"])
	
	return demo_data


def install_demo_data_for_doctype(doctype_name, force=False):
	"""
	Install demo data for a specific DocType
	
	Args:
		doctype_name: Name of the DocType
		force: If True, skip the install_demo_data flag check
		
	Returns:
		dict: {"success": bool, "created": int, "message": str}
	"""
	try:
		# Skip flag check if force=True (called from button)
		if not force:
			install_demo = frappe.db.get_single_value("Store Settings", "install_demo_data")
			if not install_demo:
				return {
					"success": False,
					"created": 0,
					"message": f"Demo data disabled - skipping {doctype_name}"
				}
		
		# Get demo data
		demo_data = get_demo_data(doctype_name)
		config = DEMO_DATA_REGISTRY[doctype_name]
		name_field = config["name_field"]
		
		# Insert records
		created_count = 0
		for record_data in demo_data:
			record_name = record_data.get(name_field)
			if not frappe.db.exists(doctype_name, record_name):
				doc = frappe.new_doc(doctype_name)
				for key, value in record_data.items():
					doc.set(key, value)
				doc.insert(ignore_permissions=True)
				created_count += 1
		
		frappe.db.commit()
		
		message = f"Created {created_count} {doctype_name} records" if created_count > 0 else f"All {doctype_name} records already exist"
		
		return {
			"success": True,
			"created": created_count,
			"message": message
		}
		
	except Exception as e:
		frappe.log_error(f"Error installing demo data for {doctype_name}: {str(e)}")
		return {
			"success": False,
			"created": 0,
			"message": f"Error: {str(e)}"
		}


def uninstall_demo_data_for_doctype(doctype_name):
	"""
	Uninstall demo data for a specific DocType
	Only deletes if exact count matches expected demo data count (safety check)
	
	Args:
		doctype_name: Name of the DocType
		
	Returns:
		dict: {"success": bool, "deleted": int, "message": str}
	"""
	try:
		config = DEMO_DATA_REGISTRY[doctype_name]
		expected_count = config["count"]
		
		# Safety check: only delete if count matches exactly
		actual_count = frappe.db.count(doctype_name)
		if actual_count != expected_count:
			return {
				"success": False,
				"deleted": 0,
				"message": f"Safety check failed: Expected {expected_count} records, found {actual_count}. Cannot delete to prevent data loss."
			}
		
		# Get demo data to know which records to delete
		demo_data = get_demo_data(doctype_name)
		name_field = config["name_field"]
		
		# Delete records
		deleted_count = 0
		for record_data in demo_data:
			record_name = record_data.get(name_field)
			if frappe.db.exists(doctype_name, record_name):
				frappe.delete_doc(doctype_name, record_name, ignore_permissions=True, force=True)
				deleted_count += 1
		
		frappe.db.commit()
		
		return {
			"success": True,
			"deleted": deleted_count,
			"message": f"Deleted {deleted_count} {doctype_name} records"
		}
		
	except Exception as e:
		frappe.log_error(f"Error uninstalling demo data for {doctype_name}: {str(e)}")
		return {
			"success": False,
			"deleted": 0,
			"message": f"Error: {str(e)}"
		}


def install_all_demo_data(force=False):
	"""
	Install demo data for all registered DocTypes
	
	Args:
		force: If True, skip the install_demo_data flag check
		
	Returns:
		dict: {"success": bool, "results": list, "total_created": int}
	"""
	results = []
	total_created = 0
	
	for doctype_name in DEMO_DATA_REGISTRY.keys():
		result = install_demo_data_for_doctype(doctype_name, force=force)
		results.append({
			"doctype": doctype_name,
			"result": result
		})
		total_created += result["created"]
	
	return {
		"success": True,
		"results": results,
		"total_created": total_created
	}


def uninstall_all_demo_data():
	"""
	Uninstall demo data for all registered DocTypes
	
	Returns:
		dict: {"success": bool, "results": list, "total_deleted": int}
	"""
	results = []
	total_deleted = 0
	
	for doctype_name in DEMO_DATA_REGISTRY.keys():
		result = uninstall_demo_data_for_doctype(doctype_name)
		results.append({
			"doctype": doctype_name,
			"result": result
		})
		total_deleted += result["deleted"]
	
	return {
		"success": True,
		"results": results,
		"total_deleted": total_deleted
	}


def get_demo_data_counts():
	"""
	Get current counts for all demo data DocTypes
	
	Returns:
		dict: {doctype_name: {"current": int, "expected": int}}
	"""
	counts = {}
	for doctype_name, config in DEMO_DATA_REGISTRY.items():
		counts[doctype_name] = {
			"current": frappe.db.count(doctype_name),
			"expected": config["count"]
		}
	return counts


def check_demo_data_status():
	"""
	Check if demo data is installed (all counts match expected)
	
	Returns:
		dict: {"installed": bool, "counts": dict, "message": str}
	"""
	counts = get_demo_data_counts()
	
	all_match = all(
		count_info["current"] == count_info["expected"]
		for count_info in counts.values()
	)
	
	all_zero = all(
		count_info["current"] == 0
		for count_info in counts.values()
	)
	
	if all_match:
		status = "installed"
		message = "Demo data is installed"
	elif all_zero:
		status = "not_installed"
		message = "No demo data installed"
	else:
		status = "partial"
		message = "Partial or real data exists"
	
	return {
		"status": status,
		"installed": all_match,
		"counts": counts,
		"message": message
	}
