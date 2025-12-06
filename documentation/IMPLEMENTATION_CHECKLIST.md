# Technical Store System - Implementation Checklist

*Based on TECHNICAL_STORE_SINGLE_DOC.md*  
*Started: December 6, 2025*

---

## ✅ Phase 0: Foundation (COMPLETED)
- [x] App scaffolding and structure
- [x] Modular installer system (auto-discovery pattern)
- [x] Workspace setup
- [x] Basic roles (Store Manager, Warehouse Staff, Inventory Admin, Store Viewer)
- [x] Store Settings (Single DocType with 43 fields, 6 sections)
- [x] Demo data management system (Install/Remove buttons)
- [x] Client Scripts auto-installer
- [x] Documentation system (8 files)

---

## 📦 Phase 1: Core Masters (Priority 1)

### Module 1: Item & Stock Management Masters
**Goal:** Complete item master with all attributes + stock tracking foundation

- [x] **1.1 Store UOM** (Unit of Measure) ✅ COMPLETED
  - [x] DocType: name, uom_name, uom_symbol, enabled, is_fraction_allowed
  - [x] Fields: description, conversion_factor_info
  - [x] Default 27 UOMs: Each, Nos, Piece, Kg, Liter, Meter, Box, Pack, Set, Roll, Bundle, Carton, etc.
  - [x] Auto-discovery installer with on_doctype_install() hook
  - [x] Demo data control (force parameter for button-triggered install)

- [x] **1.2 Store Item Group** (Category/Classification) ✅ COMPLETED
  - [x] DocType: item_group_name, parent_item_group (tree structure), is_group
  - [x] Fields: description, image, nsm fields for tree structure
  - [x] Default 19 groups: All Item Groups → Electronics (Components, Cables, Instruments), Tools (Hand, Power, Measuring), Consumables (Chemicals, Cleaning, Lubricants, Fasteners), Safety Equipment (PPE, First Aid), Office Supplies, Spare Parts, Raw Materials
  - [x] Tree view support (is_tree=1)
  - [x] Demo data control with force parameter

- [ ] **1.3 Store Brand**
  - [ ] DocType: brand_name, description, country_of_origin
  - [ ] Fields: logo, website, enabled

- [ ] **1.4 Store Unit** (Store/Warehouse/Branch)
  - [ ] DocType: unit_code (unique), unit_name, unit_type (Main Store, Sub Store, Branch)
  - [ ] Fields: address, contact_person, phone, email, is_active
  - [ ] Parent-child hierarchy support
  - [ ] Autoname: format:UNIT-{unit_code}

- [ ] **1.5 Store Item** (Enhanced - replace basic version)
  - [ ] Basic fields: item_code, item_name, description
  - [ ] Classification: item_group (link), brand (link), technical_category
  - [ ] UOM: default_uom (link), alternative_uoms (table)
  - [ ] Stock Control: maintain_stock, allow_negative_stock, has_serial_no, has_batch_no
  - [ ] Location: rack, row, column, sub_row (for physical location)
  - [ ] Min/Max: minimum_level, maximum_level, reorder_level, reorder_qty
  - [ ] Supplier: preferred_supplier (link)
  - [ ] Specifications: specifications_json (JSON field), technical_specs (Text Editor)
  - [ ] Media: image, qr_code, barcode, additional_images (table)
  - [ ] Pricing: standard_rate, valuation_method (FIFO/LIFO/Moving Average)
  - [ ] Status: enabled, is_stock_item, is_purchase_item, is_sales_item
  - [ ] Autoname: format:ITEM-{####}

- [x] **1.6 Store Location** (Comprehensive warehouse location system) ✅ COMPLETED
  - [x] DocType: location_code (unique), location_name, location_type (19 types)
  - [x] Types: Warehouse, Store Room, Area, Zone, Rack, Shelf, Bin, Row, Column, Cell, Bucket, Drawer, Cabinet, Transit, Staging, Quarantine, Reject, Other
  - [x] Physical location fields (52 total fields): zone, aisle, rack, shelf, row, column, bin, cell, bucket
  - [x] Hierarchy: parent_location (self-link), is_group, address
  - [x] Capacity: max_capacity, capacity_uom, current_utilization%, length, width, height
  - [x] Tracking: barcode, qr_code (unique), rfid_tag, gps_coordinates
  - [x] Configuration: allow_negative_stock, is_bonded, temperature_controlled, hazardous_storage
  - [x] Management: contact_person, phone, email, manager (User link), description, image
  - [x] Demo data: 11 locations (Main Warehouse → Area A → Rack → Shelves, Store Room → Rows → Columns, Transit, Staging)
  - [x] Autoname: field:location_code

- [ ] **1.7 Stock Level** (Real-time stock per item per location)
  - [ ] DocType: item (link), store_unit (link), location (link)
  - [ ] Quantities: actual_qty, reserved_qty, available_qty, in_transit_qty
  - [ ] Valuation: valuation_rate, stock_value
  - [ ] Last updated: last_transaction_date
  - [ ] Unique constraint: (item + store_unit)

- [ ] **1.8 Stock Ledger Entry** (Immutable transaction log)
  - [ ] DocType: item (link), store_unit (link), location (link)
  - [ ] Transaction: posting_date, posting_time, voucher_type, voucher_no
  - [ ] Quantities: actual_qty (change), qty_after_transaction, stock_value_difference
  - [ ] Rates: incoming_rate, valuation_rate, stock_value
  - [ ] Reference: batch_no, serial_no
  - [ ] Immutable: is_cancelled (no delete, only cancel)
  - [ ] Autoname: format:SLE-{####}

---

### Module 2: Supplier & Vendor Management
**Goal:** Track suppliers and their pricing

- [ ] **2.1 Store Supplier**
  - [ ] DocType: supplier_code, supplier_name, supplier_type (Local, Import, Authorized Dealer)
  - [ ] Contact: contact_person, email, phone, mobile, website
  - [ ] Address: address_line1, address_line2, city, state, country, pin_code
  - [ ] Details: payment_terms, credit_days, credit_limit
  - [ ] Integration: erpnext_supplier (link if integrated)
  - [ ] Status: enabled, is_preferred
  - [ ] Rating: supplier_rating (0-5)
  - [ ] Autoname: format:SUP-{####}

- [ ] **2.2 Supplier Item Price**
  - [ ] DocType: supplier (link), item (link), price, currency, uom
  - [ ] Validity: valid_from, valid_to
  - [ ] Minimum: minimum_order_qty, lead_time_days
  - [ ] Status: is_active
  - [ ] Unique constraint: (supplier + item + valid_from)

---

### Module 3: Serial & Batch Tracking
**Goal:** Track individual items and batches

- [ ] **3.1 Store Serial Number**
  - [ ] DocType: serial_no (unique), item (link)
  - [ ] Ownership: store_unit (link), current_location (link)
  - [ ] Purchase: purchase_date, purchase_rate, supplier (link)
  - [ ] Warranty: warranty_expiry_date, amc_expiry_date
  - [ ] Status: status (Available, Issued, In Transit, Damaged, Returned)
  - [ ] Assignment: issued_to, issue_date, return_date
  - [ ] Autoname: format:SN-{item_code}-{#####}

- [ ] **3.2 Store Batch**
  - [ ] DocType: batch_no (unique), item (link)
  - [ ] Dates: manufacturing_date, expiry_date
  - [ ] Supplier: supplier (link), batch_qty
  - [ ] Status: enabled
  - [ ] Autoname: format:BATCH-{item_code}-{####}

---

## 📋 Phase 2: Demand & Issue Management (Priority 2)

### Module 4: Demand Management
**Goal:** Request items with approval workflow

- [ ] **4.1 Demand Request**
  - [ ] DocType: demand_request_no, posting_date
  - [ ] Requester: requested_by (link User), department, cost_center
  - [ ] Store: store_unit (link), required_by_date
  - [ ] Purpose: purpose (Project, Maintenance, Consumption, Emergency)
  - [ ] Workflow: status (Draft, Pending Approval, Approved, Rejected, Partially Issued, Completed, Cancelled)
  - [ ] Approval: approved_by, approved_date, rejection_reason
  - [ ] Totals: total_qty, total_estimated_value
  - [ ] Child table: demand_items
  - [ ] Autoname: format:DR-{YYYY}-{#####}

- [ ] **4.2 Demand Request Item** (child table)
  - [ ] Fields: item (link), item_name, description
  - [ ] Quantity: qty, uom (link), available_qty, pending_qty
  - [ ] Location: preferred_location (link)
  - [ ] Rates: estimated_rate, amount
  - [ ] Status: item_status (Pending, Partially Issued, Fully Issued)

---

### Module 5: Issue & Return Management
**Goal:** Issue items to employees/departments and track returns

- [ ] **5.1 Issue Document**
  - [ ] DocType: issue_no, posting_date, posting_time
  - [ ] Issue to: issued_to (link User), department, cost_center
  - [ ] Store: from_store_unit (link), from_location (link)
  - [ ] Reference: demand_request (link), purpose
  - [ ] Return: return_expected, expected_return_date
  - [ ] Workflow: status (Draft, Submitted, Partially Returned, Fully Returned, Cancelled)
  - [ ] Totals: total_qty, total_value
  - [ ] Child table: issue_items
  - [ ] On submit: Update Stock Ledger, update Demand Request status
  - [ ] Autoname: format:ISS-{YYYY}-{#####}

- [ ] **5.2 Issue Document Item** (child table)
  - [ ] Fields: item (link), batch_no, serial_no
  - [ ] Quantity: qty, uom, rate, amount
  - [ ] Return: returned_qty, pending_return_qty

- [ ] **5.3 Return to Store**
  - [ ] DocType: return_no, posting_date, posting_time
  - [ ] Return from: returned_by (link User), department
  - [ ] Store: to_store_unit (link), to_location (link)
  - [ ] Reference: issue_document (link)
  - [ ] Condition: return_condition (Good, Damaged, Partial Use, Expired)
  - [ ] Workflow: status (Draft, Submitted, Cancelled)
  - [ ] Child table: return_items
  - [ ] On submit: Update Stock Ledger, update Issue Document return status
  - [ ] Autoname: format:RET-{YYYY}-{#####}

- [ ] **5.4 Return to Store Item** (child table)
  - [ ] Fields: item (link), batch_no, serial_no
  - [ ] Quantity: issued_qty, returned_qty, uom
  - [ ] Condition: item_condition, remarks

---

## 🔄 Phase 3: Transfer & Purchase (Priority 3)

### Module 6: Inter-Store Transfer
**Goal:** Move stock between stores/locations

- [ ] **6.1 Transfer Request**
  - [ ] DocType: transfer_request_no, posting_date
  - [ ] Stores: from_store_unit (link), to_store_unit (link)
  - [ ] Requester: requested_by (link User), required_by_date
  - [ ] Purpose: purpose, remarks
  - [ ] Workflow: status (Draft, Pending Approval, Approved, In Transit, Received, Rejected, Cancelled)
  - [ ] Child table: transfer_items
  - [ ] Autoname: format:TRQ-{YYYY}-{#####}

- [ ] **6.2 Transfer Issue** (Goods sent)
  - [ ] DocType: transfer_issue_no, posting_date
  - [ ] Reference: transfer_request (link)
  - [ ] Stores: from_store_unit (link), to_store_unit (link)
  - [ ] Transport: vehicle_no, driver_name, driver_contact
  - [ ] Workflow: status (Draft, In Transit, Received, Cancelled)
  - [ ] Child table: transfer_issue_items
  - [ ] On submit: Create in-transit stock ledger entries
  - [ ] Autoname: format:TIS-{YYYY}-{#####}

- [ ] **6.3 Transfer Receive** (Goods received)
  - [ ] DocType: transfer_receive_no, posting_date
  - [ ] Reference: transfer_issue (link)
  - [ ] Received by: received_by (link User), received_date
  - [ ] Inspection: inspection_required, inspection_remarks
  - [ ] Workflow: status (Draft, Completed, Cancelled)
  - [ ] Child table: transfer_receive_items (with accepted_qty, rejected_qty)
  - [ ] On submit: Update stock ledger at destination, clear in-transit
  - [ ] Autoname: format:TRC-{YYYY}-{#####}

---

### Module 7: Purchase Management
**Goal:** Purchase suggestions and receipts

- [ ] **7.1 Purchase Suggestion**
  - [ ] DocType: purchase_suggestion_no, posting_date
  - [ ] Store: store_unit (link), required_by_date
  - [ ] Source: auto_generated, demand_request (link)
  - [ ] Workflow: status (Draft, Pending Approval, Approved, Ordered, Received, Cancelled)
  - [ ] Mobile: synced_to_mobile, last_sync_date
  - [ ] Child table: purchase_suggestion_items
  - [ ] Autoname: format:PS-{YYYY}-{#####}

- [ ] **7.2 Purchase Suggestion Item** (child table)
  - [ ] Fields: item (link), qty, uom
  - [ ] Supplier: preferred_supplier (link), estimated_rate, amount
  - [ ] Stock: current_stock, minimum_level, suggested_qty
  - [ ] Status: item_status

- [ ] **7.3 Purchase Receipt**
  - [ ] DocType: purchase_receipt_no, posting_date
  - [ ] Supplier: supplier (link), supplier_invoice_no, supplier_invoice_date
  - [ ] Store: store_unit (link), location (link)
  - [ ] Reference: purchase_suggestion (link)
  - [ ] Totals: total_qty, total_amount
  - [ ] Workflow: status (Draft, Submitted, Cancelled)
  - [ ] Child table: purchase_receipt_items
  - [ ] On submit: Update Stock Ledger
  - [ ] Autoname: format:PR-{YYYY}-{#####}

- [ ] **7.4 Purchase Receipt Item** (child table)
  - [ ] Fields: item (link), qty, uom, rate, amount
  - [ ] Batch: batch_no, manufacturing_date, expiry_date
  - [ ] Serial: serial_no (if applicable)
  - [ ] Quality: accepted_qty, rejected_qty

---

## 📊 Phase 4: Analytics & Intelligence (Priority 4)

### Module 8: Usage Tracking & Analytics

- [ ] **8.1 Usage Log**
  - [ ] DocType: Auto-created on each Issue
  - [ ] Fields: item, issued_to, qty, date, department, cost_center
  - [ ] Purpose: Track consumption patterns

- [ ] **8.2 Consumption Forecast**
  - [ ] DocType: item, store_unit, forecast_period
  - [ ] Calculations: predicted_consumption, confidence_level
  - [ ] Auto-generated: Nightly scheduler

- [ ] **8.3 Intelligence Alert**
  - [ ] DocType: alert_type (Low Stock, Overstock, No Movement, Expiry)
  - [ ] Fields: item, store_unit, alert_date, severity
  - [ ] Actions: recommended_action, alert_status
  - [ ] Scheduler: Daily check

- [ ] **8.4 Anomaly Log**
  - [ ] DocType: item, transaction_type, anomaly_type
  - [ ] Fields: expected_value, actual_value, deviation_percent
  - [ ] Auto-generated: On unusual consumption patterns

---

## 📱 Phase 5: Mobile & Barcode (Priority 5)

### Module 9: Barcode & RFID Integration

- [ ] **9.1 Barcode Label**
  - [ ] DocType: item (link), label_type (Item, Location, Serial)
  - [ ] Generation: barcode_value, qr_code_value, print_format

- [ ] **9.2 Barcode Scan Log**
  - [ ] DocType: scanned_by, scan_date, scan_type
  - [ ] Data: barcode_value, item (resolved), location
  - [ ] Transaction: linked_document_type, linked_document_name

- [ ] **9.3 Mobile App Sync Log**
  - [ ] DocType: sync_type (Purchase, Issue, Transfer)
  - [ ] Mobile: device_id, app_version, sync_date
  - [ ] Status: sync_status, conflict_resolution

---

## 💰 Phase 6: Budget & Cost Control (Priority 6)

### Module 10: Budget Management

- [ ] **10.1 Department Budget**
  - [ ] DocType: department, fiscal_year, cost_center
  - [ ] Budget: total_budget, consumed_budget, available_budget
  - [ ] Period: monthly_distribution (child table)

- [ ] **10.2 Budget Alert**
  - [ ] DocType: department, alert_type (Approaching Limit, Exceeded)
  - [ ] Amounts: budget_limit, consumed_amount, percentage_consumed
  - [ ] Auto-generated: On transaction validation

---

## 🏆 Phase 7: Asset Management (Priority 7)

### Module 11: Asset Tagging & Depreciation

- [ ] **11.1 Asset Item**
  - [ ] DocType: Links to Store Item + Serial Number
  - [ ] Asset details: purchase_value, current_value, depreciation_method
  - [ ] Lifecycle: purchase_date, warranty_period, disposal_date

- [ ] **11.2 Depreciation Schedule**
  - [ ] DocType: asset_item (link), depreciation_frequency
  - [ ] Calculation: depreciation_rate, accumulated_depreciation
  - [ ] Child table: Monthly depreciation entries

- [ ] **11.3 Asset Disposal**
  - [ ] DocType: asset_item (link), disposal_date, disposal_type
  - [ ] Values: book_value, sale_value, gain_loss

---

## 🔒 Phase 8: Compliance & Audit (Priority 8)

### Module 12: Compliance & Audit Trail

- [ ] **12.1 Approval Hierarchy**
  - [ ] DocType: document_type, approval_level, approver (link User)
  - [ ] Rules: value_from, value_to, department, cost_center

- [ ] **12.2 Compliance Rule**
  - [ ] DocType: rule_name, rule_type, validation_script
  - [ ] Scope: applicable_doctypes, severity
  - [ ] Actions: on_violation_action

- [ ] **12.3 Compliance Alert**
  - [ ] DocType: rule (link), document_type, document_name
  - [ ] Details: violation_date, violation_details, severity
  - [ ] Status: alert_status (Open, Acknowledged, Resolved)

- [ ] **12.4 Audit Trail Export**
  - [ ] DocType: export_type, from_date, to_date
  - [ ] Filters: document_types, users, stores
  - [ ] Output: export_file, export_format (Excel, CSV, PDF)

---

## 📈 Phase 9: Reporting & Dashboards (Priority 9)

### Module 13: Advanced Reporting

- [ ] **13.1 Dashboard Widget**
  - [ ] DocType: widget_name, widget_type (Chart, Number, List)
  - [ ] Data: data_source, refresh_frequency
  - [ ] Display: chart_type, filters

- [ ] **13.2 Scheduled Report**
  - [ ] DocType: report_name, report_type, schedule_frequency
  - [ ] Distribution: email_to, format (PDF, Excel)
  - [ ] Auto-generation: Scheduler job

- [ ] **13.3 Custom Report Config**
  - [ ] DocType: report_name, base_doctype
  - [ ] Fields: selected_fields (table), filters (table)
  - [ ] User: created_by, is_public

---

## 🔧 Phase 10: System Configuration

### Module 14: Advanced Settings & Permissions

- [ ] **14.1 Number Series**
  - [ ] Configure autoname formats for all DocTypes
  - [ ] Prefix customization per Store Unit

- [ ] **14.2 Custom Fields**
  - [ ] Industry-specific fields via fixtures
  - [ ] User-defined fields support

- [ ] **14.3 Role Permissions**
  - [ ] Detailed permission matrix for all DocTypes
  - [ ] Store-level data isolation
  - [ ] Document-level permissions

- [ ] **14.4 Notification Templates**
  - [ ] Email templates for approvals, alerts
  - [ ] SMS templates for critical alerts
  - [ ] Push notification configs

---

## 🎯 Testing & Deployment Checklist

### Testing Phase
- [ ] Unit tests for all DocType validations
- [ ] Integration tests for workflows (Demand → Issue → Return)
- [ ] Performance tests (1000+ items, 10000+ transactions)
- [ ] Mobile sync conflict resolution tests
- [ ] Approval escalation tests
- [ ] Stock ledger accuracy tests (FIFO/LIFO/Moving Average)
- [ ] Barcode scanning tests
- [ ] Budget validation tests
- [ ] Multi-store isolation tests

### Deployment Phase
- [ ] Migration scripts for all DocTypes
- [ ] Default data fixtures (UOMs, Item Groups, Roles)
- [ ] Permission setup scripts
- [ ] Scheduler configuration
- [ ] Backup and restore procedures
- [ ] Documentation (User Manual, Admin Guide, API Docs)
- [ ] Training materials
- [ ] Go-live checklist

---

## Progress Tracking

**Current Status:** ✅ Phase 0 Complete (Foundation)  
**Next Target:** 🔄 Phase 1 - Core Masters (Module 1: Item & Stock Management)  
**Overall Progress:** 7 of 200+ tasks complete (~3%)

### Completed Tasks (Phase 0)
1. ✅ App scaffolding and structure
2. ✅ Modular installer system (`installer.py` - 318+ lines)
3. ✅ Auto-discovery pattern (`doctypes_setup.py` - discovers `setup/doctypes/*.py`)
4. ✅ Workspace setup and display
5. ✅ 4 Default roles created
6. ✅ Store Settings (Single DocType - 6 sections, 30+ fields)
7. ✅ Store Item (basic) and Store Location (basic)

**Estimated Timeline:**
- Phase 1: 2-3 days (Core Masters)
- Phase 2: 2 days (Demand & Issue)
- Phase 3: 2 days (Transfer & Purchase)
- Phase 4: 1 day (Analytics)
- Phase 5: 1 day (Mobile & Barcode)
- Phase 6-9: 2 days (Budget, Asset, Compliance, Reports)
- Phase 10: 1 day (System Config)
- Testing: 2-3 days
- **Total: ~14-16 days**

---

*This checklist is auto-updated as we progress. Each checkbox represents a completed task.*
