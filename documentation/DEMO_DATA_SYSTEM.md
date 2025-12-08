# Demo Data System - Overview

## 📍 Architecture

All demo/test data is now centrally managed with clean separation between data and logic.

```
setup/demo_data/          ← ONLY DATA (pure Python files)
├── __init__.py
├── store_uom.py         ← DEMO_UOMS = [27 records]
├── store_item_group.py  ← DEMO_ITEM_GROUPS = [19 records]
└── store_location.py    ← DEMO_LOCATIONS = [11 records]

utils/helpers/
└── demo_data_handler.py  ← ALL LOGIC (install/uninstall functions)
```

## 🎯 Key Benefits

✅ **Clean Separation** - Data files contain ONLY data, no code  
✅ **Easy to Edit** - Change demo data without touching any code  
✅ **Centralized Logic** - All install/uninstall logic in one handler  
✅ **Scalable** - Add new demo data by creating new data file  
✅ **Type Safe** - Registry validates DocTypes and field names  

## 📝 How It Works

### 1. Demo Data Files (Pure Data)

**Example:** `setup/demo_data/store_uom.py`
```python
"""Store UOM Demo Data - 27 records"""

DEMO_UOMS = [
    {"uom_name": "Each", "uom_symbol": "Ea", ...},
    {"uom_name": "Kilogram", "uom_symbol": "Kg", ...},
    # ... 25 more
]
```

**No functions, no logic - just pure data!**

### 2. Demo Data Handler (All Logic)

**File:** `utils/helpers/demo_data_handler.py`

**Registry:**
```python
DEMO_DATA_REGISTRY = {
    "Store UOM": {
        "module": "technical_store_system.setup.demo_data.store_uom",
        "data_var": "DEMO_UOMS",
        "name_field": "uom_name",
        "count": 27
    },
    # ... more DocTypes
}
```

**Functions:**
- `install_demo_data_for_doctype(doctype_name, force=False)` - Install for one DocType
- `uninstall_demo_data_for_doctype(doctype_name)` - Remove for one DocType  
- `install_all_demo_data(force=False)` - Install all registered demo data
- `uninstall_all_demo_data()` - Remove all demo data (with safety checks)
- `get_demo_data_counts()` - Get current vs expected counts
- `check_demo_data_status()` - Check installation status

### 3. DocType Integration

**File:** `setup/doctypes/StoreUOM.py`

```python
def on_doctype_install(force=False):
    """Auto-install demo data after DocType creation"""
    from technical_store_system.utils.helpers.demo_data_handler import install_demo_data_for_doctype
    
    result = install_demo_data_for_doctype("Store UOM", force=force)
    print(f"✓ {result['message']}")
```

**Simple 3-line integration - handler does all the work!**

### 4. UI Integration

**Store Settings** has buttons that call:
- `utils/controllers/store_settings_controller.py`
  - `install_demo_data()` → calls `install_all_demo_data(force=True)`
  - `uninstall_demo_data()` → calls `uninstall_all_demo_data()`

## 🔧 Adding New Demo Data

### Step 1: Create Data File
```python
# setup/demo_data/store_brand.py
"""Store Brand Demo Data"""

DEMO_BRANDS = [
    {"brand_name": "Samsung", "country": "South Korea"},
    {"brand_name": "Apple", "country": "USA"},
    # ... more brands
]
```

### Step 2: Register in Handler
```python
# In utils/helpers/demo_data_handler.py
DEMO_DATA_REGISTRY = {
    # ... existing entries
    "Store Brand": {
        "module": "technical_store_system.setup.demo_data.store_brand",
        "data_var": "DEMO_BRANDS",
        "name_field": "brand_name",
        "count": 10  # Expected count
    }
}
```

### Step 3: Use in DocType
```python
# In setup/doctypes/StoreBrand.py
def on_doctype_install(force=False):
    from technical_store_system.utils.helpers.demo_data_handler import install_demo_data_for_doctype
    result = install_demo_data_for_doctype("Store Brand", force=force)
    print(f"✓ {result['message']}")
```

**That's it! 3 steps, handler automatically manages everything.**

## 🛡️ Safety Features

1. **Count Matching** - Uninstall only works if counts exactly match expected demo data
2. **Force Parameter** - `force=True` bypasses flag check for button-triggered installs
3. **Atomic Operations** - All operations use `frappe.db.commit()`
4. **Error Handling** - Exceptions logged with full traceback
5. **Real-time Feedback** - UI shows status before/after operations

## 📊 Status Check

**Current vs Expected:**
```
Store UOM: 27/27 ✅ (demo data)
Store Item Group: 19/19 ✅ (demo data)
Store Location: 11/11 ✅ (demo data)
```

**States:**
- `not_installed` - No data (0/0/0)
- `installed` - All counts match expected demo data
- `partial` - Some data exists, counts don't match (real data)

## 🔄 Workflow

### Initial Install (First Time)
1. User installs app: `bench install-app technical_store_system`
2. DocTypes created via `doctypes_setup.py`
3. Each DocType's `on_doctype_install()` checks `install_demo_data` flag
4. If enabled, handler installs demo data automatically

### Manual Install (Button)
1. User clicks "Install Demo Data" in Store Settings
2. Controller calls `install_all_demo_data(force=True)`
3. Handler creates 27 UOMs + 19 Groups + 11 Locations
4. Status updated in UI

### Manual Uninstall (Button)
1. User clicks "Remove Demo Data" in Store Settings
2. Controller calls `uninstall_all_demo_data()`
3. Handler checks counts match expected (safety)
4. If safe, deletes all demo records
5. Status updated in UI

## 📁 File Locations

**Data:**
- `setup/demo_data/store_uom.py` (27 UOMs)
- `setup/demo_data/store_item_group.py` (19 groups)
- `setup/demo_data/store_location.py` (11 locations)

**Logic:**
- `utils/helpers/demo_data_handler.py` (central manager)
- `utils/controllers/store_settings_controller.py` (UI handlers)
- `setup/doctypes/{DocType}.py` (on_doctype_install hooks)

**UI:**
- Store Settings → Demo/Test Data Management section

---

**Last Updated:** December 8, 2025  
**Architecture:** Clean separation of data and logic  
**Scalability:** Easy to add new demo datasets  
