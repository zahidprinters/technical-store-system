# Technical Store System - Administrator Guide
===============================================

**Version:** 1.0.0
**Last Updated:** December 11, 2025
**System:** Technical Store System for Frappe/ERPNext

## 📋 Table of Contents

### [1. System Architecture](#1-system-architecture)
- [Frappe Framework Integration](#frappe-framework-integration)
- [Database Design](#database-design)
- [Security Model](#security-model)
- [Auto-Discovery Pattern](#auto-discovery-pattern)

### [2. Installation & Setup](#2-installation--setup)
- [Prerequisites](#prerequisites)
- [Installation Process](#installation-process)
- [Initial Configuration](#initial-configuration)
- [Demo Data Installation](#demo-data-installation)

### [3. User Management & Security](#3-user-management--security)
- [User Roles & Permissions](#user-roles--permissions)
- [Access Control](#access-control)
- [Audit Trails](#audit-trails)
- [Security Best Practices](#security-best-practices)

### [4. System Configuration](#4-system-configuration)
- [Store Settings](#store-settings)
- [Location Hierarchy Setup](#location-hierarchy-setup)
- [Item Catalog Configuration](#item-catalog-configuration)
- [Transaction Workflows](#transaction-workflows)

### [5. Maintenance & Operations](#5-maintenance--operations)
- [Backup & Recovery](#backup--recovery)
- [Performance Tuning](#performance-tuning)
- [Monitoring & Alerts](#monitoring--alerts)
- [Log Management](#log-management)

### [6. Customization & Development](#6-customization--development)
- [Adding Custom Fields](#adding-custom-fields)
- [Custom Workflows](#custom-workflows)
- [Client Scripts](#client-scripts)
- [API Development](#api-development)

### [7. Integration Management](#7-integration-management)
- [ERPNext Integration](#erpnext-integration)
- [Third-Party APIs](#third-party-apis)
- [Data Import/Export](#data-importexport)
- [Webhook Configuration](#webhook-configuration)

### [8. Troubleshooting & Support](#8-troubleshooting--support)
- [Common Issues](#common-issues)
- [Diagnostic Tools](#diagnostic-tools)
- [Performance Issues](#performance-issues)
- [Emergency Procedures](#emergency-procedures)

### [9. Upgrade & Migration](#9-upgrade--migration)
- [Version Upgrade Process](#version-upgrade-process)
- [Data Migration](#data-migration)
- [Rollback Procedures](#rollback-procedures)
- [Testing Protocols](#testing-protocols)

### [10. Compliance & Legal](#10-compliance--legal)
- [Data Protection](#data-protection)
- [Audit Requirements](#audit-requirements)
- [Regulatory Compliance](#regulatory-compliance)
- [Legal Considerations](#legal-considerations)

---

## 1. System Architecture

### Frappe Framework Integration

**Framework Compatibility:**
- **Frappe Framework:** v15.91.0+
- **ERPNext:** v15.0.0+ (optional integration)
- **Python:** 3.11+
- **Database:** MariaDB 10.11.14+ / MySQL 8.0+

**App Structure:**
```
technical_store_system/
├── hooks.py                 # Frappe integration hooks
├── installer.py            # Auto-discovery installer
├── setup/                  # DocType definitions
│   ├── doctypes/          # DocType Python files
│   ├── client_scripts/    # UI enhancements
│   └── demo_data/         # Sample data
├── utils/                 # Business logic
│   ├── controllers/       # DocType controllers
│   └── helpers/          # Utility functions
└── technical_store_system/doctype/  # Frappe standard
```

### Database Design

**Core Tables:**
- **tabStore Settings:** System configuration
- **tabStore Location:** Hierarchical location structure
- **tabStore Item:** Item master data
- **tabStore Item Group:** Item categorization
- **tabStore UOM:** Units of measure
- **tabStore Item Receipt:** Transaction records
- **tabStore Item Issue:** Issue records
- **tabStore Item Requisition:** Request records

**Child Tables:**
- **Store Item Receipt Item:** Receipt line items
- **Store Item Issue Item:** Issue line items
- **Store Item Serial Number:** Serial tracking
- **Store Item Batch Number:** Batch tracking

**Indexing Strategy:**
- Primary keys on all DocTypes
- Foreign key indexes for relationships
- Composite indexes for common queries
- Full-text indexes for search fields

### Security Model

**Authentication:**
- Frappe framework authentication
- Role-based access control (RBAC)
- Two-factor authentication support
- Session management

**Authorization:**
- **Store Manager:** Full system access
- **Store Supervisor:** Transaction and reporting access
- **Store Clerk:** Basic transaction access
- **Department User:** Requisition access only

**Data Protection:**
- Field-level permissions
- Record-level security
- Encrypted sensitive data
- Audit trail logging

### Auto-Discovery Pattern

**Installation Philosophy:**
- **Zero Manual Configuration:** System discovers and installs automatically
- **Modular Design:** Components install independently
- **Dependency Resolution:** Automatic prerequisite checking
- **Error Recovery:** Rollback on installation failures

**Discovery Process:**
1. Scan setup/doctypes/ for DocType definitions
2. Resolve dependencies between DocTypes
3. Install in correct order
4. Validate installation success
5. Install client scripts and demo data

---

## 2. Installation & Setup

### Prerequisites

**System Requirements:**
- **OS:** Debian 12+ / Ubuntu 20.04+ / CentOS 8+
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 20GB free space
- **CPU:** 2 cores minimum

**Software Dependencies:**
- Python 3.11+
- Node.js 18+
- Redis 6+
- Nginx (for production)
- MariaDB/MySQL

**Network Requirements:**
- Inbound: HTTP/HTTPS (80/443)
- Database connectivity
- External API access (if integrated)

### Installation Process

**Step 1: Frappe Bench Setup**
```bash
# Install Frappe Bench
pip install frappe-bench

# Create new bench
bench init frappe-bench --python python3.11

# Change to bench directory
cd frappe-bench
```

**Step 2: App Installation**
```bash
# Get the Technical Store System app
bench get-app https://github.com/zahidprinters/technical-store-system.git

# Install on site
bench --site test.local install-app technical_store_system
```

**Step 3: Database Migration**
```bash
# Run migrations (auto-discovers new DocTypes)
bench --site test.local migrate

# Clear cache
bench --site test.local clear-cache
```

**Step 4: Start Services**
```bash
# Start development server
bench start

# Access at: http://test.local:8000
```

### Initial Configuration

**Store Settings Configuration:**
1. Navigate to **Store Settings**
2. Configure system preferences:
   - Company information
   - Default locations
   - Approval workflows
   - Integration settings

**User Setup:**
1. Create user accounts
2. Assign appropriate roles
3. Set up permissions
4. Configure notifications

### Demo Data Installation

**Automated Installation:**
```bash
# Via Store Settings UI
# Go to Store Settings → Demo Data tab → Install Demo Data

# Or via console
bench --site test.local console -c "from technical_store_system.setup.demo_data_handler import install_demo_data; install_demo_data()"
```

**Demo Data Includes:**
- **27 Units of Measure:** Complete UOM library
- **19 Item Groups:** Hierarchical categories
- **11 Store Locations:** Sample warehouse structure
- **16 Store Items:** Sample inventory items

---

## 3. User Management & Security

### User Roles & Permissions

**Built-in Roles (Auto-Created):**
- **System Manager:** Full administrative access to entire Frappe instance
- **Store Manager:** Complete store operations and strategic oversight
- **Warehouse Staff:** Operational stock management and daily transactions
- **Inventory Admin:** Configuration and master data management
- **Store Viewer:** Read-only access to all store data

**Extended Roles (Manual Setup Recommended):**
- **Store Supervisor:** Transaction oversight and quality control
- **Store Clerk:** Basic transaction processing and data entry
- **Department User:** Requisition and request management
- **Dev User:** Development and testing environment access
- **Installer User:** Installation and deployment permissions

**Custom Roles:**
- Create role-specific permissions
- Department-based access control
- Project-specific roles
- Temporary access roles

### Access Control

**Permission Levels:**
- **Read:** View records
- **Write:** Create and modify
- **Create:** New record creation
- **Delete:** Record deletion
- **Submit:** Transaction submission
- **Cancel:** Transaction cancellation

**Field-Level Security:**
- Hide sensitive fields
- Read-only fields
- Required field validation
- Conditional field display

### Audit Trails

**Audit Features:**
- All transaction logging
- User action tracking
- Data modification history
- Login/logout records

**Audit Reports:**
- User activity reports
- Transaction audit trails
- Security incident logs
- Compliance reports

### Security Best Practices

**Password Policies:**
- Minimum length requirements
- Complexity rules
- Regular password changes
- Account lockout policies

**Network Security:**
- SSL/TLS encryption
- Firewall configuration
- VPN for remote access
- Intrusion detection

**Data Security:**
- Regular backups
- Encryption at rest
- Secure data disposal
- Access monitoring

---

## 4. System Configuration

### Store Settings

**Configuration Categories:**
- **General Settings:** Company info, defaults
- **Transaction Settings:** Approval workflows, numbering
- **Integration Settings:** ERPNext sync, API keys
- **Security Settings:** Password policies, audit settings

**Key Configurations:**
- Default warehouse location
- Auto-generated numbering patterns
- Approval matrix settings
- Integration toggle switches

### Location Hierarchy Setup

**Hierarchy Configuration:**
1. Define warehouse structure
2. Set up location codes
3. Configure capacity limits
4. Establish access controls

**Location Types:**
- **Warehouse:** Top-level storage facility
- **Zone:** Major divisions within warehouse
- **Area:** Subdivisions within zones
- **Row:** Shelf rows within areas
- **Section:** Segments within rows
- **Bin:** Individual storage locations

### Item Catalog Configuration

**Item Setup:**
- Define item categories
- Configure tracking options
- Set up UOM conversions
- Establish quality parameters

**Catalog Management:**
- Bulk item import
- Category standardization
- Supplier linkage
- Compliance requirements

### Transaction Workflows

**Approval Configuration:**
- Define approval hierarchies
- Set approval limits
- Configure routing rules
- Establish escalation procedures

**Workflow Automation:**
- Automatic notifications
- Status updates
- Document routing
- Deadline management

---

## 5. Maintenance & Operations

### Backup & Recovery

**Backup Strategy:**
```bash
# Full backup with files
bench --site test.local backup --with-files

# Database only backup
bench --site test.local backup

# Automated backup script
0 2 * * * bench --site test.local backup  # Daily at 2 AM
```

**Recovery Process:**
```bash
# Restore from backup
bench --site test.local restore /path/to/backup.sql

# Verify restoration
bench --site test.local migrate
bench --site test.local clear-cache
```

**Backup Verification:**
- Test restore procedures monthly
- Verify backup integrity
- Document recovery time objectives
- Maintain offsite backup copies

### Performance Tuning

**Database Optimization:**
- Regular index maintenance
- Query performance monitoring
- Table optimization
- Connection pooling

**Application Tuning:**
- Cache configuration
- Session management
- Background job optimization
- Resource allocation

**System Monitoring:**
- CPU usage monitoring
- Memory utilization tracking
- Disk I/O performance
- Network throughput analysis

### Monitoring & Alerts

**System Health Checks:**
- Application availability
- Database connectivity
- Background job status
- Error rate monitoring

**Alert Configuration:**
- Email notifications
- SMS alerts for critical issues
- Dashboard monitoring
- Automated incident response

### Log Management

**Log Types:**
- Application logs
- Database logs
- Security logs
- Audit logs

**Log Analysis:**
- Error pattern identification
- Performance bottleneck detection
- Security incident investigation
- Compliance audit preparation

---

## 6. Customization & Development

### Adding Custom Fields

**Field Addition Process:**
1. Identify DocType to modify
2. Create custom field definition
3. Test field functionality
4. Update permissions if needed

**Custom Field Types:**
- Data, Link, Select, Int, Check
- Table (child tables)
- Attach, Text Editor
- Geolocation, Signature

### Custom Workflows

**Workflow Creation:**
1. Define workflow states
2. Configure transitions
3. Set approval requirements
4. Test workflow execution

**Advanced Workflows:**
- Conditional routing
- Parallel approvals
- Time-based escalations
- Integration triggers

### Client Scripts

**Script Types:**
- **Client Script:** Form-level scripting
- **Custom Script:** Field-level enhancements
- **Print Format:** Custom document layouts

**Common Customizations:**
- Field validations
- Dynamic field display
- Custom calculations
- UI enhancements

### API Development

**REST API Endpoints:**
- CRUD operations for all DocTypes
- Custom business logic endpoints
- Report generation APIs
- Integration webhooks

**API Security:**
- Authentication requirements
- Rate limiting
- Request validation
- Response formatting

---

## 7. Integration Management

### ERPNext Integration

**Integration Setup:**
1. Enable ERPNext integration in Store Settings
2. Configure connection parameters
3. Map data fields
4. Test synchronization

**Sync Capabilities:**
- Master data synchronization
- Transaction integration
- Real-time updates
- Conflict resolution

### Third-Party APIs

**API Integration:**
- RESTful API consumption
- Webhook implementation
- OAuth authentication
- Error handling and retry logic

**Supported Integrations:**
- Barcode scanning systems
- IoT sensors
- Mobile applications
- External databases

### Data Import/Export

**Import Capabilities:**
- CSV file import
- Excel spreadsheet import
- API-based data loading
- Bulk data operations

**Export Features:**
- PDF report generation
- Excel data export
- CSV data dumps
- API data access

### Webhook Configuration

**Webhook Setup:**
1. Define webhook endpoints
2. Configure trigger events
3. Set authentication
4. Test webhook delivery

**Common Webhooks:**
- Transaction completion
- Stock level alerts
- Approval notifications
- System status changes

---

## 8. Troubleshooting & Support

### Common Issues

**Installation Issues:**
- Dependency conflicts
- Permission problems
- Database connection failures
- Cache inconsistencies

**Runtime Issues:**
- Performance degradation
- Transaction failures
- User access problems
- Integration errors

### Diagnostic Tools

**System Diagnostics:**
```bash
# Check system status
bench --site test.local doctor

# View logs
bench --site test.local logs

# Database console
bench --site test.local mariadb
```

**Performance Diagnostics:**
- Query execution analysis
- Memory usage monitoring
- Network latency testing
- Load testing procedures

### Performance Issues

**Common Performance Problems:**
- Large dataset queries
- Inefficient indexing
- Memory leaks
- Network bottlenecks

**Optimization Strategies:**
- Query optimization
- Caching implementation
- Database tuning
- Code profiling

### Emergency Procedures

**System Down Procedures:**
1. Assess situation severity
2. Notify stakeholders
3. Activate backup systems
4. Begin recovery process

**Data Recovery:**
1. Identify data loss scope
2. Restore from backups
3. Verify data integrity
4. Communicate with users

---

## 9. Upgrade & Migration

### Version Upgrade Process

**Upgrade Preparation:**
1. Review release notes
2. Backup current system
3. Test upgrade in staging
4. Schedule maintenance window

**Upgrade Execution:**
```bash
# Update the app
bench update --app technical_store_system

# Run migrations
bench --site test.local migrate

# Clear cache
bench --site test.local clear-cache
```

**Post-Upgrade Tasks:**
- Test critical functionality
- Verify integrations
- Update documentation
- Train users on new features

### Data Migration

**Migration Planning:**
- Identify data to migrate
- Map source to target fields
- Plan data transformation
- Schedule migration windows

**Migration Execution:**
- Extract data from source
- Transform data as needed
- Load data into target system
- Validate migration success

### Rollback Procedures

**Rollback Preparation:**
- Maintain backup of previous version
- Document rollback steps
- Test rollback procedures
- Prepare communication plan

**Rollback Execution:**
1. Stop application services
2. Restore from backup
3. Verify system functionality
4. Communicate rollback status

### Testing Protocols

**Testing Types:**
- Unit testing
- Integration testing
- Performance testing
- User acceptance testing

**Test Automation:**
- Automated test suites
- Continuous integration
- Regression testing
- Load testing

---

## 10. Compliance & Legal

### Data Protection

**GDPR Compliance:**
- Data minimization principles
- Consent management
- Right to erasure
- Data portability

**Data Security:**
- Encryption standards
- Access controls
- Audit logging
- Incident response

### Audit Requirements

**Audit Trails:**
- Complete transaction logging
- User action tracking
- Data modification history
- System access records

**Audit Reports:**
- Compliance reporting
- Security incident analysis
- Access pattern analysis
- Regulatory submissions

### Regulatory Compliance

**Industry Standards:**
- ISO 27001 information security
- SOX compliance for financial data
- Industry-specific regulations
- Local data protection laws

**Compliance Monitoring:**
- Regular compliance audits
- Policy enforcement
- Training programs
- Incident reporting

### Legal Considerations

**Contractual Obligations:**
- Service level agreements
- Data processing agreements
- Confidentiality agreements
- Indemnification clauses

**Legal Documentation:**
- Terms of service
- Privacy policies
- Data processing agreements
- Compliance certificates

---

## 📞 Support & Contact Information

**Technical Support:**
- **Email:** admin-support@technicalstoresystem.com
- **Emergency:** +1 (555) 999-9999 (24/7)
- **Documentation:** admin-docs.technicalstoresystem.com

**Professional Services:**
- **Custom Development:** pro-services@technicalstoresystem.com
- **Training:** training@technicalstoresystem.com
- **Consulting:** consulting@technicalstoresystem.com

**Community Resources:**
- **Forum:** community.technicalstoresystem.com
- **GitHub:** github.com/zahidprinters/technical-store-system
- **Documentation:** docs.technicalstoresystem.com

---

**🔧 System Administration Excellence**

This administrator guide provides comprehensive information for managing and maintaining the Technical Store System. Regular review and updates ensure optimal system performance and security.

**For additional support, contact the system administrator or refer to the technical documentation.**</content>
<parameter name="filePath">/home/erpnext/frappe-bench/apps/technical_store_system/documentation/ADMIN_GUIDE.md