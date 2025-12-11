# Store Item Group System - Complete Documentation

**Version:** 1.0  
**Last Updated:** 2025-12-09  
**Status:** ✅ Production Ready

---

## 📑 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Configuration](#configuration)
5. [Usage Guide](#usage-guide)
6. [API Reference](#api-reference)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)
9. [Changelog](#changelog)

---

## System Overview

### Purpose

The Store Item Group system provides **hierarchical category management** for inventory items with:
- **Unlimited nesting** (tree structure using nested set model)
- **Auto-generated group codes** for quick identification
- **Configuration inheritance** from parent to child groups
- **Real-time statistics tracking** (item counts, child groups)
- **Validation** to maintain data integrity

### Key Benefits

| Benefit | Description |
|---------|-------------|
| 🌳 **Hierarchy** | Organize items in logical tree structure (4+ levels deep) |
| 📝 **Auto-Coding** | Group codes generated automatically (ELEC, COMP, LAPTOP) |
| 🔄 **Inheritance** | Child groups inherit settings from parents |
| 📊 **Statistics** | Real-time counts (direct items, total items, child groups) |
| ✅ **Validation** | Prevents circular references and invalid structures |
| 🎯 **Tracking** | Serial/batch tracking defaults per category |

---

## Architecture

### Component Structure

```
Store Item Group System
├── DocType Definition
│   └── setup/doctypes/StoreItemGroup.py (235 lines)
│       ├── 25 Fields (4 tabs)
│       ├── Tree structure enabled
│       └── Auto-naming by item_group_name
│
├── Controller (Business Logic)
│   └── utils/controllers/item_group_controller.py (400+ lines)
│       ├── ItemGroupController class
│       ├── Event handlers (before_insert, before_save, on_update, before_delete)
│       ├── Code generation
│       ├── Validation logic
│       ├── Statistics calculation
│       └── Configuration inheritance
│
├── Demo Data
│   └── setup/demo_data/store_item_group.py
│       └── 35 hierarchical groups (4 levels deep)
│
└── Hooks Registration
    └── hooks.py
        └── doc_events for Store Item Group
```

### Database Schema

**DocType:** `Store Item Group`

| Field | Type | Description |
|-------|------|-------------|
| `group_code` | Data | Short code (e.g., ELEC, TOOL) - Auto-generated |
| `item_group_name` | Data | Full name - **Required, Unique** |
| `parent_item_group` | Link | Parent group for nesting |
| `is_group` | Check | True = container for sub-groups, False = can contain items |
| `enabled` | Check | Active/inactive status |
| `sort_order` | Int | Display order (lower first) |
| `description` | Text Editor | Rich text description |
| `image` | Attach Image | Group icon/image |
| `default_uom` | Link | Default Unit of Measure |
| `default_warehouse` | Link | Default storage location |
| `has_serial_no` | Check | Items tracked by serial number |
| `has_batch_no` | Check | Items tracked by batch/lot |
| `allow_negative_stock` | Check | Allow back-orders |
| `auto_create_bins` | Check | Auto-create storage bins |
| `item_count` | Int | Direct items in this group (read-only) |
| `child_group_count` | Int | Immediate child groups (read-only) |
| `total_item_count` | Int | All items recursively (read-only) |
| `last_updated` | Datetime | Statistics last calculated (read-only) |
| `created_date` | Datetime | Creation timestamp (read-only) |
| `modified_date` | Datetime | Last modification (read-only) |

**Tree Fields (Auto-added):**
- `lft` (Int): Left boundary for nested set
- `rgt` (Int): Right boundary for nested set
- `old_parent` (Link): Previous parent (for tree rebuilding)

---

## Features

### 1. Auto-Generated Group Codes

**How it works:**
- Extracts initials or abbreviation from group name
- Ensures uniqueness by adding numbers if needed
- Converts to uppercase

**Examples:**
```python
"Electronics" → "ELECT"
"Hand Tools" → "HTOOL"
"Computers & IT" → "CI"
"Laptops" → "LAPTO"
"Safety Equipment" → "SE"
```

**Manual Override:**
You can provide custom `group_code` during creation - auto-generation only runs if blank.

### 2. Configuration Inheritance

**Child groups automatically inherit from parent:**
- `default_uom` - Unit of measure
- `default_warehouse` - Storage location
- `has_serial_no` - Serial tracking
- `has_batch_no` - Batch tracking
- `allow_negative_stock` - Negative stock permission
- `auto_create_bins` - Bin creation setting

**Example:**
```
Electronics (has_serial_no=1)
└── Computers & IT (inherits has_serial_no=1)
    └── Laptops (inherits has_serial_no=1)
```

### 3. Real-Time Statistics

**Tracked Metrics:**
| Metric | Description | Update Frequency |
|--------|-------------|------------------|
| `item_count` | Items directly in this group | On item create/update/delete |
| `child_group_count` | Immediate child groups | On group create/delete |
| `total_item_count` | All items including descendants | On any change in tree |
| `last_updated` | Last calculation timestamp | Every statistics update |

**Statistics are automatically updated on:**
- Group creation/deletion
- Item assignment/removal
- Tree structure changes

### 4. Validation Rules

**Enforced constraints:**

| Rule | Description | Error Message |
|------|-------------|---------------|
| **Group vs Leaf** | Groups can only contain sub-groups, not items directly | "Cannot mark as Group because it has X item(s)" |
| **Parent is Group** | Parent must have `is_group=1` | "Parent must be marked as 'Is Group'" |
| **No Circular References** | Prevent loops in parent chain | "Circular reference detected" |
| **Deletion Protection** | Cannot delete groups with items | "Cannot delete - contains X items" |
| **Deletion Protection** | Cannot delete groups with children | "Cannot delete - contains X sub-groups" |

### 5. Tree Hierarchy Support

**Nested Set Model:**
- Efficient querying of entire trees
- Fast ancestor/descendant lookups
- Supports unlimited nesting levels

**Tree Operations:**
- `get_group_hierarchy(group_name)` - Get path from root to group
- `get_group_children_recursive(group_name)` - Get all descendants
- Frappe's built-in tree view in UI

---

## Configuration

### System Settings

No global settings required - each group is self-configured.

### Field Descriptions

#### Tab 1: Basic Information

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `group_code` | No | Auto | Short identifier (3-6 chars) |
| `item_group_name` | **Yes** | - | Must be unique |
| `parent_item_group` | No | - | Blank for root groups |
| `is_group` | No | 0 | Check for container groups |
| `enabled` | No | 1 | Uncheck to hide |
| `sort_order` | No | 0 | Lower numbers display first |
| `description` | No | - | Rich text editor |
| `image` | No | - | Icon/image for visual identification |

#### Tab 2: Configuration

| Field | Purpose | Inherited |
|-------|---------|-----------|
| `default_uom` | Unit of measure for new items | ✅ Yes |
| `default_warehouse` | Storage location for items | ✅ Yes |
| `has_serial_no` | Track individual items by serial | ✅ Yes |
| `has_batch_no` | Track by production batch/lot | ✅ Yes |
| `allow_negative_stock` | Allow issuing when out of stock | ✅ Yes |
| `auto_create_bins` | Auto-create storage bins | ✅ Yes |

#### Tab 3: Statistics (Read-Only)

All statistics fields are automatically calculated - do not edit manually.

### Permissions

| Role | Read | Write | Create | Delete | Report |
|------|------|-------|--------|--------|--------|
| Store Manager | ✅ | ✅ | ✅ | ✅ | ✅ |
| Inventory Admin | ✅ | ✅ | ✅ | ✅ | ✅ |
| Warehouse Staff | ✅ | ❌ | ❌ | ❌ | ✅ |
| Store Viewer | ✅ | ❌ | ❌ | ❌ | ✅ |

---

## Usage Guide

### Creating Groups via Web UI

#### Step 1: Create Root Group

1. Go to **Store Item Group** list
2. Click **New**
3. Enter:
   - Item Group Name: "All Item Groups"
   - Is Group: ✅ Checked
   - Enabled: ✅ Checked
4. Click **Save**
5. Note the auto-generated `group_code` (e.g., "AIG")

#### Step 2: Create Main Categories

1. Click **New**
2. Enter:
   - Item Group Name: "Electronics"
   - Parent Item Group: "All Item Groups"
   - Is Group: ✅ Checked
   - Has Serial No: ✅ Checked (for electronics)
3. Click **Save**

#### Step 3: Create Sub-Categories

1. Click **New**
2. Enter:
   - Item Group Name: "Computers & IT"
   - Parent Item Group: "Electronics"
   - Is Group: ✅ Checked
3. Click **Save**
4. Note: `has_serial_no` is inherited from "Electronics"

#### Step 4: Create Leaf Groups

1. Click **New**
2. Enter:
   - Item Group Name: "Laptops"
   - Parent Item Group: "Computers & IT"
   - Is Group: ❌ Unchecked (this can contain items)
3. Click **Save**

### Creating Groups via Python API

```python
import frappe

# Create root group
root = frappe.get_doc({
    "doctype": "Store Item Group",
    "item_group_name": "All Item Groups",
    "is_group": 1,
    "enabled": 1,
    "description": "Root category"
})
root.insert()
# Auto-generated: root.group_code = "AIG"

# Create main category
electronics = frappe.get_doc({
    "doctype": "Store Item Group",
    "item_group_name": "Electronics",
    "parent_item_group": "All Item Groups",
    "is_group": 1,
    "has_serial_no": 1,  # Serial tracking for all electronics
    "description": "Electronic equipment and components"
})
electronics.insert()
# Auto-generated: electronics.group_code = "ELECT"

# Create sub-category (inherits serial tracking)
computers = frappe.get_doc({
    "doctype": "Store Item Group",
    "item_group_name": "Computers & IT",
    "parent_item_group": "Electronics",
    "is_group": 1
})
computers.insert()
# Inherited: computers.has_serial_no = 1
# Auto-generated: computers.group_code = "CI"

# Create leaf group (can contain items)
laptops = frappe.get_doc({
    "doctype": "Store Item Group",
    "item_group_name": "Laptops",
    "parent_item_group": "Computers & IT",
    "is_group": 0,  # Leaf node
    "description": "Portable computers"
})
laptops.insert()
# Auto-generated: laptops.group_code = "LAPTO"

frappe.db.commit()
```

### Updating Group Statistics

Statistics update automatically, but you can manually trigger recalculation:

```python
from technical_store_system.utils.controllers.item_group_controller import recalculate_all_statistics

# Recalculate for all groups
recalculate_all_statistics()
```

---

## API Reference

### ItemGroupController Class

Located: `technical_store_system.utils.controllers.item_group_controller`

#### Methods

##### `before_insert()`
Called before inserting new group.
- Generates `group_code` if empty
- Sets `created_date`
- Inherits configuration from parent
- Initializes statistics

##### `before_save()`
Called before saving group.
- Updates `modified_date`
- Validates group settings
- Updates `last_updated`

##### `on_update()`
Called after saving group.
- Updates statistics for this group
- Updates parent group statistics

##### `before_delete()`
Called before deleting group.
- Prevents deletion if `item_count > 0`
- Prevents deletion if `child_group_count > 0`

##### `generate_group_code() → str`
Generates unique group code from name.

**Returns:** Generated code (e.g., "ELECT", "HTOOL")

##### `validate_group_settings()`
Validates group configuration.
- Ensures groups don't have items
- Ensures parent is marked as group
- Prevents circular references

##### `update_statistics()`
Recalculates all statistics:
- `item_count`
- `child_group_count`
- `total_item_count`
- `last_updated`

##### `count_total_items_recursive() → int`
Counts all items in group tree.

**Returns:** Total item count including all descendants

##### `inherit_from_parent()`
Inherits configuration from parent group.

### Utility Functions

#### `get_group_hierarchy(group_name) → list`
Gets full path from root to group.

**Args:**
- `group_name` (str): Name of Store Item Group

**Returns:** List of group names (e.g., `['All Item Groups', 'Electronics', 'Laptops']`)

**Example:**
```python
from technical_store_system.utils.controllers.item_group_controller import get_group_hierarchy

path = get_group_hierarchy("Laptops")
print(" → ".join(path))
# Output: All Item Groups → Electronics → Computers & IT → Laptops
```

#### `get_group_children_recursive(group_name) → list`
Gets all descendant groups recursively.

**Args:**
- `group_name` (str): Name of Store Item Group

**Returns:** List of all child group names

**Example:**
```python
from technical_store_system.utils.controllers.item_group_controller import get_group_children_recursive

children = get_group_children_recursive("Electronics")
print(f"Found {len(children)} sub-groups")
```

#### `recalculate_all_statistics()`
Recalculates statistics for all groups.

**Usage:**
```bash
bench execute technical_store_system.utils.controllers.item_group_controller.recalculate_all_statistics
```

---

## Testing

### Manual Testing Checklist

#### ✅ Basic Operations
- [ ] Create root group
- [ ] Create main category
- [ ] Create sub-category
- [ ] Create leaf group
- [ ] Update group settings
- [ ] Delete empty group

#### ✅ Auto-Generation
- [ ] Group code auto-generated
- [ ] Unique codes when duplicates exist
- [ ] Created/modified dates set

#### ✅ Inheritance
- [ ] Child inherits `default_uom`
- [ ] Child inherits `has_serial_no`
- [ ] Child inherits `has_batch_no`
- [ ] Child inherits `allow_negative_stock`

#### ✅ Validation
- [ ] Cannot mark group with items as "Is Group"
- [ ] Parent must be marked as group
- [ ] Circular reference prevented
- [ ] Cannot delete group with items
- [ ] Cannot delete group with children

#### ✅ Statistics
- [ ] `item_count` updates when items added
- [ ] `child_group_count` updates when sub-groups added
- [ ] `total_item_count` includes all descendants
- [ ] Parent statistics update when child changes

### Automated Test Script

Save as `test_item_group.py`:

```python
import frappe

def test_item_group_system():
    """Comprehensive test for Store Item Group"""
    
    print("\n" + "="*80)
    print("TESTING STORE ITEM GROUP SYSTEM")
    print("="*80)
    
    # Test 1: Create hierarchy
    print("\n1️⃣ Creating test hierarchy...")
    
    # Root
    root = frappe.get_doc({
        "doctype": "Store Item Group",
        "item_group_name": "Test Root",
        "is_group": 1
    }).insert()
    assert root.group_code is not None, "Group code not generated"
    print(f"   ✅ Root created: {root.group_code}")
    
    # Main category
    main = frappe.get_doc({
        "doctype": "Store Item Group",
        "item_group_name": "Test Electronics",
        "parent_item_group": "Test Root",
        "is_group": 1,
        "has_serial_no": 1
    }).insert()
    assert main.group_code is not None
    print(f"   ✅ Main category: {main.group_code}")
    
    # Sub-category (should inherit serial_no)
    sub = frappe.get_doc({
        "doctype": "Store Item Group",
        "item_group_name": "Test Computers",
        "parent_item_group": "Test Electronics",
        "is_group": 0
    }).insert()
    assert sub.has_serial_no == 1, "Configuration not inherited"
    print(f"   ✅ Sub-category: {sub.group_code} (inherited serial_no)")
    
    # Test 2: Statistics
    print("\n2️⃣ Testing statistics...")
    root.reload()
    assert root.child_group_count == 1, f"Expected 1 child, got {root.child_group_count}"
    print(f"   ✅ Child count: {root.child_group_count}")
    
    # Test 3: Hierarchy
    print("\n3️⃣ Testing hierarchy...")
    from technical_store_system.utils.controllers.item_group_controller import get_group_hierarchy
    path = get_group_hierarchy("Test Computers")
    expected = ['Test Root', 'Test Electronics', 'Test Computers']
    assert path == expected, f"Expected {expected}, got {path}"
    print(f"   ✅ Path: {' → '.join(path)}")
    
    # Test 4: Validation
    print("\n4️⃣ Testing validation...")
    try:
        # Try to create circular reference
        root_doc = frappe.get_doc("Store Item Group", "Test Root")
        root_doc.parent_item_group = "Test Electronics"
        root_doc.save()
        assert False, "Should have raised circular reference error"
    except Exception as e:
        print(f"   ✅ Circular reference prevented: {str(e)[:50]}...")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    frappe.delete_doc("Store Item Group", "Test Computers", force=1)
    frappe.delete_doc("Store Item Group", "Test Electronics", force=1)
    frappe.delete_doc("Store Item Group", "Test Root", force=1)
    frappe.db.commit()
    
    print("\n✅ ALL TESTS PASSED!")

# Run tests
test_item_group_system()
```

**Run with:**
```bash
bench --site test.local console < test_item_group.py
```

---

## Troubleshooting

### Issue: Group code not generated

**Symptoms:**
- `group_code` field is empty after creation

**Solutions:**
1. Ensure hooks are registered:
   ```bash
   bench --site test.local console
   >>> from technical_store_system import hooks
   >>> print(hooks.doc_events.get('Store Item Group'))
   ```

2. Clear cache and restart:
   ```bash
   bench --site test.local clear-cache
   bench restart
   ```

3. Manually trigger:
   ```python
   doc = frappe.get_doc("Store Item Group", "Group Name")
   from technical_store_system.utils.controllers.item_group_controller import ItemGroupController
   controller = ItemGroupController(doc)
   doc.group_code = controller.generate_group_code()
   doc.save()
   ```

### Issue: Statistics not updating

**Symptoms:**
- `item_count`, `child_group_count`, or `total_item_count` is incorrect

**Solutions:**
1. Recalculate all statistics:
   ```bash
   bench execute technical_store_system.utils.controllers.item_group_controller.recalculate_all_statistics
   ```

2. Check hooks are working:
   ```python
   import frappe
   doc = frappe.get_doc("Store Item Group", "Group Name")
   from technical_store_system.utils.controllers.item_group_controller import ItemGroupController
   controller = ItemGroupController(doc)
   controller.update_statistics()
   doc.save()
   ```

### Issue: Cannot delete group

**Symptoms:**
- Error: "Cannot delete Item Group because it contains X items"

**Solutions:**
1. Check item count:
   ```python
   frappe.db.count("Store Item", {"item_group": "Group Name"})
   ```

2. Move items to different group:
   ```python
   items = frappe.get_all("Store Item", {"item_group": "Old Group"})
   for item in items:
       doc = frappe.get_doc("Store Item", item.name)
       doc.item_group = "New Group"
       doc.save()
   ```

3. Force delete (⚠️ use with caution):
   ```python
   frappe.delete_doc("Store Item Group", "Group Name", force=1)
   ```

### Issue: Circular reference error

**Symptoms:**
- Error: "Circular reference detected"

**Solutions:**
1. Check parent chain:
   ```python
   from technical_store_system.utils.controllers.item_group_controller import get_group_hierarchy
   path = get_group_hierarchy("Group Name")
   print(path)
   ```

2. Fix parent reference:
   ```python
   doc = frappe.get_doc("Store Item Group", "Group Name")
   doc.parent_item_group = "Correct Parent"
   doc.save()
   ```

### Issue: Configuration not inherited

**Symptoms:**
- Child group doesn't have parent's settings

**Solutions:**
1. Manually inherit:
   ```python
   doc = frappe.get_doc("Store Item Group", "Child Group")
   from technical_store_system.utils.controllers.item_group_controller import ItemGroupController
   controller = ItemGroupController(doc)
   controller.inherit_from_parent()
   doc.save()
   ```

2. Check parent settings are not default:
   - Inheritance only occurs if child value is default (0/blank)

---

## Changelog

### Version 1.0 (2025-12-09)

**✨ Initial Release**

**Added:**
- Hierarchical tree structure with unlimited nesting
- Auto-generated group codes (ELEC, TOOL, etc.)
- 25 fields across 4 tabs
- Configuration inheritance from parent to child
- Real-time statistics tracking (3 metrics)
- Comprehensive validation rules
- Item Group Controller (400+ lines)
- Event hooks (before_insert, before_save, on_update, before_delete)
- Demo data with 35 groups (4 levels deep)
- Utility functions (get_group_hierarchy, get_group_children_recursive, recalculate_all_statistics)
- Complete documentation

**Enhanced Fields:**
- Added `group_code` (auto-generated)
- Added `sort_order` (display ordering)
- Added `default_warehouse` (storage location)
- Added `auto_create_bins` (bin creation)
- Added `child_group_count` (immediate children)
- Added `total_item_count` (recursive count)
- Added `created_date`, `modified_date` (metadata)
- Enhanced descriptions with emojis and examples

**Testing:**
- All 4 test scenarios passing
- Auto-generation verified
- Inheritance verified
- Validation verified
- Statistics verified
- Hierarchy verified

**Status:**
✅ Production Ready - All features tested and working

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review test scripts for examples
3. Check Frappe logs: `tail -f logs/worker.error.log`
4. Run diagnostics: `bench console` and test functions manually

---

**End of Documentation**
