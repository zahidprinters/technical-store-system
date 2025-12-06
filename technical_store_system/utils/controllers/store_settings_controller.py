"""
Store Settings Controller
Handles button actions and validation for Store Settings
"""

import frappe
from frappe.model.document import Document


class StoreSettings(Document):
	"""Controller for Store Settings DocType"""
	
	def validate(self):
		"""Validate and update demo data status before save"""
		self.update_demo_data_status()
	
	def update_demo_data_status(self):
		"""Update HTML field showing current demo data status"""
		uom_count = frappe.db.count("Store UOM")
		group_count = frappe.db.count("Store Item Group")
		location_count = frappe.db.count("Store Location")
		
		# Check if data is demo data or real data (heuristic: demo data has specific counts)
		is_likely_demo = (uom_count == 27 and group_count == 19 and location_count == 11)
		has_data = uom_count > 0 or group_count > 0 or location_count > 0
		
		if not has_data:
			status_html = """
				<div style='padding: 10px; background: #f8f9fa; border-left: 4px solid #6c757d;'>
					<strong style='color: #6c757d;'>⚪ No Data</strong><br>
					<small>No UOMs, Item Groups, or Locations exist. Click "Install Demo Data" to create samples.</small>
				</div>
			"""
		elif is_likely_demo:
			status_html = f"""
				<div style='padding: 10px; background: #fff3cd; border-left: 4px solid #ffc107;'>
					<strong style='color: #856404;'>⚠️ Demo Data Installed</strong><br>
					<small>
						• <strong>{uom_count}</strong> UOMs (27 demo UOMs)<br>
						• <strong>{group_count}</strong> Item Groups (19 demo groups)<br>
						• <strong>{location_count}</strong> Locations (11 demo locations)<br>
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
						<em style='color: #d9534f;'>⚠️ Demo data management disabled to prevent data loss.</em>
					</small>
				</div>
			"""
		
		self.demo_data_status = status_html


@frappe.whitelist()
def install_demo_data():
	"""Install demo/test data via button click"""
	try:
		# Check if data already exists
		uom_count = frappe.db.count("Store UOM")
		group_count = frappe.db.count("Store Item Group")
		location_count = frappe.db.count("Store Location")
		
		if uom_count > 0 or group_count > 0 or location_count > 0:
			frappe.throw(
				"Data already exists! Cannot install demo data when UOMs, Item Groups, or Locations exist.<br>"
				"Please remove existing data first or use 'Remove Demo Data' button.",
				title="Data Already Exists"
			)
		
		# Import installer functions
		from technical_store_system.setup.doctypes.StoreUOM import on_doctype_install as create_uoms
		from technical_store_system.setup.doctypes.StoreItemGroup import on_doctype_install as create_groups
		from technical_store_system.setup.doctypes.StoreLocation import on_doctype_install as create_locations
		
		# Create demo data (force=True bypasses the install_demo_data flag check)
		frappe.publish_realtime('msgprint', 'Creating demo UOMs...', user=frappe.session.user)
		create_uoms(force=True)
		
		frappe.publish_realtime('msgprint', 'Creating demo Item Groups...', user=frappe.session.user)
		create_groups(force=True)
		
		frappe.publish_realtime('msgprint', 'Creating demo Locations...', user=frappe.session.user)
		create_locations(force=True)
		
		# Commit all changes
		frappe.db.commit()
		
		return {
			"success": True,
			"message": "Demo data installed successfully!<br>• 27 UOMs<br>• 19 Item Groups<br>• 11 Locations"
		}
		
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "Demo Data Installation Failed")
		frappe.throw(str(e), title="Installation Failed")


@frappe.whitelist()
def uninstall_demo_data():
	"""Remove demo/test data via button click"""
	try:
		# Check for transactions (prevent data loss)
		# Add transaction checks here when transaction DocTypes are created
		
		uom_count = frappe.db.count("Store UOM")
		group_count = frappe.db.count("Store Item Group")
		location_count = frappe.db.count("Store Location")
		
		# Check if it looks like demo data (exact counts)
		is_demo = (uom_count == 27 and group_count == 19 and location_count == 11)
		
		if not is_demo and (uom_count > 0 or group_count > 0 or location_count > 0):
			frappe.throw(
				"This doesn't appear to be demo data (counts don't match expected demo data).<br>"
				f"Current: {uom_count} UOMs, {group_count} Item Groups, {location_count} Locations<br>"
				"Expected demo data: 27 UOMs, 19 Item Groups, 11 Locations<br><br>"
				"To prevent accidental data loss, only demo data with exact counts can be auto-removed.",
				title="Not Demo Data"
			)
		
		if uom_count == 0 and group_count == 0 and location_count == 0:
			return {
				"success": True,
				"message": "No data to remove."
			}
		
		# Delete demo data
		frappe.publish_realtime('msgprint', 'Removing demo Locations...', user=frappe.session.user)
		locations = frappe.get_all("Store Location", pluck="name")
		for loc in locations:
			frappe.delete_doc("Store Location", loc, force=1, ignore_permissions=True)
		
		frappe.publish_realtime('msgprint', 'Removing demo Item Groups...', user=frappe.session.user)
		groups = frappe.get_all("Store Item Group", pluck="name")
		for group in groups:
			frappe.delete_doc("Store Item Group", group, force=1, ignore_permissions=True)
		
		frappe.publish_realtime('msgprint', 'Removing demo UOMs...', user=frappe.session.user)
		uoms = frappe.get_all("Store UOM", pluck="name")
		for uom in uoms:
			frappe.delete_doc("Store UOM", uom, force=1, ignore_permissions=True)
		
		# Commit deletion
		frappe.db.commit()
		
		return {
			"success": True,
			"message": f"Demo data removed successfully!<br>Deleted: {len(uoms)} UOMs, {len(groups)} Item Groups, {len(locations)} Locations"
		}
		
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "Demo Data Removal Failed")
		frappe.throw(str(e), title="Removal Failed")
