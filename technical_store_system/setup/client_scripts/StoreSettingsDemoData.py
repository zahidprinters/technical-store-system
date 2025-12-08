"""
Store Settings Client Script
Handles button clicks and UI behavior for demo data management
"""

client_script = {
	"name": "Store Settings - Demo Data Manager",
	"dt": "Store Settings",
	"script_type": "Form",
	"enabled": 1,
	"script": """
frappe.ui.form.on('Store Settings', {
	refresh: function(frm) {
		// Setup Install Demo Data button
		frm.fields_dict.install_demo_data_btn.$input.off('click');
		frm.fields_dict.install_demo_data_btn.$input.on('click', () => {
			// Check if data exists
			check_data_exists(frm, (has_data, is_demo) => {
				if (has_data && !is_demo) {
					frappe.msgprint({
						title: 'Cannot Install',
						indicator: 'red',
						message: 'Real data already exists in the system. Cannot install demo data.'
					});
					return;
				}
				
				if (has_data && is_demo) {
					frappe.msgprint({
						title: 'Already Installed',
						indicator: 'orange',
						message: 'Demo data is already installed.'
					});
					return;
				}
				
				// Build list of selected items
				let selected_items = [];
				if (frm.doc.install_demo_uoms) selected_items.push('• UOMs (27 units)');
				if (frm.doc.install_demo_item_groups) selected_items.push('• Item Groups (19 categories)');
				if (frm.doc.install_demo_locations) selected_items.push('• Locations (11 warehouse positions)');
				
				if (selected_items.length === 0) {
					frappe.msgprint({
						title: 'No Selection',
						indicator: 'orange',
						message: 'Please check at least one data type to install:<br>• UOMs<br>• Item Groups<br>• Locations'
					});
					return;
				}
				
				// Confirm installation
				frappe.confirm(
					'<strong>Install selected demo data?</strong><br><br>' +
					'Selected data types:<br>' +
					selected_items.join('<br>') + '<br><br>' +
					'<em>Use this for testing and training purposes.</em>',
					() => {
						// Save form first to capture checkbox selections
						frm.save().then(() => {
							frappe.dom.freeze('Installing selected demo data...');
							frappe.call({
								method: 'technical_store_system.utils.controllers.store_settings_controller.install_demo_data',
								callback: (r) => {
									frappe.dom.unfreeze();
									if (r.message && r.message.success) {
										frappe.show_alert({
											message: r.message.message,
											indicator: 'green'
										}, 5);
										frm.reload_doc();
									}
								},
								error: (r) => {
									frappe.dom.unfreeze();
								}
							});
						});
					}
				);
			});
		});
		
		// Setup Remove Demo Data button
		frm.fields_dict.uninstall_demo_data_btn.$input.off('click');
		frm.fields_dict.uninstall_demo_data_btn.$input.on('click', () => {
			// Check if data exists
			check_data_exists(frm, (has_data, is_demo, counts) => {
				if (!has_data) {
					frappe.msgprint({
						title: 'No Data',
						indicator: 'blue',
						message: 'No data to remove.'
					});
					return;
				}
				
				if (!is_demo) {
					frappe.msgprint({
						title: 'Cannot Remove',
						indicator: 'red',
						message: `This doesn't appear to be demo data.<br><br>` +
							`Current data:<br>` +
							`• ${counts.uom} UOMs<br>` +
							`• ${counts.group} Item Groups<br>` +
							`• ${counts.location} Locations<br><br>` +
							`Expected demo data: 27 UOMs, 19 Groups, 11 Locations<br><br>` +
							`To prevent accidental data loss, only demo data can be auto-removed.`
					});
					return;
				}
				
				// Confirm removal
				frappe.confirm(
					'<strong style="color: #d9534f;">Remove all demo data?</strong><br><br>' +
					`This will delete:<br>` +
					`• ${counts.uom} UOMs<br>` +
					`• ${counts.group} Item Groups<br>` +
					`• ${counts.location} Locations<br><br>` +
					`<em style="color: #d9534f;">This action cannot be undone!</em>`,
					() => {
						frappe.dom.freeze('Removing demo data...');
						frappe.call({
							method: 'technical_store_system.utils.controllers.store_settings_controller.uninstall_demo_data',
							callback: (r) => {
								frappe.dom.unfreeze();
								if (r.message && r.message.success) {
									frappe.show_alert({
										message: r.message.message,
										indicator: 'green'
									}, 5);
									frm.reload_doc();
								}
							},
							error: (r) => {
								frappe.dom.unfreeze();
							}
						});
					}
				);
			});
		});
		
		// Update button states
		update_button_states(frm);
	},
	
	onload: function(frm) {
		update_button_states(frm);
	}
});

function check_data_exists(frm, callback) {
	frappe.call({
		method: 'frappe.client.get_count',
		args: { doctype: 'Store UOM' },
		callback: (r1) => {
			let uom_count = r1.message || 0;
			frappe.call({
				method: 'frappe.client.get_count',
				args: { doctype: 'Store Item Group' },
				callback: (r2) => {
					let group_count = r2.message || 0;
					frappe.call({
						method: 'frappe.client.get_count',
						args: { doctype: 'Store Location' },
						callback: (r3) => {
							let location_count = r3.message || 0;
							let has_data = uom_count > 0 || group_count > 0 || location_count > 0;
							let is_demo = (uom_count === 27 && group_count === 19 && location_count === 11);
							callback(has_data, is_demo, {
								uom: uom_count,
								group: group_count,
								location: location_count
							});
						}
					});
				}
			});
		}
	});
}

function update_button_states(frm) {
	check_data_exists(frm, (has_data, is_demo) => {
		let install_btn = frm.fields_dict.install_demo_data_btn.$input;
		let uninstall_btn = frm.fields_dict.uninstall_demo_data_btn.$input;
		
		if (has_data && !is_demo) {
			// Real data exists - disable both buttons
			install_btn.prop('disabled', true).css('opacity', '0.5');
			uninstall_btn.prop('disabled', true).css('opacity', '0.5');
			install_btn.attr('title', 'Disabled: Real data exists in system');
			uninstall_btn.attr('title', 'Disabled: Not demo data');
		} else if (has_data && is_demo) {
			// Demo data exists - disable install, enable uninstall
			install_btn.prop('disabled', true).css('opacity', '0.5');
			uninstall_btn.prop('disabled', false).css('opacity', '1');
			install_btn.attr('title', 'Disabled: Demo data already installed');
			uninstall_btn.attr('title', 'Click to remove demo data');
		} else {
			// No data - enable install, disable uninstall
			install_btn.prop('disabled', false).css('opacity', '1');
			uninstall_btn.prop('disabled', true).css('opacity', '0.5');
			install_btn.attr('title', 'Click to install demo data');
			uninstall_btn.attr('title', 'Disabled: No data to remove');
		}
	});
}
"""
}
