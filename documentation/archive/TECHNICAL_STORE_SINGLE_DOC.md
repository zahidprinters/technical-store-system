# Technical Store System — Consolidated Master Document

*Last updated: December 2025*

This single document merges the full scope from `app/newapp` and `app/store` (now under `documentation/08-app-imports`) so nothing is missed. It covers architecture, modules, APIs, database schema, integrations, security, and implementation steps.

---

## 1) Snapshot
- **Status:** Scaffolding complete; 10 enhancement modules + 8 core modules designed. Hooks and schedulers mapped; Phase 3 implementation pending.
- **Stack:** Frappe v15+, MariaDB/PostgreSQL, Python 3.9+, Node 16+, REST JSON APIs.
- **Multi-Store:** All data is store/unit scoped with isolated ledgers and approvals.
- **Audit & Compliance:** Immutable ledgers, approval hierarchies, scheduled compliance exports.
- **Automation:** 16+ scheduled tasks; 20+ doc events; 50+ server methods; 35+ Doctypes.

## 2) Architecture & Principles
- **Modular ERP add-on:** Technical store as a multi-tenant module with strict store filters.
- **Approval-first workflows:** Value-based, hierarchical approvals with escalation.
- **Data integrity:** Referential constraints, no orphan records, immutable stock ledger.
- **Performance:** Indexed queries, paginated lists, caching for masters, async jobs for heavy tasks.
- **Security:** Role-based access, API rate limits, audit trails, compliance alerts.

## 3) Module Catalog (no omissions)

### Core Operational Modules (8)
1) **Item & Stock Management** — Item, Item Group, Store/Unit, Item Location, Stock Ledger Entry, UOM.
2) **Demand Management** — Demand Request + Demand Item; multi-level approvals; auto purchase suggestions on shortage.
3) **Issue & Return Management** — Issue Document + Issue Item; Return to Store/Market; usage log updates.
4) **Inter-Store Transfer** — Transfer Request/Issue/Receive/Return with min-level checks and in-transit ledgers.
5) **Purchase Management** — Purchase Suggestion + items; approvals; mobile sync; receipts.
6) **Intelligence & Analytics (core ops)** — Usage Log; nightly analytics; trends and alerts.
7) **Reporting & Dashboards** — Scheduled reports, widgets; operational KPIs.
8) **Audit & Compliance (core ops)** — Approval rules, audit log exports, immutable trails.

### Enhancement Modules (10) — all COMPLETE (from `newapp`)
1) **Intelligence & Analytics** — Intelligence Alert, Consumption Forecast, Anomaly Log; methods: `predict_weekly_consumption`, `detect_abnormal_usage`, `auto_adjust_minimum_level`, `suggest_bulk_purchase`.
2) **Mobile Purchase App Integration** — Mobile App Sync Log, Barcode Capture, Voice Input Log; methods: `sync_approved_pr_list`, `update_receipt_from_mobile`, `log_barcode_capture`.
3) **Vendor Management** — Vendor, Vendor Item Price, Tender/RFQ, Vendor Performance; methods: `calculate_vendor_performance`, `sync_vendor_item_prices`.
4) **Inventory Valuation & Costing** — Inventory Valuation, Stock Variance, Cost Center; methods: `calculate_stock_variance`, FIFO/LIFO/Weighted Average costing.
5) **Employee Performance & Compliance** — Employee Performance, Misuse Alert, Compliance Rule; methods: `detect_duplicate_usage`, `calculate_employee_performance`.
6) **Advanced Reporting & Analytics Dashboard** — Dashboard Widget, Scheduled Report, Custom Report Config; methods: `update_dashboard_widget`, `generate_scheduled_reports`.
7) **Barcode & RFID Integration** — Barcode Label, Scan Log, RFID Tag; methods: `generate_barcode_labels`, `log_barcode_scan`, `process_rfid_tag`.
8) **Budget & Cost Control** — Department Budget, PR Approval Rule, Budget Alert; methods: `check_budget_availability`, `get_approval_authority`, `update_consumed_budget`.
9) **Asset Tagging & Depreciation** — Asset Item, Depreciation Schedule, Asset Disposal; methods: `calculate_depreciation`, `get_asset_book_value`, `record_asset_disposal`.
10) **Compliance & Audit Trail Enhancements** — Approval Hierarchy, Compliance Alert, Compliance Rule, Audit Trail Export; methods: `check_approval_hierarchy`, `validate_compliance_rules`, `escalate_pending_approvals`, `generate_audit_trail_export`, `acknowledge_compliance_alert`.

### ERPNext Technical Store Module (from `store` import)
- **Feature highlights:** Inventory tracking by rack/row/column/sub-row, minimum levels, preferred suppliers, QR/Barcode labels.
- **Workflows:** Demand → Approval → Issue → Return; Purchase Suggestion → Mobile sync → Purchase updates → Store verification; Inter-store transfers with in-transit stock.
- **Mobile-first:** Offline-friendly purchase updates with conflict resolution.
- **Analytics:** Usage Log trends, predictive purchase recommendations.

## 4) API Surface (merged)
- **Auth:** Session login (`frappe.auth.login`), Token (`Authorization: token user:key`), API key/secret headers; logout via `frappe.auth.logout`.
- **General patterns:** JSON payloads, pagination (`limit`, `offset`), filters, role checks, HTTP 429 on rate limits.
- **Core resource APIs:** `/api/resource/Item`, `/api/resource/Stock Level`, `/api/resource/Demand Request`, `/api/resource/Issue Document`, `/api/resource/Transfer Request`, `/api/resource/Purchase Suggestion` (standard CRUD and filtered lists).
- **Mobile purchase endpoints (store import):**
  - `GET /api/method/tsm.get_purchase_list` — fetch approved purchase suggestions (filters: store, since, status, pagination).
  - `POST /api/method/tsm.push_purchase_updates` — push purchased items, suppliers, photos, availability with conflict handling.
- **Whitelisted server methods (examples):** forecasting, anomaly detection, budget checks, approval hierarchy lookup, barcode generation, RFID processing.

## 5) Database Schema (combined highlights)
- **Masters:** Item (extended fields: technical_category, rack/column/row/sub_row, min_level, preferred_supplier, specs_json, images, qr_code), Store Unit, Unit, Vendor, Cost Center, Department Budget.
- **Transactions:** Stock Level (unique item+store), Stock Ledger Entry (immutable), Demand Request + Items, Issue Document + Items, Return Document, Transfer Request/Issue/Receive/Return, Purchase Suggestion + Items, Purchase Receipt, Usage Log, Intelligence Alert, Compliance Alert, Budget Alert.
- **Indexes/constraints:** PKs on codes/IDs; unique (item, store) for stock; checks on quantities >= 0; FK links across items, stores, vendors; workflow status enums; audit timestamps.
- **Scalability:** Indexed date/status fields; pagination-first queries; partition by store where applicable.

## 6) Integration & Hooks
- **Scheduler events:** Hourly (anomaly detection, budget checks, approval escalation), Daily (demand forecasting, variance calc, performance metrics), Monthly (audit trail export).
- **Doc events:** Purchase Request → budget+compliance checks; Stock Issue → duplicate usage detection + barcode logging; Return to Store → variance calc; Transfer Request → demand suggestions + barcode generation; Budget/Compliance docs → analytics triggers.
- **Fixtures:** Custom Fields, Compliance Rules, PR Approval Rules, Approval Hierarchies.
- **Inter-module data flows:** Demand → Issue → Return → Ledger; Purchase flow links Vendor Mgmt → Budget Control → Compliance; Performance links Employee Compliance ↔ Audit; Mobile scans feed Barcode/RFID + Analytics.

## 7) Security & Compliance
- **RBAC:** Role checks on all endpoints; store-scoped permissions; Purchase Officer/Admin for purchase endpoints.
- **Rate limits:** Example 500 req/hour per user (newapp) and 1 req/5s for mobile batches (store).
- **Data protection:** Immutable ledgers, audit exports, escalation on overdue approvals, compliance alerts.
- **Validation:** Min-level checks, duplication detection, conflict responses (409) on concurrent mobile updates.

## 8) Implementation Plan (Phase 3)
1) **Doctypes:** Generate JSON + .py controllers for all ~35 doctypes (see module lists above). Ensure unique indexes and FK constraints match schema rules.
2) **Methods:** Implement server methods per module; wire to hooks and permissions.
3) **Hooks:** Finalize `hooks.py` with schedulers, doc_events, fixtures; verify import paths.
4) **UI:** Build forms, lists, dashboards, barcode/RFID UI, mobile sync controls.
5) **Tests:** Unit tests for methods, integration tests for approvals/stock, performance tests for analytics jobs, mobile sync conflict tests.
6) **Deployment:** Bench setup, migrations, scheduler enablement, RBAC roles, monitoring/alerts.

## 9) Source Pointers (full detail)
- Imported originals: `documentation/08-app-imports/newapp/*`, `documentation/08-app-imports/store/*`.
- Key references: `APP_ARCHITECTURE.md`, `API_SPECIFICATION.md`, `DATABASE_SCHEMA.md`, `MODULES_INTEGRATION_COMPLETE.md`, `SETUP_GUIDE.md`, `DELIVERABLES_SUMMARY.md`, `PROJECT_COMPLETE.md`, `SECURITY_COMPLIANCE.md`, module READMEs under `modules/`.

---

Use this file as the single, merged reference. For deeper tables, payload examples, or step-by-step workflows, jump to the source pointers above.
