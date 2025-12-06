# Project Documentation Overview

## Document Structure

This project contains comprehensive documentation organized for different purposes:

### 📋 Quick Access Documents

1. **[TECHNICAL_STORE_SINGLE_DOC.md](TECHNICAL_STORE_SINGLE_DOC.md)** - 🎯 MASTER SPECIFICATION
   - Complete system architecture (35+ DocTypes, 14 modules)
   - All modules detailed (Core + Enhancements)
   - API surface and database schema
   - Integration hooks and workflows
   - Security and compliance requirements
   - **Use this for**: Understanding complete system scope
   - **Status**: Consolidated master reference

2. **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** - 📊 ROADMAP
   - 200+ implementation tasks organized in 10 phases
   - Detailed checklist for each DocType
   - Current progress tracking (Phase 0 complete)
   - Estimated timeline (14-16 days)
   - **Use this for**: Tracking what's done and what's next
   - **Status**: Active, updated as we progress

3. **[PROJECT_CONFIG.md](PROJECT_CONFIG.md)** - ⚙️ Environment Configuration
   - System information (Debian 12, Python 3.11, Frappe v15.91.0)
   - Site: test.local
   - Current architecture (modular installer with auto-discovery)
   - Installed DocTypes and their status
   - **Use this for**: Environment-specific settings and current state
   - **Status**: Updated with actual values

4. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - ⚡ START HERE
   - Essential commands cheat sheet
   - Current DocTypes list
   - Code patterns and examples
   - Testing checklist
   - **Use this for**: Daily development tasks
   - **Status**: Updated with auto-discovery pattern

5. **[DEVELOPMENT.md](DEVELOPMENT.md)** - 📖 Complete Guide
   - Auto-discovery pattern explained
   - DocType creation template
   - Complete workflow and commands
   - Current implementation status
   - **Use this for**: Understanding development workflow
   - **Status**: Updated with modular pattern

6. **[.cursorrules](../.cursorrules)** - 🤖 AI Assistant Guidelines
   - Project architecture decisions
   - Coding standards and conventions
   - Critical rules (NEVER/ALWAYS)
   - Frappe patterns
   - **Use this for**: AI-assisted development

7. **[README.md](../README.md)** - 📄 Project Overview
   - Project description
   - Installation instructions
   - Quick start guide
   - **Use this for**: Project introduction

## When to Use Which Document?

### I need to know site name, paths, or system details
→ **PROJECT_CONFIG.md**

### I need to quickly find a command
→ **QUICK_REFERENCE.md**

### I'm adding a new feature
→ **DEVELOPMENT.md** (Step-by-step process)

### I want to understand project architecture
→ **.cursorrules** (Architecture section)

### I need code examples
→ **QUICK_REFERENCE.md** (Quick patterns) or **.cursorrules** (Detailed patterns)

### I'm setting up the project for first time
→ **README.md** (Installation) → **DEVELOPMENT.md** (Setup)

### I'm working with AI assistant
→ **.cursorrules** (AI reads this automatically)

### I want to contribute
→ **README.md** (Contributing section)

### I need to troubleshoot an issue
→ **QUICK_REFERENCE.md** (Quick fixes) → **DEVELOPMENT.md** (Detailed troubleshooting)

## Key Principles (Found in All Docs)

### 1. Standalone Architecture
- App works WITHOUT ERPNext
- Optional ERPNext integration if installed
- No hard dependencies

### 2. Incremental Development
- ONE feature at a time
- Test after each feature
- Never break existing functionality

### 3. Naming Conventions
- DocTypes: `Store Item` (PascalCase + Store prefix)
- Files: `store_item.py` (snake_case)
- Fields: `item_code` (snake_case)

### 4. Code Quality
- TABS for Python/JS/CSS/HTML
- 2 SPACES for JSON
- Max 110 chars per line (Python)
- Descriptive variable names

### 5. Safety First
- Backup before major changes
- Git branch per feature
- Test immediately after changes
- Never skip testing phase

## Project Status Tracking

Current status maintained in: **DEVELOPMENT.md**

Format:
```
✅ Feature Name - Working
⏳ Feature Name - In Progress
⬜ Feature Name - Not Started
❌ Feature Name - Blocked
```

## Command Categories

### Most Used (Memorize These)
```bash
bench start                          # Start development
bench --site [site] migrate          # Apply changes
bench --site [site] clear-cache      # Clear cache
bench --site [site] console          # Python console
```

### DocType Creation
```bash
bench --site [site] new-doctype      # Create new DocType
```

### Testing
```bash
bench --site [site] run-tests --app technical_store_system
```

### Backup
```bash
bench --site [site] backup --with-files
sudo zfs snapshot zstore/frappe-bench@snapshot-name
```

## File Organization

```
technical_store_system/
├── README.md                    # Project overview
├── DOCS_OVERVIEW.md             # Documentation guide
├── PROJECT_CONFIG.md            # Environment configuration ⚙️
├── DEVELOPMENT.md               # Complete development guide
├── QUICK_REFERENCE.md           # Command cheat sheet
├── .cursorrules                 # AI guidelines
├── .editorconfig                # Editor settings
├── .gitignore                   # Git exclusions
├── pyproject.toml               # Python config
├── license.txt                  # MIT license
└── technical_store_system/      # Main code
    ├── hooks.py                 # App hooks
    ├── modules.txt              # Modules
    ├── patches.txt              # Migrations
    ├── config/                  # Configuration
    ├── public/                  # Static files
    ├── templates/               # Jinja templates
    ├── www/                     # Web pages
    └── technical_store_system/  # DocTypes
        ├── doctype/             # DocType definitions
        ├── report/              # Reports
        ├── page/                # Pages
        ├── api/                 # API endpoints
        └── utils/               # Utilities
```

## Next Steps

1. **First Time Setup**
   - Read README.md (Installation)
   - Follow DEVELOPMENT.md (Initial Setup)
   - Bookmark QUICK_REFERENCE.md

2. **Daily Development**
   - Check QUICK_REFERENCE.md for commands
   - Follow incremental approach (DEVELOPMENT.md)
   - Let AI read .cursorrules

3. **Before Adding Feature**
   - Create backup/snapshot
   - Create git branch
   - Read DEVELOPMENT.md workflow

4. **After Adding Feature**
   - Test using checklist (QUICK_REFERENCE.md)
   - Commit to git
   - Update status in DEVELOPMENT.md

## Resources

- **Frappe Documentation**: https://frappeframework.com/docs
- **Frappe Forum**: https://discuss.frappe.io/
- **ERPNext Docs** (for integration): https://docs.erpnext.com/

## Maintenance

Keep documentation updated:
- Add new commands to QUICK_REFERENCE.md
- Update status in DEVELOPMENT.md
- Add new patterns to .cursorrules
- Update README.md for major changes

---

**Remember**: Documentation is code. Keep it clean, updated, and useful! 📚
