# Enterprise Backend - ISA-95 Business & Operations

## Purpose

ISA-95 Level 4 business planning and logistics interfaces with hierarchical navigation to L3 (MES), L2 (SCADA/HMI), L1 (PLC), and L0 (Physical) levels.

## Directory Structure

```
/screens/Enterprise/
├── structure.md                   This file
├── docking-hmi.html              ISA-101 docking interface (main)
├── enterprise-portal.html         Business dashboard
├── production-planning.html       Scheduling & resource allocation
├── quality-management.html        QA/QC tracking & reporting
├── analytics-reporting.html       Business intelligence & KPIs
├── asset-management.html          Equipment & inventory tracking
├── maintenance-planning.html      PM/CM scheduling
├── configuration.html             System settings & admin
│
└── L3/                            MES Operations (Level 3)
    ├── structure.md               L3 documentation
    └── L2/                        Supervisory Control (Level 2)
        ├── hmi.html               Human-Machine Interface
        ├── scada.html             SCADA monitoring dashboard
        ├── structure.md           L2 documentation
        └── L1/                    Basic Control (Level 1)
            ├── plc.html           PLC programming interface
            ├── structure.md       L1 documentation
            └── L0/                Physical Processes (Level 0)
                ├── structure.md   L0 documentation (ready for devices)
                └── [future]       Direct device interfaces
```

## ISA-95 Level 4 Screens

### Docking HMI (`docking-hmi.html`)
**Purpose:** Main enterprise interface with ISA-101 docking design
**Access:** Default enterprise landing page
**Features:**
- L4 business KPIs (production, quality, assets)
- Quick access buttons to all L4 screens
- Navigation to lower levels (L3→L2→L1→L0)
- Real-time system status
- Alarm summary panel

**Design:** ISA-101 cream & purple theme with docking paradigm

### Enterprise Portal (`enterprise-portal.html`)
**Purpose:** Executive dashboard for business planning
**Metrics:**
- Overall Equipment Effectiveness (OEE)
- Production throughput
- Quality metrics (defect rates, compliance)
- Asset utilization
- Financial KPIs

**Navigation:** Hub for accessing all other L4 screens

### Production Planning (`production-planning.html`)
**Purpose:** Schedule imaging workflows and resource allocation
**Features:**
- Medical imaging workflow scheduler
- Equipment calendar (CT, MRI, X-ray)
- Patient scheduling (de-identified)
- Resource optimization (rooms, staff, equipment)
- Batch job queueing

**Integration:** ISA-88 batch control, PackML state machines

### Quality Management (`quality-management.html`)
**Purpose:** QA/QC tracking and compliance reporting
**Features:**
- Image quality metrics dashboard
- Compliance tracking (HIPAA, FDA 21 CFR Part 11)
- Audit trail viewer
- Defect tracking (artifacts, incorrect parameters)
- Corrective action workflow

**Standards:** ISO 13485, IEC 62304

### Analytics & Reporting (`analytics-reporting.html`)
**Purpose:** Business intelligence and data visualization
**Features:**
- Imaging volume trends (by modality)
- AI algorithm performance metrics
- Equipment utilization reports
- Financial analytics (cost per study)
- Custom report builder

**Exports:** PDF, CSV, Excel

### Asset Management (`asset-management.html`)
**Purpose:** Equipment and inventory tracking
**Features:**
- Equipment registry (CT, MRI, X-ray devices)
- Inventory tracking (contrast agents, supplies)
- Depreciation schedules
- Warranty tracking
- Asset transfer workflow

**Integration:** CMMS (Computerized Maintenance Management System)

### Maintenance Planning (`maintenance-planning.html`)
**Purpose:** Preventive and corrective maintenance scheduling
**Features:**
- PM schedule calendar
- Work order management
- Equipment downtime tracking
- Spare parts inventory
- Maintenance history logs

**Types:**
- Preventive Maintenance (PM)
- Corrective Maintenance (CM)
- Predictive Maintenance (PdM) - future

### Configuration (`configuration.html`)
**Purpose:** System administration and settings
**Features:**
- User management (roles, permissions)
- System parameters
- Integration settings (PACS, MQTT, OPC-UA)
- Theme customization
- Backup/restore

**Access:** Admin only

## ISA-95 Hierarchical Navigation

### Level Flow
```
L4 (Enterprise) - Business Planning
  │
  ├─→ Production Planning
  ├─→ Quality Management
  ├─→ Analytics & Reporting
  ├─→ Asset Management
  ├─→ Maintenance Planning
  └─→ Configuration
  │
  ↓ Navigate Down
  │
L3 (MES) - Operations Management
  │
  ↓ Navigate Down
  │
L2 (Supervisory) - SCADA & HMI
  │
  ├─→ SCADA Dashboard
  ├─→ HMI Controls
  │
  ↓ Navigate Down
  │
L1 (Basic Control) - PLC Programming
  │
  ├─→ PLC Ladder Logic
  ├─→ Device Control
  │
  ↓ Navigate Down
  │
L0 (Physical) - Devices & Sensors
  │
  └─→ [Future: Direct device interfaces]
```

### Upward Navigation
Each level can navigate back to parent:
- L1 → L2 (breadcrumb or "Back to SCADA" button)
- L2 → L3 (breadcrumb or "Back to MES" button)
- L3 → L4 (breadcrumb or "Back to Enterprise" button)

## L3 - MES Operations (Manufacturing Execution System)

**Purpose:** Workflow orchestration and batch management
**Location:** `/screens/Enterprise/L3/`
**Status:** Directory created, screens pending implementation

**Planned Screens:**
- `mes-dashboard.html` - Operations overview
- `workflow-manager.html` - Medical imaging workflows
- `batch-control.html` - ISA-88 batch execution
- `recipe-manager.html` - Workflow recipes

**Integration:**
- ISA-88 batch control
- PackML state machines
- MQTT messaging for real-time updates

## L2 - Supervisory Control

**Purpose:** SCADA monitoring and HMI interfaces
**Location:** `/screens/Enterprise/L3/L2/`
**Files:** `hmi.html`, `scada.html`

### HMI (`hmi.html`)
**Purpose:** Human-Machine Interface for operator control
**Features:**
- Real-time device status
- Manual control overrides
- Alarm acknowledgment
- Trend charts
- Process mimics

**Design:** ISA-101 compliant (high contrast, alarm colors)

### SCADA (`scada.html`)
**Purpose:** Supervisory Control And Data Acquisition
**Features:**
- Multi-device monitoring (CT, MRI, X-ray)
- Telemetry visualization
- Historical data trends
- Alert management
- Remote control capabilities

**Protocols:** MQTT, OPC-UA

## L1 - Basic Control

**Purpose:** PLC programming and device control
**Location:** `/screens/Enterprise/L3/L2/L1/`
**Files:** `plc.html`

### PLC Interface (`plc.html`)
**Purpose:** Programmable Logic Controller programming
**Features:**
- Ladder logic editor
- Function block diagrams
- Structured text programming
- Device I/O mapping
- Real-time debugging

**Standards:** IEC 61131-3 programming languages

**Languages:**
- LD (Ladder Diagram)
- FBD (Function Block Diagram)
- ST (Structured Text)
- SFC (Sequential Function Chart)
- IL (Instruction List)

## L0 - Physical Processes

**Purpose:** Direct device and sensor interfaces
**Location:** `/screens/Enterprise/L3/L2/L1/L0/`
**Status:** Ready for future expansion

**Planned Interfaces:**
- CT scanner control
- MRI sequence programming
- X-ray exposure settings
- Sensor calibration
- Actuator testing

**Connection Methods:**
- USB/Serial communication
- Ethernet (TCP/IP)
- OPC-UA
- DICOM DIMSE

## Theme & Styling

### ISA-101 Compliance
**Base Theme:** `/os/medical/styles/isa101-theme.css`
**Enterprise Styles:** `/styles/index.css`

**Color Usage:**
- **Background:** Deep purple (#2a1a3a) - operator focus on data
- **Text:** Cream (#f5f2e8) - high readability
- **Normal State:** Green (#90ee90) - equipment running OK
- **Warning State:** Yellow (#ffd700) - attention needed
- **Alarm State:** Red (#ff6b6b) - immediate action required
- **Accents:** Purple (#b794f4, #8b5cf6) - UI elements

### Docking Paradigm
- Fixed navigation panel (left or right)
- Content area updates without page reload
- Breadcrumb trail always visible
- Consistent layout across all screens

### Responsive Design
- Desktop optimized (operators use workstations)
- Minimum 1920x1080 resolution
- Touch-friendly for HMI screens
- Keyboard shortcuts for efficiency

## Integration Points

### Frontend Portal
**Link:** `/screens/frontend/index.html`
**Connection:** Footer link "Access Enterprise Portal"
**Purpose:** Transition from user-facing to backend operations

### Medical OS
**Path:** `/os/medical/`
**Integration:** AI algorithm results feed into analytics
**Usage:** Quality metrics, batch processing status

### Standards
**Path:** `/standards/`
**Integration:**
- ISA-95 level definitions
- ISA-101 HMI design
- PackML state machines
- MQTT/OPC-UA protocols

### Examples
**Path:** `/examples/`
**Integration:** Test data for quality control validation
**Usage:** Equipment calibration verification

## User Roles & Access

### Executive (L4 Only)
- Enterprise portal
- Analytics & reporting
- High-level KPIs
- No control access

### Manager (L4 + L3)
- All L4 screens
- MES operations monitoring
- Production planning
- Quality management

### Engineer (L4 + L3 + L2)
- All above
- SCADA monitoring
- HMI configuration
- Alarm management

### Technician (L2 + L1)
- SCADA monitoring
- HMI control
- PLC programming
- Device troubleshooting

### Admin (All Levels)
- Full system access
- Configuration
- User management
- System maintenance

## Development Guidelines

### File Size Limit
**Target:** <250 tokens per HTML file
**Approach:**
- Extract CSS to `/styles/`
- Extract JS to `/scripts/`
- Use external references
- Modular design

### ISA-101 Design Rules
1. **High Contrast:** Cream on dark purple
2. **Minimal Chartjunk:** Clean, data-focused
3. **Alarm Colors:** Green/yellow/red only
4. **Consistent Layout:** Docking paradigm
5. **Operator Focus:** Data, not decoration

### Navigation Consistency
- Breadcrumbs on every screen
- "Up" button to parent level
- "Home" button to docking HMI
- Level indicator (L4, L3, L2, L1, L0)

## Testing

```bash
# Start server
python -m http.server 8000

# Test L4 screens
http://localhost:8000/screens/Enterprise/docking-hmi.html
http://localhost:8000/screens/Enterprise/enterprise-portal.html

# Test hierarchical navigation
http://localhost:8000/screens/Enterprise/L3/L2/scada.html
http://localhost:8000/screens/Enterprise/L3/L2/L1/plc.html

# Test with sample data
python examples/download-samples.py --all
```

## Future Enhancements

### L3 MES Screens
- Complete workflow management
- ISA-88 batch control interface
- Recipe builder
- Real-time performance monitoring

### L1 PLC Expansion
- Online editing (no stop required)
- Simulation mode
- Auto-tuning for control loops
- IEC 61131-3 full language support

### L0 Device Integration
- Direct CT scanner control
- MRI sequence editor
- X-ray exposure calculator
- DICOM modality worklist

### Advanced Features
- Digital twin visualization
- Augmented reality for maintenance
- Predictive maintenance AI
- Energy management dashboard

See `/screens/structure.md` for overall screen organization.
See `/standards/structure.md` for ISA-95 standard details.
See root `/structure.md` for complete project architecture.
