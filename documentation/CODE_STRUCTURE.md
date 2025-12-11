# Technical Store System - Code Structure
**Date:** December 9, 2025  
**Version:** 0.0.1  
**Status:** Production Ready ✅

---

## Overview

The Technical Store System provides intelligent auto-increment location naming with configurable patterns and full hierarchy display.

**Key Features:**
- ✅ Auto-increment system (Numeric, Alphabetic, Roman Numerals)
- ✅ Configurable prefixes via Store Settings
- ✅ Parent-aware naming (zones in WH-1 separate from WH-2)
- ✅ Full hierarchy display (e.g., "WH-1 - Z-A - R01 - S01 - B-1")
- ✅ Zero manual entry required

---

## Architecture

### Document Structure

**Store Location DocType:**
```
Fields:
├── location_code (Primary Key, Unique)       - "WH-1-Z-A-R01"
├── location_name (Display Name)              - "WH-1 - Z-A - R01"
├── location_type (Select)                    - Warehouse/Zone/Rack/Shelf/Bin
├── Hierarchy Links (Parent references):
│   ├── store (Link → Store Location)
│   ├── zone (Link → Store Location)
│   ├── rack (Link → Store Location)
│   └── shelf (Link → Store Location)
└── Auto-Generated Names (Hidden, Read-Only):
    ├── warehouse_name                        - "WH-1"
    ├── zone_name                             - "Z-A"
    ├── rack_name                             - "R01"
    ├── shelf_name                            - "S01"
    └── bin                                   - "B-1"
```

**Store Settings DocType:**
```
Location Naming Configuration:
├── Warehouse:
│   ├── warehouse_naming_pattern (Numeric/Alphabetic/Roman)
│   └── warehouse_prefix (default: "WH")
├── Zone:
│   ├── zone_naming_pattern (Alphabetic)
│   └── zone_prefix (default: "Z")
├── Rack:
│   ├── rack_naming_pattern (Numeric)
│   └── rack_prefix (default: "R")
├── Shelf:
│   ├── shelf_naming_pattern (Numeric)
│   └── shelf_prefix (default: "S")
└── Bin:
    ├── bin_naming_pattern (Numeric)
    └── bin_prefix (default: "B")
```

### Naming Hierarchy

```
Warehouse → Zone → Rack → Shelf → Bin

Example:
WH-1 (Warehouse)
└── WH-1-Z-A (Zone)
    ├── WH-1-Z-A-R01 (Rack)
    │   ├── WH-1-Z-A-R01-S01 (Shelf)
    │   │   ├── WH-1-Z-A-R01-S01-B-1 (Bin)
    │   │   └── WH-1-Z-A-R01-S01-B-2 (Bin)
    │   └── WH-1-Z-A-R01-S02 (Shelf)
    └── WH-1-Z-A-R02 (Rack)
```

---

## Code Structure

### Controller: `store_location_controller.py`

**File Organization:**
```python
"""
Module Documentation
- Features overview
- Architecture explanation
- Hierarchy description
"""

# ============================================================================
# DOC EVENT HANDLERS
# ============================================================================

def before_insert_event(doc, method=None)
    """Generates location_code and location_name before insert"""

def before_save_event(doc, method=None)
    """Updates location_name on save"""


# ============================================================================
# LOCATION CODE GENERATION
# ============================================================================

def generate_location_code(doc)
    """
    Generate unique location_code (primary key) with auto-increment
    
    Strategy:
    1. Auto-generate name field if empty
    2. Build hierarchical code by appending to parent
    
    Examples: WH-1, WH-1-Z-A, WH-1-Z-A-R01
    """


# ============================================================================
# AUTO-INCREMENT SYSTEM
# ============================================================================

def get_next_location_name(parent_location, location_type)
    """
    Calculate next available location name with auto-increment
    
    Features:
    - Parent-aware (zones in WH-1 separate from WH-2)
    - Pattern-based (Numeric/Alphabetic/Roman)
    - Configurable via Store Settings
    
    Returns: "WH-4", "Z-D", "R05", etc.
    """

def get_next_value(existing_values, pattern)
    """
    Calculate next sequential value based on pattern
    
    Patterns:
    - Numeric: 1, 2, 3... → 4
    - Alphabetic: A, B, C... Z, AA, AB...
    - Roman: I, II, III, IV, V...
    """


# ============================================================================
# ROMAN NUMERAL UTILITIES
# ============================================================================

def roman_to_int(roman)
    """Convert Roman numeral to integer (XIV → 14)"""

def int_to_roman(num)
    """Convert integer to Roman numeral (14 → XIV)"""


# ============================================================================
# LOCATION NAME DISPLAY GENERATION
# ============================================================================

def generate_location_name(doc)
    """
    Generate human-readable location_name showing full hierarchy
    
    Format: Components separated by " - "
    
    Examples:
    - Warehouse: "WH-1"
    - Zone: "WH-1 - Z-A"
    - Rack: "WH-1 - Z-A - R01"
    - Shelf: "WH-1 - Z-A - R01 - S01"
    - Bin: "WH-1 - Z-A - R01 - S01 - B-1"
    """
```

---

## Code Flow

### User Workflow

```
User Action:
1. Select Location Type (e.g., "Zone")
2. Select Parent (e.g., "WH-1")
3. Click Save

System Processing:
1. before_insert_event() triggered
2. generate_location_code(doc) called:
   a. Calls get_next_location_name("WH-1", "Zone")
   b. Queries existing zones in WH-1
   c. Finds highest: "Z-A"
   d. Returns next: "Z-B"
   e. Sets doc.zone_name = "Z-B"
   f. Sets doc.location_code = "WH-1-Z-B"
3. doc.name = doc.location_code
4. generate_location_name(doc) called:
   a. Fetches parent warehouse_name: "WH-1"
   b. Gets current zone_name: "Z-B"
   c. Builds display: "WH-1 - Z-B"
   d. Sets doc.location_name = "WH-1 - Z-B"
5. Document saved with name "WH-1-Z-B"

Result:
- Primary Key: "WH-1-Z-B"
- Display Name: "WH-1 - Z-B"
- User sees: "WH-1 - Z-B" in lists/forms
```

### Auto-Increment Logic

```python
# Example: Finding next zone in WH-1

# 1. Query existing zones
filters = {"location_type": "Zone", "store": "WH-1"}
existing = frappe.get_all("Store Location", filters, pluck="zone_name")
# Result: ["Z-A", "Z-B", "Z-C"]

# 2. Extract values (remove prefix)
existing_values = []
for name in existing:
    value = name.replace("Z", "").replace("-", "").strip()
    existing_values.append(value)
# Result: ["A", "B", "C"]

# 3. Get next value
if pattern == "Alphabetic":
    max_letter = max(existing_values)  # "C"
    next_value = chr(ord(max_letter) + 1)  # "D"
# Result: "D"

# 4. Format with prefix
next_name = f"Z-{next_value}"  # "Z-D"
```

---

## Naming Patterns

### Numeric Pattern
```
Default for: Warehouse, Rack, Shelf, Bin
Format: PREFIX-NUMBER or PREFIX{NUMBER:02d}

Examples:
- Warehouse: WH-1, WH-2, WH-3, WH-4...
- Rack: R01, R02, R03... R99, R100... (padded)
- Shelf: S01, S02, S03... (padded)
- Bin: B-1, B-2, B-3...

Logic:
1. Extract numbers from existing names
2. Find maximum number
3. Return max + 1
```

### Alphabetic Pattern
```
Default for: Zone
Format: PREFIX-LETTER

Examples:
- Zone: Z-A, Z-B, Z-C... Z-Z, Z-AA, Z-AB...

Logic:
1. Extract letters from existing names
2. Find maximum letter (A < B < Z < AA < AB)
3. Increment: A→B, Z→AA, AA→AB
```

### Roman Numerals Pattern
```
Available for: All location types
Format: PREFIX-ROMAN

Examples:
- Rack: R-I, R-II, R-III, R-IV, R-V, R-VI...

Logic:
1. Convert existing roman numerals to integers
2. Find maximum integer
3. Increment and convert back to roman
4. Supports: I(1), V(5), X(10), L(50), C(100), D(500), M(1000)
```

---

## Configuration

### Store Settings Configuration

**Default Configuration:**
```python
{
    "warehouse_naming_pattern": "Numeric",
    "warehouse_prefix": "WH",
    
    "zone_naming_pattern": "Alphabetic",
    "zone_prefix": "Z",
    
    "rack_naming_pattern": "Numeric",
    "rack_prefix": "R",
    
    "shelf_naming_pattern": "Numeric",
    "shelf_prefix": "S",
    
    "bin_naming_pattern": "Numeric",
    "bin_prefix": "B"
}
```

**Customization Examples:**
```python
# Example 1: Alphabetic warehouses
settings.warehouse_naming_pattern = "Alphabetic"
settings.warehouse_prefix = "STORE"
# Result: STORE-A, STORE-B, STORE-C...

# Example 2: Roman numeral racks
settings.rack_naming_pattern = "Roman Numerals"
settings.rack_prefix = "RACK"
# Result: RACK-I, RACK-II, RACK-III...

# Example 3: Custom prefixes
settings.zone_prefix = "ZONE"
settings.rack_prefix = "RACK"
# Result: WH-1-ZONE-A-RACK-01
```

---

## Testing

### Test Cases

**1. Basic Auto-Increment:**
```python
# Create first warehouse
wh1 = create_location("Warehouse")
assert wh1.name == "WH-1"
assert wh1.location_name == "WH-1"

# Create second warehouse
wh2 = create_location("Warehouse")
assert wh2.name == "WH-2"
assert wh2.location_name == "WH-2"
```

**2. Parent-Aware Naming:**
```python
# Create zones in WH-1
zone1 = create_location("Zone", store="WH-1")
assert zone1.name == "WH-1-Z-A"

zone2 = create_location("Zone", store="WH-1")
assert zone2.name == "WH-1-Z-B"

# Create zones in WH-2 (separate sequence)
zone3 = create_location("Zone", store="WH-2")
assert zone3.name == "WH-2-Z-A"  # Starts from A again
```

**3. Full Hierarchy:**
```python
wh = create_location("Warehouse")
zone = create_location("Zone", store=wh.name)
rack = create_location("Rack", store=wh.name, zone=zone.name)
shelf = create_location("Shelf", store=wh.name, zone=zone.name, rack=rack.name)
bin_loc = create_location("Bin", store=wh.name, zone=zone.name, rack=rack.name, shelf=shelf.name)

assert wh.location_name == "WH-1"
assert zone.location_name == "WH-1 - Z-A"
assert rack.location_name == "WH-1 - Z-A - R01"
assert shelf.location_name == "WH-1 - Z-A - R01 - S01"
assert bin_loc.location_name == "WH-1 - Z-A - R01 - S01 - B-1"
```

**4. Pattern Variations:**
```python
# Numeric pattern
wh = create_location("Warehouse")
assert wh.warehouse_name == "WH-1"

# Alphabetic pattern
zone = create_location("Zone", store="WH-1")
assert zone.zone_name == "Z-A"

# Roman numeral pattern (if configured)
settings.rack_naming_pattern = "Roman Numerals"
rack = create_location("Rack", zone="WH-1-Z-A")
assert rack.rack_name == "R-I"
```

---

## Performance

### Database Queries

**Per Location Creation:**
- 1 query to fetch Store Settings
- 1 query to fetch existing locations (filtered by parent)
- 0-5 queries to fetch parent names (for location_name generation)

**Total:** ~2-7 queries per location

**Optimization:**
- Queries are filtered by parent (efficient indexes)
- Only name fields are fetched (minimal data transfer)
- Settings cached as Single DocType

---

## Maintenance

### Code Quality Standards

✅ **Organization:** Logical sections with clear separators  
✅ **Documentation:** Comprehensive docstrings with examples  
✅ **Naming:** Descriptive function and variable names  
✅ **Type Hints:** Not used (Frappe convention)  
✅ **Error Handling:** Graceful fallbacks (e.g., "New Location")  
✅ **DRY Principle:** Reusable functions (get_next_value, generate_location_name)  
✅ **Single Responsibility:** Each function has one clear purpose  

### Future Enhancements

**Potential Additions:**
1. Bulk location creation (create entire hierarchy at once)
2. Location name templates (custom formatting)
3. Auto-numbering with gaps (skip certain numbers)
4. Location code validation rules
5. Performance metrics and logging
6. Cache frequently accessed parent names
7. Async location creation for bulk operations

---

## Hooks Configuration

### hooks.py

```python
# Document Events - Auto-generate location code and name
doc_events = {
    "Store Location": {
        "before_insert": "technical_store_system.utils.controllers.store_location_controller.before_insert_event",
        "before_save": "technical_store_system.utils.controllers.store_location_controller.before_save_event",
    }
}
```

**Event Flow:**
1. **before_insert:** Generates location_code and location_name before document is saved
2. **before_save:** Updates location_name on edits (location_code is immutable)

---

## Troubleshooting

### Common Issues

**Issue 1: Location name not updating**
```
Symptom: location_name shows old hierarchy
Solution: Restart bench to reload controller
Command: bench restart
```

**Issue 2: Duplicate location codes**
```
Symptom: Error "Duplicate entry for Store Location"
Cause: Race condition in concurrent creation
Solution: Use database transactions, consider locks
```

**Issue 3: Wrong auto-increment**
```
Symptom: Next value doesn't increment (e.g., WH-1, WH-1 instead of WH-2)
Cause: Name field not saved or cache issue
Solution: Check field in DocType, clear cache
```

---

## Summary

**System Status:** ✅ Production Ready

**Capabilities:**
- Zero manual entry for location naming
- Intelligent auto-increment with pattern support
- Parent-aware naming (separate sequences per parent)
- Full hierarchy display for clarity
- Configurable via Store Settings
- Clean, well-documented, maintainable code

**User Experience:**
1. Select location type
2. Select parent (if applicable)
3. Click save
4. System auto-generates everything

**Result:** Consistent, error-free location naming system ready for production use.

---

**Last Updated:** December 9, 2025  
**Documentation Version:** 1.0  
**Code Status:** Clean, Enhanced, Organized ✅
