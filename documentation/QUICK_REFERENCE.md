# Quick Reference - Technical Store System

## Essential Commands

**Site:** test.local  
**App Version:** v0.0.1  
**Frappe Version:** v15.91.0

### Installation
```bash
bench get-app [git-url]                                      # Get app from repository
bench --site test.local install-app technical_store_system   # Install app (modular installer runs)
bench --site test.local uninstall-app technical_store_system # Uninstall app (cleanup runs)
bench --site test.local list-apps                           # Check installed apps
```

### Development
```bash
bench start                              # Start server (http://test.local:8000)
bench restart                            # Restart after code changes
bench --site test.local migrate          # Run migrations (auto-discovers new DocTypes)
bench --site test.local clear-cache      # Clear cache
bench --site test.local console          # Python console
bench --site test.local mariadb          # Database console
```

### DocType Management (Auto-Discovery Pattern)
```bash
# Option 1: Add DocType file (Recommended - our modular pattern)
# 1. Create file: setup/doctypes/YourDocType.py
# 2. Define doctype dict (see DEVELOPMENT.md for template)
# 3. Run: bench --site test.local migrate
# No installer changes needed - auto-discovered!

# Option 2: Use Frappe UI (then export)
bench --site test.local set-config developer_mode 1  # Enable developer mode
# Create via UI, then export to Python file
bench --site test.local export-doc --name "Your DocType"
```

### Testing
```bash
bench --site [site] run-tests --app technical_store_system                    # All tests
bench --site [site] run-tests --app technical_store_system --doctype "Store Item"  # Specific test
```

### Backup & Restore
```bash
# Backup database with files
bench --site [site] backup --with-files

# List backups
ls -lh ~/frappe-bench/sites/[site]/private/backups/

# Restore from backup
bench --site [site] restore [backup-file.sql.gz]
```

### Git Workflow
```bash
git checkout -b feature/feature-name     # New feature branch
git commit -m "feat: description"        # Commit changes
git tag -a v0.1.0 -m "Release v0.1.0"   # Tag release
```

## Current DocTypes (Phase 0 Complete)

### Installed & Working
1. **Store Settings** (Single DocType)
   - Route: `/app/store-settings`
   - Sections: General, Stock, Pricing, ERPNext Integration, Notifications, Advanced
   - File: `setup/doctypes/StoreSettings.py`

2. **Store Item** (Basic - to be enhanced in Phase 1)
   - Route: `/app/store-item`
   - Fields: item_name, description
   - File: `setup/doctypes/StoreItem.py`

3. **Store Location** (Basic - to be enhanced in Phase 1)
   - Route: `/app/store-location`
   - Fields: location_name, location_type, address
   - File: `setup/doctypes/StoreLocation.py`

### Roles Created
- Store Manager (full access)
- Warehouse Staff (operational)
- Inventory Admin (configuration)
- Store Viewer (read-only)

## DocType Creation Checklist (Modular Pattern)

When adding a new DocType:

1. ✅ Use "Store" prefix (e.g., Store UOM, Store Supplier)
2. ✅ Create file: `setup/doctypes/YourDocType.py`
3. ✅ Define doctype dict with fields, permissions (see DEVELOPMENT.md)
4. ✅ Set `custom: 1` (no developer mode needed)
5. ✅ Set `issingle: 1` if Single DocType
6. ✅ Configure autoname pattern
7. ✅ Add required fields and validations
8. ✅ Configure permissions for roles
9. ✅ Run `bench --site test.local migrate` (auto-discovers!)
10. ✅ Test in UI (create, edit, list)
11. ✅ Verify in database
12. ✅ Commit to git
13. ✅ Update IMPLEMENTATION_CHECKLIST.md

## Testing Checklist

After adding feature:

1. ✅ Backend: `bench migrate` without errors
2. ✅ UI: Can access DocType in desk
3. ✅ Create: Can create new record
4. ✅ Save: Can save without errors
5. ✅ List: Records appear in list view
6. ✅ Edit: Can modify and save
7. ✅ Console: No errors (F12)
8. ✅ Logs: No errors in bench logs
9. ✅ Old Features: Still working
10. ✅ Performance: Acceptable load time

## Code Patterns

### Get/Create Document
```python
# Get
doc = frappe.get_doc("Store Item", "ITEM-001")

# Create
doc = frappe.new_doc("Store Item")
doc.item_name = "Test"
doc.insert()
```

### Query Database
```python
# Get all
items = frappe.get_all("Store Item",
    fields=["name", "item_name"],
    filters={"disabled": 0},
    order_by="item_name"
)

# Get value
qty = frappe.db.get_value("Store Stock Balance",
    {"item": "ITEM-001"},
    "quantity"
)

# Check exists
if frappe.db.exists("Store Item", "ITEM-001"):
    pass
```

### API Method
```python
@frappe.whitelist()
def get_stock(item_code):
    # Check permission
    if not frappe.has_permission("Store Stock Balance", "read"):
        frappe.throw("Not permitted")
    
    # Validate
    if not item_code:
        frappe.throw("Item required")
    
    # Query
    return frappe.get_all("Store Stock Balance",
        filters={"item": item_code}
    )
```

### Error Handling
```python
try:
    doc.save()
except frappe.ValidationError:
    frappe.throw("Invalid data")
except Exception as e:
    frappe.log_error(frappe.get_traceback())
    frappe.throw("Error occurred")
```

## ERPNext Integration (Optional)

```python
from technical_store_system.utils.erpnext_integration import is_erpnext_installed

# Check before using
if is_erpnext_installed():
    # Safe to use ERPNext features
    pass
else:
    # Use standalone features
    pass
```

## Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| DocType | PascalCase + Store prefix | Store Item |
| File | snake_case | store_item.py |
| Field | snake_case | item_code |
| Function | snake_case | get_stock_balance() |
| Class | PascalCase | StoreItem |
| Variable | snake_case | stock_quantity |

## Indentation Rules

- **Python/JS/CSS/HTML**: TABS (4 spaces visual)
- **JSON**: 2 SPACES
- See `.editorconfig`

## Error Locations

```bash
# Browser Console
F12 → Console tab

# Bench Logs
tail -f logs/bench.log

# Site Error Log
tail -f sites/[site]/logs/error.log

# Frappe Error Log (UI)
Tools → Error Log
```

## Progress Tracking Format

```
✅ Store Item - Working
✅ Store Location - Working
⏳ Store Stock Entry - In Progress
⬜ Store Supplier - Not Started
❌ Feature X - Blocked: [reason]
```

## Git Commit Prefixes

- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `docs:` Documentation
- `test:` Tests
- `chore:` Maintenance

## Troubleshooting Quick Fixes

```bash
# App not showing
bench --site [site] clear-cache
bench --site [site] rebuild-doctype-for-desk

# Import errors
bench restart

# Permission issues
bench --site [site] set-admin-password [password]

# Schema mismatch
bench --site [site] migrate
```

## Safety Rules

❌ NEVER:
- Modify without reading code
- Use spaces instead of tabs
- Create DocTypes manually
- Use ERPNext DocTypes directly
- Hardcode values
- Skip testing

✅ ALWAYS:
- Read file before editing
- Use TABS for indentation
- Use `bench new-doctype`
- Create Store* DocTypes
- Test immediately
- One feature at a time

## Resources

- Full Guide: [DEVELOPMENT.md](DEVELOPMENT.md)
- AI Guidelines: [.cursorrules](.cursorrules)
- Frappe Docs: https://frappeframework.com/docs
