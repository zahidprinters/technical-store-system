# Utils Folder Structure

This folder contains all reusable code that is called by the app. Organized into logical subfolders for better maintainability.

## Folder Structure

```
utils/
├── __init__.py
├── README.md (this file)
├── controllers/          # DocType controllers and business logic
│   ├── __init__.py
│   └── store_settings_controller.py
├── helpers/             # Helper functions and utilities
│   └── __init__.py
├── validators/          # Validation functions
│   └── __init__.py
└── [future folders]     # Can add more as needed
```

## Subfolders

### 1. **controllers/**
Contains controller classes for DocTypes that need custom business logic beyond the DocType definition.

**Current files:**
- `store_settings_controller.py` - Store Settings controller with whitelisted methods for demo data management

**When to add here:**
- DocType controllers with custom methods
- Business logic that extends DocType behavior
- Whitelisted API methods for client-side calls

**Naming convention:** `{doctype_name}_controller.py` (lowercase with underscores)

---

### 2. **helpers/**
General utility functions that can be used across the app.

**Examples of what goes here:**
- Data formatting functions
- Common calculations
- Reusable query builders
- File operations
- Report helpers

**Naming convention:** `{purpose}_helper.py` (e.g., `date_helper.py`, `report_helper.py`)

---

### 3. **validators/**
Functions for validating data, checking permissions, and enforcing business rules.

**Examples of what goes here:**
- Field validation functions
- Business rule validators
- Permission checkers
- Data integrity validators

**Naming convention:** `{entity}_validator.py` (e.g., `stock_validator.py`, `item_validator.py`)

---

## Usage Guidelines

### Importing from utils

```python
# From controllers
from technical_store_system.utils.controllers.store_settings_controller import StoreSettings

# From helpers
from technical_store_system.utils.helpers.date_helper import format_date

# From validators
from technical_store_system.utils.validators.stock_validator import validate_quantity
```

### Creating New Utils Files

1. **Determine the category** - Is it a controller, helper, or validator?
2. **Name the file** - Use lowercase with underscores: `entity_category.py`
3. **Add to appropriate subfolder** - Place in controllers/, helpers/, or validators/
4. **Update hooks.py** - If it's a DocType controller, register it in `doc_events`
5. **Document the purpose** - Add docstring at top of file explaining its purpose

### Example: Adding a new helper

```python
# File: technical_store_system/utils/helpers/barcode_helper.py
"""
Barcode Helper Functions
Utilities for generating and validating barcodes
"""

import frappe

def generate_barcode(item_code):
    """Generate a barcode for an item"""
    # Implementation here
    pass

def validate_barcode(barcode):
    """Validate barcode format"""
    # Implementation here
    pass
```

---

## Future Expansion

As the app grows, consider adding more subfolders:

- **api/** - REST API endpoints and integrations
- **reports/** - Report generation logic
- **services/** - External service integrations
- **constants/** - App-wide constants and enums
- **tasks/** - Background tasks and scheduled jobs
- **queries/** - Complex database queries

---

**Last Updated:** December 6, 2025
