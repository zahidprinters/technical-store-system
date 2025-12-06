# Project Environment Configuration

## System Information

### Operating System
- **OS**: Debian 12 (Bookworm)
- **Architecture**: x86_64
- **Shell**: bash
- **User**: erpnext
- **Installation Type**: Standard (No Docker, No ZFS)

## Frappe Bench Configuration

### Bench Details
- **Bench Path**: `/home/erpnext/frappe-bench`
- **Bench Type**: Development

### Site Information
- **Site Name**: test.local
- **Site Path**: `/home/erpnext/frappe-bench/sites/test.local`

**Commands:**
```bash
bench --site test.local migrate
bench --site test.local console
bench --site test.local mariadb
```

### Installed Apps
```
1. frappe v15.91.0 (Core framework)
2. technical_store_system v0.0.1 (This app)
```

## Storage Configuration

### Standard File System
- **File System**: ext4 (standard Debian 12)
- **Backup Method**: Database backups + file archives
- **No ZFS**: Using standard backup methods only

**Backup Commands:**
```bash
# Database + files backup
bench --site [site] backup --with-files

# Database only
bench --site [site] backup

# List backups
ls -lh ~/frappe-bench/sites/[site]/private/backups/
```

## Database Configuration

### Database Type
- **DBMS**: MariaDB (default for Frappe)
- **Default Port**: 3306

### Database Access
```bash
# Access MariaDB console
bench --site [site] mariadb

# Or direct access
mysql -u [db_user] -p [db_name]
```

## Python Configuration

### Python Version
- **Required**: Python 3.10+
- **Current**: Python 3.11
- **Virtual Environment**: Managed by bench

### Virtual Environment Path
```bash
# Activate bench environment
cd ~/frappe-bench
source env/bin/activate
```

## Network Configuration

### Development Server
- **Default Port**: 8000 (bench start)
- **Access URL**: http://localhost:8000

### Production Server (If Configured)
- **Port**: 80/443
- **Reverse Proxy**: nginx (if configured)
- **Supervisor**: For process management

## App-Specific Configuration

### App Name
- **Technical Name**: `technical_store_system`
- **Display Name**: Technical Store System
- **Version**: 0.0.1

### App Location
```bash
# App directory
cd ~/frappe-bench/apps/technical_store_system

# Main module
cd ~/frappe-bench/apps/technical_store_system/technical_store_system
```

### Module Configuration
- **Module Name**: Technical Store System
- **Module Path**: `technical_store_system/technical_store_system/`

## Development Tools

### Editor/IDE
- **Recommended**: VS Code with Frappe extensions
- **Alternative**: Cursor (AI-powered)

### Required Extensions (VS Code)
- Python
- Frappe Framework Snippets
- GitLens
- EditorConfig

### Browser Development Tools
- **Browser**: Chrome/Firefox (with DevTools)
- **Console Access**: F12 → Console tab

## File Permissions

### Ownership
```bash
# Bench files should be owned by bench user
ls -la ~/frappe-bench/

# Should show: erpnext:erpnext or bench:bench
```

### Common Permission Issues Fix
```bash
# If permission denied
sudo chown -R $USER:$USER ~/frappe-bench/apps/technical_store_system
```

## Log Locations

### Bench Logs
```bash
~/frappe-bench/logs/bench.log
~/frappe-bench/logs/web.error.log
~/frappe-bench/logs/web.log
```

### Site Logs
```bash
~/frappe-bench/sites/[site]/logs/error.log
~/frappe-bench/sites/[site]/logs/web.log
```

### Error Log (In Desk)
```
Navigate to: Tools → Error Log
```

## Backup Locations

### Database Backups
```bash
~/frappe-bench/sites/[site]/private/backups/
```

### File Backups
```bash
~/frappe-bench/sites/[site]/private/backups/
# Contains: database.sql.gz and files.tar
```

## Environment Variables

### Common Variables
```bash
# Check current bench
echo $BENCH_PATH

# Python path
which python3

# Frappe version
bench version
```

## Ports & Services

### Default Ports
- **8000**: Web server (development)
- **9000**: Socketio server
- **6379**: Redis cache
- **11000**: Redis queue
- **3306**: MariaDB

### Check Services
```bash
# Check if services are running
bench status

# Check specific port
netstat -tlnp | grep 8000
```

## Git Configuration

### Repository Info
- **Remote**: [Add your git remote URL]
- **Branch**: develop (default development branch)

### Git User Config
```bash
# Check git config
git config user.name
git config user.email
```

## Environment Setup

### Required Python Version
- **Python**: 3.10+ (Debian 12 default: Python 3.11)
- **Virtual Environment**: Managed by bench in `~/frappe-bench/env/`

### Frappe Installation
```bash
# Check Frappe version
bench version

# Should show:
# frappe: 15.x.x or higher
```

### Bench Setup
```bash
# Bench location
cd ~/frappe-bench

# Initialize bench (if fresh install)
bench init frappe-bench --frappe-branch version-15

# Create site
bench new-site [sitename]

# Start development
bench start
```

## Installed Dependencies

### System Packages (Check Installation)
```bash
# Core requirements
python3 --version          # ✅ Should be 3.10+
python3-pip --version      # ✅ Required
python3-dev --version      # ✅ Required
git --version              # ✅ Required
node --version             # ✅ Should be 18+
npm --version              # ✅ Required
yarn --version             # ✅ Required
redis-server --version     # ✅ Required for caching
mariadb --version          # ✅ Required (database)

# Additional packages
sudo apt list --installed | grep -E "python3|redis|mariadb|nginx|supervisor"
```

### Required System Packages (If Missing)
```bash
# Install missing dependencies
sudo apt update

# Python and build tools
sudo apt install -y python3-dev python3-pip python3-venv

# Database
sudo apt install -y mariadb-server mariadb-client

# Redis (for caching and queues)
sudo apt install -y redis-server

# Node.js and package managers
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g yarn

# Other essentials
sudo apt install -y git curl wget
sudo apt install -y wkhtmltopdf  # For PDF generation
sudo apt install -y nginx         # For production (optional)
sudo apt install -y supervisor    # For production (optional)
```

### Python Dependencies
- Located in: `~/frappe-bench/apps/technical_store_system/pyproject.toml`
- Installed automatically by bench when app is installed

### Frappe Framework Dependencies
```bash
# Check installed apps
bench --site [site] list-apps

# Should show:
# frappe
# technical_store_system
```

## Quick Environment Check

Run this to verify your setup:

```bash
#!/bin/bash
echo "=== Environment Check ==="
echo "User: $(whoami)"
echo "OS: $(uname -a)"
echo "Python: $(python3 --version)"
echo "Bench Path: $(pwd)"
echo "Frappe Version: $(bench version)"
echo ""
echo "=== Site Information ==="
bench --site all list
echo ""
echo "=== Installed Apps ==="
bench --site [site] list-apps
echo ""
echo "=== Services Status ==="
bench status
```

Save this as `check_env.sh`, make executable, and run:
```bash
chmod +x check_env.sh
./check_env.sh
```

## Important Paths Quick Reference

```bash
# Bench root
~/frappe-bench/

# This app
~/frappe-bench/apps/technical_store_system/

# Site files
~/frappe-bench/sites/[site]/

# Logs
~/frappe-bench/logs/

# Backups
~/frappe-bench/sites/[site]/private/backups/

# Config
~/frappe-bench/sites/common_site_config.json
~/frappe-bench/sites/[site]/site_config.json
```

## App Installation & Configuration

### Installation Architecture

**IMPORTANT**: This app uses a modular installer system that automatically installs all fixtures during app installation.

```
App Installation Flow:
1. bench install-app technical_store_system
   ↓
2. hooks.py triggers after_install hook
   ↓
3. installer.py (universal orchestrator) runs
   ↓
4. Calls modular setup files:
   - workspace_setup.install()  → Installs workspace
   - roles setup                → Creates user roles
   - settings setup             → Initializes Store Settings
   - uom setup                  → Creates default UOMs
   ↓
5. App ready to use
```

### Installing the App
```bash
# Get app from repository
cd ~/frappe-bench
bench get-app [git-url-or-path]

# Install on site (installer runs automatically)
bench --site [site] install-app technical_store_system

# Check installation
bench --site [site] list-apps

# App is ready - fixtures installed automatically!
```

### What Gets Installed Automatically

During `install-app`, the modular installer will:
- ✅ **Workspace**: Technical Store System workspace with shortcuts and cards
- ✅ **Roles**: Store Manager, Warehouse Staff, Inventory Admin, Store Viewer
- ✅ **Settings**: Store Settings with default configuration
- ✅ **UOMs**: Default units (Piece, Box, Kg, Liter, Meter, Dozen)

**No manual configuration needed after installation!**

### Workspace Installation

The workspace system uses three components:

1. **Workspace.py** - Workspace definition
   - Location: `setup/workspace/Workspace.py`
   - Defines shortcuts, cards, links

2. **workspace_setup.py** - Workspace installer
   - Location: `setup/workspace_setup.py`
   - Functions: install(), update(), uninstall()

3. **installer.py** - Universal orchestrator
   - Location: `technical_store_system/installer.py`
   - Calls workspace_setup.install() during installation

**Installed Workspace Contains:**
- 4 Shortcuts: Store Item, Store Location, Stock Entry, Stock Balance
- 5 Cards:
  1. Inventory Management
  2. Masters (Items, Locations, Suppliers, etc.)
  3. Transactions (Orders, Receipts, Transfers)
  4. Reports & Analytics
  5. Settings & Configuration

### Uninstalling the App
```bash
# Uninstall from site (cleanup runs automatically)
bench --site [site] uninstall-app technical_store_system

# Modular uninstaller will:
# - Remove workspace (via workspace_setup.uninstall())
# - Clean up app-specific data (optional)
# - Keep historical transactions (by default)
```

### Store Settings Configuration
After installation, you can customize settings:

1. Go to: **Store → Store Settings** (already created by installer)
2. Configure:
   - **Enable ERPNext Sync**: Check if you want ERPNext integration
   - **Auto Sync Items**: Enable automatic item synchronization
   - **Stock Validation**: Enable stock balance validation
   - **Allow Negative Stock**: Configure inventory rules

### Optional ERPNext Integration
If ERPNext is installed and you want integration:

1. Enable in **Store Settings**
2. Map DocTypes:
   - Store Item → Item
   - Store Supplier → Supplier
   - Store Location → Warehouse
3. Run initial sync (if needed)

**Note**: App works perfectly WITHOUT ERPNext enabled.

## Data Migration & Backup

### Before Major Changes
```bash
# Create backup before adding DocTypes or features
bench --site [site] backup --with-files

# Create timestamped backup
bench --site [site] backup --with-files
mv ~/frappe-bench/sites/[site]/private/backups/[latest-backup].sql.gz \
   ~/frappe-bench/sites/[site]/private/backups/backup-$(date +%Y%m%d-%H%M).sql.gz
```

### Safe Migration Practices
1. **Always backup before migration**
2. Test migrations on development site first
3. Run migration: `bench --site [site] migrate`
4. Check for errors in logs
5. Verify data integrity after migration

### Automated Daily Backups
```bash
# Add to crontab
crontab -e

# Add this line for daily 2 AM backups
0 2 * * * cd /home/erpnext/frappe-bench && bench --site [site] backup --with-files >> /var/log/frappe-backup.log 2>&1
```

### Restore from Backup
```bash
# Restore database
bench --site [site] restore ~/frappe-bench/sites/[site]/private/backups/[backup-file].sql.gz

# Restore with files
bench --site [site] restore ~/frappe-bench/sites/[site]/private/backups/[backup-file].sql.gz --with-private-files [files].tar --with-public-files [public-files].tar
```

## User Roles & Permissions

### Default Roles

#### 1. Store Manager (Full Access)
**Permissions:**
- Create, Read, Update, Delete all DocTypes
- Configure Store Settings
- Generate all reports
- Manage users and permissions
- Approve stock adjustments

**Assign to**: Store supervisors, managers

#### 2. Warehouse Staff (Operational Access)
**Permissions:**
- Create Store Stock Entry
- Update Store Stock Balance
- Read Store Item, Store Location
- Create Store Stock Transfer
- View stock reports

**Assign to**: Warehouse workers, stock clerks

#### 3. Inventory Admin (Configuration Access)
**Permissions:**
- Create/Edit Store Item, Store UOM, Store Category
- Manage Store Location
- Configure Store Price List
- View all reports
- No access to Store Settings

**Assign to**: Inventory controllers, product managers

#### 4. Viewer (Read-Only)
**Permissions:**
- Read all Store DocTypes
- View all reports
- No create/update/delete access
- Export data allowed

**Assign to**: Accountants, auditors, external viewers

### Setting Up Roles
```bash
# In Frappe desk:
1. Go to: User Management → Role
2. Create custom roles if needed
3. Assign permissions to roles in each DocType
4. Assign roles to users: User → Roles section
```

### Permission Rules Example
```python
# In DocType permissions JSON
{
	"Store Manager": {
		"read": 1, "write": 1, "create": 1, "delete": 1,
		"submit": 1, "cancel": 1, "amend": 1
	},
	"Warehouse Staff": {
		"read": 1, "write": 1, "create": 1, "delete": 0
	},
	"Inventory Admin": {
		"read": 1, "write": 1, "create": 1, "delete": 0
	},
	"Viewer": {
		"read": 1, "write": 0, "create": 0, "delete": 0
	}
}
```

## Reporting & Analytics

### Key Reports Available

#### Stock Reports
1. **Stock Summary Report**
   - Current stock levels per location
   - Item-wise stock balance
   - Stock valuation
   - **Path**: Store → Reports → Stock Summary

2. **Stock Movement Report**
   - Transaction history
   - Item movements between locations
   - Date-wise stock changes
   - **Path**: Store → Reports → Stock Movement

3. **Low Stock Alert Report**
   - Items below reorder level
   - Location-wise alerts
   - Reorder suggestions
   - **Path**: Store → Reports → Low Stock Alert

#### Supplier Reports
4. **Supplier Performance Report**
   - Delivery time analysis
   - Quality metrics
   - Purchase history
   - **Path**: Store → Reports → Supplier Performance

#### Analytics Dashboard
5. **Store Analytics Dashboard**
   - Real-time KPIs
   - Stock turnover ratio
   - Top moving items
   - Location-wise stock distribution
   - **Path**: Store → Store Analytics Dashboard

### Generating Reports
```bash
# Export report to Excel
1. Open report
2. Apply filters
3. Click "Export" → Excel

# Schedule automated reports (via email)
1. Go to: Tools → Auto Email Report
2. Set report name and frequency
3. Add recipients
```

## Mobile & API Integration

### REST API Endpoints

All whitelisted methods accessible via REST API:

**Base URL**: `https://[your-site]/api/method/technical_store_system.api.[method_name]`

#### Authentication
```bash
# Get API key
1. User → API Access → Generate Keys
2. Use in headers:
   Authorization: token [api_key]:[api_secret]
```

#### Example API Calls
```python
# Get item stock
GET /api/method/technical_store_system.api.get_item_stock
Params: {"item_code": "ITEM-001"}

# Create stock entry (mobile app)
POST /api/method/technical_store_system.api.create_stock_entry
Data: {
	"item": "ITEM-001",
	"location": "LOC-001",
	"quantity": 100,
	"entry_type": "Receipt"
}
```

### Barcode Scanning Integration
```python
# Barcode lookup API
GET /api/method/technical_store_system.api.barcode.get_item_by_barcode
Params: {"barcode": "1234567890"}

# Returns: Item details with stock balance
```

### Mobile App Integration
- Use Frappe's mobile app framework
- Create custom screens for Store DocTypes
- Implement offline sync capability
- Use barcode scanner for stock transactions

## Error Logging & Debugging

### Browser Console Errors
```bash
# Check JavaScript errors
1. Open browser (Chrome/Firefox)
2. Press F12 → Console tab
3. Look for red errors
4. Check Network tab for API failures
```

### Bench Logs
```bash
# Watch live logs
bench --site [site] --verbose

# Check error log
tail -f ~/frappe-bench/logs/bench.log

# Check site-specific log
tail -f ~/frappe-bench/sites/[site]/logs/error.log

# Filter errors only
grep -i "error" ~/frappe-bench/logs/bench.log
```

### Frappe Error Log (In Desk)
```bash
# Access in UI
1. Go to: Tools → Error Log
2. Filter by: Date, User, Method
3. View full traceback
4. Mark as resolved after fixing
```

### Common Error Patterns
```python
# ValidationError
frappe.ValidationError: [message]
→ Check validation rules in DocType

# PermissionError
frappe.PermissionError: [message]
→ Check user roles and permissions

# DoesNotExistError
frappe.DoesNotExistError: [DocType] [name] not found
→ Verify record exists in database

# LinkValidationError
frappe.LinkValidationError: [field] must be a valid [DocType]
→ Check link field values
```

## Versioning & Change Management

### Version Tracking
```python
# In technical_store_system/__init__.py
__version__ = "0.0.1"

# Update after each release
# Format: MAJOR.MINOR.PATCH
# 0.1.0 → First stable release
# 0.1.1 → Bug fixes
# 0.2.0 → New features
# 1.0.0 → Production ready
```

### Changelog Maintenance
Create `CHANGELOG.md` in project root:

```markdown
# Changelog

## [0.1.0] - 2025-12-06
### Added
- Store Item DocType
- Store Location DocType
- Store Stock Entry DocType
- Basic stock balance tracking

### Changed
- Updated validation rules for stock entry

### Fixed
- Stock calculation error in negative scenarios

## [0.0.1] - 2025-12-05
### Added
- Initial project setup
- App structure created
```

### Feature Progress Tracking
Update in `DEVELOPMENT.md`:

```markdown
## Feature Status

### Core DocTypes
- ✅ Store Location - v0.1.0 (Working)
- ✅ Store Item - v0.1.0 (Working)
- ⏳ Store Stock Entry - v0.2.0 (In Progress)
- ⬜ Store Supplier - Planned for v0.3.0
```

### Git Tags for Releases
```bash
# Tag stable version
git tag -a v0.1.0 -m "Release v0.1.0 - Core DocTypes"
git push origin v0.1.0

# View version history
git log --tags --oneline
```

## Testing & QA Guidelines

### Testing Checklist (For Each Feature)

#### 1. Record Creation
```
✅ Can create new record
✅ Required fields validated
✅ Default values populate correctly
✅ Auto-naming works (if configured)
```

#### 2. Saving & Validation
```
✅ Can save without errors
✅ Validation rules work correctly
✅ Invalid data rejected with clear message
✅ Linked fields validate properly
```

#### 3. Editing Records
```
✅ Can modify and save changes
✅ Changes persist after save
✅ Modified timestamp updates
✅ No data loss on edit
```

#### 4. Deleting Records
```
✅ Can delete if no links exist
✅ Cannot delete if linked to other docs
✅ Confirmation prompt appears
✅ Cascade delete works (if configured)
```

#### 5. Calculations & Logic
```
✅ Stock calculations correct
✅ Price calculations accurate
✅ Totals match individual items
✅ Rounding handled properly
```

#### 6. UI & UX
```
✅ Form layout clean and organized
✅ List view shows relevant columns
✅ Filters work correctly
✅ Search functionality works
✅ No console errors (F12)
```

#### 7. Permissions
```
✅ Roles respected (read/write/delete)
✅ Unauthorized access blocked
✅ Permission errors clear
```

#### 8. Performance
```
✅ Page loads in < 2 seconds
✅ List view paginates properly
✅ Large datasets handled well
✅ No memory leaks
```

### Running Automated Tests
```bash
# Run all app tests
bench --site [site] run-tests --app technical_store_system

# Run specific DocType test
bench --site [site] run-tests --app technical_store_system --doctype "Store Item"

# Run with coverage
bench --site [site] run-tests --app technical_store_system --coverage
```

### Manual Testing Script
```bash
# Create test script: test_feature.sh
#!/bin/bash
echo "Testing Store Item..."
bench --site [site] console << EOF
item = frappe.new_doc("Store Item")
item.item_name = "Test Item"
item.item_code = "TEST-001"
item.insert()
print(f"Created: {item.name}")
EOF
```

## Security & Compliance

### Input Validation
```python
# Always validate user input
def validate_quantity(qty):
	if not qty or qty <= 0:
		frappe.throw("Quantity must be positive")
	if qty > 1000000:
		frappe.throw("Quantity too large")
```

### Permission Checks
```python
# Check before any operation
@frappe.whitelist()
def delete_stock_entry(name):
	if not frappe.has_permission("Store Stock Entry", "delete"):
		frappe.throw("Not permitted", frappe.PermissionError)
	
	doc = frappe.get_doc("Store Stock Entry", name)
	doc.delete()
```

### Audit Logs
```python
# Log sensitive operations
def on_submit(self):
	frappe.log_error(
		title=f"Stock Entry Submitted: {self.name}",
		message=f"User: {frappe.session.user}, Qty: {self.quantity}"
	)
```

### SQL Injection Prevention
```python
# ✅ GOOD: Use frappe.db methods
items = frappe.get_all("Store Item", filters={"item_code": code})

# ❌ BAD: Never use raw SQL with user input
# frappe.db.sql(f"SELECT * FROM `tabStore Item` WHERE item_code = '{code}'")
```

### Data Encryption
```python
# Encrypt sensitive fields
from frappe.utils.password import encrypt, decrypt

encrypted_data = encrypt("sensitive_data")
decrypted_data = decrypt(encrypted_data)
```

### Compliance Requirements
- ✅ Maintain audit trail of all transactions
- ✅ Log user actions (who, what, when)
- ✅ Implement data retention policies
- ✅ Enable role-based access control
- ✅ Regular security audits

## Common Pitfalls / Red Flags

### 🛑 NEVER Do These

#### 1. Using ERPNext DocTypes Directly
```python
# ❌ BAD
item = frappe.get_doc("Item", "ITEM-001")  # ERPNext Item

# ✅ GOOD
item = frappe.get_doc("Store Item", "ITEM-001")  # Our Store Item
```

#### 2. Skipping Incremental Testing
```python
# ❌ BAD: Adding multiple features without testing
- Add Store Item
- Add Store Supplier
- Add Store Stock Entry
- Test everything together → BREAKS

# ✅ GOOD: Test after each feature
- Add Store Item → TEST ✅
- Add Store Supplier → TEST ✅
- Add Store Stock Entry → TEST ✅
```

#### 3. Modifying Core Frappe Files
```bash
# ❌ NEVER modify these
~/frappe-bench/apps/frappe/
~/frappe-bench/apps/erpnext/

# ✅ Only modify your app
~/frappe-bench/apps/technical_store_system/
```

#### 4. Hardcoding Values
```python
# ❌ BAD
site = "mysite.localhost"
db_name = "production_db"

# ✅ GOOD
site = frappe.local.site
db_name = frappe.conf.db_name
```

#### 5. Bypassing Permissions
```python
# ❌ BAD
frappe.db.sql("UPDATE `tabStore Item` SET price = 0")

# ✅ GOOD
if frappe.has_permission("Store Item", "write"):
	doc = frappe.get_doc("Store Item", name)
	doc.price = 0
	doc.save()
```

#### 6. Ignoring Errors in Logs
```bash
# ❌ BAD: Ignoring red errors in console
# Continuing development despite errors

# ✅ GOOD: Fix ALL errors immediately
# Check console (F12) after every change
# Fix errors before proceeding
```

#### 7. Not Using Version Control
```bash
# ❌ BAD: No git commits, working directly

# ✅ GOOD: Commit after each working feature
git add .
git commit -m "feat: Add Store Item DocType"
```

#### 8. Using Spaces Instead of Tabs
```python
# ❌ BAD (spaces in Python files)
def my_function():
    return True

# ✅ GOOD (tabs in Python files)
def my_function():
	return True
```

#### 9. Adding ERPNext to required_apps
```python
# ❌ BAD in hooks.py
required_apps = ["erpnext"]

# ✅ GOOD
required_apps = []  # Empty, app is standalone
```

#### 10. Skipping Backups Before Changes
```bash
# ❌ BAD: Making major changes without backup

# ✅ GOOD: Always backup first
bench --site [site] backup --with-files
# Then make changes
```

### ⚠️ Warning Signs

Watch out for these indicators of problems:

```
🚨 White screen after changes → Rollback immediately
🚨 Import errors on bench start → Check syntax/indentation
🚨 Cannot access DocType → Clear cache, rebuild
🚨 Old features broken → Rollback and test incrementally
🚨 Console full of errors → Stop and fix all errors
🚨 Slow page loads → Check database queries, add indexes
🚨 Permission errors → Review role permissions
🚨 Data not saving → Check validation rules
```

### Safe Development Checklist

Before pushing to production:

```
✅ All tests pass
✅ No errors in browser console
✅ No errors in bench logs
✅ All features tested manually
✅ Backup created
✅ Git committed
✅ Documentation updated
✅ Permissions configured
✅ Performance acceptable
✅ Security validated
```

## Notes for AI Assistant

When I ask about:
- **Site commands**: Replace `[site]` with actual site name from config
- **Paths**: Use full paths starting from `/home/erpnext/frappe-bench/`
- **Backups**: Use standard database backups (NO ZFS)
- **Permissions**: Verify user permissions before file operations
- **Testing**: Always remind to test after changes
- **ERPNext**: Check if installed before suggesting integration

## To Be Filled By User

**IMPORTANT**: Fill in your actual values below:

```yaml
# Site Configuration
SITE_NAME: "[Your site name - e.g., site1.local or mysite.localhost]"
SITE_URL: "[Your site URL - e.g., http://localhost:8000]"
SITE_ADMIN_EMAIL: "[Admin email address]"

# Database
DB_NAME: "[Database name - usually matches site name with _ instead of .]"
DB_USER: "[Database user - usually your site name]"
DB_PASSWORD: "[Store securely, don't commit to git]"

# Git Repository
GIT_REMOTE_URL: "[Your git remote URL - e.g., https://github.com/user/repo.git]"
GIT_BRANCH: "[Current working branch - usually 'develop']"

# Production Details (if applicable)
PRODUCTION_URL: "[Production URL if deployed]"
PRODUCTION_SERVER: "[Server IP/hostname if deployed]"

# Installed Apps
INSTALLED_APPS:
  - frappe: v15.91.0
  - technical_store_system: v0.0.1

# ERPNext Integration
ERPNEXT_INSTALLED: no
ERPNEXT_SYNC_ENABLED: no
```

---

## Current Implementation Architecture

### Implementation Pattern: Modular Auto-Discovery System

Based on **TECHNICAL_STORE_SINGLE_DOC.md** specification, we use a modular installer with auto-discovery pattern.

#### Core Components

**1. Universal Orchestrator: `installer.py`**
- Universal installer that orchestrates all setup modules
- Hooks: `after_install`, `after_uninstall`, `after_migrate`
- Functions: `install_workspace()`, `install_doctypes()`, `create_default_roles()`, etc.
- No code changes needed when adding new components

**2. Setup Modules (Auto-discovered)**
- `setup/workspace_setup.py` - Workspace lifecycle management
- `setup/doctypes_setup.py` - Auto-discovers DocTypes from `setup/doctypes/*.py`
- Future: `setup/reports_setup.py`, `setup/dashboards_setup.py`, etc.

**3. DocType Auto-Discovery**
- Drop any DocType definition file in `setup/doctypes/*.py`
- Automatically discovered and installed (no installer changes)
- Pattern: Each DocType = one Python file with full definition

#### Current DocTypes (Phase 0 - Foundation Complete)

1. **Store Settings** (Single DocType)
   - Path: `setup/doctypes/StoreSettings.py`
   - Configuration: General, Stock, Pricing, ERPNext Integration, Notifications, Advanced
   - Status: ✅ Installed, initialized with defaults

2. **Store Item** (Basic version)
   - Path: `setup/doctypes/StoreItem.py`
   - Fields: item_name, description
   - Status: ✅ Installed (will be enhanced in Phase 1)

3. **Store Location** (Basic version)
   - Path: `setup/doctypes/StoreLocation.py`
   - Fields: location_name, location_type, address
   - Status: ✅ Installed (will be enhanced in Phase 1)

#### Default Roles Created
- Store Manager
- Warehouse Staff
- Inventory Admin
- Store Viewer

#### Workspace
- Name: "Technical Store System"
- Sections: Masters, Settings, Administration
- Status: ✅ Displays in UI with all links

### Implementation Roadmap

Following **TECHNICAL_STORE_SINGLE_DOC.md** + **IMPLEMENTATION_CHECKLIST.md**:

**✅ Phase 0: Foundation (COMPLETED)**
- Modular installer with auto-discovery
- Workspace setup
- Basic roles
- Store Settings (Single DocType)
- Basic Store Item and Store Location

**🔄 Phase 1: Core Masters (NEXT - Priority 1)**
- Module 1: Item & Stock Management Masters
  - Store UOM, Store Item Group, Store Brand
  - Store Unit, Enhanced Store Item, Enhanced Store Location
  - Stock Level, Stock Ledger Entry (immutable)
- Module 2: Supplier & Vendor Management
- Module 3: Serial & Batch Tracking

**📋 Phase 2-9: Operational Modules (Priority 2-9)**
- Demand & Issue Management
- Transfer & Purchase
- Analytics & Intelligence
- Mobile & Barcode
- Budget & Cost Control
- Asset Management
- Compliance & Audit
- Reporting & Dashboards

**Total Scope:**
- 35+ DocTypes
- 14 Modules
- 200+ implementation tasks
- Estimated: 14-16 days

### Key Design Principles

From TECHNICAL_STORE_SINGLE_DOC.md:

1. **Modular ERP Add-on**: Standalone app with optional ERPNext integration
2. **Approval-First Workflows**: Multi-level hierarchical approvals
3. **Data Integrity**: Immutable stock ledger, referential constraints
4. **Multi-Store Support**: Store/unit scoped data with isolated ledgers
5. **Performance**: Indexed queries, pagination, caching
6. **Security**: RBAC, audit trails, compliance alerts
7. **Mobile-First**: Offline-capable mobile app integration
8. **Automation**: 16+ scheduled tasks, 20+ doc events, 50+ server methods

### Technical Details

**DocType Pattern:**
```python
# File: setup/doctypes/ExampleDocType.py
doctype = {
    "name": "Example DocType",
    "module": "Technical Store System",
    "custom": 1,  # Custom DocTypes (no developer mode needed)
    "issingle": 0,  # or 1 for Single DocTypes
    "fields": [...],
    "permissions": [...]
}
```

**Installation Flow:**
1. User: `bench --site test.local install-app technical_store_system`
2. Frappe calls: `hooks.py` → `after_install`
3. Executes: `installer.after_install()`
4. Calls: `workspace_setup.install()`, `doctypes_setup.install()`, etc.
5. DocTypes setup: `get_all_doctypes()` scans `setup/doctypes/*.py`
6. Creates: All discovered DocTypes automatically

**Commands:**
```bash
# Install/Uninstall
bench --site test.local install-app technical_store_system
bench --site test.local uninstall-app technical_store_system

# Migrate (after code changes)
bench --site test.local migrate

# Database access
bench --site test.local mariadb
bench --site test.local console
```

---

## Update This File

Whenever environment changes:
- ✅ Add new site
- ✅ Change storage configuration
- ✅ Add new services
- ✅ Update paths
- ✅ Add new tools/dependencies
- ✅ Update implementation status
- ✅ Add new DocTypes

Keep this file updated as it helps AI understand your specific setup and progress!
