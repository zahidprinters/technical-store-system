# Technical Store System - Documentation Index

**Quick Navigation** | [Installation](#installation) | [Development](#development) | [Configuration](#configuration) | [Reference](#reference)

---

## 📖 Documentation Structure

This project uses a **compact, indexed documentation system** with only essential files:

### 🎯 Core Documentation

| File | Purpose | When to Use |
|------|---------|-------------|
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Daily commands & patterns | ⚡ **START HERE** - Quick commands, code patterns |
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Complete development guide | 📘 Full workflow, DocType creation, troubleshooting |
| **[STORE_LOCATION_HIERARCHY.md](STORE_LOCATION_HIERARCHY.md)** | Location hierarchy system | 📍 5-level warehouse structure, cascading dropdowns |
| **[DEMO_DATA_SYSTEM.md](DEMO_DATA_SYSTEM.md)** | Demo data documentation | 🧪 Sample data, testing, training |

### 📋 Reference Documentation

| File | Purpose | When to Use |
|------|---------|-------------|
| **[PROJECT_STATUS.md](PROJECT_STATUS.md)** | Current implementation status | 📊 What's built, what's working, recent changes |
| **[ROADMAP.md](ROADMAP.md)** | Development roadmap & phases | 🗺️ What's next, future features, project timeline |
| **[PROJECT_CONFIG.md](PROJECT_CONFIG.md)** | Environment & configuration | ⚙️ System info, dependencies, site setup |
| **[FUTURE_ENHANCEMENTS.md](FUTURE_ENHANCEMENTS.md)** | Complete field inventory | 📝 All fields, removed features, technical details |
| **[TESTING_ERPNEXT.md](TESTING_ERPNEXT.md)** | ERPNext integration testing | 🔗 Enable/disable ERPNext features |

---

## 🚀 Quick Start Guide

### Installation
```bash
# 1. Install the app
bench get-app https://github.com/zahidprinters/technical-store-system
bench --site test.local install-app technical_store_system

# 2. Run migrations
bench --site test.local migrate

# 3. Restart
bench restart
```

### First Steps
1. Open **Store Settings** (Modules → Technical Store System)
2. Configure general settings (company name, currency)
3. Install demo data (optional - for testing)
4. Start creating Store Items, Locations, UOMs

---

## 📚 Documentation by Use Case

### For Developers

**Starting Development**
→ Read: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Essential commands
→ Read: [DEVELOPMENT.md](DEVELOPMENT.md) - Full workflow

**Adding New DocTypes**
→ Read: [DEVELOPMENT.md](DEVELOPMENT.md) - Section: "Adding New DocTypes"
→ Pattern: Create JSON → Auto-discovery handles installation

**Understanding Architecture**
→ Read: [PROJECT_CONFIG.md](PROJECT_CONFIG.md) - Section: "System Architecture"
→ Pattern: Modular installer with auto-discovery

### For System Administrators

**Installation & Setup**
→ Read: [README.md](../README.md) - Installation instructions
→ Read: [PROJECT_CONFIG.md](PROJECT_CONFIG.md) - Environment requirements

**Configuration**
→ Read: [PROJECT_CONFIG.md](PROJECT_CONFIG.md) - Section: "Configuration"
→ UI: Store Settings DocType (all app settings)

**Demo Data**
→ Read: [DEMO_DATA_SYSTEM.md](DEMO_DATA_SYSTEM.md) - Complete reference
→ UI: Store Settings → Demo Data tab

### For Users

**Getting Started**
→ Read: [README.md](../README.md) - Features overview
→ UI: Technical Store System workspace

**Using the System**
→ Workspace: Technical Store System (all modules)
→ Help: Hover tooltips on fields

---

## 📋 What's Documented

### Current System Status
- **Version**: 0.0.1
- **Framework**: Frappe v15.91.0
- **DocTypes**: 8 (6 master + 2 child)
- **Status**: Core system complete, tabs in progress

### DocTypes Overview

| DocType | Tabs | Status | Purpose |
|---------|------|--------|---------|
| **Store Settings** | 7 | ✅ Working | App configuration |
| **Store Item** | 6 | ✅ Working | Items/products |
| **Store Location** | 4 | ✅ Working | Warehouse structure |
| **Store UOM** | 3 | ⏳ Pending | Units of measure |
| **Store Item Group** | 3 | ⏳ Pending | Item categories |
| **Store Technical Category** | 1 | ⏳ Pending | Technical classification |
| Store Item Serial Number | - | ✅ Working | Serial tracking (child) |
| Store Item Batch Number | - | ✅ Working | Batch tracking (child) |

### Demo Data Available
- 27 UOMs (Units of Measure)
- 19 Item Groups (Categories)
- 12 Technical Categories
- 11 Locations (Warehouse structure)
- 16 Sample Items

---

## 🗂️ File Locations

### Code Structure
```
technical_store_system/
├── setup/                          # Installation system
│   ├── doctypes/                   # DocType definitions
│   ├── demo_data/                  # Sample data
│   └── workspace/                  # Workspace config
├── technical_store_system/
│   └── doctype/                    # DocType implementations
│       ├── store_item/
│       ├── store_location/
│       └── ...
└── utils/                          # Helper functions
    ├── controllers/                # Business logic
    ├── helpers/                    # Utility functions
    └── validators/                 # Validation logic
```

### Documentation Structure
```
documentation/
├── INDEX.md                        # This file - navigation hub
│
├── Core Guides/
│   ├── QUICK_REFERENCE.md          # Daily commands & patterns  
│   ├── DEVELOPMENT.md              # Complete dev guide
│   ├── STORE_LOCATION_HIERARCHY.md # Location system implementation
│   └── DEMO_DATA_SYSTEM.md         # Demo data reference
│
├── Reference/
│   ├── PROJECT_STATUS.md           # Current status & recent changes
│   ├── ROADMAP.md                  # Development phases & timeline ✨ NEW
│   ├── PROJECT_CONFIG.md           # Environment & configuration
│   ├── FUTURE_ENHANCEMENTS.md      # Complete field inventory
│   └── TESTING_ERPNEXT.md          # ERPNext integration testing
│
└── archive/                        # Historical docs (deprecated)
```

---

## 🔍 Common Tasks

### Daily Development
```bash
# Make changes to DocType
bench --site test.local migrate

# Clear cache
bench --site test.local clear-cache

# Restart
bench restart

# Rebuild assets (if JS/CSS changed)
bench build --app technical_store_system
```

### Debugging
```bash
# Check DocType exists
bench --site test.local console
>>> frappe.get_meta("Store Item")

# Check demo data counts
>>> frappe.db.count("Store UOM")
>>> frappe.db.count("Store Item")

# View field ordering
>>> meta = frappe.get_meta("Store UOM")
>>> [(f.idx, f.fieldname, f.fieldtype) for f in meta.fields[:5]]
```

### Testing
```bash
# Run migrations
bench --site test.local migrate

# Install demo data (via UI)
Store Settings → Demo Data tab → Install Selected Demo Data

# Verify data
bench --site test.local console
>>> frappe.db.count("Store UOM")  # Should be 27
```

---

## 📝 Document Details

### QUICK_REFERENCE.md (290 lines)
**Essential daily commands and patterns**
- Migrate, cache, restart commands
- Code organization patterns
- Tab structure template
- File locations
- Common debugging commands
- Troubleshooting guide

### DEVELOPMENT.md (677 lines)
**Complete development guide**
- Auto-discovery pattern explained
- DocType creation workflow
- Step-by-step instructions
- Git workflow
- Feature status tracking
- Comprehensive troubleshooting

### PROJECT_CONFIG.md (1,294 lines)
**Comprehensive environment reference**
- System information (Debian 12, Python 3.11, Frappe v15.91.0)
- Dependencies checklist
- Site configuration
- User roles & permissions
- Security & compliance
- Testing guidelines
- Complete configuration reference

### DEMO_DATA_SYSTEM.md (191 lines)
**Demo data documentation**
- All demo data sets documented
- 27 UOMs, 19 groups, 12 categories, 11 locations, 16 items
- Installation via Store Settings
- Uninstall procedures
- Data structure details

---

## 🗄️ Archived Documentation

Old documentation files moved to `archive/` folder:
- `DOCS_OVERVIEW.md` (226 lines) - Replaced by INDEX.md
- `DOCUMENTATION_MAP.md` (287 lines) - Replaced by INDEX.md
- `TECHNICAL_STORE_SINGLE_DOC.md` (94 lines) - Future system design
- `INSTALLATION_SYSTEM.md` (338 lines) - Merged into README.md
- `ARCHITECTURE_SCHEMA.md` (263 lines) - Merged into PROJECT_CONFIG.md

These files are preserved for reference but not actively maintained.

---

## 🔗 External Resources

### Repository
- **GitHub**: [zahidprinters/technical-store-system](https://github.com/zahidprinters/technical-store-system)
- **Branch**: main (private)
- **License**: See [license.txt](../license.txt)

### Frappe Documentation
- **Frappe Framework**: https://frappeframework.com/docs
- **Frappe API**: https://frappeframework.com/docs/user/en/api
- **DocType Development**: https://frappeframework.com/docs/user/en/basics/doctypes

### Project Files
- **README.md**: Project introduction and installation
- **PROJECT_STATUS.md**: Current implementation status
- **DEVELOPER_GUIDE.md**: Quick developer reference
- **.cursorrules**: AI assistant guidelines

---

## 📊 Documentation Metrics

| Metric | Value |
|--------|-------|
| **Total Active Docs** | 4 files |
| **Total Lines** | 2,452 lines |
| **Archived Docs** | 5 files |
| **Archive Lines** | 1,208 lines |
| **Code Files** | 48 Python, 6 JSON, 6 JS |
| **Last Updated** | December 8, 2025 |

---

## 🎯 Next Steps

### For New Developers
1. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) (10 minutes)
2. Read [DEVELOPMENT.md](DEVELOPMENT.md) sections as needed
3. Check [PROJECT_CONFIG.md](PROJECT_CONFIG.md) for environment details
4. Start coding!

### For Current Issues
- **Tabs not showing**: 3 DocTypes need field reordering (UOM, Item Group, Technical Category)
- **Solution**: Use Frappe Customize Form to move Tab Break field to position 1
- **Status**: 50% complete (3 of 6 DocTypes working)

### For Future Development
- Implement transaction DocTypes (Stock Entry, Issue, Return)
- Add validation rules and automation
- Complete tab implementation for remaining DocTypes
- End-to-end testing of demo data system

---

**Last Updated**: December 8, 2025  
**Maintained By**: Development Team  
**Questions?** Check [DEVELOPMENT.md](DEVELOPMENT.md) troubleshooting section
