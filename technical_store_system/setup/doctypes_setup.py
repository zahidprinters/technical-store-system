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
	
	# Sort by dependencies (child tables first, then parent DocTypes, then DocTypes with dependencies)
	return sort_doctypes_by_dependencies(doctypes)


def sort_doctypes_by_dependencies(doctypes):
	"""
	Sort DocTypes by dependencies to ensure proper installation order
	Uses topological sort to handle complex dependency chains
	"""
	# Build dependency graph
	dependency_map = {}
	doctype_by_name = {}
	
	for dt in doctypes:
		name = dt.get("name")
		doctype_by_name[name] = dt
		dependency_map[name] = get_link_dependencies(dt)
	
	# Separate child tables (always first)
	child_tables = [dt for dt in doctypes if dt.get("istable") == 1]
	child_table_names = {dt.get("name") for dt in child_tables}
	
	# Remove child tables from dependency sorting
	regular_doctypes = [dt for dt in doctypes if dt.get("istable") != 1]
	
	# Topological sort for regular doctypes
	sorted_doctypes = topological_sort(regular_doctypes, dependency_map)
	
	# Return: Child tables first, then sorted DocTypes
	return child_tables + sorted_doctypes


def get_link_dependencies(doctype_dict):
	"""Get list of DocType names that this DocType depends on"""
	doctype_name = doctype_dict.get("name", "")
	dependencies = set()
	
	# Check for Link fields to other DocTypes in this app
	for field in doctype_dict.get("fields", []):
		if field.get("fieldtype") == "Link":
			options = field.get("options", "")
			# Check if it links to another DocType in our app (starts with "Store")
			if options and options.startswith("Store") and options != doctype_name:
				dependencies.add(options)
	
	return dependencies


def topological_sort(doctypes, dependency_map):
	"""
	Topological sort to order DocTypes by dependencies
	DocTypes with no dependencies come first
	"""
	sorted_list = []
	visited = set()
	visiting = set()
	
	def visit(doctype_name):
		if doctype_name in visited:
			return
		if doctype_name in visiting:
			# Circular dependency - skip
			return
		
		visiting.add(doctype_name)
		
		# Visit dependencies first
		for dep in dependency_map.get(doctype_name, []):
			if dep in dependency_map:  # Only if dependency is in our list
				visit(dep)
		
		visiting.remove(doctype_name)
		visited.add(doctype_name)
		
		# Find the actual doctype dict
		for dt in doctypes:
			if dt.get("name") == doctype_name:
				sorted_list.append(dt)
				break
	
	# Visit all doctypes
	for dt in doctypes:
		visit(dt.get("name"))
	
	return sorted_list


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
		
		updated_count = 0
		unchanged_count = 0
		
		for doctype_dict in doctypes:
			# Delegate to helper
			result = update_doctype(doctype_dict)
			
			if result["success"]:
				action = result.get("action")
				
				if action == "updated":
					# Show detailed changes
					print(f"    ✓ {result['message']}")
					updated_count += 1
					
					# Show field details if available
					changes = result.get("changes", {})
					if changes.get("fields_added"):
						for field in changes["fields_added"]:
							print(f"      + Field added: {field}")
					if changes.get("fields_updated"):
						for field in changes["fields_updated"]:
							print(f"      ~ Field updated: {field}")
					if changes.get("properties_updated"):
						for prop in changes["properties_updated"]:
							print(f"      ~ Property updated: {prop}")
							
				elif action == "unchanged":
					print(f"    ℹ {result['message']}")
					unchanged_count += 1
					
				elif action == "skipped":
					print(f"    ⚠️ {result['message']}")
			else:
				print(f"    ✗ {result['message']}")
		
		# Summary
		if updated_count > 0:
			print(f"    ✓ Updated {updated_count} DocType(s)")
		if unchanged_count > 0:
			print(f"    ✓ Checked {unchanged_count} DocType(s) (no changes needed)")
		
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
