# Architecture Schema - Code Organization

## 🎯 Core Principle: Clean Separation

**"Data in setup/, Logic in utils/, UI in controllers/"**

---

## 📁 Folder Structure

```
technical_store_system/
├── setup/                          ← ONLY DATA (no logic, no functions)
│   ├── doctypes_setup.py          ← Universal installer (discovers + delegates)
│   ├── client_scripts_setup.py    ← Universal installer (discovers + delegates)
│   ├── demo_data_setup.py         ← Universal installer (discovers + delegates)
│   ├── workspace_setup.py         ← Universal installer (discovers + delegates)
│   │
│   ├── doctypes/                  ← Pure data files
│   │   ├── StoreUOM.py           ← doctype = {...} ONLY
│   │   ├── StoreItem.py          ← doctype = {...} ONLY
│   │   └── StoreLocation.py      ← doctype = {...} ONLY
│   │
│   ├── client_scripts/            ← Pure data files
│   │   └── StoreSettingsDemoData.py  ← script_config = {...} ONLY
│   │
│   ├── demo_data/                 ← Pure data files
│   │   ├── store_uom.py          ← DEMO_UOMS = [...] ONLY
│   │   ├── store_item_group.py   ← DEMO_ITEM_GROUPS = [...] ONLY
│   │   └── store_location.py     ← DEMO_LOCATIONS = [...] ONLY
│   │
│   └── workspace/                 ← Pure data files
│       └── TechnicalStoreSystem.py  ← workspace = {...} ONLY
│
├── utils/                          ← ALL LOGIC (small, focused files)
│   ├── helpers/                   ← Business logic & operations
│   │   ├── doctype_installer.py  ← Install/uninstall DocTypes
│   │   ├── doctype_updater.py    ← Update existing DocTypes
│   │   ├── demo_data_handler.py  ← Install/uninstall demo data ✅
│   │   ├── client_script_handler.py  ← Install/uninstall client scripts
│   │   ├── workspace_handler.py  ← Create/update workspaces
│   │   └── [more helpers]        ← Each does ONE thing
│   │
│   ├── controllers/               ← UI API endpoints
│   │   ├── store_settings_controller.py  ← Button handlers
│   │   └── [future controllers]
│   │
│   └── validators/                ← Validation logic
│       └── [future validators]
│
└── installer.py                    ← Main orchestrator (calls setup/*_setup.py)
```

---

## 🔄 Data Flow

### Installation Flow (bench migrate)
```
bench migrate
  ↓
installer.py (orchestrator)
  ↓
setup/doctypes_setup.py (discovers files)
  ↓
utils/helpers/doctype_installer.py (does the work)
  ↓
Reads: setup/doctypes/StoreUOM.py (pure data)
  ↓
Creates DocType
  ↓
Optionally: utils/helpers/demo_data_handler.py
  ↓
Returns: Messages & status
```

### UI Button Flow
```
User clicks "Install Demo Data"
  ↓
Store Settings (UI)
  ↓
utils/controllers/store_settings_controller.py
  ↓
utils/helpers/demo_data_handler.py
  ↓
Reads: setup/demo_data/*.py (pure data)
  ↓
Installs records
  ↓
Returns: Success/failure message to UI
```

---

## 📋 Design Rules

### 1. **setup/** folder - ONLY DATA
```python
# ✅ GOOD - Pure data
doctype = {
    "name": "Store UOM",
    "fields": [...]
}

# ❌ BAD - Has functions
def on_doctype_install():
    # logic here
```

**Rules:**
- NO functions
- NO import statements for logic
- ONLY dictionaries and lists
- One file = one entity
- If 5 DocTypes → 5 files
- If 4 client scripts → 4 files

### 2. **setup/*_setup.py** - Universal Installers
```python
# Discovers files in folder
# Delegates to utils/helpers/
# Returns messages

def install_all_doctypes():
    # 1. Scan setup/doctypes/ folder
    # 2. For each .py file found:
    #    - Call utils/helpers/doctype_installer.py
    # 3. Collect results
    # 4. Print messages
    # NO HARDCODING!
```

**Rules:**
- Auto-discover files (no hardcoded list)
- Delegate work to helpers
- Print clear messages
- Handle errors gracefully
- Universal = works for any number of files

### 3. **utils/helpers/** - Small Focused Files
```python
# Each file does ONE thing
# doctype_installer.py → Install DocTypes
# doctype_updater.py → Update DocTypes
# demo_data_handler.py → Demo data operations

# ✅ GOOD - Small, focused
# doctype_installer.py (150 lines)
def install_doctype(doctype_dict):
    # Install logic

# ❌ BAD - Too big, does everything
# doctype_manager.py (1000 lines)
def install_doctype():
def update_doctype():
def delete_doctype():
def migrate_doctype():
# ... 20 more functions
```

**Rules:**
- One file = one responsibility
- Max ~200-300 lines per file
- Reusable functions
- Clear function names
- Well documented

### 4. **utils/controllers/** - UI Endpoints
```python
# Whitelisted functions called from UI

@frappe.whitelist()
def install_demo_data():
    # 1. Validate request
    # 2. Call helper
    # 3. Return user-friendly message
    
    result = demo_data_handler.install_all_demo_data()
    return result
```

**Rules:**
- Whitelisted for UI access
- Validate inputs
- Call helpers for work
- Return user-friendly messages
- Handle errors for UI

---

## 🎯 Benefits

### For Development
✅ **Easy to Add** - Create data file + register (3 steps)  
✅ **Easy to Update** - Edit data file (no code changes)  
✅ **Easy to Debug** - Small files, clear responsibility  
✅ **No Breaking** - Change one file without affecting others

### For Maintenance
✅ **Clear Structure** - Know exactly where everything is  
✅ **Reusable Code** - Helpers can be used anywhere  
✅ **Testable** - Small functions easy to test  
✅ **Scalable** - Add new entity types easily

### For Collaboration
✅ **Understandable** - Clear separation of concerns  
✅ **Safe** - Changes isolated to specific files  
✅ **Documented** - Architecture clearly defined  
✅ **Consistent** - All components follow same pattern

---

## 📝 Example: Adding New DocType

### Old Way (Mixed data + logic)
```python
# setup/doctypes/NewDocType.py - 300 lines
def on_doctype_install():
    # 100 lines of logic

def get_demo_data():
    # 50 lines of data

doctype = {...}  # 150 lines
```

### New Way (Clean separation)
```python
# setup/doctypes/NewDocType.py - 50 lines
doctype = {...}  # Pure data only

# setup/demo_data/new_doctype.py - 30 lines  
DEMO_DATA = [...]  # Pure data only

# setup/doctypes_setup.py - Auto-discovers!
# No changes needed - just drop the file

# utils/helpers/doctype_installer.py
# Already handles generic installation
```

**Result:** 80 lines total vs 300 lines, reusable, maintainable!

---

## 🔍 Current Status

✅ **Completed:**
- demo_data/ - Pure data files
- demo_data_handler.py - Centralized logic

⏳ **To Refactor:**
- doctypes/ - Still has functions mixed with data
- doctypes_setup.py - Some hardcoded logic
- client_scripts/ - Mixed data and logic
- workspace/ - Need to check structure

---

**Last Updated:** December 8, 2025  
**Architecture Version:** 2.0 (Clean Separation)  
**Status:** In Progress - Refactoring to match schema
