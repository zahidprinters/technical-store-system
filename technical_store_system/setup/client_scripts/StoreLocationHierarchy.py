"""
Store Location Hierarchy Client Script
Provides cascading dropdown filters for hierarchical location selection
"""

client_script = {
	"name": "Store Location - Hierarchical Filters",
	"dt": "Store Location",
	"script_type": "Form",
	"enabled": 1,
	"script": """
// Store Location Hierarchical Filtering
// Provides cascading dropdowns: Store → Zone → Rack → Shelf → Bin

frappe.ui.form.on('Store Location', {
	refresh: function(frm) {
		// Set up filters for hierarchical location fields
		setup_location_filters(frm);
		update_field_visibility(frm);
		control_field_access(frm);
		preview_location_code(frm);
	},
	
	location_type: function(frm) {
		// Clear child fields based on selected type
		clear_child_fields(frm);
		
		// Update visibility and filters when location type changes
		setup_location_filters(frm);
		update_field_visibility(frm);
		control_field_access(frm);
		preview_location_code(frm);
	},
	
	warehouse_name: function(frm) {
		preview_location_code(frm);
	},
	
	zone_name: function(frm) {
		preview_location_code(frm);
	},
	
	rack_name: function(frm) {
		preview_location_code(frm);
	},
	
	shelf_name: function(frm) {
		preview_location_code(frm);
	},
	
	store: function(frm) {
		// Clear child selections when parent changes
		if (frm.doc.zone) {
			frm.set_value('zone', '');
		}
		if (frm.doc.rack) {
			frm.set_value('rack', '');
		}
		if (frm.doc.shelf) {
			frm.set_value('shelf', '');
		}
		if (frm.doc.bin) {
			frm.set_value('bin', '');
		}
		setup_location_filters(frm);
		control_field_access(frm);
		preview_location_code(frm);
	},
	
	zone: function(frm) {
		// Clear child selections when parent changes
		if (frm.doc.rack) {
			frm.set_value('rack', '');
		}
		if (frm.doc.shelf) {
			frm.set_value('shelf', '');
		}
		if (frm.doc.bin) {
			frm.set_value('bin', '');
		}
		setup_location_filters(frm);
		control_field_access(frm);
		preview_location_code(frm);
	},
	
	rack: function(frm) {
		// Clear child selections when parent changes
		if (frm.doc.shelf) {
			frm.set_value('shelf', '');
		}
		if (frm.doc.bin) {
			frm.set_value('bin', '');
		}
		setup_location_filters(frm);
		control_field_access(frm);
		preview_location_code(frm);
	},
	
	shelf: function(frm) {
		// Clear child selections when parent changes
		if (frm.doc.bin) {
			frm.set_value('bin', '');
		}
		setup_location_filters(frm);
		control_field_access(frm);
		preview_location_code(frm);
	},
	
	bin: function(frm) {
		preview_location_code(frm);
	}
});

function setup_location_filters(frm) {
	// Filter Store field - show only Warehouse type locations
	frm.set_query('store', function() {
		return {
			filters: {
				'location_type': 'Warehouse',
				'enabled': 1
			}
		};
	});
	
	// Filter Zone field - show only Zone type locations that belong to selected store
	frm.set_query('zone', function() {
		let filters = {
			'location_type': 'Zone',
			'enabled': 1
		};
		
		if (frm.doc.store) {
			// Filter zones where store field matches selected store
			filters['store'] = frm.doc.store;
		}
		
		return { filters: filters };
	});
	
	// Filter Rack field - show only Rack type locations in selected zone
	frm.set_query('rack', function() {
		let filters = {
			'location_type': 'Rack',
			'enabled': 1
		};
		
		if (frm.doc.store) {
			filters['store'] = frm.doc.store;
		}
		
		if (frm.doc.zone) {
			// Filter racks where zone field matches selected zone
			filters['zone'] = frm.doc.zone;
		}
		
		return { filters: filters };
	});
	
	// Filter Shelf field - show only Shelf type locations in selected rack
	frm.set_query('shelf', function() {
		let filters = {
			'location_type': 'Shelf',
			'enabled': 1
		};
		
		if (frm.doc.store) {
			filters['store'] = frm.doc.store;
		}
		
		if (frm.doc.zone) {
			filters['zone'] = frm.doc.zone;
		}
		
		if (frm.doc.rack) {
			// Filter shelves where rack field matches selected rack
			filters['rack'] = frm.doc.rack;
		}
		
		return { filters: filters };
	});
	
	// Filter Bin field - show only Bin type locations in selected shelf
	frm.set_query('bin', function() {
		let filters = {
			'location_type': 'Bin',
			'enabled': 1
		};
		
		if (frm.doc.store) {
			filters['store'] = frm.doc.store;
		}
		
		if (frm.doc.zone) {
			filters['zone'] = frm.doc.zone;
		}
		
		if (frm.doc.rack) {
			filters['rack'] = frm.doc.rack;
		}
		
		if (frm.doc.shelf) {
			// Filter bins where shelf field matches selected shelf
			filters['shelf'] = frm.doc.shelf;
		}
		
		return { filters: filters };
	});
}

function clear_child_fields(frm) {
	// Clear only child fields based on location type
	// Keep parent fields, clear children
	const type = frm.doc.location_type;
	
	if (type === 'Warehouse') {
		// Top level - clear all
		frm.set_value('store', '');
		frm.set_value('zone', '');
		frm.set_value('rack', '');
		frm.set_value('shelf', '');
		frm.set_value('bin', '');
	} else if (type === 'Zone') {
		// Keep nothing, clear children
		frm.set_value('zone', '');
		frm.set_value('rack', '');
		frm.set_value('shelf', '');
		frm.set_value('bin', '');
	} else if (type === 'Rack') {
		// Keep store, clear children
		frm.set_value('rack', '');
		frm.set_value('shelf', '');
		frm.set_value('bin', '');
	} else if (type === 'Shelf') {
		// Keep store + zone, clear children
		frm.set_value('shelf', '');
		frm.set_value('bin', '');
	} else if (type === 'Bin') {
		// Keep store + zone + rack, clear bin
		frm.set_value('bin', '');
	}
}

function update_field_visibility(frm) {
	// Show/hide fields based on location type
	// Hierarchy logic:
	// - Warehouse: No parent fields (top level)
	// - Zone: Show Store only
	// - Rack: Show Store + Zone
	// - Shelf: Show Store + Zone + Rack
	// - Bin: Show Store + Zone + Rack + Shelf
	
	const location_type = frm.doc.location_type;
	
	// Zone: Show Store only
	if (location_type === 'Zone') {
		frm.set_df_property('store', 'hidden', 0);
		frm.set_df_property('store', 'reqd', 1);
	}
	
	// Rack: Show Store + Zone
	if (location_type === 'Rack') {
		frm.set_df_property('store', 'hidden', 0);
		frm.set_df_property('store', 'reqd', 1);
		frm.set_df_property('zone', 'hidden', 0);
		frm.set_df_property('zone', 'reqd', 1);
	}
	
	// Shelf: Show Store + Zone + Rack
	if (location_type === 'Shelf') {
		frm.set_df_property('store', 'hidden', 0);
		frm.set_df_property('store', 'reqd', 1);
		frm.set_df_property('zone', 'hidden', 0);
		frm.set_df_property('zone', 'reqd', 1);
		frm.set_df_property('rack', 'hidden', 0);
		frm.set_df_property('rack', 'reqd', 1);
	}
	
	// Bin: Show all parent fields
	if (location_type === 'Bin') {
		frm.set_df_property('store', 'hidden', 0);
		frm.set_df_property('store', 'reqd', 1);
		frm.set_df_property('zone', 'hidden', 0);
		frm.set_df_property('zone', 'reqd', 1);
		frm.set_df_property('rack', 'hidden', 0);
		frm.set_df_property('rack', 'reqd', 1);
		frm.set_df_property('shelf', 'hidden', 0);
		frm.set_df_property('shelf', 'reqd', 1);
	}
}

function control_field_access(frm) {
	// Disable fields until their parent is selected
	// This prevents selecting a zone without a store, etc.
	
	const location_type = frm.doc.location_type;
	
	// Zone field: only enabled if Store is selected
	if (['Zone', 'Rack', 'Shelf', 'Bin'].includes(location_type)) {
		if (frm.doc.store) {
			frm.set_df_property('zone', 'read_only', 0);
		} else {
			frm.set_df_property('zone', 'read_only', 1);
		}
	}
	
	// Rack field: only enabled if Zone is selected
	if (['Rack', 'Shelf', 'Bin'].includes(location_type)) {
		if (frm.doc.zone) {
			frm.set_df_property('rack', 'read_only', 0);
		} else {
			frm.set_df_property('rack', 'read_only', 1);
		}
	}
	
	// Shelf field: only enabled if Rack is selected
	if (['Shelf', 'Bin'].includes(location_type)) {
		if (frm.doc.rack) {
			frm.set_df_property('shelf', 'read_only', 0);
		} else {
			frm.set_df_property('shelf', 'read_only', 1);
		}
	}
}

function preview_location_code(frm) {
	// Live preview of auto-generated location_code
	let preview = '';
	const location_type = frm.doc.location_type;
	
	if (location_type === 'Warehouse') {
		preview = frm.doc.warehouse_name || '';
	}
	else if (location_type === 'Zone' && frm.doc.store && frm.doc.zone_name) {
		preview = frm.doc.store + '-' + frm.doc.zone_name;
	}
	else if (location_type === 'Rack' && frm.doc.zone && frm.doc.rack_name) {
		preview = frm.doc.zone + '-' + frm.doc.rack_name;
	}
	else if (location_type === 'Shelf' && frm.doc.rack && frm.doc.shelf_name) {
		preview = frm.doc.rack + '-' + frm.doc.shelf_name;
	}
	else if (location_type === 'Bin' && frm.doc.shelf && frm.doc.bin) {
		preview = frm.doc.shelf + '-' + frm.doc.bin;
	}
	
	// Update location_code field with preview
	if (preview && preview !== frm.doc.location_code) {
		frm.set_value('location_code', preview);
	}
}
"""
}
