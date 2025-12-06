"""
DocTypes Setup Module
Handles installation, update, and uninstallation of DocTypes
Automatically discovers all DocType definitions in setup/doctypes/ folder
"""

import frappe
from frappe import _
import os
import importlib


def get_all_doctypes():
	"""Automatically discover and load all DocType definitions from setup/doctypes/ folder"""
	doctypes = []
	
	# Get the path to doctypes folder
	doctypes_folder = os.path.join(
		frappe.get_app_path("technical_store_system"),
		"setup",
		"doctypes"
	)
	
	# Get all .py files except __init__.py
	for filename in os.listdir(doctypes_folder):
		if filename.endswith(".py") and filename != "__init__.py":
			module_name = filename[:-3]  # Remove .py extension
			
			try:
				# Import the module dynamically
				module = importlib.import_module(
					f"technical_store_system.setup.doctypes.{module_name}"
				)
				
				# Get the doctype definition
				if hasattr(module, "doctype"):
					doctype_dict = module.doctype.copy()
					# Store module reference for post-install hooks
					doctype_dict["__module__"] = module
					doctypes.append(doctype_dict)
					
			except Exception as e:
				print(f"    ⚠️ Error loading {filename}: {str(e)}")
	
	return doctypes


def install():
	"""Install DocTypes during app installation"""
	try:
		print("  → Installing DocTypes...")
		
		doctypes = get_all_doctypes()
		
		if not doctypes:
			print("    ℹ No DocType definitions found")
			return
		
		installed_count = 0
		for doctype_def in doctypes:
			doctype_name = doctype_def.get("name")
			
			# Check if DocType already exists
			if frappe.db.exists("DocType", doctype_name):
				print(f"    ℹ DocType '{doctype_name}' already exists, skipping...")
				continue
			
			# Create DocType
			doc = frappe.new_doc("DocType")
			
			# Set basic properties
			doc.name = doctype_def.get("name")
			doc.module = doctype_def.get("module", "Technical Store System")
			doc.custom = doctype_def.get("custom", 0)
			doc.issingle = doctype_def.get("issingle", 0) or doctype_def.get("is_single", 0)
			doc.is_submittable = doctype_def.get("is_submittable", 0)
			doc.is_tree = doctype_def.get("is_tree", 0)
			doc.editable_grid = doctype_def.get("editable_grid", 1)
			doc.track_changes = doctype_def.get("track_changes", 1)
			doc.autoname = doctype_def.get("autoname", "hash")
			doc.title_field = doctype_def.get("title_field", "")
			
			# Add fields
			for field in doctype_def.get("fields", []):
				doc.append("fields", field)
			
			# Add permissions
			for perm in doctype_def.get("permissions", []):
				doc.append("permissions", perm)
			
			# Insert DocType
			doc.insert(ignore_permissions=True)
			installed_count += 1
			print(f"    ✓ DocType '{doctype_name}' created successfully")
			
			# Call on_doctype_install hook if exists in the module
			try:
				module = doctype_def.get("__module__")
				if module and hasattr(module, "on_doctype_install"):
					module.on_doctype_install()
			except Exception as e:
				print(f"    ⚠ Post-install hook error for '{doctype_name}': {str(e)}")
		
		if installed_count > 0:
			print(f"    ✓ {installed_count} DocType(s) installed successfully")
		else:
			print("    ℹ No new DocTypes to install")
		
	except Exception as e:
		print(f"    ✗ Error installing DocTypes: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "DocTypes Installation Failed")


def update():
	"""Update existing DocTypes with latest configuration"""
	try:
		print("  → Checking DocTypes for updates...")
		
		doctypes = get_all_doctypes()
		
		if not doctypes:
			print("    ℹ No DocType definitions found")
			return
		
		updated_count = 0
		for doctype_def in doctypes:
			doctype_name = doctype_def.get("name")
			
			if not frappe.db.exists("DocType", doctype_name):
				print(f"    ℹ DocType '{doctype_name}' doesn't exist, skipping update...")
				continue
			
			# For now, just log that update would happen here
			# Actual field updates can be added later
			print(f"    ℹ DocType '{doctype_name}' exists (update logic can be added)")
			updated_count += 1
		
		if updated_count > 0:
			print(f"    ✓ Checked {updated_count} DocType(s)")
		
	except Exception as e:
		print(f"    ✗ Error updating DocTypes: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "DocTypes Update Failed")


def uninstall():
	"""Remove DocTypes during app uninstallation"""
	try:
		print("  → Uninstalling DocTypes...")
		
		doctypes = get_all_doctypes()
		
		if not doctypes:
			print("    ℹ No DocType definitions found")
			return
		
		removed_count = 0
		for doctype_def in doctypes:
			doctype_name = doctype_def.get("name")
			
			if not frappe.db.exists("DocType", doctype_name):
				print(f"    ℹ DocType '{doctype_name}' doesn't exist, skipping...")
				continue
			
			# Delete DocType
			frappe.delete_doc("DocType", doctype_name, force=True, ignore_permissions=True)
			removed_count += 1
			print(f"    ✓ DocType '{doctype_name}' removed")
		
		if removed_count > 0:
			print(f"    ✓ {removed_count} DocType(s) uninstalled successfully")
		else:
			print("    ℹ No DocTypes to remove")
		
	except Exception as e:
		print(f"    ✗ Error uninstalling DocTypes: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "DocTypes Uninstallation Failed")
