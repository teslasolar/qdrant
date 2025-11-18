# Medical Imaging Control Dashboard - SCADA PACS System

## Overview

A comprehensive medical imaging control dashboard designed for the virtual factory SCADA system, combining professional PACS (Picture Archiving and Communication System) functionality with industrial SCADA aesthetics. This system integrates DICOM image processing, AI-powered screening, and vector similarity search using Qdrant.

**PLC Area:** PLC-004 Medical Imaging
**ISA-95 Level:** L2 - Control
**Tags:** 223 tags, 28 routines

## System Components

### Main Applications

1. **Dashboard** (`dashboard.html`) - Central control interface
   - Real-time system status (DICOM, Qdrant, AlF-DETECT)
   - Patient study queue with priority management
   - Modality workstation navigation (CT, MRI, X-Ray, Ultrasound, Mammography)
   - DICOM processing pipeline visualization
   - Quality control metrics and AlF-DETECT results
   - Vector similarity search (Qdrant integration)

2. **DICOM Workflow** (`dicom-workflow.html`) - Pipeline monitoring
   - Live stage counters (Receive → Analysis → AI → Storage → Complete)
   - Performance metrics and active tasks
   - AI model statistics and activity timeline

3. **Patient Study Manager** (`patient-study-manager.html`) - Study management
   - Advanced search and filtering
   - Multiple view modes (grid/list)
   - New study creation with AlF-DETECT option
   - Export functionality

4. **AlF-DETECT** (`alf-detect.html`) - AI screening system
   - Dual-energy X-ray subtraction
   - Alzheimer's/Autism probability analysis
   - Brain region AlF concentration mapping
   - Qdrant similarity search

### Template Library

**Screen Templates** (`/templates/screens/medical/`)
- PACS Dashboard
- CT Workstation
- MRI Workstation
- X-Ray Workstation
- AlF-DETECT Screening

**Component Templates** (`/templates/components/medical/`)
- DICOM Viewport
- Patient Info Card
- AlF Probability Display
- Study Queue Panel
- Workflow Diagram
- Qdrant Similarity Panel

## Supported Modalities

- **CT** - Computed Tomography with Hounsfield units, multiple window presets
- **MRI** - Magnetic Resonance Imaging with multi-sequence viewing (T1, T2, FLAIR)
- **X-Ray** - Digital Radiography with auto-contrast and AlF screening
- **Ultrasound** - Real-time imaging with cine mode
- **Mammography** - Dedicated breast imaging with CAD integration

## AI Integration

### BiomedCLIP Embeddings
- Vector dimension: 768
- Average inference: 2.1s
- Total indexed: 1,247+ images

### AlF-DETECT Screening
- Method: Dual-energy X-ray subtraction
- Biomarker: AlF₃/AlF₄⁻ accumulation
- Conditions: Alzheimer's Disease, Autism Spectrum
- Brain regions: Hippocampus, Frontal Cortex, Temporal/Parietal Lobes
- Average analysis: 4.2s

### Qdrant Vector Search
- Search performance: ~0.3s
- Use cases: Similar case finding, diagnostic support

## Performance Metrics

- Image Quality Pass: 98.7%
- Average Processing: 2.4s per study
- System Uptime: 99.1%
- Studies Per Day: ~732
- Average Rate: 45 studies/hour

## Navigation

- **Main Dashboard:** `os/medical/dashboard.html`
- **AlF-DETECT:** `os/medical/alf-detect.html`
- **Workflow Monitor:** `os/medical/dicom-workflow.html`
- **Study Manager:** `os/medical/patient-study-manager.html`
- **DICOM Viewer:** `os/frontend/`
- **HMI Panel:** `os/medical/hmi.html`
- **PLC Logic:** `os/medical/plc.html`
- **Tag Provider:** `os/controls/tag-providers/medical.json`

## Key Tags

- `dicomReady` - DICOM viewer status
- `qdrantConnected` - Vector database connection
- `alfDetectReady` - AlF-DETECT system status
- `imagesProcessed` - Total images processed
- `similaritySearches` - Vector searches performed
- `embedModel` - Current AI model (BiomedCLIP)
- `avgProcessTime` - Average processing time

## Design Theme

**SCADA Industrial Aesthetics:**
- Dark theme (#0a0a0a background)
- Neon accents (green #00ff88, cyan #00ccff, purple #ff88ff)
- Monospace typography
- Glowing borders and pulsing indicators
- Industrial control panel aesthetic

---

**System Version:** 2.1
**Last Updated:** 2025-11-17
