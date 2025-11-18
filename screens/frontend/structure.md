# Frontend Medical Imaging Portal

## Purpose

User-facing interface for clinicians, radiologists, and researchers to access AI-powered medical imaging analysis tools.

## Architecture

```
/screens/frontend/
├── index.html              Main portal dashboard
├── structure.md            This file
├── viewers/                Image viewing interfaces
│   ├── ct-viewer.html     CT scan viewer
│   ├── mri-viewer.html    MRI viewer
│   └── xray-viewer.html   X-ray viewer
├── ai-tools/               AI/ML analysis tools
│   ├── segmentation.html  U-Net, Mask R-CNN, DeepLab
│   ├── detection.html     YOLOv8, Faster R-CNN
│   └── alf-detect.html    Alzheimer's/Autism screening
└── utilities/              Support tools
    ├── batch.html         Batch processing
    ├── search.html        Vector similarity search
    └── qc.html            Quality control metrics
```

## Main Portal (index.html)

**Purpose:** Central dashboard for tool selection
**Size:** 110 lines (~130 tokens) ✓
**Features:**
- Welcome banner with quick stats
- 8 tool cards with icons and descriptions
- Link to Enterprise portal (bottom)
- HIPAA/FDA compliance badges

**Styling:**
- ISA-101 theme: `/os/medical/styles/isa101-theme.css`
- Portal-specific: `/styles/frontend-portal.css`

## Tool Categories

### 1. Image Viewers
**Location:** `/os/medical/screens/`
**Linked from:** Main portal tool grid

**CT Viewer** (`ct-viewer.html`)
- Window/level controls
- Slice navigation
- Multi-planar reconstruction
- Measurement tools

**MRI Viewer** (`mri-viewer.html`)
- Sequence selection (T1, T2, FLAIR, DWI)
- Multi-echo display
- Signal intensity analysis
- ROI measurement

**X-Ray Viewer** (planned)
- Single image display
- Zoom/pan controls
- Annotation tools
- DICOM metadata viewer

### 2. AI Analysis Tools
**Location:** `/os/medical/screens/`
**Algorithms:** `/os/medical/ai/*.js`

**Segmentation Tool** (`segmentation-tool.html`)
- Model selection: U-Net, Mask R-CNN, DeepLab v3+
- Organ type: liver, kidney, lungs, heart, brain
- Mask overlay visualization
- Confidence scores

**Detection Tool** (`detection-tool.html`)
- Model selection: YOLOv8, Faster R-CNN, RetinaNet
- Detection targets: nodules, lesions, tumors
- Bounding box display
- Classification labels

**AlF-DETECT Screening** (`alf-screening.html`)
- Dual-energy X-ray analysis
- Aluminum concentration mapping
- Risk assessment (Alzheimer's/Autism)
- Treatment recommendations

### 3. Utility Tools
**Location:** `/os/medical/screens/`

**Vector Search** (`vector-search.html`)
- BiomedCLIP embedding generation
- Qdrant similarity search
- Similar case retrieval
- 768-dimensional vectors

**Batch Processing** (`batch-processing.html`)
- Multi-image upload
- Automated pipeline execution
- Progress tracking
- Results export

**Quality Control** (`quality-control.html`)
- SNR calculation
- Contrast metrics
- Artifact detection
- DICOM validation

## User Workflows

### Workflow 1: Single Image Analysis
1. Land on main portal
2. Select CT/MRI/X-ray viewer
3. Upload or select sample image
4. Adjust viewing parameters
5. Run AI segmentation/detection
6. Review results and export

### Workflow 2: AI Screening
1. Select AlF-DETECT tool
2. Upload dual-energy X-ray
3. System analyzes aluminum concentration
4. View risk assessment
5. Download report for physician

### Workflow 3: Similar Case Search
1. Select Vector Search tool
2. Upload reference image
3. System generates embedding
4. Search Qdrant database
5. Review similar cases
6. Compare diagnoses

### Workflow 4: Batch Analysis
1. Select Batch Processing tool
2. Upload multiple DICOM files
3. Configure pipeline (preprocessing + AI)
4. Monitor progress
5. Download results package

## Data Sources

### Sample Data
**Location:** `/examples/`
**Types:** X-ray, CT, MRI, DICOM
**Datasets:** MIMIC-CXR, NIH, TCIA, OASIS, ADNI

**Usage:**
```javascript
// Load sample CT scan
const sampleCT = '/examples/ct/lung_sample.dcm';
loadDICOM(sampleCT);
```

### User Uploads
**Format:** DICOM (.dcm), NIfTI (.nii, .nii.gz), JPEG, PNG
**Size Limit:** 50MB per file
**Validation:** DICOM tag verification, format checking

## Styling & Theme

### Colors (ISA-101 Compliant)
```css
--bg-primary: #2a1a3a;        /* Deep purple */
--bg-secondary: #3d2a52;      /* Medium purple */
--cream: #f5f2e8;             /* Cream text */
--purple-accent: #b794f4;     /* Light purple */
--purple-glow: #8b5cf6;       /* Bright purple */
--normal: #90ee90;            /* Green (normal state) */
--warning: #ffd700;           /* Yellow (warning) */
--alarm: #ff6b6b;             /* Red (alarm) */
```

### Typography
- **Font:** -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- **Headers:** 2.5em, cream, purple glow shadow
- **Body:** 1em, cream
- **Descriptions:** 0.9-1.1em, muted cream (#d4cdb4)

### Layout
- **Container:** Max-width 1200px, centered
- **Grid:** Auto-fit, min 300px columns
- **Cards:** Purple border, hover elevation
- **Spacing:** 20-40px gaps

## Integration Points

### Medical OS API
**Base:** `/os/medical/`

```javascript
// Segmentation
import { MedicalSegmentation } from '/os/medical/ai/segmentation.js';
const seg = new MedicalSegmentation();
const mask = await seg.unetSegment(imageData, 'liver');

// Classification
import { MedicalClassification } from '/os/medical/ai/classification.js';
const clf = new MedicalClassification();
const embedding = await clf.biomedclipEmbed(imageData);

// Detection
import { MedicalDetection } from '/os/medical/ai/detection.js';
const det = new MedicalDetection();
const boxes = await det.yolov8Detect(imageData, 'nodule');
```

### Qdrant Vector Database
**Endpoint:** http://localhost:6333
**Collection:** `medical_images`
**Dimensions:** 768 (BiomedCLIP)

```javascript
// Search similar images
const results = await vectorSearch.search(embedding, topK=10);
```

### Enterprise Portal Link
**URL:** `/screens/Enterprise/enterprise-portal.html`
**Access:** Footer link on main portal
**Purpose:** Backend operations, analytics, configuration

## Compliance & Security

### HIPAA Compliance
- De-identified data only
- No PHI displayed or stored
- Audit logging (future)
- Encrypted transmission (HTTPS)

### FDA 21 CFR Part 11
- Electronic signatures (future)
- Audit trails
- System validation
- Access controls

### Data Retention
- Session-based only
- No server-side storage
- User responsible for downloads
- Clear cache on exit

## Development

### Adding New Tools

1. **Create HTML file** (<250 tokens)
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <link rel="stylesheet" href="../../os/medical/styles/isa101-theme.css">
     <link rel="stylesheet" href="../../styles/frontend-portal.css">
   </head>
   <body>
     <!-- Tool interface -->
   </body>
   </html>
   ```

2. **Add to main portal** (`index.html`)
   ```html
   <a href="../../os/medical/screens/new-tool.html" class="tool-card">
     <div class="tool-icon">🔬</div>
     <div class="tool-title">New Tool</div>
     <div class="tool-description">Description here</div>
   </a>
   ```

3. **Test with sample data**
   ```bash
   python examples/download-samples.py --all
   # Open: http://localhost:8000/screens/frontend/
   ```

### File Size Compliance
- **Keep HTML <250 tokens**
- **Extract CSS to `/styles/`**
- **Extract JS to `/scripts/` or `/os/medical/ai/`**
- **Use external references**

## Testing

```bash
# Start local server
python -m http.server 8000

# Open portal
# http://localhost:8000/screens/frontend/

# Download samples
python examples/download-samples.py --xray --ct --mri

# Run tests
pytest tests/test_frontend.py
```

## Future Enhancements

- **Real-time Collaboration:** Multi-user annotation
- **Voice Controls:** Hands-free operation in OR
- **Mobile Responsive:** Touch-optimized interfaces
- **Offline Mode:** PWA for field use
- **3D Visualization:** Volume rendering for CT/MRI
- **Report Generation:** Automated diagnostic reports
- **PACS Integration:** Direct connection to hospital systems

See `/os/medical/structure.md` for AI/ML algorithm details.
