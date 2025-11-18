# Screens Directory - User Interface Hierarchy

## Purpose

ISA-95 hierarchical screen organization separating user-facing interfaces from enterprise backend controls.

## Directory Structure

```
/screens/
├── frontend/                    User-facing medical imaging portal
│   ├── index.html              Main patient/clinician portal
│   ├── structure.md            Frontend organization
│   └── [sub-screens]/          Modular interface components
│
└── Enterprise/                  ISA-95 L4 Business & Planning
    ├── L3/                      MES Operations Management
    │   └── L2/                  Supervisory Control (SCADA/HMI)
    │       └── L1/              Basic Control (PLC)
    │           └── L0/          Physical Processes (empty, future)
    │
    ├── docking-hmi.html         ISA-101 docking interface
    ├── enterprise-portal.html   Main business dashboard
    ├── production-planning.html Scheduling & resource allocation
    ├── quality-management.html  QA/QC tracking
    ├── analytics-reporting.html Business intelligence
    ├── asset-management.html    Equipment & inventory
    ├── maintenance-planning.html PM/CM scheduling
    └── configuration.html       System settings
```

## Frontend vs Enterprise

### Frontend (User-Facing)
**Purpose:** Clinical users accessing medical imaging tools
**Users:** Radiologists, physicians, technicians, patients
**Focus:** Diagnostics, image viewing, AI analysis
**Design:** Clean, intuitive, task-focused
**Access:** Direct landing page (auto-redirect from root)

**Tools Available:**
- CT/MRI viewers
- AI segmentation
- Tumor detection
- AlF-DETECT screening
- Vector search
- Batch processing
- Quality control

### Enterprise (Backend Operations)
**Purpose:** Business and operational management
**Users:** Administrators, operators, engineers, managers
**Focus:** Planning, scheduling, monitoring, configuration
**Design:** ISA-101 HMI, hierarchical navigation
**Access:** Via link from frontend or direct URL

**Levels:**
- **L4:** Business planning, analytics, asset management
- **L3:** Workflow orchestration, batch management
- **L2:** SCADA monitoring, HMI controls
- **L1:** PLC programming, device control
- **L0:** Physical devices (future expansion)

## ISA-95 Hierarchical Navigation

The Enterprise screens follow the Purdue Model nesting:

```
Enterprise Portal (L4)
  └─→ Navigate to L3 (MES Operations)
       └─→ Navigate to L2 (Supervisory - SCADA/HMI)
            └─→ Navigate to L1 (Basic Control - PLC)
                 └─→ Navigate to L0 (Physical Processes)
```

**Upward Navigation:** Each level can navigate back to parent
**Breadcrumbs:** Show current position in hierarchy
**Quick Access:** Jump directly to any level from portal

## File Organization

### HTML Files
**Limit:** <250 tokens per file
**Approach:** Extract CSS/JS to `/styles/` and `/scripts/`
**References:** Use `<link>` and `<script src>` for external configs

### Modular Sub-Screens
Instead of monolithic pages, break into components:
```
frontend/
├── index.html                  Main portal (dashboard)
├── viewers/
│   ├── ct-viewer.html         CT scan interface
│   ├── mri-viewer.html        MRI interface
│   └── xray-viewer.html       X-ray interface
├── ai-tools/
│   ├── segmentation.html      AI segmentation
│   ├── detection.html         Object detection
│   └── alf-detect.html        AlF-DETECT screening
└── utilities/
    ├── batch-processing.html  Batch workflows
    ├── vector-search.html     Similarity search
    └── quality-control.html   QC metrics
```

## Theme & Styling

**Base Theme:** `/os/medical/styles/isa101-theme.css`
**Frontend Styles:** `/styles/frontend-portal.css`
**Enterprise Styles:** `/styles/index.css` (reusable ISA-95 components)

**Colors:**
- Background: Deep purple (#2a1a3a)
- Text: Cream (#f5f2e8)
- Accents: Purple (#b794f4, #8b5cf6)

## Integration Points

### Medical OS
**Path:** `/os/medical/`
**Link:** AI algorithms, DICOM workflows, preprocessing
**Usage:** Frontend screens call medical OS APIs

### Examples
**Path:** `/examples/`
**Link:** Sample datasets for testing tools
**Usage:** Load example X-rays, CT, MRI into viewers

### Standards
**Path:** `/standards/isa101/`
**Link:** HMI design patterns, alarm management
**Usage:** Enterprise screens follow ISA-101 guidelines

## Navigation Flow

```
User Visits Root (/)
  │
  ├─→ Auto-redirect to /screens/frontend/index.html
  │    │
  │    ├─→ Select imaging tool (CT viewer, MRI, AI segmentation)
  │    │    └─→ Use tool with sample data from /examples/
  │    │
  │    └─→ Access Enterprise Portal (bottom link)
  │         └─→ Navigate L4 → L3 → L2 → L1 hierarchy
  │
  └─→ Direct access: /screens/Enterprise/enterprise-portal.html
```

## Screen Development Guidelines

1. **Keep HTML under 250 tokens**
   - Extract CSS to `/styles/`
   - Extract JS to `/scripts/`
   - Use external references

2. **Follow ISA-101 for Enterprise screens**
   - High contrast (cream on purple)
   - Clear alarm states (green/yellow/red)
   - Minimal chartjunk

3. **Modular design for Frontend**
   - Break into sub-screens
   - Reusable components
   - Clear user workflows

4. **Accessibility**
   - ARIA labels
   - Keyboard navigation
   - Screen reader support

5. **Responsive design**
   - Mobile-friendly layouts
   - Touch-friendly controls
   - Adaptive grid systems

## Testing

```bash
# Test frontend screens
python -m http.server 8000
# Open: http://localhost:8000/screens/frontend/

# Test Enterprise screens
# Open: http://localhost:8000/screens/Enterprise/enterprise-portal.html

# Load sample data
python examples/download-samples.py --all
```

## Future Enhancements

- **L0 Physical Devices:** Direct device interfaces when connected to imaging equipment
- **Real-time Monitoring:** WebSocket connections for live DICOM feeds
- **Multi-user Collaboration:** Shared annotation and consultation tools
- **Mobile Apps:** Native iOS/Android versions of frontend portal
- **Offline Mode:** PWA capabilities for field use

See individual subdirectory `structure.md` files for detailed component documentation.
