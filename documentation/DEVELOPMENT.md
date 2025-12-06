# Development Guide - Technical Store System

## Quick Start

### Initial Setup
```bash
# Navigate to bench directory
cd ~/frappe-bench

# Install app
bench --site [site] install-app technical_store_system

# Start development
bench start
```

### Development Workflow

#### 1. Before Starting Work
```bash
# Create backup/snapshot
sudo zfs snapshot zstore/frappe-bench@before-work-$(date +%Y%m%d)

# Create feature branch
git checkout -b feature/your-feature-name

# Verify current state
bench --site [site] migrate
bench --site [site] clear-cache
```

#### 2. Adding New DocType (Auto-Discovery Pattern)

**Our modular system auto-discovers DocTypes - no installer changes needed!**

```bash
# Step 1: Create new DocType file in setup/doctypes/
# Example: setup/doctypes/StoreUOM.py

# Step 2: Define DocType structure (see template below)

# Step 3: Run migrate to install
bench --site test.local migrate

# The system automatically:
# - Discovers the new .py file
# - Reads the doctype definition
# - Creates the DocType in database
# - Sets up fields and permissions

# No changes to installer.py needed!
```

**DocType Template:**
```python
# File: technical_store_system/setup/doctypes/YourDocType.py

doctype = {
    "name": "Your DocType",
    "module": "Technical Store System",
    "custom": 1,  # Custom DocTypes (no developer mode needed)
    "issingle": 0,  # Set to 1 for Single DocTypes
    "is_submittable": 0,  # Set to 1 if needs Submit workflow
    "is_tree": 0,  # Set to 1 for tree/nested structure
    "autoname": "format:YDT-{####}",  # Or "hash" or "field:fieldname"
    
    "fields": [
        {
            "fieldname": "field_name",
            "label": "Field Name",
            "fieldtype": "Data",  # Data, Link, Select, Int, Check, etc.
            "reqd": 1,  # Required field
            "in_list_view": 1,  # Show in list
        },
        # Add more fields...
    ],
    
    "permissions": [
        {
            "role": "Store Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        },
        # Add more permissions...
    ]
}
```

**Alternative: Use Frappe UI to create, then export definition**
```bash
# 1. Enable developer mode
bench --site test.local set-config developer_mode 1

# 2. Create DocType via UI (http://test.local:8000/app/doctype)

# 3. Export DocType definition
bench --site test.local export-doc --name "Your DocType"

# 4. Convert exported JSON to Python dict format
# 5. Place in setup/doctypes/YourDocType.py
# 6. Add to version control
```

#### 3. Testing Changes
```bash
# Run specific test
bench --site [site] run-tests --app technical_store_system --doctype "Store Item"

# Run all app tests
bench --site [site] run-tests --app technical_store_system

# Check console for errors (F12 in browser)
```

#### 4. Committing Changes
```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: Add Store Item DocType with validation"

# Push to remote
git push origin feature/your-feature-name
```

## Project Status Tracking

**See IMPLEMENTATION_CHECKLIST.md for complete roadmap (200+ tasks)**

### Current Implementation Status
```
✅ = Working and Tested
⏳ = In Progress  
⬜ = Not Started
❌ = Blocked/Error
```

### Phase 0: Foundation (✅ COMPLETED)
- ✅ Modular installer with auto-discovery (`installer.py`)
- ✅ Workspace setup (`setup/workspace_setup.py`)
- ✅ DocTypes auto-discovery (`setup/doctypes_setup.py`)
- ✅ Basic roles (Store Manager, Warehouse Staff, Inventory Admin, Store Viewer)
- ✅ Store Settings (Single DocType with 6 sections, 30+ fields)
- ✅ Store Item (basic version - to be enhanced)
- ✅ Store Location (basic version - to be enhanced)

### Phase 1: Core Masters (⏳ NEXT - Priority 1)
**Module 1: Item & Stock Management Masters**
- ⬜ Store UOM (Unit of Measure)
- ⬜ Store Item Group (Category with tree structure)
- ⬜ Store Brand
- ⬜ Store Unit (Store/Warehouse/Branch)
- ⏳ Store Item (enhanced with full fields)
- ⏳ Store Location (enhanced with physical location)
- ⬜ Stock Level (real-time stock tracking)
- ⬜ Stock Ledger Entry (immutable transaction log)

**Module 2: Supplier & Vendor Management**
- ⬜ Store Supplier
- ⬜ Supplier Item Price

**Module 3: Serial & Batch Tracking**
- ⬜ Store Serial Number
- ⬜ Store Batch

### Phase 2-9: Operational Modules (⬜ Planned)
- ⬜ Demand Management (Demand Request + Items)
- ⬜ Issue & Return Management
- ⬜ Inter-Store Transfer (Request/Issue/Receive)
- ⬜ Purchase Management (Suggestion + Receipt)
- ⬜ Analytics & Intelligence (Usage Log, Forecasting, Alerts)
- ⬜ Mobile & Barcode Integration
- ⬜ Budget & Cost Control
- ⬜ Asset Management
- ⬜ Compliance & Audit Trail

**Progress:** 7 of 200+ tasks complete (~3%)  
**Based on:** TECHNICAL_STORE_SINGLE_DOC.md specification
- ⬜ Store Category
- ⬜ Store Brand

#### Reports & Analytics
- ⬜ Stock Summary Report
- ⬜ Stock Movement Report
- ⬜ Low Stock Alert Report
- ⬜ Supplier Performance Report
- ⬜ Store Analytics Dashboard

#### Mobile & Integration
- ⬜ Mobile API
- ⬜ Barcode Scanner
- ⬜ ERPNext Sync (Optional)

#### Compliance
- ⬜ Store Audit Log
- ⬜ Store Compliance Report

## Useful Commands Reference

### Development
```bash
# Start bench
bench start

# Restart after code changes
bench restart

# Watch logs
bench --site [site] --verbose

# Python console
bench --site [site] console
```

### Database
```bash
# Migrate database
bench --site [site] migrate

# Backup
bench --site [site] backup --with-files

# Restore
bench --site [site] restore [backup-file.sql.gz]

# MariaDB console
bench --site [site] mariadb
```

### Cache & Build
```bash
# Clear cache
bench --site [site] clear-cache

# Rebuild desk
bench --site [site] rebuild-doctype-for-desk

# Build assets
bench build --app technical_store_system
```

### Testing
```bash
# Run all tests
bench --site [site] run-tests --app technical_store_system

# Run specific DocType tests
bench --site [site] run-tests --app technical_store_system --doctype "Store Item"

# With coverage
bench --site [site] run-tests --app technical_store_system --coverage
```

### Fixtures & Export
```bash
# Export fixtures
bench --site [site] export-fixtures

# Export specific DocType
bench --site [site] export-doc "Store Settings"
```

## Backup Strategy

### Before Major Changes
```bash
# ZFS snapshot
sudo zfs snapshot zstore/frappe-bench@pre-$(date +%Y%m%d-%H%M)

# Database backup
bench --site [site] backup --with-files
```

### Daily Backups (Automated)
```bash
# Add to crontab
0 2 * * * cd ~/frappe-bench && bench --site [site] backup --with-files
0 3 * * * sudo zfs snapshot zstore/frappe-bench@daily-$(date +\%Y\%m\%d)
```

### Restore If Needed
```bash
# Rollback ZFS snapshot
sudo zfs rollback zstore/frappe-bench@pre-2025-12-06

# Restore database
bench --site [site] restore ~/frappe-bench/sites/[site]/private/backups/[backup-file.sql.gz]
```

## Git Workflow

### Branch Naming
```
feature/store-item-doctype
bugfix/stock-calculation-error
hotfix/critical-login-issue
refactor/cleanup-api-code
```

### Commit Message Format
```
feat: Add Store Item DocType
fix: Correct stock balance calculation
refactor: Simplify API error handling
docs: Update README with setup instructions
test: Add unit tests for Store Item
chore: Update dependencies
```

### Release Tagging
```bash
# Tag stable release
git tag -a v0.1.0 -m "Release v0.1.0 - Core DocTypes working"
git push origin v0.1.0

# List tags
git tag -l
```

## Universal Installer System

### Installation Architecture

The app uses a **modular installer system** with three components:

1. **hooks.py** - App lifecycle hooks
2. **installer.py** - Universal orchestrator
3. **setup/** - Modular setup files

### Installation Hooks

```python
# In technical_store_system/hooks.py
after_install = "technical_store_system.installer.after_install"
after_uninstall = "technical_store_system.installer.after_uninstall"
after_migrate = "technical_store_system.installer.after_migrate"
```

### Installer.py Structure

The `technical_store_system/installer.py` orchestrates all installation tasks:

```python
import frappe
from frappe import _
from technical_store_system.setup import workspace_setup

def after_install():
	"""Universal installer - runs after app installation"""
	try:
		print("\n🚀 Installing Technical Store System...")
		
		# 1. Install workspace
		install_workspace()
		
		# 2. Create default roles
		create_default_roles()
		
		# 3. Create Store Settings
		create_store_settings()
		
		# 4. Install default UOMs
		install_default_uoms()
		
		print("✅ Technical Store System installed successfully!")
		frappe.db.commit()
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Installation Failed")
		print(f"❌ Installation error: {str(e)}")
		raise

def install_workspace():
	"""Install Technical Store System workspace"""
	try:
		print("  📋 Installing workspace...")
		workspace_setup.install()
		print("  ✅ Workspace installed")
	except Exception as e:
		print(f"  ⚠️ Workspace installation error: {str(e)}")
		frappe.log_error(frappe.get_traceback(), "Workspace Installation Error")

def create_default_roles():
	"""Create Store Manager, Warehouse Staff, etc."""
	roles = [
		{"role_name": "Store Manager", "desk_access": 1},
		{"role_name": "Warehouse Staff", "desk_access": 1},
		{"role_name": "Inventory Admin", "desk_access": 1},
		{"role_name": "Store Viewer", "desk_access": 1}
	]
	
	for role_data in roles:
		if not frappe.db.exists("Role", role_data["role_name"]):
			role = frappe.new_doc("Role")
			role.role_name = role_data["role_name"]
			role.desk_access = role_data["desk_access"]
			role.insert(ignore_permissions=True)
			print(f"✓ Created role: {role.role_name}")

def create_store_settings():
	"""Create Store Settings with defaults"""
	if not frappe.db.exists("Store Settings", "Store Settings"):
		settings = frappe.new_doc("Store Settings")
		settings.enable_erpnext_sync = 0
		settings.allow_negative_stock = 0
		settings.insert(ignore_permissions=True)
		print("✓ Created Store Settings")

def install_default_uoms():
	"""Install default Units of Measure"""
	uoms = ["Piece", "Box", "Kg", "Liter", "Meter", "Dozen"]
	
	for uom_name in uoms:
		if not frappe.db.exists("Store UOM", uom_name):
			uom = frappe.new_doc("Store UOM")
			uom.uom_name = uom_name
			uom.insert(ignore_permissions=True)
			print(f"✓ Created UOM: {uom_name}")

def setup_default_permissions():
	"""Set up role permissions for DocTypes"""
	# Will be called after DocTypes are created
	pass

def create_default_categories():
	"""Create sample categories"""
	# Optional: Create default item categories
	pass
```

### Modular Setup System

Create individual setup files in `technical_store_system/setup/`:

```
setup/
├── __init__.py
├── workspace/
│   ├── __init__.py
│   └── Workspace.py              # Workspace definition
├── workspace_setup.py             # Workspace installer
├── roles_setup.py                 # (Future) Roles installer
├── settings_setup.py              # (Future) Settings installer
└── uom_setup.py                   # (Future) UOM installer
```

### Workspace Setup Example

**setup/workspace/Workspace.py** - Workspace definition:
```python
workspace = {
	"name": "Technical Store System",
	"title": "Technical Store System",
	"icon": "store",
	"category": "Modules",
	"shortcuts": [
		{"label": "Store Item", "type": "DocType", "doc_type": "Store Item"},
		{"label": "Store Location", "type": "DocType", "doc_type": "Store Location"},
		# ... more shortcuts
	],
	"cards": [
		{
			"label": "Inventory Management",
			"items": [
				{"type": "DocType", "name": "Store Item", "label": "Store Item"},
				# ... more items
			]
		}
	]
}
```

**setup/workspace_setup.py** - Installer:
```python
import frappe
from .workspace.Workspace import workspace

def install():
	"""Install workspace"""
	if not frappe.db.exists("Workspace", workspace["name"]):
		doc = frappe.new_doc("Workspace")
		doc.update(workspace)
		doc.insert(ignore_permissions=True)
	else:
		update()

def update():
	"""Update existing workspace"""
	doc = frappe.get_doc("Workspace", workspace["name"])
	doc.update(workspace)
	doc.save(ignore_permissions=True)

def uninstall():
	"""Remove workspace"""
	if frappe.db.exists("Workspace", workspace["name"]):
		frappe.delete_doc("Workspace", workspace["name"], force=True)
```

### Uninstaller in installer.py

```python
def after_uninstall():
	"""Universal uninstaller - runs after app uninstallation"""
	try:
		print("\n🗑️ Uninstalling Technical Store System...")
		
		# 1. Uninstall workspace
		uninstall_workspace()
		
		# 2. Clear caches
		frappe.clear_cache()
		
		print("✅ Technical Store System uninstalled successfully!")
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Uninstallation Failed")
		print(f"❌ Uninstallation error: {str(e)}")

def uninstall_workspace():
	"""Uninstall Technical Store System workspace"""
	try:
		print("  📋 Uninstalling workspace...")
		workspace_setup.uninstall()
		print("  ✅ Workspace uninstalled")
	except Exception as e:
		print(f"  ⚠️ Workspace uninstallation error: {str(e)}")
```

### Fixtures Directory Structure

```
technical_store_system/
└── fixtures/
    ├── custom_field.json         # Custom fields
    ├── property_setter.json      # Property overrides
    ├── role.json                 # Roles (if using fixtures)
    └── workflow.json             # Workflows (if needed)
```

### Using Fixtures in hooks.py

```python
# In hooks.py
fixtures = [
	{
		"doctype": "Custom Field",
		"filters": [["module", "=", "Technical Store System"]]
	},
	{
		"doctype": "Property Setter",
		"filters": [["module", "=", "Technical Store System"]]
	}
]
```

### Testing Installation

```bash
# Test installation
bench --site [site] install-app technical_store_system

# Check what was created
bench --site [site] console
>>> frappe.get_all("Role", filters={"role_name": ["like", "Store%"]})
>>> frappe.db.exists("Store Settings", "Store Settings")

# Test uninstallation
bench --site [site] uninstall-app technical_store_system
```

### Installation Best Practices

1. ✅ **Use install.py** for all initial setup
2. ✅ **Check existence** before creating (avoid duplicates)
3. ✅ **Use ignore_permissions=True** during install
4. ✅ **Commit after success** (`frappe.db.commit()`)
5. ✅ **Log errors** for debugging
6. ✅ **Print progress** for user feedback
7. ✅ **Handle failures gracefully**
8. ✅ **Test on fresh site** before distributing

## Troubleshooting

### Common Issues

#### App not appearing in desk
```bash
bench --site [site] clear-cache
bench --site [site] rebuild-doctype-for-desk
```

#### Import errors
```bash
bench restart
bench --site [site] migrate
```

#### Permission errors
```bash
# Reset permissions
bench --site [site] set-admin-password [password]
```

#### Database schema mismatch
```bash
bench --site [site] migrate --skip-failing
bench --site [site] console
>>> frappe.reload_doctype("Store Item")
```

### Error Logs Location
```bash
# Bench logs
tail -f logs/bench.log

# Site error log
tail -f sites/[site]/logs/error.log

# Web error log (in desk)
Tools → Error Log
```

## Performance Tips

### Database Indexing
Add to DocType JSON:
```json
{
  "fieldname": "item_code",
  "fieldtype": "Data",
  "db_index": 1
}
```

### Caching Expensive Queries
```python
# Cache for 1 hour
@frappe.whitelist()
def get_stock_summary():
	cache_key = "stock_summary"
	data = frappe.cache().get_value(cache_key)
	
	if not data:
		data = frappe.get_all("Store Stock Balance", ...)
		frappe.cache().set_value(cache_key, data, expires_in_sec=3600)
	
	return data
```

### Background Jobs
```python
# For heavy operations
frappe.enqueue(
	method="technical_store_system.utils.stock_utils.recalculate_all_stock",
	queue="long",
	timeout=3600
)
```

## Resources

- [Frappe Documentation](https://frappeframework.com/docs)
- [Frappe Forum](https://discuss.frappe.io/)
- [ERPNext Documentation](https://docs.erpnext.com/) (for optional integration)
- Project Guidelines: `.cursorrules`
- API Documentation: `API.md` (create as needed)

## Notes

- Always test in development before production
- Keep backups before major changes
- Follow one-feature-at-a-time approach
- Document complex business logic
- Update this file as project evolves
