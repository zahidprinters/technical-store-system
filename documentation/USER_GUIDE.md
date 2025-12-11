# Technical Store System - User Guide
====================================

**Version:** 1.0.0
**Last Updated:** December 11, 2025
**System:** Technical Store System for Frappe/ERPNext

## 📋 Table of Contents

### [1. Quick Start Guide](#1-quick-start-guide)
- [System Setup in 5 Minutes](#system-setup-in-5-minutes)
- [First Item Creation](#first-item-creation)
- [Basic Transactions](#basic-transactions)

### [2. System Overview](#2-system-overview)
- [Key Features](#key-features)
- [User Roles](#user-roles)
- [Navigation](#navigation)

### [3. Location Management](#3-location-management)
- [Understanding Location Hierarchy](#understanding-location-hierarchy)
- [Creating Locations](#creating-locations)
- [Location Codes](#location-codes)

### [4. Item Catalog Setup](#4-item-catalog-setup)
- [Item Groups](#item-groups)
- [Item Creation](#item-creation)
- [Units of Measure](#units-of-measure)
- [Technical Categories](#technical-categories)

### [5. Inventory Transactions](#5-inventory-transactions)
- [Store Item Receipt](#store-item-receipt)
- [Store Item Issue](#store-item-issue)
- [Store Item Requisition](#store-item-requisition)

### [6. Advanced Features](#6-advanced-features)
- [Batch & Serial Tracking](#batch--serial-tracking)
- [Quality Control](#quality-control)
- [Supplier Integration](#supplier-integration)

### [7. Reporting & Analytics](#7-reporting--analytics)
- [Basic Reports](#basic-reports)
- [Analytics Dashboard](#analytics-dashboard)
- [Custom Reports](#custom-reports)

### [8. Mobile & Integration](#8-mobile--integration)
- [Mobile Access](#mobile-access)
- [API Integration](#api-integration)
- [ERPNext Integration](#erpnext-integration)

### [9. Troubleshooting](#9-troubleshooting)
- [Common Issues](#common-issues)
- [Error Messages](#error-messages)
- [Performance Tips](#performance-tips)

### [10. Support & Resources](#10-support--resources)
- [Getting Help](#getting-help)
- [Training Resources](#training-resources)
- [Contact Information](#contact-information)

---

## 1. Quick Start Guide

### System Setup in 5 Minutes

**Step 1: Access the System**
- Log in to your Frappe/ERPNext instance
- Navigate to the **Technical Store System** workspace

**Step 2: Install Demo Data**
- Go to **Store Settings**
- Click the **Demo Data** tab
- Click **"Install Demo Data"**
- Wait for confirmation (loads 27 UOMs, 19 groups, 11 locations, 16 items)

**Step 3: Verify Installation**
- Check **Store Items** - should show demo items
- Check **Store Locations** - should show hierarchical locations
- Check **Store Item Groups** - should show organized categories

**Step 4: Basic Configuration**
- Review **Store Settings** for system preferences
- Set up user roles and permissions
- Configure location hierarchy if needed

### First Item Creation

**Navigate to Store Items:**
1. Go to **Technical Store System** workspace
2. Click **Store Items**
3. Click **"New"** button

**Fill Basic Information:**
- **Item Code:** Auto-generated (e.g., ITEM-00001)
- **Item Name:** Enter descriptive name
- **Item Group:** Select from dropdown (e.g., "Electronics")
- **Technical Category:** Select type (e.g., "Component")
- **Unit of Measure:** Select UOM (e.g., "Piece")

**Configure Tracking:**
- **Has Batch Number:** Check if item uses batch tracking
- **Has Serial Number:** Check if item uses serial tracking
- **Track Expiry:** Check if item has expiration dates

**Set Stock Information:**
- **Opening Stock:** Enter initial quantity
- **Valuation Rate:** Enter cost per unit
- **Store Location:** Select default storage location

**Save and Verify:**
- Click **"Save"**
- System auto-generates item code
- Item appears in the list view

### Basic Transactions

**Receiving Items (Store Item Receipt):**
1. Go to **Store Item Receipts**
2. Click **"New"**
3. Enter receipt details:
   - Receipt number (auto-generated)
   - Supplier information
   - Receipt date
4. Add items in the Items table:
   - Select item code
   - Enter quantity received
   - Select location
   - Enter unit cost
5. Submit the receipt

**Issuing Items (Store Item Issue):**
1. Go to **Store Item Issues**
2. Click **"New"**
3. Select issue type and department
4. Add items to be issued
5. Get approval if required
6. Submit the issue

---

## 2. System Overview

### Key Features

**Hierarchical Location System:**
- 6-level warehouse structure (WH → Zone → Area → Row → Section → Bin)
- Auto-generated location codes (WH-1-Z-A-R01-S01-B01)
- Unlimited nesting for complex facilities

**Advanced Item Tracking:**
- Serial number tracking for individual items
- Batch number tracking for grouped items
- Expiry date management
- Quality control integration

**Multi-UOM Support:**
- Primary and secondary units of measure
- Automatic conversion calculations
- Flexible measurement systems

**Transaction Management:**
- Comprehensive receipt processing
- Approval-based issue workflows
- Requisition management
- Real-time stock updates

### User Roles

**System Manager (Frappe Built-in):**
- Full administrative access to entire Frappe instance
- System configuration, user management, app installations
- IT administrators, system owners

**Store Manager:**
- Full access to all features
- User and permission management
- System configuration
- All transaction approvals
- Department heads, store directors, senior management

**Store Supervisor:**
- Transaction processing and oversight
- Inventory management and quality control
- Report generation and team supervision
- Limited configuration access
- Warehouse supervisors, inventory managers, team leads

**Inventory Admin:**
- Configuration and master data management
- Item setup, location configuration, system parameters
- Master data DocTypes (full access), settings management
- Inventory coordinators, system configurators, data administrators

**Warehouse Staff:**
- Operational stock management
- Daily transactions, stock movements, basic reporting
- Transaction DocTypes (full access), item/location management
- Warehouse operators, stock clerks, inventory technicians

**Store Clerk:**
- Basic transactions (receipt/issue)
- Item lookup and search
- Basic reporting
- No configuration access
- Front desk staff, basic inventory clerks, data entry personnel

**Department User:**
- Requisition creation and management
- Item requests and approval workflows
- Limited transaction viewing
- No direct inventory access
- Department representatives, end users, request initiators

**Store Viewer:**
- Read-only access to all store data
- Reporting, monitoring, auditing, compliance checking
- All DocTypes (read-only), no modification permissions
- Auditors, compliance officers, management reporting, external consultants

**Dev User (Development Environment):**
- Development and testing environment access
- Code development, feature testing, debugging
- Test data manipulation, limited production access
- Developers, QA engineers, technical team members

**Installer User (System Deployment):**
- Installation and deployment permissions
- System installation, configuration, migration, maintenance
- File system access, database operations, deployment tools
- System administrators, DevOps engineers, deployment specialists

### Navigation

**Main Workspace:**
- Dashboard with key metrics
- Quick links to common functions
- Recent transactions
- System status indicators

**Menu Structure:**
- **Setup:** Settings, locations, items, groups
- **Transactions:** Receipts, issues, requisitions
- **Reports:** Inventory reports, analytics
- **Tools:** Utilities, imports, maintenance

---

## 3. Location Management

### Understanding Location Hierarchy

The system uses a 6-level hierarchical structure:

```
Warehouse (WH)
├── Zone (Z)
│   ├── Area (A)
│   │   ├── Row (R)
│   │   │   ├── Section (S)
│   │   │   │   └── Bin (B)
```

**Example:** `WH-1-Z-A-R01-S01-B01`
- WH-1: Warehouse 1
- Z: Zone A
- A: Area 1
- R01: Row 1
- S01: Section 1
- B01: Bin 1

### Creating Locations

**Step 1: Access Location Management**
- Go to **Store Locations**
- Click **"New"**

**Step 2: Select Location Type**
- Choose the hierarchy level (Warehouse, Zone, Area, etc.)
- Select parent location from dropdown

**Step 3: Enter Details**
- **Location Code:** Auto-generated based on hierarchy
- **Location Name:** Descriptive name
- **Description:** Additional details
- **Capacity:** Storage capacity (optional)
- **Status:** Active/Inactive

**Step 4: Configure Properties**
- **Is Warehouse:** Check for top-level locations
- **Allow Negative Stock:** Override system settings
- **Default Location:** Set as default for receipts

### Location Codes

**Auto-Generation Rules:**
- **Warehouse:** WH-[Number]
- **Zone:** [ParentCode]-Z-[Letter]
- **Area:** [ParentCode]-A-[Number]
- **Row:** [ParentCode]-R-[Number]
- **Section:** [ParentCode]-S-[Number]
- **Bin:** [ParentCode]-B-[Number]

**Manual Override:**
- Uncheck "Auto Generate Code" for custom codes
- Ensure uniqueness across the system
- Maintain hierarchical relationships

---

## 4. Item Catalog Setup

### Item Groups

**Tree Structure:**
- Unlimited nesting levels
- Parent-child relationships
- Statistical calculations
- Hierarchical reporting

**Creating Item Groups:**
1. Go to **Store Item Groups**
2. Click **"New"**
3. Enter group name
4. Select parent group (optional)
5. Add description
6. Save

### Item Creation

**Comprehensive Item Setup:**
- Basic information (code, name, group)
- Technical specifications
- Tracking preferences
- Stock parameters
- Supplier information

**Advanced Configuration:**
- Multiple UOMs
- Quality parameters
- Safety stock levels
- Reorder points

### Units of Measure

**UOM Categories:**
- Weight (kg, g, lb, oz)
- Volume (L, mL, gal, qt)
- Length (m, cm, mm, ft, in)
- Quantity (pcs, box, pack, dozen)

**UOM Conversions:**
- Define conversion factors
- Automatic calculations
- Multi-level conversions

### Technical Categories

**Purpose:**
- Equipment classification
- Maintenance categorization
- Technical specifications
- Compliance tracking

**Common Categories:**
- Components
- Equipment
- Tools
- Consumables
- Spare Parts

---

## 5. Inventory Transactions

### Store Item Receipt

**Receipt Process:**
1. Create new receipt
2. Enter supplier details
3. Add items received
4. Quality inspection (if required)
5. Submit for approval

**Key Features:**
- Multi-item receipts
- Quality control integration
- Supplier tracking
- Purchase order linking
- Automatic stock updates

### Store Item Issue

**Issue Workflow:**
1. Create issue request
2. Select items and quantities
3. Choose destination department
4. Get approvals (if required)
5. Process the issue

**Approval Matrix:**
- Configurable approval levels
- Department-based routing
- Budget validation
- Stock availability checks

### Store Item Requisition

**Requisition Process:**
1. Department user creates request
2. Specifies required items
3. Adds justification and priority
4. Routes for approval
5. Converts to issue when approved

**Priority Levels:**
- Low: Standard processing
- Medium: Expedited handling
- High: Immediate attention
- Critical: Emergency processing

---

## 6. Advanced Features

### Batch & Serial Tracking

**Batch Tracking:**
- Group identical items
- Track manufacturing dates
- Monitor expiry dates
- FIFO/LIFO management

**Serial Tracking:**
- Individual item identification
- Complete lifecycle tracking
- Maintenance history
- Warranty management

### Quality Control

**QC Process:**
- Inspection criteria definition
- Automated quality checks
- Pass/fail decisions
- Corrective action tracking

**Quality Parameters:**
- Dimensional checks
- Functional testing
- Visual inspection
- Documentation verification

### Supplier Integration

**Supplier Management:**
- Supplier master data
- Performance tracking
- Quality ratings
- Contract management

**Integration Features:**
- Purchase order linking
- Automated receipts
- Supplier performance analytics
- Preferred supplier lists

---

## 7. Reporting & Analytics

### Basic Reports

**Standard Reports:**
- Stock status reports
- Transaction history
- Location utilization
- Item movement analysis

**Export Options:**
- PDF generation
- Excel export
- CSV downloads
- Scheduled reports

### Analytics Dashboard

**Key Metrics:**
- Stock levels overview
- Transaction volumes
- Location utilization
- Supplier performance

**Interactive Features:**
- Drill-down capabilities
- Date range filtering
- Real-time updates
- Customizable widgets

### Custom Reports

**Report Builder:**
- Drag-and-drop interface
- Custom calculations
- Advanced filtering
- Scheduled execution

**Template System:**
- Save report templates
- Share with team members
- Version control
- Access permissions

---

## 8. Mobile & Integration

### Mobile Access

**Mobile Features:**
- Inventory scanning
- Location navigation
- Transaction processing
- Offline capability

**Supported Devices:**
- iOS and Android
- Barcode scanning
- GPS location
- Push notifications

### API Integration

**REST API Endpoints:**
- Item management
- Transaction processing
- Report generation
- Real-time data access

**Authentication:**
- API key management
- OAuth 2.0 support
- Rate limiting
- Audit logging

### ERPNext Integration

**Bidirectional Sync:**
- Master data synchronization
- Transaction integration
- Real-time updates
- Conflict resolution

**Integration Points:**
- Item catalog
- Customer/vendor data
- Financial transactions
- Reporting integration

---

## 9. Troubleshooting

### Common Issues

**Login Problems:**
- Check user credentials
- Verify role permissions
- Clear browser cache
- Check network connectivity

**Transaction Errors:**
- Verify item availability
- Check location validity
- Validate user permissions
- Review approval workflows

**Performance Issues:**
- Clear system cache
- Optimize database queries
- Check server resources
- Review system logs

### Error Messages

**Common Error Codes:**
- **ERR-001:** Insufficient permissions
- **ERR-002:** Item not found
- **ERR-003:** Location unavailable
- **ERR-004:** Invalid quantity

**Resolution Steps:**
- Check error details
- Verify input data
- Contact system administrator
- Review system logs

### Performance Tips

**System Optimization:**
- Regular database maintenance
- Cache management
- Index optimization
- Resource monitoring

**User Best Practices:**
- Batch processing for bulk operations
- Regular data cleanup
- Efficient search techniques
- Proper logout procedures

---

## 10. Support & Resources

### Getting Help

**In-App Help:**
- Contextual help buttons
- Interactive tutorials
- Searchable knowledge base
- Video guides

**Self-Service Options:**
- Help articles
- FAQ database
- User forums
- Training videos

### Training Resources

**Available Materials:**
- Quick start guides
- Feature tutorials
- Video demonstrations
- Best practice guides

**Training Programs:**
- System administrator training
- End-user training
- Advanced features training
- Customization training

### Contact Information

**Technical Support:**
- Email: support@technicalstoresystem.com
- Phone: +1 (555) 123-4567
- Hours: 9 AM - 6 PM EST, Monday - Friday

**Emergency Support:**
- 24/7 emergency line: +1 (555) 999-9999
- Critical system issues only

**Documentation Updates:**
- Website: docs.technicalstoresystem.com
- Release notes: updates.technicalstoresystem.com

---

**🎉 Welcome to the Technical Store System!**

This guide will help you get started quickly and make the most of all available features. Remember to use the in-app help system for contextual assistance, and don't hesitate to contact support if you need additional help.

**Happy Inventory Managing! 🚀**</content>
<parameter name="filePath">/home/erpnext/frappe-bench/apps/technical_store_system/documentation/USER_GUIDE.md