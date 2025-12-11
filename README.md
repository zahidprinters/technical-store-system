## Technical Store System

A complete inventory management system for technical/maintenance stores with hierarchical location tracking, serial/batch management, and multi-UOM support.

**Version:** 0.0.1  
**Author:** Nadeem  
**Email:** zahid_printers@yahoo.com  
**License:** MIT

### Key Features

- **Hierarchical Location System** - 5-level warehouse structure (Store → Zone → Rack → Shelf → Bin)
- **Smart Tracking** - Serial numbers and batch tracking with expiry management
- **Multi-UOM Support** - 27+ units with conversion support
- **Demo Data** - Complete sample data for testing and training
- **100% Setup-Based** - No JSON files, pure Python definitions
- Built on Frappe Framework v15

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/zahidprinters/technical-store-system --branch main
bench install-app technical_store_system
```

### Repository

**GitHub:** https://github.com/zahidprinters/technical-store-system (Private)

### Quick Start

```bash
# Install the app
bench get-app https://github.com/zahidprinters/technical-store-system
bench --site your-site install-app technical_store_system

# Migrate
bench --site your-site migrate

# Optional: Install demo data
# Go to: Store Settings → Demo Data tab → Install Demo Data
```

### Documentation

📖 **[documentation/INDEX.md](documentation/INDEX.md)** ← **START HERE**

**Core Documentation:**
- **[QUICK_REFERENCE.md](documentation/QUICK_REFERENCE.md)** - Commands & patterns
- **[DEVELOPMENT.md](documentation/DEVELOPMENT.md)** - Development guide  
- **[STORE_LOCATION_HIERARCHY.md](documentation/STORE_LOCATION_HIERARCHY.md)** - Location system
- **[DEMO_DATA_SYSTEM.md](documentation/DEMO_DATA_SYSTEM.md)** - Sample data
- **[ROADMAP.md](documentation/ROADMAP.md)** - Project phases & timeline ✨

### Current Status

✅ **Phase 1 Complete** - Foundation ready for transactions
- 8 DocTypes operational
- Hierarchical location system (Store → Zone → Rack → Shelf → Bin)
- Auto-generation of location names with cascading dropdowns
- Complete demo data system (27 UOMs, 19 groups, 11 locations, 16 items)
- Client-side filtering for fast UX

🚀 **Next:** Phase 2 - Transaction DocTypes (Receipt, Issue, Requisition)

```bash
# Quick start
cd ~/frappe-bench
bench --site [site] install-app technical_store_system
bench start

# Create feature
git checkout -b feature/your-feature
bench --site [site] new-doctype
bench --site [site] migrate

# Test and commit
bench --site [site] run-tests --app technical_store_system
git commit -m "feat: Add feature description"
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for complete workflow guide.

### Contributing

This app uses `pre-commit` for code formatting and linting:

```bash
cd apps/technical_store_system
pre-commit install
```

**Code Quality Tools:**
- ruff (Python linting and formatting)
- eslint (JavaScript linting)
- prettier (Code formatting)
- pyupgrade (Python syntax upgrades)

### Backup & Safety

**Before major changes:**
```bash
# Database backup
bench --site [site] backup --with-files
```

### CI/CD

GitHub Actions configured for:
- **CI**: Unit tests on push to `main`
- **Linters**: [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on PRs


### License

mit
