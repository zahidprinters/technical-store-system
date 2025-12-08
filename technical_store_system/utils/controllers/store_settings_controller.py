"""
Store Settings Controller
Handles button actions and validation for Store Settings
Uses centralized demo_data_handler for all demo data operations
"""

import frappe
from frappe.model.document import Document
from technical_store_system.utils.helpers.demo_data_handler import (
	get_demo_data_counts,
	check_demo_data_status
)


class StoreSettings(Document):
	"""Controller for Store Settings DocType"""
	
	def validate(self):
		"""Validate and update demo data status before save"""
		self.update_demo_data_status()
	
	def update_demo_data_status(self):
		"""Update HTML field showing current demo data status"""
		status_info = check_demo_data_status()
		counts = status_info["counts"]
		
		uom_count = counts["Store UOM"]["current"]
		group_count = counts["Store Item Group"]["current"]
		location_count = counts["Store Location"]["current"]
		item_count = counts.get("Store Item", {}).get("current", 0)
		
		has_data = uom_count > 0 or group_count > 0 or location_count > 0 or item_count > 0
		
		if not has_data:
			status_html = """
				<div style='padding: 10px; background: #f8f9fa; border-left: 4px solid #6c757d;'>
					<strong style='color: #6c757d;'>⚪ No Data</strong><br>
					<small>No UOMs, Item Groups, Locations, or Items exist. Click "Install Demo Data" to create samples.</small>
				</div>
			"""
		elif status_info["installed"]:
			status_html = f"""
				<div style='padding: 10px; background: #fff3cd; border-left: 4px solid #ffc107;'>
					<strong style='color: #856404;'>⚠️ Demo Data Installed</strong><br>
				<small>
					• <strong>{uom_count}</strong> UOMs ({counts["Store UOM"]["expected"]} demo UOMs)<br>
					• <strong>{group_count}</strong> Item Groups ({counts["Store Item Group"]["expected"]} demo groups)<br>
					• <strong>{location_count}</strong> Locations ({counts["Store Location"]["expected"]} demo locations)<br>
					• <strong>{item_count}</strong> Items ({counts.get("Store Item", {}).get("expected", 0)} demo items)<br>
					<em>Safe to remove if no transactions exist.</em>
				</small>
				</div>
			"""
		else:
			status_html = f"""
				<div style='padding: 10px; background: #d1ecf1; border-left: 4px solid #17a2b8;'>
					<strong style='color: #0c5460;'>✅ Real Data Exists</strong><br>
				<small>
					• <strong>{uom_count}</strong> UOMs<br>
					• <strong>{group_count}</strong> Item Groups<br>
					• <strong>{location_count}</strong> Locations<br>
					• <strong>{item_count}</strong> Items<br>
					<em style='color: #d9534f;'>⚠️ Demo data management disabled to prevent data loss.</em>
				</small>
				</div>
			"""
		
		self.demo_data_status = status_html


@frappe.whitelist()
def install_demo_data():
	"""Install selected demo/test data via button click"""
	try:
		from technical_store_system.utils.helpers.demo_data_handler import (
			install_demo_data_for_doctype
		)
		
		# Get Store Settings to check selections
		settings = frappe.get_single("Store Settings")
		
		# Build list of selected DocTypes
		selected_doctypes = []
		if settings.install_demo_uoms:
			selected_doctypes.append("Store UOM")
		if settings.install_demo_item_groups:
			selected_doctypes.append("Store Item Group")
		if settings.install_demo_locations:
			selected_doctypes.append("Store Location")
		if settings.install_demo_items:
			selected_doctypes.append("Store Item")
		
		if not selected_doctypes:
			frappe.throw(
				"Please select at least one data type to install!<br>"
				"Check the boxes for: UOMs, Item Groups, Locations, or Items.",
				title="No Selection"
			)
		
		# Install each selected type
		frappe.publish_realtime('msgprint', f'Installing {len(selected_doctypes)} data type(s)...', user=frappe.session.user)
		
		results = []
		total_created = 0
		
		for doctype in selected_doctypes:
			result = install_demo_data_for_doctype(doctype, force=True)
			if result["success"] and result["created"] > 0:
				results.append(f"• {result['created']} {doctype}")
				total_created += result["created"]
			elif not result["success"]:
				frappe.msgprint(f"⚠️ {result['message']}", indicator="orange")
		
		if total_created > 0:
			message = f"<strong>Demo data installed successfully!</strong><br><br>{'<br>'.join(results)}"
			return {
				"success": True,
				"message": message
			}
		else:
			return {
				"success": True,
				"message": "No new data was created. Data may already exist."
			}
		
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "Demo Data Installation Failed")
		frappe.throw(str(e), title="Installation Failed")


@frappe.whitelist()
def uninstall_demo_data():
	"""Remove demo/test data via button click - uses centralized handler"""
	try:
		from technical_store_system.utils.helpers.demo_data_handler import (
			uninstall_all_demo_data,
			check_demo_data_status
		)
		
		# Check if it looks like demo data (safety check)
		status_info = check_demo_data_status()
		
		if status_info["status"] == "not_installed":
			return {
				"success": True,
				"message": "No data to remove."
			}
		
		if status_info["status"] == "partial":
			counts = status_info["counts"]
			frappe.throw(
				"This doesn't appear to be demo data (counts don't match expected demo data).<br><br>"
				f"Current counts:<br>"
				f"• {counts['Store UOM']['current']} UOMs (expected {counts['Store UOM']['expected']})<br>"
				f"• {counts['Store Item Group']['current']} Item Groups (expected {counts['Store Item Group']['expected']})<br>"
				f"• {counts['Store Location']['current']} Locations (expected {counts['Store Location']['expected']})<br><br>"
				"To prevent accidental data loss, only demo data with exact counts can be auto-removed.",
				title="Not Demo Data"
			)
		
		# Remove all demo data
		frappe.publish_realtime('msgprint', 'Removing demo data...', user=frappe.session.user)
		result = uninstall_all_demo_data()
		
		if result["success"]:
			# Build success message
			messages = ["Demo data removed successfully!<br>"]
			for item in result["results"]:
				if item["result"]["deleted"] > 0:
					messages.append(f"• Deleted {item['result']['deleted']} {item['doctype']}")
			
			return {
				"success": True,
				"message": "<br>".join(messages)
			}
		else:
			frappe.throw("Removal failed. See error log for details.", title="Removal Failed")
		
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "Demo Data Removal Failed")
		frappe.throw(str(e), title="Removal Failed")
