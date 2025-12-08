"""
DocTypes Setup Module
Universal installer/uninstaller for DocTypes
Auto-discovers all DocType definitions in setup/doctypes/
Delegates all logic to utils/helpers/doctype_installer.py
"""

import frappe
import os
import importlib
from technical_store_system.utils.helpers.doctype_installer import (
	create_doctype,
	update_doctype,
	delete_doctype,
	install_demo_data_for_doctype_if_enabled
)


def get_all_doctypes():
	"""Auto-discover all DocType definitions from setup/doctypes/ folder"""
	doctypes = []
	
	# Get path to doctypes folder
	doctypes_folder = os.path.join(
		frappe.get_app_path("technical_store_system"),
		"setup",
		"doctypes"
	)
	
	# Get all .py files except __init__.py
	for filename in os.listdir(doctypes_folder):
		if filename.endswith(".py") and filename != "__init__.py":
			module_name = filename[:-3]  # Remove .py
			
			try:
				# Import module dynamically
				module = importlib.import_module(
					f"technical_store_system.setup.doctypes.{module_name}"
				)
				
				# Get doctype definition
				if hasattr(module, "doctype"):
					doctypes.append(module.doctype.copy())
					
			except Exception as e:
				print(f"    ⚠️ Error loading {filename}: {str(e)}")
	
	return doctypes


def install():
	"""Install all DocTypes - delegates to doctype_installer helper"""
	try:
		print("  → Installing DocTypes...")
		
		doctypes = get_all_doctypes()
		
		if not doctypes:
			print("    ℹ No DocType definitions found")
			return
		
		created_count = 0
		for doctype_dict in doctypes:
			doctype_name = doctype_dict.get("name")
			
			# Delegate to helper
			result = create_doctype(doctype_dict)
			
			if result["action"] == "created":
				created_count += 1
				print(f"    ✓ {result['message']}")
				
				# Install demo data if enabled
				demo_result = install_demo_data_for_doctype_if_enabled(doctype_name)
				if demo_result.get("created", 0) > 0:
					print(f"      → Demo data: {demo_result['created']} records")
			
			elif result["action"] == "skipped":
				print(f"    ℹ {result['message']}")
			
			elif result["action"] == "failed":
				print(f"    ✗ {result['message']}")
		
		if created_count > 0:
			print(f"    ✓ {created_count} DocType(s) installed successfully")
		
	except Exception as e:
		print(f"    ✗ Error installing DocTypes: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "DocTypes Installation Failed")


def update():
	"""Update existing DocTypes - delegates to doctype_installer helper"""
	try:
		print("  → Checking DocTypes for updates...")
		
		doctypes = get_all_doctypes()
		
		if not doctypes:
			print("    ℹ No DocType definitions found")
			return
		
		checked_count = 0
		for doctype_dict in doctypes:
			# Delegate to helper
			result = update_doctype(doctype_dict)
			
			if result["success"]:
				print(f"    ℹ {result['message']}")
				checked_count += 1
		
		if checked_count > 0:
			print(f"    ✓ Checked {checked_count} DocType(s)")
		
	except Exception as e:
		print(f"    ✗ Error updating DocTypes: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "DocTypes Update Failed")


def uninstall():
	"""Remove all DocTypes - delegates to doctype_installer helper"""
	try:
		print("  → Uninstalling DocTypes...")
		
		doctypes = get_all_doctypes()
		
		if not doctypes:
			print("    ℹ No DocType definitions found")
			return
		
		removed_count = 0
		for doctype_dict in doctypes:
			doctype_name = doctype_dict.get("name")
			
			# Delegate to helper
			result = delete_doctype(doctype_name)
			
			if result["action"] == "deleted":
				removed_count += 1
				print(f"    ✓ {result['message']}")
			
			elif result["action"] == "skipped":
				print(f"    ℹ {result['message']}")
			
			elif result["action"] == "failed":
				print(f"    ✗ {result['message']}")
		
		if removed_count > 0:
			print(f"    ✓ {removed_count} DocType(s) uninstalled successfully")
		
	except Exception as e:
		print(f"    ✗ Error uninstalling DocTypes: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "DocTypes Uninstallation Failed")
