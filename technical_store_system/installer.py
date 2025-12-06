"""
Universal Installer for Technical Store System
Central installer that calls all setup modules during installation/uninstallation
"""

import frappe
from frappe import _


def after_install():
	"""
	Universal installer - runs after app installation
	Calls all setup modules in proper order
	"""
	try:
		print("\n" + "="*60)
		print("🚀 Installing Technical Store System...")
		print("="*60)
		
		# 1. Create default roles (before DocTypes for permissions)
		create_default_roles()
		
		# 2. Install DocTypes (auto-discovers all DocTypes + runs post-install hooks)
		install_doctypes()
		
		# 3. Create Store Settings (if not auto-created)
		create_store_settings()
		
		# 4. Install client scripts (for UI behavior)
		install_client_scripts()
		
		# 5. Install workspace (after DocTypes exist, to avoid link errors)
		install_workspace()
		
		# 6. Set up default permissions
		setup_default_permissions()
		
		# Commit changes
		frappe.db.commit()
		
		print("\n" + "="*60)
		print("✅ Technical Store System installed successfully!")
		print("="*60 + "\n")
		
	except Exception as e:
		frappe.db.rollback()
		print(f"\n❌ Installation failed: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Technical Store System Installation Failed")
		raise


def after_uninstall():
	"""
	Universal uninstaller - runs after app uninstallation
	Calls all cleanup modules in proper order
	"""
	try:
		print("\n" + "="*60)
		print("🗑️  Uninstalling Technical Store System...")
		print("="*60)
		
		# 1. Uninstall DocTypes
		uninstall_doctypes()
		
		# 2. Uninstall workspace
		uninstall_workspace()
		
		# 3. Optional: Remove custom roles (be careful!)
		# remove_custom_roles()
		
		# 4. Clear caches
		frappe.clear_cache()
		
		# Commit changes
		frappe.db.commit()
		
		print("\n" + "="*60)
		print("✅ Technical Store System uninstalled successfully!")
		print("="*60 + "\n")
		
	except Exception as e:
		frappe.db.rollback()
		print(f"\n❌ Uninstallation failed: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Technical Store System Uninstallation Failed")


def after_migrate():
	"""
	Run after migrations to update workspace and other configurations
	"""
	try:
		print("\n📦 Updating Technical Store System configurations...")
		
		# Update workspace with latest configuration
		update_workspace()
		
		# Update DocTypes
		update_doctypes()
		
		# Update any other configurations
		# update_permissions()
		
		frappe.db.commit()
		print("✅ Configurations updated successfully!\n")
		
	except Exception as e:
		print(f"❌ Configuration update failed: {str(e)}\n")
		frappe.log_error(frappe.get_traceback(), "Configuration Update Failed")


# ============================================================================
# WORKSPACE INSTALLATION
# ============================================================================

def install_workspace():
	"""Install workspace using workspace_setup module"""
	try:
		from technical_store_system.setup import workspace_setup
		workspace_setup.install()
	except Exception as e:
		print(f"  ✗ Workspace installation failed: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Workspace Installation Error")


def update_workspace():
	"""Update workspace using workspace_setup module"""
	try:
		from technical_store_system.setup import workspace_setup
		workspace_setup.update()
	except Exception as e:
		print(f"  ✗ Workspace update failed: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Workspace Update Error")


def uninstall_workspace():
	"""Uninstall workspace using workspace_setup module"""
	try:
		from technical_store_system.setup import workspace_setup
		workspace_setup.uninstall()
	except Exception as e:
		print(f"  ✗ Workspace uninstallation failed: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Workspace Uninstallation Error")


# ============================================================================
# CLIENT SCRIPTS INSTALLATION
# ============================================================================

def install_client_scripts():
	"""Install client scripts using client_scripts_setup module"""
	try:
		from technical_store_system.setup import client_scripts_setup
		client_scripts_setup.install()
	except Exception as e:
		print(f"  ✗ Client scripts installation failed: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Client Scripts Installation Error")


def uninstall_client_scripts():
	"""Uninstall client scripts using client_scripts_setup module"""
	try:
		from technical_store_system.setup import client_scripts_setup
		client_scripts_setup.uninstall()
	except Exception as e:
		print(f"  ✗ Client scripts uninstallation failed: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Client Scripts Uninstallation Error")


# ============================================================================
# DOCTYPES INSTALLATION
# ============================================================================

def install_doctypes():
	"""Install DocTypes using doctypes_setup module"""
	try:
		from technical_store_system.setup import doctypes_setup
		doctypes_setup.install()
	except Exception as e:
		print(f"  ⚠️ DocTypes installation error: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "DocTypes Installation Error")


def update_doctypes():
	"""Update DocTypes using doctypes_setup module"""
	try:
		from technical_store_system.setup import doctypes_setup
		doctypes_setup.update()
	except Exception as e:
		print(f"  ⚠️ DocTypes update error: {str(e)}")



		print(f"  ⚠️ DocTypes update error: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "DocTypes Update Error")


def uninstall_doctypes():
	"""Uninstall DocTypes using doctypes_setup module"""
	try:
		from technical_store_system.setup import doctypes_setup
		doctypes_setup.uninstall()
	except Exception as e:
		print(f"  ⚠️ DocTypes uninstallation error: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "DocTypes Uninstallation Error")


# ============================================================================
# ROLES & PERMISSIONS
# ============================================================================

def create_default_roles():
	"""Create default roles for the app"""
	try:
		print("  → Creating default roles...")
		
		roles = [
			{
				"role_name": "Store Manager",
				"desk_access": 1,
				"description": "Full access to all Store features"
			},
			{
				"role_name": "Warehouse Staff",
				"desk_access": 1,
				"description": "Operational access to stock management"
			},
			{
				"role_name": "Inventory Admin",
				"desk_access": 1,
				"description": "Configuration access to items and settings"
			},
			{
				"role_name": "Store Viewer",
				"desk_access": 1,
				"description": "Read-only access to all Store data"
			}
		]
		
		for role_data in roles:
			if not frappe.db.exists("Role", role_data["role_name"]):
				role = frappe.new_doc("Role")
				role.role_name = role_data["role_name"]
				role.desk_access = role_data["desk_access"]
				role.disabled = 0
				role.insert(ignore_permissions=True)
				print(f"    ✓ Created role: {role.role_name}")
			else:
				print(f"    ℹ Role '{role_data['role_name']}' already exists")
		
	except Exception as e:
		print(f"    ✗ Error creating roles: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Roles Creation Failed")


def setup_default_permissions():
	"""Set up default permissions for DocTypes"""
	try:
		print("  → Setting up default permissions...")
		# This will be implemented after DocTypes are created
		print("    ℹ Permissions will be set after DocTypes are created")
	except Exception as e:
		print(f"    ✗ Error setting permissions: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Permissions Setup Failed")


# ============================================================================
# SETTINGS & CONFIGURATION
# ============================================================================

def create_store_settings():
	"""Create Store Settings with default values"""
	try:
		print("  → Creating Store Settings...")
		
		if not frappe.db.exists("Store Settings", "Store Settings"):
			settings = frappe.get_doc({
				"doctype": "Store Settings",
				"name": "Store Settings",
				"enable_erpnext_sync": 0,
				"allow_negative_stock": 0,
				"auto_sync_items": 0,
				"stock_validation": 1
			})
			settings.insert(ignore_permissions=True)
			print("    ✓ Store Settings created successfully")
		else:
			print("    ℹ Store Settings already exists")
		
	except Exception as e:
		print(f"    ✗ Error creating Store Settings: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Store Settings Creation Failed")





def create_default_categories():
	"""Create sample categories (optional)"""
	try:
		print("  → Creating default categories...")
		# Implementation here if needed
		print("    ℹ Default categories skipped (implement if needed)")
	except Exception as e:
		print(f"    ✗ Error creating categories: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Categories Creation Failed")


# ============================================================================
# CLEANUP
# ============================================================================

def remove_custom_roles():
	"""
	Optional: Remove custom roles during uninstallation
	WARNING: Only remove if roles are not assigned to users
	"""
	try:
		print("  → Removing custom roles...")
		
		roles = ["Store Manager", "Warehouse Staff", "Inventory Admin", "Store Viewer"]
		
		for role_name in roles:
			if frappe.db.exists("Role", role_name):
				# Check if role is assigned to any user
				user_count = frappe.db.count("Has Role", {"role": role_name})
				if user_count == 0:
					frappe.delete_doc("Role", role_name, force=True)
					print(f"    ✓ Removed role: {role_name}")
				else:
					print(f"    ℹ Role '{role_name}' is assigned to {user_count} user(s), skipping...")
		
	except Exception as e:
		print(f"    ✗ Error removing roles: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Roles Removal Failed")
