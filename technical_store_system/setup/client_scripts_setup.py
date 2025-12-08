"""
Client Scripts Setup Module
Universal installer/uninstaller for Client Scripts
Auto-discovers all client script definitions in setup/client_scripts/
Delegates all logic to utils/helpers/client_script_handler.py
"""

import os
import frappe
import importlib.util
from technical_store_system.utils.helpers.client_script_handler import (
	create_client_script,
	update_client_script,
	delete_client_script
)


def get_all_client_scripts():
	"""Auto-discover all client script definitions from setup/client_scripts/ folder"""
	scripts = []
	
	# Get path to client_scripts folder
	client_scripts_path = os.path.join(
		frappe.get_app_path("technical_store_system"),
		"setup",
		"client_scripts"
	)
	
	if not os.path.exists(client_scripts_path):
		return scripts
	
	# Get all .py files (except __init__.py)
	files = [f for f in os.listdir(client_scripts_path) 
			 if f.endswith('.py') and f != '__init__.py']
	
	# Import each file and get client_script definition
	for file in files:
		try:
			module_path = os.path.join(client_scripts_path, file)
			module_name = file[:-3]  # Remove .py
			
			# Load module
			spec = importlib.util.spec_from_file_location(module_name, module_path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			
			# Get client_script definition
			if hasattr(module, 'client_script'):
				scripts.append(module.client_script)
		
		except Exception as e:
			print(f"    ✗ Error loading {file}: {str(e)}")
	
	return scripts


def install():
	"""Install all Client Scripts - delegates to client_script_handler helper"""
	try:
		print("  → Installing Client Scripts...")
		
		scripts = get_all_client_scripts()
		
		if not scripts:
			print("    ℹ No Client Script definitions found")
			return
		
		created_count = 0
		for script_dict in scripts:
			# Delegate to helper
			result = create_client_script(script_dict)
			
			if result["action"] == "created":
				created_count += 1
				print(f"    ✓ {result['message']}")
			
			elif result["action"] == "skipped":
				print(f"    ℹ {result['message']}")
			
			elif result["action"] == "failed":
				print(f"    ✗ {result['message']}")
		
		if created_count > 0:
			print(f"    ✓ {created_count} Client Script(s) installed successfully")
		
	except Exception as e:
		print(f"    ✗ Error installing client scripts: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Client Scripts Installation Failed")


def uninstall():
	"""Remove all Client Scripts - delegates to client_script_handler helper"""
	try:
		print("  → Removing Client Scripts...")
		
		scripts = get_all_client_scripts()
		
		if not scripts:
			print("    ℹ No Client Script definitions found")
			return
		
		removed_count = 0
		for script_dict in scripts:
			script_name = script_dict.get("name")
			
			# Delegate to helper
			result = delete_client_script(script_name)
			
			if result["action"] == "deleted":
				removed_count += 1
				print(f"    ✓ {result['message']}")
			
			elif result["action"] == "skipped":
				print(f"    ℹ {result['message']}")
			
			elif result["action"] == "failed":
				print(f"    ✗ {result['message']}")
		
		if removed_count > 0:
			print(f"    ✓ {removed_count} Client Script(s) removed successfully")
		
	except Exception as e:
		print(f"    ✗ Error removing client scripts: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Client Scripts Uninstallation Failed")
