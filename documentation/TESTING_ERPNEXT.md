# Testing ERPNext Integration

## Quick Toggle Commands

### To ENABLE ERPNext integration for testing:
```bash
cd /home/erpnext/frappe-bench
bench --site test.local console << 'EOF'
frappe.db.set_value("Store Settings", "Store Settings", "erpnext_installed", "Installed")
frappe.db.commit()
print("✅ ERPNext integration ENABLED")
EOF
```

### To DISABLE ERPNext integration (back to default):
```bash
cd /home/erpnext/frappe-bench
bench --site test.local console << 'EOF'
frappe.db.set_value("Store Settings", "Store Settings", "erpnext_installed", "Not Installed")
frappe.db.commit()
print("✅ ERPNext integration DISABLED")
EOF
```

## What This Controls

**When ERPNext Status = "Not Installed":**
- Shows message: "ℹ️ ERPNext Not Installed"
- Hides all integration checkboxes
- User cannot enable sync features

**When ERPNext Status = "Installed":**
- Hides the "not installed" message
- Shows "Enable ERPNext Integration" checkbox
- User can enable/disable integration
- Shows sync options (Company, Items, Stock) when enabled

## Location in UI
- Store Settings → Advanced tab → ERPNext Integration section (collapsible)

## How It Works
- The controller (`store_settings_controller.py`) automatically checks if ERPNext is installed on save
- You can manually override the status using the commands above for testing
- The field visibility uses `depends_on: "eval:doc.erpnext_installed=='Installed'"`
