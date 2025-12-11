# Installation System Overview

## Architecture

The Technical Store System uses a **modular installation architecture** with three key components:

### 1. Hooks Configuration (`hooks.py`)
```python
after_install = "technical_store_system.installer.after_install"
after_uninstall = "technical_store_system.installer.after_uninstall"
after_migrate = "technical_store_system.installer.after_migrate"
```

### 2. Universal Orchestrator (`installer.py`)
Central installer that coordinates all setup modules during app lifecycle events.

**Location**: `technical_store_system/installer.py`

**Functions**:
- `after_install()` - Called after app installation
- `after_uninstall()` - Called after app uninstallation  
- `after_migrate()` - Called after database migration
- `install_workspace()` - Install workspace
- `create_default_roles()` - Create user roles
- `create_store_settings()` - Initialize settings
- `install_default_uoms()` - Create default UOMs

### 3. Modular Setup Files (`setup/`)
Individual modules for different installation tasks.

```
setup/
├── __init__.py
├── workspace/
│   ├── __init__.py
│   └── Workspace.py              # Workspace definition (175 lines)
├── workspace_setup.py             # Workspace installer (185 lines)
├── roles_setup.py                 # (Future) Roles installer
├── settings_setup.py              # (Future) Settings installer
└── uom_setup.py                   # (Future) UOM installer
```

## Installation Flow

```
┌─────────────────────────────────────────────────────┐
│  bench install-app technical_store_system           │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  hooks.py: after_install hook triggered             │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  installer.py: after_install() function runs        │
└────────────────┬────────────────────────────────────┘
                 │
                 ├──► install_workspace()
                 │    └──► workspace_setup.install()
                 │         └──► Creates Workspace DocType
                 │
                 ├──► create_default_roles()
                 │    └──► Creates: Store Manager, Warehouse Staff, 
                 │                  Inventory Admin, Store Viewer
                 │
                 ├──► create_store_settings()
                 │    └──► Creates Store Settings single DocType
                 │
                 └──► install_default_uoms()
                      └──► Creates: Piece, Box, Kg, Liter, 
                                    Meter, Dozen
```

## Workspace System

### Components

#### 1. Workspace Definition (`setup/workspace/Workspace.py`)
Complete workspace structure definition (175 lines).

**Contains**:
- Workspace metadata (name, title, icon, category)
- 4 Shortcuts: Store Item, Store Location, Stock Entry, Stock Balance
- 5 Cards:
  1. **Inventory Management**: Stock Entry, Stock Balance, Stock Movement
  2. **Masters**: Store Item, Store Location, Store Supplier, Store Customer, Store UOM
  3. **Transactions**: Purchase Orders, Receipts, Sales, Transfers, Adjustments
  4. **Reports & Analytics**: Stock reports, supplier reports, analytics dashboard
  5. **Settings & Configuration**: Store Settings, Workflows, Permissions

#### 2. Workspace Installer (`setup/workspace_setup.py`)
Workspace lifecycle management (185 lines).

**Functions**:
- `install()` - Install workspace (creates new Workspace DocType)
- `update()` - Update existing workspace (preserves customizations)
- `uninstall()` - Remove workspace (cleanup on app uninstall)

**Import Pattern**:
```python
from .workspace.Workspace import workspace
```

#### 3. Universal Orchestrator (`installer.py`)
Calls workspace installer at appropriate times.

```python
from technical_store_system.setup import workspace_setup

def install_workspace():
    print("  📋 Installing workspace...")
    workspace_setup.install()
    print("  ✅ Workspace installed")
```

## What Gets Installed

### During Installation (`bench install-app`)

✅ **Workspace**: Technical Store System
- 4 shortcuts for quick access
- 5 organized cards with links to DocTypes, Reports, Pages
- Fully customizable after installation

✅ **User Roles** (4 roles):
- Store Manager (full access)
- Warehouse Staff (operational access)
- Inventory Admin (configuration access)
- Store Viewer (read-only access)

✅ **Store Settings**: Single DocType with configuration:
- `enable_erpnext_sync`: Default 0 (disabled)
- `allow_negative_stock`: Default 0 (disabled)
- Additional settings can be configured after installation

✅ **Default UOMs** (6 units):
- Piece
- Box
- Kg
- Liter
- Meter
- Dozen

### During Uninstallation (`bench uninstall-app`)

- Workspace removed
- App-specific data kept (by default)
- Historical transactions preserved
- Clean uninstall without breaking data

### During Migration (`bench migrate`)

- Workspace updated if definition changes
- Preserves user customizations
- Updates structure as needed

## Adding New Setup Modules

### Example: Adding Roles Setup

1. **Create definition file**:
```python
# setup/roles/Roles.py
roles = [
    {
        "role_name": "Store Manager",
        "desk_access": 1,
        "description": "Full access to all store operations"
    },
    # ... more roles
]
```

2. **Create installer**:
```python
# setup/roles_setup.py
import frappe
from .roles.Roles import roles

def install():
    """Install roles"""
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert(ignore_permissions=True)

def uninstall():
    """Remove roles (optional)"""
    # Only if safe to remove
    pass
```

3. **Update installer.py**:
```python
from technical_store_system.setup import roles_setup

def create_default_roles():
    print("  👥 Installing roles...")
    roles_setup.install()
    print("  ✅ Roles installed")
```

## Files Created

### Core Installation Files
```
technical_store_system/
├── hooks.py                       # Updated (3 hooks added)
├── installer.py                   # Created (303 lines)
└── setup/
    ├── __init__.py                # Created (module marker)
    ├── workspace/
    │   ├── __init__.py            # Created (module marker)
    │   └── Workspace.py           # Created (175 lines)
    └── workspace_setup.py         # Created (185 lines)
```

### Documentation Updates
```
.cursorrules                       # Updated (installer section)
DEVELOPMENT.md                     # Updated (installation system section)
PROJECT_CONFIG.md                  # Updated (installation architecture)
INSTALLATION_SYSTEM.md             # Created (this file)
```

## Testing the Installation

### Manual Test
```bash
# 1. Navigate to bench
cd ~/frappe-bench

# 2. Install app
bench --site [site] install-app technical_store_system

# 3. Verify installation
# Should see output:
# 🚀 Installing Technical Store System...
# 📋 Installing workspace...
# ✅ Workspace installed
# 👥 Creating user roles...
# ✅ Roles created
# ⚙️ Creating Store Settings...
# ✅ Settings created
# 📦 Installing default UOMs...
# ✅ UOMs installed
# ✅ Installation completed successfully!

# 4. Check workspace
# Login to desk → Go to workspaces → Should see "Technical Store System"

# 5. Check roles
# Go to: User Management → Role
# Should see: Store Manager, Warehouse Staff, Inventory Admin, Store Viewer

# 6. Check settings
# Search for "Store Settings" in search bar
# Should see Store Settings with default values

# 7. Verify console
bench --site [site] console
```

```python
# In console
frappe.db.exists("Workspace", "Technical Store System")  # Should return "Technical Store System"
frappe.get_all("Role", filters={"name": ["like", "Store%"]})  # Should show 4 roles
frappe.get_single("Store Settings")  # Should return settings doc
```

### Uninstallation Test
```bash
# 1. Uninstall app
bench --site [site] uninstall-app technical_store_system

# 2. Verify cleanup
# - Workspace removed
# - App removed from installed apps list
# - Data preserved (if configured)
```

## Current Status

✅ **Completed**:
- Modular installer architecture designed
- Universal orchestrator created (installer.py)
- Workspace definition created (Workspace.py)
- Workspace installer created (workspace_setup.py)
- Hooks configured to call installer
- Documentation updated

⏳ **Ready for**:
- Installation testing
- DocType creation (start with Store Item)
- Additional setup modules (roles, settings, etc.)

⬜ **Future**:
- Separate roles_setup.py module
- Separate settings_setup.py module
- Separate uom_setup.py module
- Permission setup module
- Custom field fixtures

## Benefits of This Architecture

✅ **Modularity**: Each feature has its own setup file
✅ **Maintainability**: Easy to update individual modules
✅ **Testability**: Can test each module independently
✅ **Clarity**: Clear separation of concerns
✅ **Scalability**: Easy to add new setup modules
✅ **Reusability**: Setup modules can be reused/shared
✅ **Documentation**: Each module is self-documenting

## Next Steps

1. **Test installation**:
   ```bash
   bench --site [site] install-app technical_store_system
   ```

2. **Verify workspace appears** in desk

3. **Start DocType creation**:
   - Begin with Store Item (core DocType)
   - Test thoroughly before proceeding
   - Add one feature at a time

4. **Expand setup modules** as needed:
   - Move roles to roles_setup.py
   - Move settings to settings_setup.py
   - Move UOMs to uom_setup.py

---

**Installation system is ready for testing!** 🚀
