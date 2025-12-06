"""
Client Scripts Setup Module
Auto-discovers and installs all client scripts from setup/client_scripts/
"""

import os
import frappe
import importlib.util


def install():
	"""
	Install all client scripts from setup/client_scripts/
	Auto-discovers .py files and creates Client Script DocTypes
	"""
	try:
		print("  → Installing Client Scripts...")
		
		# Get all client script definitions
		scripts = get_all_client_scripts()
		
		if not scripts:
			print("    ℹ No Client Script definitions found")
			return
		
		installed_count = 0
		for script_def in scripts:
			script_name = script_def.get("name")
			
			# Check if Client Script already exists
			if frappe.db.exists("Client Script", script_name):
				print(f"    ℹ Client Script '{script_name}' already exists, skipping...")
				continue
			
			# Create Client Script
			doc = frappe.new_doc("Client Script")
			doc.name = script_def.get("name")
			doc.dt = script_def.get("dt")
			doc.script_type = script_def.get("script_type", "Form")
			doc.enabled = script_def.get("enabled", 1)
			doc.script = script_def.get("script", "")
			
			doc.insert(ignore_permissions=True)
			installed_count += 1
			print(f"    ✓ Client Script '{script_name}' created successfully")
		
		if installed_count > 0:
			frappe.db.commit()
			print(f"    ✓ {installed_count} Client Script(s) installed successfully")
		
	except Exception as e:
		print(f"    ✗ Error installing client scripts: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Client Scripts Installation Failed")


def get_all_client_scripts():
	"""
	Scan setup/client_scripts/ folder and import all client script definitions
	Returns list of client script dictionaries
	"""
	scripts = []
	
	# Get path to client_scripts folder
	app_path = frappe.get_app_path("technical_store_system")
	client_scripts_path = os.path.join(app_path, "setup", "client_scripts")
	
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
				script_def = module.client_script
				scripts.append(script_def)
		
		except Exception as e:
			print(f"    ✗ Error loading {file}: {str(e)}")
	
	return scripts


def uninstall():
	"""Remove all client scripts created by this app"""
	try:
		print("  → Removing Client Scripts...")
		
		scripts = get_all_client_scripts()
		removed_count = 0
		
		for script_def in scripts:
			script_name = script_def.get("name")
			if frappe.db.exists("Client Script", script_name):
				frappe.delete_doc("Client Script", script_name, force=1, ignore_permissions=True)
				removed_count += 1
				print(f"    ✓ Client Script '{script_name}' removed")
		
		if removed_count > 0:
			frappe.db.commit()
			print(f"    ✓ {removed_count} Client Script(s) removed successfully")
		else:
			print("    ℹ No Client Scripts to remove")
	
	except Exception as e:
		print(f"    ✗ Error removing client scripts: {str(e)}")
