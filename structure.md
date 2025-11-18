# CHAZON Medical Imaging SCADA - Project Structure

## Overview

ISA-95 Level 4 Medical Imaging Virtual Factory with AI/ML capabilities for diagnostic image analysis.

## Architecture

```
/
├── index.html                      Root auto-redirect to frontend
├── screens/                        User interfaces (hierarchical)
│   ├── frontend/                   User-facing medical imaging portal
│   └── Enterprise/                 ISA-95 hierarchical backend (L4→L3→L2→L1→L0)
├── os/                            Medical Operating System
│   └── medical/                    DICOM workflows, AI/ML algorithms
├── standards/                      Standards-as-Tags Framework
│   ├── packml/                     PackML state machine
│   ├── isa88/                      Batch control
│   ├── isa95/                      Enterprise integration
│   └── isa101/                     High-performance HMI
├── examples/                       Open-source medical imaging datasets
│   ├── xray/                       X-ray samples
│   ├── ct/                         CT scan samples
│   ├── mri/                        MRI samples
│   └── dicom/                      DICOM files
├── templates/                      JSON templating system
├── docs/                          Documentation
├── tests/                         Test infrastructure
├── cli/                           Maintenance tools
├── styles/                        Shared CSS configurations
└── scripts/                       Shared JavaScript modules
```

## ISA-95 Levels (Purdue Model)

**L4 - Business Planning & Logistics**
- Enterprise resource planning
- Production scheduling
- Quality management
- Asset tracking

**L3 - Manufacturing Execution System (MES)**
- Workflow orchestration
- Batch management
- Recipe execution
- Performance monitoring

**L2 - Supervisory Control**
- SCADA systems
- HMI interfaces
- Alarm management
- Trend analysis

**L1 - Basic Control**
- PLC programming
- Device control
- Real-time automation
- Safety systems

**L0 - Physical Processes**
- Sensors and actuators
- Medical imaging devices
- Physical equipment
- Field instrumentation

## Key Components

### Medical Imaging AI/ML
- **Segmentation:** U-Net, Mask R-CNN, DeepLab v3+
- **Classification:** ResNet-50, DenseNet, BiomedCLIP (768-dim)
- **Detection:** YOLOv8, Faster R-CNN, RetinaNet
- **AlF-DETECT:** Alzheimer's/Autism screening via dual-energy X-ray

### Data Formats
- **DICOM** - Primary medical imaging format
- **NIfTI** - Neuroimaging format
- **JPEG/PNG** - Converted images
- **HDF5** - Processed datasets

### Vector Database
- **Qdrant** - 768-dimensional BiomedCLIP embeddings
- Similarity search for medical images
- Collections per imaging modality

## Standards Compliance

- **ISA-95** - Enterprise-control system integration
- **ISA-88** - Batch control
- **ISA-101** - High-performance HMI design
- **PackML** - Packaging machinery state machine
- **HIPAA** - Healthcare privacy
- **FDA 21 CFR Part 11** - Electronic records

## Theme

**ISA-101 Cream & Purple**
- Background: Deep purple (#2a1a3a, #1a0f26)
- Text: Cream (#f5f2e8)
- Accents: Purple (#b794f4, #8b5cf6)
- Normal: Green (#90ee90)
- Warning: Yellow (#ffd700)
- Alarm: Red (#ff6b6b)

## File Size Policy

**HTML files:** <250 tokens (~30-130 lines)
**Config files:** CSS/JS extracted to `/styles/` and `/scripts/`
**Modularity:** Separation of structure, style, behavior

## Navigation

**Frontend Entry:** `/screens/frontend/index.html` (auto-redirect from root)
**Enterprise Portal:** `/screens/Enterprise/enterprise-portal.html`
**Documentation:** `/docs/`
**Examples:** `/examples/README.md`

## Tags & Metadata

Each directory contains `index/tag.json` with:
- UUID (unique identifier)
- ISA_Level (L0-L4)
- Title, Description, Icon
- Child_Directories, Features, Quick_Actions
- Breadcrumb navigation data

## Development Workflow

```bash
# Run tests
pytest tests/

# Validate tags
python cli/validate-tags.py

# Download sample datasets
python examples/download-samples.py --all

# Start local server
python -m http.server 8000
# Open: http://localhost:8000
```

## Directory Documentation

Each major directory contains `structure.md` explaining:
- Purpose and scope
- Subdirectory organization
- Key files and their roles
- Integration points
- Usage examples

See individual `structure.md` files for detailed subsystem documentation.
