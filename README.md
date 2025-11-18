# CHAZON Medical Imaging SCADA

AI-powered medical imaging analysis with industrial automation (ISA-95/88) architecture.

**Built for lablab.ai Hackathon** 🚀 | **Live:** https://teslasolar.github.io/qdrant/ | **License:** MIT

---

## ⚡ Quick Start (lablab.ai Demo)

**Zero setup required** - Works in seconds!

```bash
git clone https://github.com/teslasolar/qdrant && cd qdrant
./start.sh   # Starts demo server on port 8000
```

Then open: **http://localhost:8000/screens/frontend/**

**Demo Features:**
- ✅ Mock AI (no GPU needed)
- ✅ Pre-loaded sample images
- ✅ All tools functional
- ✅ Perfect for presentations

**Switch Environments:** Edit `config.yaml` → change `environment: demo` to `dev` or `prod`

---

## Full Installation

### Client-Side Only (No Installation)
```bash
git clone https://github.com/teslasolar/qdrant && cd qdrant
open index.html  # Opens SCADA gateway
```

### Full Stack (with Backend)
```bash
# 1. Start Qdrant vector database
docker run -p 6333:6333 qdrant/qdrant

# 2. Start backend API
pip install -r os/backend/requirements.txt
python os/backend/api.py

# 3. Open browser
open index.html
```

### Using CLI Tools
```bash
# Boot the OS
./cli/boot.md

# Start all services
./cli/start.md

# Health check
./cli/health.md

# Deploy to GitHub Pages
./cli/deploy.md
```

---

## Navigation

### L4: Business Layer (Root)
| Path | Description |
|------|-------------|
| `/index.html` | Main business gateway |
| `/scada.html` | Master SCADA overview |
| `/plc.html` | Master PLC coordinator |
| `/hmi.html` | Master HMI dashboard |

### L3: MES Layer (/os/)
| Path | Description |
|------|-------------|
| `/os/index.html` | Operating system gateway |
| `/os/backend/` | API services (FastAPI, Qdrant) |
| `/os/frontend/` | Medical imaging viewer (React) |
| `/os/modules/` | 114+ executable modules |
| `/os/boot/` | 6-phase boot system |
| `/os/models/` | AI models (ONNX) |
| `/os/medical/` | DICOM processing, AlF-DETECT |
| `/os/data/` | Databases, architecture |
| `/os/language/` | SNT/trinary compiler |
| `/os/logs/` | System-wide logging |
| `/os/equipment/` | ISA-88 hierarchy definitions |

### L2: Supervisory Layer
| Path | Description |
|------|-------------|
| `/os/controls/` | Tag providers, SCADA controls |
| `/os/{area}/scada.html` | Area SCADA interfaces |
| `/os/{area}/hmi.html` | Area HMI panels |

### L1: Control Layer
| Path | Description |
|------|-------------|
| `/os/{area}/plc.html` | PLC controllers (32 total) |

### L0: Physical Layer
| Path | Description |
|------|-------------|
| `/os/controls/tag-providers/` | Tag definitions (sensors/actuators) |

---

## Architecture

### ISA-95 Functional Hierarchy
```
L4 (Business)      → / (root)          → Documentation, deployment
L3 (MES)           → /os/              → Master SCADA/HMI/PLC coordination
L2 (Supervisory)   → /os/controls/     → Tag providers, area SCADA
L1 (Control)       → /os/{area}/plc/   → 32 PLC controllers
L0 (Physical)      → Tag definitions   → Sensors, actuators, I/O
```

### ISA-88 Equipment Hierarchy
```
Enterprise         → Chazon Medical Imaging SCADA
└── Site           → GitHub Pages Production Site
    └── Areas (8)  → Backend, Frontend, Medical, Models, Data, Modules, Boot, Language
        └── Process Cells (24+)
            └── Units (72+)
                └── Equipment Modules (200+)
                    └── Control Modules (500+)
```

See: `/os/equipment/README.md` for complete hierarchy

### 8 PLC Areas
| Area | Scan Time | Tags | Purpose |
|------|-----------|------|---------|
| Backend | 100ms | 28 | API, Qdrant integration |
| Frontend | 50ms | 47 | UI, DICOM viewer |
| Modules | 75ms | Dynamic | 114+ module execution |
| Boot | Phase | 18 | 6-phase startup |
| Models | Variable | 12/model | AI inference (ONNX) |
| Data | 100ms | 15 | Database operations |
| Medical | 200ms | 25 | DICOM, AlF-DETECT |
| Language | Compile | 10 | SNT/trinary compiler |

---

## Medical Imaging

### Capabilities
- **DICOM Viewer:** X-Ray, CT, MRI support
- **AlF-DETECT:** Alzheimer's & Autism early detection
- **Vector Search:** Qdrant similarity search for similar cases
- **AI Models:** ONNX Runtime with WebGPU acceleration
- **Modalities:** CR (X-Ray), CT, MR, US, MG

### AlF-DETECT
Location: `/os/medical/alf-detect.html`
- Alzheimer's probability detection
- Autism probability detection
- Confidence scoring
- Multi-modal analysis

---

## Technology Stack

### Frontend
- **UI:** HTML5, JavaScript, React
- **AI:** ONNX Runtime, WebGPU
- **Storage:** IndexedDB, LocalStorage
- **Viewer:** DICOM.js-compatible

### Backend
- **API:** FastAPI (Python)
- **Vector DB:** Qdrant
- **Database:** SQLite
- **Embeddings:** OpenAI, CodeBERT, CLIP

### Deployment
- **Static Hosting:** GitHub Pages
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions

### Standards
- **Industrial:** ISA-88, ISA-95, ISA-101, PackML
- **Medical:** DICOM, HL7, IHE, FHIR
- **Regulatory:** 21 CFR Part 11, EU Annex 11, ISO 13485, HIPAA

---

## API Endpoints

```bash
# Health check
GET /api/health

# Vector search
POST /api/search
{
  "query": "chest x-ray pneumonia",
  "top_k": 10
}

# Index embedding
POST /api/index
{
  "text": "Patient presents with...",
  "metadata": {...}
}

# Create collection
POST /api/collections
{
  "name": "medical_cases",
  "vector_size": 1536
}
```

---

## CLI Commands

### System Management
```bash
./cli/boot.md           # Boot the OS
./cli/start.md          # Start all services
./cli/stop.md           # Stop all services
./cli/restart.md        # Restart services
./cli/health.md         # System health check
./cli/logs.md [area]    # View logs
```

### Development
```bash
./cli/dev/setup.md      # Development setup
./cli/dev/test.md       # Run tests
./cli/dev/lint.md       # Lint code
./cli/dev/build.md      # Build assets
```

### Deployment
```bash
./cli/deploy.md         # Deploy to GitHub Pages
./cli/backup.md         # Backup databases
./cli/restore.md        # Restore from backup
```

### Models
```bash
./cli/models/download.md    # Download AI models
./cli/models/list.md        # List available models
./cli/models/validate.md    # Validate models
```

---

## Environment Variables

Create `.env` file (see `.env.example`):
```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
COHERE_API_KEY=...

# Qdrant
QDRANT_URL=https://xyz.qdrant.io
QDRANT_API_KEY=...

# Application
DEBUG=false
LOG_LEVEL=INFO
PORT=8000
```

---

## Directory Structure

```
qdrant/
├── index.html              # L4: Business gateway
├── scada.html              # L4: Master SCADA
├── plc.html                # L4: Master PLC
├── hmi.html                # L4: Master HMI
├── cli/                    # CLI tools for OS management
│   ├── boot.md
│   ├── start.md
│   ├── health.md
│   └── ...
├── docs/                   # Documentation
│   ├── standards/          # ISA-88, ISA-95, ISA-101
│   └── ISA-95-COMPLETE-HIERARCHY.md
├── collab/                 # Multi-agent workspace
└── os/                     # L3: Operating System (MES layer)
    ├── index.html          # OS gateway
    ├── backend/            # API services
    ├── frontend/           # Medical viewer
    ├── modules/            # 114+ modules
    ├── boot/               # Boot system
    ├── models/             # AI models
    ├── medical/            # DICOM, AlF-DETECT
    ├── data/               # Databases
    ├── language/           # Compiler
    ├── logs/               # System logs
    ├── controls/           # L2: Tag providers, SCADA
    ├── equipment/          # ISA-88 hierarchy
    └── templates/          # Template engine
```

---

## Documentation

### Quick Reference
- **Architecture:** `/docs/ISA-95-COMPLETE-HIERARCHY.md`
- **Equipment:** `/os/equipment/README.md`
- **Standards:** `/docs/standards/`
- **About:** `/ABOUT.md`

### Key Documents
| Document | Description |
|----------|-------------|
| `docs/ISA-95-COMPLETE-HIERARCHY.md` | Complete ISA-95 L4→L0 mapping |
| `os/equipment/README.md` | ISA-88 equipment hierarchy |
| `docs/standards/isa/isa-95/README.md` | ISA-95 standard details |
| `docs/standards/isa/isa-88/README.md` | ISA-88 batch control |
| `os/modules/REGISTRY.md` | Module registry |
| `MANIFEST.md` | Complete project manifest |

---

## Development

### Run Locally
```bash
# Development server
python3 -m http.server 8080
open http://localhost:8080

# Or use live-server
npx live-server --port=8080
```

### Run Backend
```bash
cd os/backend
pip install -r requirements.txt
python api.py
# Runs on http://localhost:8000
```

### Run Tests
```bash
./cli/dev/test.md
# Or manually:
cd os/test-modules
pytest
```

---

## Key Features

### Medical Imaging
- ✅ DICOM compliance
- ✅ Multi-modality support (X-Ray, CT, MRI)
- ✅ AlF-DETECT AI analysis
- ✅ Vector similarity search
- ✅ Client-side WebGPU inference

### Industrial Automation
- ✅ ISA-95 5-level hierarchy
- ✅ ISA-88 equipment hierarchy
- ✅ 32 PLC controllers
- ✅ PackML state machines
- ✅ Real-time SCADA monitoring
- ✅ Tag provider system

### Development
- ✅ Markdown-first architecture (114+ modules)
- ✅ Hot module reloading
- ✅ Comprehensive logging
- ✅ Full test coverage
- ✅ Docker containerization

---

## Support & Contributing

### Issues
Report bugs: https://github.com/teslasolar/qdrant/issues

### Contributing
See `docs/guides/CONTRIBUTING.md`

### License
MIT License - See `LICENSE` file

---

## Learn More

- **Vision & Features:** `ABOUT.md`
- **Change History:** `CHANGELOG.md`
- **Architecture Docs:** `docs/`
- **Quick Start Guide:** `docs/guides/QUICKSTART.md`
