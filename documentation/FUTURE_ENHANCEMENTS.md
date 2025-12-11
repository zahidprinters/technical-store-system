# Technical Store System - Future Enhancements & Feature Pipeline

**Last Updated:** December 11, 2025
**Current Version:** 0.0.1
**Focus:** Detailed specifications for upcoming features and enhancements

---

## 🎯 Overview

This document outlines the detailed technical specifications and implementation plans for future enhancements to the Technical Store System. All features are aligned with the comprehensive roadmap and prioritized for development.

---

## 🚀 Phase 2: Transaction Management (Q1 2026)

### Store Item Receipt DocType - Detailed Specification

#### **Core Fields & Structure**
```python
class StoreItemReceipt(Document):
    # Header Information
    receipt_no = DataField(unique=True, read_only=True)  # Auto-generated: REC-2025-001
    receipt_date = DateField(default=today)
    supplier = LinkField("Supplier", optional=True)  # ERPNext integration
    purchase_order = LinkField("Purchase Order", optional=True)
    reference_document = DataField()  # Invoice, Delivery Note, etc.

    # Transaction Details
    receipt_type = SelectField(["Purchase", "Return", "Transfer", "Adjustment"])
    priority = SelectField(["Normal", "Urgent", "Critical"], default="Normal")
    department = LinkField("Department", optional=True)

    # Items Table (Child DocType: Store Receipt Item)
    items = TableField("Store Receipt Item")

    # Quality & Inspection
    quality_check_required = CheckField(default=False)
    quality_inspector = LinkField("User", optional=True)
    inspection_date = DateField()
    quality_status = SelectField(["Pending", "Passed", "Failed", "Conditional"])

    # Workflow & Status
    status = SelectField([
        "Draft", "Pending Approval", "Quality Check",
        "Approved", "Received", "Cancelled"
    ], default="Draft")
    approval_status = SelectField(["Not Required", "Pending", "Approved", "Rejected"])

    # Financial Information
    total_quantity = FloatField(read_only=True)
    total_value = CurrencyField(read_only=True)
    currency = LinkField("Currency", default="USD")

    # Audit Trail
    created_by = LinkField("User", read_only=True)
    approved_by = LinkField("User", read_only=True)
    received_by = LinkField("User", read_only=True)
    submitted_date = DateTimeField(read_only=True)
    approval_date = DateTimeField(read_only=True)
```

#### **Store Receipt Item Child Table**
```python
class StoreReceiptItem(Document):
    # Parent Link
    parent = LinkField("Store Item Receipt")
    parentfield = DataField(default="items")
    parenttype = DataField(default="Store Item Receipt")

    # Item Details
    item_code = LinkField("Store Item", required=True)
    item_name = DataField(read_only=True)  # Auto-populated
    description = TextField()

    # Quantity & UOM
    quantity = FloatField(required=True, min=0)
    uom = LinkField("Store UOM", required=True)
    conversion_factor = FloatField(default=1.0)

    # Location & Storage
    warehouse = LinkField("Store Location", required=True)
    location_details = TextField()  # Specific bin/shelf information

    # Tracking Information
    has_serial_no = CheckField(read_only=True)  # From item master
    has_batch_no = CheckField(read_only=True)  # From item master

    # Serial Numbers (if applicable)
    serial_numbers = TableField("Store Receipt Serial")

    # Batch Information (if applicable)
    batch_no = DataField()
    manufacturing_date = DateField()
    expiry_date = DateField()

    # Quality Control
    quality_status = SelectField(["Accepted", "Rejected", "Conditional"])
    quality_notes = TextField()

    # Pricing (for valuation)
    rate = CurrencyField()
    amount = CurrencyField(read_only=True)  # Calculated: quantity * rate

    # References
    purchase_order_item = LinkField("Purchase Order Item", optional=True)
    supplier_item_code = DataField()
```

#### **Business Logic Implementation**
```python
class StoreItemReceiptController(Document):
    def before_insert(self):
        self.generate_receipt_number()

    def validate(self):
        self.validate_items()
        self.validate_quantities()
        self.validate_quality_requirements()
        self.calculate_totals()

    def on_submit(self):
        self.create_stock_entries()
        self.update_item_stock()
        self.create_serial_batch_records()
        self.send_notifications()

    def generate_receipt_number(self):
        # Format: REC-YYYY-NNN
        year = today().year
        last_receipt = frappe.db.get_value(
            "Store Item Receipt",
            {"receipt_date": ["between", [f"{year}-01-01", f"{year}-12-31"]]},
            "receipt_no",
            order_by="creation desc"
        )
        if last_receipt:
            sequence = int(last_receipt.split("-")[-1]) + 1
        else:
            sequence = 1
        self.receipt_no = f"REC-{year}-{sequence:03d}"
```

#### **Quality Control Workflow**
```python
def quality_inspection_workflow(self):
    if self.quality_check_required:
        # Create Quality Inspection record
        inspection = frappe.get_doc({
            "doctype": "Quality Inspection",
            "inspection_type": "Incoming",
            "reference_type": "Store Item Receipt",
            "reference_name": self.name,
            "item_code": self.items[0].item_code if self.items else None,
            "sample_size": len(self.items),
            "inspected_by": self.quality_inspector
        })
        inspection.insert()

        # Set status based on inspection
        if inspection.status == "Accepted":
            self.quality_status = "Passed"
        elif inspection.status == "Rejected":
            self.quality_status = "Failed"
        else:
            self.quality_status = "Conditional"
```

---

## 📊 Phase 3: Advanced Analytics & Reporting (Q2 2026)

### Predictive Analytics Engine

#### **Demand Forecasting Model**
```python
class DemandForecaster:
    def __init__(self, item_code, historical_data_months=24):
        self.item_code = item_code
        self.historical_data = self.get_historical_data(historical_data_months)

    def forecast_demand(self, periods=12):
        """Forecast demand using multiple algorithms"""
        algorithms = [
            self.exponential_smoothing,
            self.linear_regression,
            self.arima_model,
            self.machine_learning_model
        ]

        forecasts = []
        for algorithm in algorithms:
            forecast = algorithm(periods)
            forecasts.append(forecast)

        # Ensemble forecasting - weighted average
        return self.ensemble_forecast(forecasts)

    def exponential_smoothing(self, periods):
        """Simple exponential smoothing"""
        alpha = 0.3  # Smoothing factor
        forecast = []
        current = self.historical_data[-1]

        for _ in range(periods):
            current = alpha * current + (1 - alpha) * current
            forecast.append(current)

        return forecast

    def machine_learning_model(self, periods):
        """ML-based forecasting using scikit-learn"""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split

        # Prepare features
        X = self.prepare_features()
        y = self.historical_data

        # Train model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Generate forecast
        future_features = self.generate_future_features(periods)
        return model.predict(future_features)
```

#### **Real-time Dashboard Architecture**
```python
class InventoryDashboard:
    def __init__(self):
        self.cache_timeout = 300  # 5 minutes
        self.redis_client = redis.Redis()

    def get_dashboard_data(self, user=None):
        """Get personalized dashboard data"""
        cache_key = f"dashboard:{user or 'global'}"

        # Try cache first
        cached_data = self.redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        # Generate fresh data
        data = {
            "kpis": self.get_kpi_data(),
            "alerts": self.get_active_alerts(user),
            "charts": self.get_chart_data(),
            "recent_activity": self.get_recent_activity(user)
        }

        # Cache for 5 minutes
        self.redis_client.setex(cache_key, self.cache_timeout, json.dumps(data))

        return data

    def get_kpi_data(self):
        """Calculate key performance indicators"""
        return {
            "total_stock_value": self.calculate_total_stock_value(),
            "stock_turnover_ratio": self.calculate_stock_turnover(),
            "low_stock_items": self.count_low_stock_items(),
            "pending_requisitions": self.count_pending_requisitions(),
            "monthly_consumption": self.calculate_monthly_consumption(),
            "expiry_alerts": self.count_expiry_alerts()
        }

    def calculate_total_stock_value(self):
        """Calculate total value of current stock"""
        return frappe.db.sql("""
            SELECT SUM(stock_value)
            FROM (
                SELECT
                    item_code,
                    SUM(actual_qty * valuation_rate) as stock_value
                FROM `tabStock Ledger Entry`
                WHERE is_cancelled = 0
                GROUP BY item_code
                HAVING SUM(actual_qty) > 0
            ) stock_values
        """)[0][0] or 0
```

---

## 🔗 Phase 4: ERPNext Integration (Q3 2026)

### Bidirectional Synchronization Engine

#### **Data Mapping Configuration**
```python
ERPNext_MAPPING = {
    "Item": {
        "source_fields": {
            "item_code": "item_code",
            "item_name": "item_name",
            "description": "description",
            "item_group": "item_group",
            "default_uom": "stock_uom",
            "is_stock_item": "is_stock_item",
            "valuation_method": "valuation_method"
        },
        "target_doctype": "Store Item",
        "sync_direction": "bidirectional",
        "conflict_resolution": "last_modified_wins"
    },
    "Warehouse": {
        "source_fields": {
            "name": "location_code",
            "warehouse_name": "location_name",
            "parent_warehouse": "parent_location",
            "is_group": "is_group"
        },
        "target_doctype": "Store Location",
        "sync_direction": "bidirectional",
        "conflict_resolution": "manual_resolution"
    },
    "Stock Entry": {
        "source_fields": {
            "name": "stock_entry_no",
            "stock_entry_type": "entry_type",
            "posting_date": "transaction_date",
            "items": "stock_entry_items"
        },
        "target_doctype": "Store Transaction",
        "sync_direction": "erpnext_to_store",
        "conflict_resolution": "erpnext_wins"
    }
}
```

#### **Synchronization Controller**
```python
class ERPNextSyncController:
    def __init__(self, site_name):
        self.site = site_name
        self.mappings = ERPNext_MAPPING
        self.sync_log = []

    def sync_all(self):
        """Complete bidirectional synchronization"""
        self.sync_items()
        self.sync_warehouses()
        self.sync_stock_entries()
        self.sync_purchase_orders()
        self.generate_sync_report()

    def sync_items(self):
        """Synchronize item masters"""
        # Get last sync timestamp
        last_sync = self.get_last_sync_timestamp("Item")

        # Get changed items from ERPNext
        erpnext_items = self.get_erpnext_changes("Item", last_sync)

        # Get changed items from Store
        store_items = self.get_store_changes("Store Item", last_sync)

        # Resolve conflicts and sync
        for item in erpnext_items + store_items:
            self.sync_single_item(item)

    def sync_single_item(self, item_data):
        """Sync individual item with conflict resolution"""
        erpnext_item = self.get_erpnext_item(item_data.get("item_code"))
        store_item = self.get_store_item(item_data.get("item_code"))

        if not erpnext_item and not store_item:
            return  # Item doesn't exist in either system

        # Determine which version is newer
        erpnext_modified = erpnext_item.get("modified") if erpnext_item else None
        store_modified = store_item.get("modified") if store_item else None

        if erpnext_modified and store_modified:
            if erpnext_modified > store_modified:
                self.update_store_from_erpnext(erpnext_item)
            elif store_modified > erpnext_modified:
                self.update_erpnext_from_store(store_item)
            else:
                # Same timestamp, check for actual differences
                self.handle_conflict_resolution(erpnext_item, store_item)
        elif erpnext_item:
            self.create_store_item_from_erpnext(erpnext_item)
        elif store_item:
            self.create_erpnext_item_from_store(store_item)
```

---

## 📱 Phase 5: Mobile & IoT Integration (Q4 2026)

### Mobile Application Architecture

#### **React Native Mobile App Structure**
```
mobile-app/
├── src/
│   ├── components/
│   │   ├── BarcodeScanner.tsx
│   │   ├── InventoryList.tsx
│   │   ├── LocationNavigator.tsx
│   │   └── Dashboard.tsx
│   ├── screens/
│   │   ├── LoginScreen.tsx
│   │   ├── InventoryScreen.tsx
│   │   ├── TransactionScreen.tsx
│   │   └── SettingsScreen.tsx
│   ├── services/
│   │   ├── ApiService.ts
│   │   ├── OfflineStorage.ts
│   │   ├── BarcodeService.ts
│   │   └── LocationService.ts
│   ├── utils/
│   │   ├── AuthUtils.ts
│   │   ├── ValidationUtils.ts
│   │   └── SyncUtils.ts
│   └── App.tsx
├── android/
├── ios/
└── package.json
```

#### **Offline-First Architecture**
```typescript
class OfflineStorage {
    private db: SQLiteDatabase;

    async initialize(): Promise<void> {
        this.db = await SQLite.openDatabase('inventory.db');

        // Create offline tables
        await this.db.executeSql(`
            CREATE TABLE IF NOT EXISTS offline_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT,
                data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                synced INTEGER DEFAULT 0
            )
        `);
    }

    async saveTransaction(type: string, data: any): Promise<void> {
        const jsonData = JSON.stringify(data);

        await this.db.executeSql(
            'INSERT INTO offline_transactions (transaction_type, data) VALUES (?, ?)',
            [type, jsonData]
        );
    }

    async syncPendingTransactions(): Promise<void> {
        const pending = await this.getPendingTransactions();

        for (const transaction of pending) {
            try {
                await this.syncTransaction(transaction);
                await this.markSynced(transaction.id);
            } catch (error) {
                console.error('Sync failed:', error);
                // Keep transaction for retry
            }
        }
    }

    private async syncTransaction(transaction: OfflineTransaction): Promise<void> {
        const apiEndpoint = this.getApiEndpoint(transaction.transaction_type);
        const response = await fetch(apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.authToken}`
            },
            body: transaction.data
        });

        if (!response.ok) {
            throw new Error(`Sync failed: ${response.statusText}`);
        }
    }
}
```

#### **AR-Powered Location Navigation**
```typescript
class LocationNavigator {
    private camera: Camera;
    private arSession: ARSession;

    async initializeAR(): Promise<void> {
        // Request camera permissions
        const hasPermission = await this.requestCameraPermission();
        if (!hasPermission) throw new Error('Camera permission denied');

        // Initialize AR session
        this.arSession = await ARSession.create({
            tracking: 'world',
            camera: this.camera
        });

        // Load warehouse map
        const warehouseMap = await this.loadWarehouseMap();
        this.arSession.addAnchors(warehouseMap.anchors);
    }

    async navigateToLocation(targetLocation: Location): Promise<void> {
        // Get current position
        const currentPosition = await this.getCurrentPosition();

        // Calculate navigation path
        const path = await this.calculatePath(currentPosition, targetLocation);

        // Display AR navigation
        this.displayNavigationOverlay(path);

        // Provide voice guidance
        this.startVoiceGuidance(path);
    }

    private async calculatePath(from: Position, to: Location): Promise<Path> {
        // Use A* algorithm for pathfinding
        const graph = await this.buildWarehouseGraph();
        return aStarSearch(graph, from, to);
    }

    private displayNavigationOverlay(path: Path): void {
        // Render AR arrows and distance indicators
        this.arSession.addOverlay({
            type: 'navigation',
            path: path,
            style: {
                arrowColor: '#007AFF',
                distanceText: true,
                voiceGuidance: true
            }
        });
    }
}
```

---

## 🧠 Phase 6: AI & Advanced Features (2027)

### Machine Learning Pipeline

#### **Computer Vision for Inventory Recognition**
```python
class InventoryVisionAI:
    def __init__(self):
        self.model = self.load_pretrained_model()
        self.label_encoder = self.load_label_encoder()

    def identify_item_from_image(self, image_path: str) -> Dict[str, Any]:
        """Identify item from photo using computer vision"""
        # Preprocess image
        image = self.preprocess_image(image_path)

        # Extract features
        features = self.extract_features(image)

        # Classify item
        predictions = self.model.predict_proba(features)[0]
        top_predictions = self.get_top_predictions(predictions, top_k=5)

        # Get item details
        identified_items = []
        for item_code, confidence in top_predictions:
            item_details = self.get_item_details(item_code)
            identified_items.append({
                'item_code': item_code,
                'item_name': item_details.get('item_name'),
                'confidence': confidence,
                'location': item_details.get('default_location'),
                'stock': item_details.get('current_stock')
            })

        return {
            'identified_items': identified_items,
            'processing_time': time.time() - start_time,
            'image_quality': self.assess_image_quality(image)
        }

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for model input"""
        image = cv2.imread(image_path)
        image = cv2.resize(image, (224, 224))
        image = image.astype(np.float32) / 255.0

        # Apply image augmentations for robustness
        image = self.apply_augmentations(image)

        return np.expand_dims(image, axis=0)

    def extract_features(self, image: np.ndarray) -> np.ndarray:
        """Extract features using pre-trained CNN"""
        return self.feature_extractor.predict(image)

    def train_model(self, training_data: pd.DataFrame):
        """Fine-tune model on organization-specific data"""
        # Prepare training data
        X_train, X_val, y_train, y_val = self.prepare_training_data(training_data)

        # Fine-tune pre-trained model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=50,
            callbacks=[self.get_callbacks()]
        )

        # Save fine-tuned model
        self.model.save('fine_tuned_inventory_model.h5')

        return history
```

#### **Natural Language Processing for Voice Commands**
```python
class VoiceCommandProcessor:
    def __init__(self):
        self.nlp_model = self.load_nlp_model()
        self.intent_classifier = self.load_intent_classifier()
        self.entity_extractor = self.load_entity_extractor()

    def process_voice_command(self, audio_data: bytes) -> Dict[str, Any]:
        """Process voice command and execute appropriate action"""
        # Convert speech to text
        text = self.speech_to_text(audio_data)

        # Classify intent
        intent = self.classify_intent(text)

        # Extract entities
        entities = self.extract_entities(text)

        # Execute command
        result = self.execute_command(intent, entities)

        return {
            'original_text': text,
            'intent': intent,
            'entities': entities,
            'result': result,
            'confidence': self.get_confidence_score()
        }

    def speech_to_text(self, audio_data: bytes) -> str:
        """Convert audio to text using speech recognition"""
        # Use Google Speech Recognition or similar service
        recognizer = sr.Recognizer()

        with sr.AudioFile(io.BytesIO(audio_data)) as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            raise Exception("Speech recognition service unavailable")

    def classify_intent(self, text: str) -> str:
        """Classify the intent of the voice command"""
        features = self.extract_text_features(text)
        intent_scores = self.intent_classifier.predict_proba([features])[0]

        # Get highest scoring intent
        intent_index = np.argmax(intent_scores)
        intent = self.intent_labels[intent_index]

        return intent

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract relevant entities from text"""
        doc = self.nlp_model(text)

        entities = {}
        for ent in doc.ents:
            if ent.label_ in ['ITEM', 'LOCATION', 'QUANTITY', 'UOM']:
                entities[ent.label_.lower()] = ent.text

        return entities

    def execute_command(self, intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the appropriate action based on intent and entities"""
        command_handlers = {
            'check_stock': self.handle_check_stock,
            'find_item': self.handle_find_item,
            'create_issue': self.handle_create_issue,
            'get_location': self.handle_get_location
        }

        handler = command_handlers.get(intent)
        if handler:
            return handler(entities)
        else:
            return {'error': f'Unknown intent: {intent}'}

    def handle_check_stock(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Handle stock checking commands"""
        item_code = entities.get('item')
        if not item_code:
            return {'error': 'No item specified'}

        # Find item by name/code
        item = self.find_item(item_code)
        if not item:
            return {'error': f'Item not found: {item_code}'}

        # Get current stock
        stock_info = self.get_stock_info(item['item_code'])

        return {
            'item': item,
            'stock': stock_info,
            'message': f"{item['item_name']} has {stock_info['quantity']} {stock_info['uom']} in stock"
        }
```

---

## 🏢 Phase 7: Enterprise Features (2028-2030)

### Multi-tenant Architecture

#### **Tenant Isolation Controller**
```python
class TenantManager:
    def __init__(self):
        self.current_tenant = None
        self.tenant_cache = {}

    def set_tenant(self, tenant_id: str):
        """Set the current tenant context"""
        if tenant_id not in self.tenant_cache:
            self.load_tenant_config(tenant_id)

        self.current_tenant = tenant_id
        self.apply_tenant_context()

    def load_tenant_config(self, tenant_id: str):
        """Load tenant-specific configuration"""
        tenant_config = frappe.get_doc("Tenant", tenant_id)

        self.tenant_cache[tenant_id] = {
            'name': tenant_config.tenant_name,
            'database': tenant_config.database_name,
            'schema': tenant_config.schema_name,
            'settings': tenant_config.settings,
            'limits': tenant_config.usage_limits,
            'features': tenant_config.enabled_features
        }

    def apply_tenant_context(self):
        """Apply tenant-specific database context"""
        tenant_config = self.tenant_cache[self.current_tenant]

        # Set database connection
        frappe.db.set_db(tenant_config['database'])

        # Apply row-level security
        self.apply_rls_policies()

        # Set tenant-specific settings
        self.apply_tenant_settings(tenant_config['settings'])

    def apply_rls_policies(self):
        """Apply Row Level Security policies"""
        # Ensure users can only see their tenant's data
        frappe.db.execute("""
            SET LOCAL app.tenant_id = %s
        """, [self.current_tenant])

    def validate_tenant_limits(self, operation: str) -> bool:
        """Validate operation against tenant limits"""
        limits = self.tenant_cache[self.current_tenant]['limits']

        if operation == 'create_item':
            current_items = self.count_tenant_items()
            if current_items >= limits.get('max_items', 10000):
                raise TenantLimitExceeded("Item limit exceeded")

        elif operation == 'create_user':
            current_users = self.count_tenant_users()
            if current_users >= limits.get('max_users', 100):
                raise TenantLimitExceeded("User limit exceeded")

        return True
```

#### **Tenant Provisioning System**
```python
class TenantProvisioner:
    def provision_tenant(self, tenant_data: Dict[str, Any]) -> str:
        """Provision a new tenant"""
        # Generate tenant ID
        tenant_id = self.generate_tenant_id()

        # Create tenant database schema
        self.create_tenant_schema(tenant_id)

        # Initialize tenant data
        self.initialize_tenant_data(tenant_id, tenant_data)

        # Create admin user
        admin_user = self.create_tenant_admin(tenant_id, tenant_data)

        # Send welcome email
        self.send_welcome_email(admin_user, tenant_data)

        return tenant_id

    def create_tenant_schema(self, tenant_id: str):
        """Create isolated database schema for tenant"""
        schema_name = f"tenant_{tenant_id}"

        # Create schema
        frappe.db.execute(f"CREATE SCHEMA {schema_name}")

        # Create tenant-specific tables
        self.create_tenant_tables(schema_name)

        # Set up foreign key relationships
        self.setup_tenant_relationships(schema_name)

    def initialize_tenant_data(self, tenant_id: str, tenant_data: Dict[str, Any]):
        """Initialize tenant with default data"""
        # Switch to tenant context
        tenant_manager = TenantManager()
        tenant_manager.set_tenant(tenant_id)

        # Install demo data
        self.install_demo_data()

        # Configure settings
        self.configure_tenant_settings(tenant_data)

        # Set up default roles and permissions
        self.setup_default_security()

    def create_tenant_admin(self, tenant_id: str, tenant_data: Dict[str, Any]) -> str:
        """Create tenant administrator"""
        admin_data = {
            'email': tenant_data['admin_email'],
            'first_name': tenant_data['admin_first_name'],
            'last_name': tenant_data['admin_last_name'],
            'role': 'Tenant Admin',
            'tenant_id': tenant_id
        }

        user = frappe.get_doc({
            'doctype': 'User',
            **admin_data
        })
        user.insert()

        return user.name
```

---

## 📋 Implementation Roadmap

### Q1 2026: Transaction Foundation
- [ ] Complete Store Item Receipt DocType
- [ ] Implement receipt business logic
- [ ] Add quality control workflow
- [ ] Create receipt printing templates
- [ ] Test receipt-to-stock integration

### Q2 2026: Analytics & Intelligence
- [ ] Build dashboard framework
- [ ] Implement basic reporting engine
- [ ] Add predictive analytics foundation
- [ ] Create custom report builder
- [ ] Develop alert system

### Q3 2026: Integration & Automation
- [ ] Complete ERPNext bidirectional sync
- [ ] Enhance API platform (v2)
- [ ] Add third-party integrations
- [ ] Implement webhook engine
- [ ] Create integration testing suite

### Q4 2026: Mobile & IoT
- [ ] Develop native mobile apps
- [ ] Implement AR location navigation
- [ ] Add IoT sensor integration
- [ ] Create offline synchronization
- [ ] Test RFID integration

### 2027: AI & Advanced Features
- [ ] Implement ML-based demand forecasting
- [ ] Add computer vision for inventory
- [ ] Create voice command processing
- [ ] Develop recommendation engine
- [ ] Build anomaly detection system

---

## 🔧 Technical Specifications

### Performance Requirements
- **Response Time**: <500ms for 95% of requests
- **Concurrent Users**: Support 1,000+ simultaneous users
- **Data Processing**: Handle 10,000+ transactions/hour
- **Mobile Sync**: <30 seconds for full sync
- **AI Processing**: <5 seconds for image recognition

### Scalability Architecture
- **Microservices**: Modular, independently scalable components
- **Database Sharding**: Horizontal scaling for large datasets
- **CDN Integration**: Global content delivery
- **Load Balancing**: Automatic traffic distribution
- **Auto-scaling**: Dynamic resource allocation

### Security Framework
- **Multi-tenant Isolation**: Complete data separation
- **End-to-end Encryption**: Data protection at rest and in transit
- **Audit Logging**: Comprehensive activity tracking
- **Compliance**: GDPR, HIPAA, SOX compliance frameworks
- **Access Control**: Role-based and attribute-based access

---

*This document provides detailed technical specifications for future enhancements. All features are designed to be modular, scalable, and backward-compatible with the existing Technical Store System.*

**Last Updated:** December 11, 2025

---

## Store Settings

**Type:** Single DocType (one global record)  
**Purpose:** Application-wide configuration and settings  
**Location:** `technical_store_system/setup/doctypes/StoreSettings.py`

### Tab 1: General Settings
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `company_name` | Data | Your company/store name | ✅ Active |
| `default_currency` | Link (Currency) | Currency for pricing and transactions (default: USD) | ✅ Active |

### Tab 2: Stock Management
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `allow_negative_stock` | Check | Allow issuing items even when stock is zero (for backorders) | ✅ Active |
| `stock_validation` | Check | Check available quantity before allowing issue (hidden if negative stock allowed) | ✅ Active |
| `auto_stock_reorder` | Check | Send alerts when stock reaches minimum level | ✅ Active |
| `enable_batch_tracking` | Check | Track items by batch numbers (manufacturing date, expiry, etc.) | ✅ Active |
| `enable_serial_tracking` | Check | Track items by unique serial numbers (warranty, maintenance, etc.) | ✅ Active |
| `auto_create_serial_no` | Check | Automatically create serial numbers (SN001, SN002, etc.) | ✅ Active |

### Tab 3: Integration
**Status:** Empty tab reserved for future integrations

### Tab 4: Pricing & Tax
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `default_price_list` | Data | Default price list for items | ✅ Active |
| `include_tax_in_price` | Check | Include tax in item price | ✅ Active |
| `default_tax_rate` | Float | Default tax percentage | ✅ Active |
| `round_off_amount` | Check | Round off amount in transactions | ✅ Active |

### Tab 5: Notifications
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `enable_email_notifications` | Check | Enable email notifications | ✅ Active |
| `notification_email` | Data | Email address for notifications (shown if emails enabled) | ✅ Active |
| `low_stock_alert` | Check | Send alerts for low stock | ✅ Active |
| `stock_expiry_alert` | Check | Send alerts for expiring stock | ✅ Active |

### Tab 6: Demo Data
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `demo_data_info` | HTML | Information about demo data | ✅ Active |
| `install_demo_uoms` | Check | Install 27 UOMs (Each, Kg, Liter, Meter, Box, etc.) | ✅ Active |
| `install_demo_item_groups` | Check | Install 19 item groups (Electronics, Tools, Consumables, etc.) | ✅ Active |
| `install_demo_locations` | Check | Install 11 locations (Warehouses, Areas, Racks, Shelves, etc.) | ✅ Active |
| `install_demo_items` | Check | Install 16 sample items (Tools, Safety, Electrical, etc.) | ✅ Active |
| `install_demo_data_btn` | Button | Trigger demo data installation | ✅ Active |
| `uninstall_demo_data_btn` | Button | Remove all demo data | ✅ Active |
| `demo_data_status` | HTML | Show demo data installation status | ✅ Active |

### Tab 7: Advanced
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `enable_audit_trail` | Check | Track all changes in system | ✅ Active |
| `enable_barcode_scanning` | Check | Enable barcode scanning | ✅ Active |
| `enable_mobile_app` | Check | Enable mobile app access | ✅ Active |
| `enable_api_access` | Check | Enable API access | ✅ Active |
| `erpnext_installed` | Data (Read-only) | ERPNext installation status (auto-detected) | ✅ Active |
| `enable_erpnext_integration` | Check | Enable ERPNext integration (hidden if ERPNext not installed) | 🔜 Future |

---

## Store Item

**Type:** Master DocType  
**Purpose:** Inventory items with comprehensive tracking  
**Location:** `technical_store_system/setup/doctypes/StoreItem.py`  
**Auto-naming:** ITEM-#####

### Tab 1: Basic Information
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `item_code` | Data (Auto) | Auto-generated: ITEM-##### | ✅ Active |
| `item_name` | Data* | Item name (required) | ✅ Active |
| `item_group` | Link* (Store Item Group) | Category/classification (required) | ✅ Active |
| `technical_category` | Link (Store Technical Category) | Technical classification (Electrical, Mechanical, etc.) | ✅ Active |
| `description` | Text Editor | Detailed description | ✅ Active |
| `image` | Attach Image | Item image/photo | ✅ Active |
| `default_uom` | Link* (Store UOM) | Default unit of measure (required) | ✅ Active |
| `allow_alternative_uom` | Check | Allow using alternative UOMs | ✅ Active |

### Tab 2: Stock Control
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `maintain_stock` | Check | Track stock levels (default: Yes) | ✅ Active |
| `is_stock_item` | Check | Is this a stock item (default: Yes) | ✅ Active |
| `allow_negative_stock` | Check | Allow negative stock for this item | ✅ Active |
| `has_serial_no` | Check | Track individual serial numbers | ✅ Active |
| `has_batch_no` | Check | Track batch numbers | ✅ Active |
| `has_expiry_date` | Check | Item has expiry date (for batches) | ✅ Active |
| `shelf_life_days` | Int | Shelf life in days (shown if has expiry) | ✅ Active |
| `valuation_method` | Select | FIFO / LIFO / Moving Average (default: FIFO) | ✅ Active |

### Tab 3: Inventory Tracking
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `serial_numbers` | Table (Store Item Serial Number) | Serial number tracking (shown if has_serial_no) | ✅ Active |
| `batch_numbers` | Table (Store Item Batch Number) | Batch number tracking (shown if has_batch_no) | ✅ Active |
| `opening_stock` | Float | Opening stock quantity | ✅ Active |
| `opening_valuation_rate` | Currency | Opening valuation rate | ✅ Active |
| `default_location` | Link (Store Location) | Default storage location | ✅ Active |
| `minimum_level` | Float | Alert when stock falls below this level | ✅ Active |
| `reorder_level` | Float | Trigger reorder at this level | ✅ Active |
| `reorder_qty` | Float | Standard quantity to reorder | ✅ Active |
| `maximum_level` | Float | Maximum stock allowed | ✅ Active |

### Tab 4: Pricing & Specifications
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `standard_rate` | Currency | Standard valuation rate | ✅ Active |
| `last_purchase_rate` | Currency (Read-only) | Last purchase rate | ✅ Active |
| `technical_specs` | Text Editor | Technical specifications (free text) | ✅ Active |
| `specifications_json` | JSON | Structured specifications data | ✅ Active |

### Tab 5: Barcodes & Identification
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `barcode` | Data (Unique) | Barcode for scanning | ✅ Active |
| `qr_code` | Data (Unique) | QR code data | ✅ Active |

### Tab 6: Settings
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `is_purchase_item` | Check | Can be purchased from suppliers (default: Yes) | ✅ Active |
| `is_returnable` | Check | Can be returned to purchase department (default: Yes) | ✅ Active |
| `is_restricted` | Check | Requires special authorization to issue | ✅ Active |
| `enabled` | Check | Item is active and usable (default: Yes) | ✅ Active |

---

## Store Location

**Type:** Master DocType  
**Purpose:** Physical location tracking (warehouse, area, rack, shelf)  
**Location:** `technical_store_system/setup/doctypes/StoreLocation.py`  
**Auto-naming:** field:location_code  
**Examples:** Main Warehouse → Area A → Rack 1 → Shelf 2  
**Status:** ✅ **Cleaned up - removed 30 unused fields (Dec 8, 2025)**

### Tab 1: Basic Information
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `location_code` | Data* (Unique) | Unique code (e.g., WH-A-R01-S1) | ✅ Active |
| `location_name` | Data* | Descriptive name | ✅ Active |
| `location_type` | Select* | Warehouse, Store Room, Area, Zone, Rack, Shelf, Bin, Row, Column, Transit, Staging, Other | ✅ Active |
| `enabled` | Check | Location is active (default: Yes) | ✅ Active |
| `parent_location` | Link (Store Location) | Parent location in hierarchy | ✅ Active |
| `is_group` | Check | Can contain sub-locations | ✅ Active |
| `address` | Small Text | Full physical address (for main warehouses) | ✅ Active |
| `zone` | Data | Zone or area code (e.g., A, B, C) | ✅ Active |
| `rack` | Data | Rack number | ✅ Active |
| `shelf` | Data | Shelf number | ✅ Active |
| `row` | Data | Row number | ✅ Active |
| `column` | Data | Column number | ✅ Active |

### Tab 2: Additional Details
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `barcode` | Data (Unique) | Barcode for scanning | ✅ Active |
| `qr_code` | Data (Unique) | QR code data | ✅ Active |
| `description` | Text Editor | Detailed description and notes | ✅ Active |
| `image` | Attach Image | Photo of the location (collapsible) | ✅ Active |

### 🗑️ Removed Fields (30 fields deleted)
**Reason:** Over-engineering - demo data only used 10 fields out of 35+

**Physical Details (removed):**
- `aisle`, `bin`, `cell`, `bucket` - Redundant with location_type

**Capacity & Dimensions Tab (removed):**
- `max_capacity`, `capacity_uom`, `current_utilization` - Not used in basic inventory
- `length`, `width`, `height` - Physical dimensions rarely needed

**Advanced Features (removed):**
- `rfid_tag`, `gps_coordinates` - Advanced warehouse automation
- `is_bonded`, `temperature_controlled`, `hazardous_storage` - Specialized use cases
- `allow_negative_stock` - Controlled at global settings level

**Contact & Management (removed):**
- `contact_person`, `contact_phone`, `contact_email`, `manager` - Can be in description

**Note:** These fields can be added back as future enhancements if needed for advanced warehouse management.

---

## Store UOM

**Type:** Master DocType  
**Purpose:** Unit of Measure definitions (Each, Kg, Liter, etc.)  
**Location:** `technical_store_system/setup/doctypes/StoreUOM.py`  
**Auto-naming:** field:uom_name  
**Demo Data:** 27 units available

### Tab 1: Basic Information
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `uom_name` | Data* (Unique) | Unit of Measure name (e.g., Each, Kg, Liter) | ✅ Active |
| `uom_symbol` | Data | Short symbol (e.g., Ea, kg, L) | ✅ Active |
| `enabled` | Check | UOM is active (default: Yes) | ✅ Active |
| `is_default` | Check | Set as default UOM for new items | ✅ Active |

### Tab 2: Classification & Conversion
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `uom_type` | Select | Quantity, Weight, Volume, Length, Area, Time, Other (default: Quantity) | ✅ Active |
| `must_be_whole_number` | Check | Quantities must be integers (e.g., Each, Box) | ✅ Active |
| `has_conversion` | Check | Can convert to other UOMs | 🔜 Future |
| `base_uom` | Link (Store UOM) | Reference UOM for conversion (shown if has_conversion) | 🔜 Future |
| `conversion_factor` | Float | 1 [This UOM] = X [Base UOM] (shown if has_conversion) | 🔜 Future |

### Tab 3: Additional Information
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `description` | Text Editor | Detailed description and usage notes | ✅ Active |

---

## Store Item Group

**Type:** Master DocType (Tree Structure)  
**Purpose:** Hierarchical category/classification for items  
**Location:** `technical_store_system/setup/doctypes/StoreItemGroup.py`  
**Auto-naming:** field:item_group_name  
**Demo Data:** 19 categories available  
**Example:** Electronics → Computers → Laptops

### Tab 1: Basic Information
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `item_group_name` | Data* (Unique) | Name of the item category/group | ✅ Active |
| `parent_item_group` | Link (Store Item Group) | Parent category (leave blank for root) | ✅ Active |
| `is_group` | Check | Check if this is a group (can have sub-groups) | ✅ Active |
| `enabled` | Check | Group is active (default: Yes) | ✅ Active |
| `description` | Text Editor | Detailed description of the item group | ✅ Active |
| `image` | Attach Image | Representative image for this group | ✅ Active |

### Tab 2: Configuration
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `default_uom` | Link (Store UOM) | Default unit of measure for items in this group | ✅ Active |
| `has_serial_no` | Check | Items in this group have serial numbers by default | ✅ Active |
| `has_batch_no` | Check | Items in this group have batch numbers by default | ✅ Active |
| `allow_negative_stock` | Check | Allow negative stock for items in this group | ✅ Active |

### Tab 3: Statistics
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `item_count` | Int (Read-only) | Number of items in this group | ✅ Active |
| `last_updated` | Datetime (Read-only) | Last time statistics were updated | ✅ Active |

---

## Store Technical Category

**Type:** Master DocType  
**Purpose:** Technical classification of items (Electrical, Mechanical, Electronic, etc.)  
**Location:** `technical_store_system/setup/doctypes/StoreTechnicalCategory.py`  
**Auto-naming:** field:category_name  
**Demo Data:** 12 categories (Electrical, Mechanical, Electronic, Consumable, Chemical, Hardware, Tool, Safety, Office, IT, Spare Part, Raw Material)

### Fields
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `category_name` | Data* (Unique) | Category name | ✅ Active |
| `description` | Text | Description of the category | ✅ Active |
| `enabled` | Check | Category is active (default: Yes) | ✅ Active |

---

## Store Item Serial Number

**Type:** Child Table (for Store Item)  
**Purpose:** Track individual serial numbers for items  
**Location:** `technical_store_system/setup/doctypes/StoreItemSerialNumber.py`

### Fields
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `serial_no` | Data* (Unique) | Serial number | ✅ Active |
| `status` | Select* | Available, Issued, In Transit, Damaged, Returned (default: Available) | ✅ Active |
| `purchase_date` | Date | Purchase date | ✅ Active |
| `warranty_expiry` | Date | Warranty expiry date | ✅ Active |

---

## Store Item Batch Number

**Type:** Child Table (for Store Item)  
**Purpose:** Track batch numbers for items  
**Location:** `technical_store_system/setup/doctypes/StoreItemBatchNumber.py`

### Fields
| Field Name | Type | Description | Status |
|------------|------|-------------|--------|
| `batch_no` | Data* | Batch number | ✅ Active |
| `quantity` | Float* | Quantity in this batch | ✅ Active |
| `manufacturing_date` | Date | Manufacturing date | ✅ Active |
| `expiry_date` | Date | Expiry date | ✅ Active |

---

## Future Enhancements

Features with placeholder fields that need full implementation later.

### 1. ERPNext Integration

**Status:** Placeholder exists in Store Settings  
**Location:** `setup/doctypes/StoreSettings.py` (Advanced tab)  
**Priority:** LOW (implement at the very end)

**Fields Ready:**
- `erpnext_section` - Section header (collapsible)
- `erpnext_installed` - Auto-detection status (read-only)
- `enable_erpnext_integration` - Enable/disable checkbox (hidden if ERPNext not installed)

**What's Needed:**
- Sync Store Items ↔ ERPNext Items
- Sync Stock levels ↔ ERPNext Stock Ledger
- Sync Locations ↔ ERPNext Warehouses
- Two-way data synchronization
- Conflict resolution logic
- Mapping configuration UI
- Field mapping system
- Sync triggers (realtime vs scheduled)

**Implementation Roadmap:**
1. Create mapping table (Store Item ↔ ERPNext Item)
2. Create sync functions (push/pull)
3. Add conflict detection
4. Add manual sync buttons in UI
5. Add automatic sync on save (optional)
6. Add sync logs and error handling

---

### 2. UOM Conversion System

**Status:** Placeholder exists in Store UOM  
**Location:** `setup/doctypes/StoreUOM.py` (Classification & Conversion tab)  
**Priority:** MEDIUM (useful for multi-unit items)

**Fields Ready:**
- `has_conversion` - Enable conversion checkbox
- `base_uom` - Reference UOM link (shown if has_conversion)
- `conversion_factor` - Conversion multiplier (shown if has_conversion)

**What's Needed:**
- Validation to prevent circular conversions
- Support for conversion chains (Box → Each → Piece)
- Helper functions to convert quantities between UOMs
- Maybe child table for multiple conversion paths if complex
- Auto-calculation in transactions (optional)
- Conversion history tracking

**Implementation Roadmap:**
1. Create validation for circular references
2. Build conversion calculation functions
3. Add conversion testing (round-trip conversions)
4. Create API for other DocTypes to use conversions
5. Add conversion preview in UI
6. Optional: Create UOM Conversion child table for multiple paths

**Example Use Cases:**
- 1 Box = 12 Each
- 1 Kg = 1000 g
- 1 Carton = 20 Boxes = 240 Each
- 1 Pallet = 40 Cartons = 800 Boxes = 9600 Each

---

## Field Statistics

### Total Field Count by DocType
| DocType | Total Fields | Status |
|---------|-------------|--------|
| Store Settings | 35 fields (7 tabs) | ✅ Complete |
| Store Item | 40+ fields (6 tabs) | ✅ Complete |
| Store Location | 16 fields (2 tabs) | ✅ Cleaned (30 fields removed) |
| Store UOM | 10 fields (3 tabs) | ✅ Complete (3 future fields) |
| Store Item Group | 11 fields (3 tabs) | ✅ Complete |
| Store Technical Category | 3 fields (1 tab) | ✅ Complete |
| Store Item Serial Number | 4 fields (child) | ✅ Complete |
| Store Item Batch Number | 4 fields (child) | ✅ Complete |
| **TOTAL** | **120+ fields** | **8 DocTypes** |

### Field Type Distribution
- **Check:** ~40 fields (boolean flags)
- **Data:** ~35 fields (text input)
- **Link:** ~20 fields (references)
- **Float/Currency:** ~15 fields (numbers)
- **Select:** ~10 fields (dropdowns)
- **Text Editor:** ~8 fields (rich text)
- **Date/Datetime:** ~6 fields (dates)
- **Table:** 2 fields (child tables)
- **JSON:** 1 field (structured data)
- **HTML:** 2 fields (display only)
- **Button:** 2 fields (actions)

---

## Implementation Status

### ✅ Completed (100% functional)
1. Store Settings - All 7 tabs complete with demo data system
2. Store Item - Full master with tracking, pricing, specifications
3. Store Location - Comprehensive location hierarchy
4. Store UOM - Basic UOM management (conversion placeholder)
5. Store Item Group - Tree structure with configuration
6. Store Technical Category - Simple classification
7. Child Tables - Serial and Batch tracking structures

### 🔜 Future (Placeholders exist)
1. ERPNext Integration - Fields exist, logic pending
2. UOM Conversion - Fields exist, logic pending

### ⬜ Not Started (To be built)
1. Transaction DocTypes (Stock Entry, Issue, Return, Transfer)
2. Reports and analytics
3. Dashboard widgets
4. Mobile app features
5. API endpoints
6. Barcode scanning integration

---

## Implementation Sequence

**Recommended order for remaining work:**

1. ✅ **Store Settings complete** - DONE
2. ⬜ **Clean existing DocTypes** - IN PROGRESS (user's request)
3. ⬜ **Transaction DocTypes** - Core functionality
   - Stock Entry (receive, adjust)
   - Stock Issue (issue to departments)
   - Stock Return (return from departments)
   - Stock Transfer (between locations)
4. ⬜ **Reports & Analytics** - Business intelligence
   - Stock Balance Report
   - Movement History
   - Low Stock Report
   - Valuation Report
5. ⬜ **ERPNext Integration** - Optional enhancement (if ERPNext installed)
6. ⬜ **UOM Conversion** - Optional enhancement (if multi-unit items needed)

---

*Last Updated: December 8, 2025*  
*Total DocTypes: 8 (6 Masters + 1 Single + 2 Child Tables)*  
*Total Fields: 140+ across all DocTypes*
