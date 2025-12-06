"""
Workspace Setup Module
Handles installation, update, and uninstallation of Technical Store System workspace
"""

import frappe
from frappe import _


def install():
	"""Install workspace during app installation"""
	try:
		print("  → Installing workspace...")
		
		from technical_store_system.setup.workspace.Workspace import workspace
		
		# Check if workspace already exists
		if frappe.db.exists("Workspace", workspace["name"]):
			print(f"    ✓ Workspace '{workspace['name']}' already exists, updating...")
			update()
			return
		
		# Create new workspace
		workspace_doc = frappe.new_doc("Workspace")
		
		# Set basic properties
		workspace_doc.name = workspace["name"]
		workspace_doc.title = workspace["title"]
		workspace_doc.icon = workspace.get("icon", "folder-open")
		workspace_doc.is_hidden = workspace.get("is_hidden", 0)
		workspace_doc.public = workspace.get("public", 1)
		workspace_doc.module = workspace.get("module", "Technical Store System")
		workspace_doc.label = workspace.get("label", workspace["title"])
		workspace_doc.hide_custom = workspace.get("hide_custom", 0)
		workspace_doc.content = workspace.get("content", "[]")
		
		# Add shortcuts
		for shortcut in workspace.get("shortcuts", []):
			workspace_doc.append("shortcuts", {
				"type": shortcut["type"],
				"label": shortcut["label"],
				"doc_type": shortcut.get("doc_type"),
				"link_to": shortcut.get("link_to"),
				"color": shortcut.get("color", "#3498db"),
			})
		
		# Add links (Card Breaks and Links)
		for link in workspace.get("links", []):
			workspace_doc.append("links", {
				"type": link["type"],
				"label": link["label"],
				"link_type": link.get("link_type", ""),
				"link_to": link.get("link_to", ""),
				"description": link.get("description", ""),
				"hidden": link.get("hidden", 0),
			})
		
		# Insert workspace
		workspace_doc.insert(ignore_permissions=True)
		print(f"    ✓ Workspace '{workspace['name']}' created successfully")
		
	except Exception as e:
		print(f"    ✗ Error installing workspace: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Workspace Installation Failed")
		# Don't raise - allow installation to continue


def update():
	"""Update existing workspace with latest configuration"""
	try:
		print("  → Updating workspace...")
		
		from technical_store_system.setup.workspace.Workspace import workspace
		
		if not frappe.db.exists("Workspace", workspace["name"]):
			print(f"    ℹ Workspace '{workspace['name']}' doesn't exist, installing...")
			install()
			return
		
		# Get existing workspace
		workspace_doc = frappe.get_doc("Workspace", workspace["name"])
		
		# Update basic properties
		workspace_doc.title = workspace["title"]
		workspace_doc.icon = workspace.get("icon", workspace_doc.icon)
		workspace_doc.is_hidden = workspace.get("is_hidden", 0)
		workspace_doc.public = workspace.get("public", 1)
		workspace_doc.hide_custom = workspace.get("hide_custom", 0)
		workspace_doc.content = workspace.get("content", "[]")
		
		# Clear and rebuild shortcuts
		workspace_doc.shortcuts = []
		for shortcut in workspace.get("shortcuts", []):
			workspace_doc.append("shortcuts", {
				"type": shortcut["type"],
				"label": shortcut["label"],
				"doc_type": shortcut.get("doc_type"),
				"link_to": shortcut.get("link_to"),
				"color": shortcut.get("color", "#3498db"),
			})
		
		# Clear and rebuild links
		workspace_doc.links = []
		
		for link in workspace.get("links", []):
			workspace_doc.append("links", {
				"type": link["type"],
				"label": link["label"],
				"link_type": link.get("link_type", ""),
				"link_to": link.get("link_to", ""),
				"icon": link.get("icon", ""),
				"description": link.get("description", ""),
			})
		
		# Save changes
		workspace_doc.save(ignore_permissions=True)
		print(f"    ✓ Workspace '{workspace['name']}' updated successfully")
		
	except Exception as e:
		print(f"    ✗ Error updating workspace: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Workspace Update Failed")


def uninstall():
	"""Remove workspace during app uninstallation"""
	try:
		print("  → Uninstalling workspace...")
		
		from technical_store_system.setup.workspace.Workspace import workspace
		
		if frappe.db.exists("Workspace", workspace["name"]):
			frappe.delete_doc("Workspace", workspace["name"], force=True, ignore_permissions=True)
			print(f"    ✓ Workspace '{workspace['name']}' removed successfully")
		else:
			print(f"    ℹ Workspace '{workspace['name']}' not found, skipping...")
		
	except Exception as e:
		print(f"    ✗ Error uninstalling workspace: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Workspace Uninstallation Failed")
