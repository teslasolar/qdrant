# Medical Operating System - Core Imaging & AI

## Purpose

Core medical imaging processing system with AI/ML algorithms, DICOM workflows, and multi-modal analysis capabilities.

## Directory Structure

```
/os/medical/
├── structure.md                This file
├── ai/                         AI/ML algorithm modules
│   ├── segmentation.js        U-Net, Mask R-CNN, DeepLab v3+
│   ├── classification.js      ResNet-50, DenseNet, BiomedCLIP
│   ├── detection.js           YOLOv8, Faster R-CNN, RetinaNet
│   ├── preprocessing.js       CLAHE, normalization, windowing
│   ├── alf-detect.js          Alzheimer's/Autism screening
│   └── vector-search.js       Qdrant integration (768-dim)
├── screens/                    Medical imaging UI components
│   ├── ct-viewer.html         CT scan interface
│   ├── mri-viewer.html        MRI viewer
│   ├── segmentation-tool.html AI segmentation interface
│   ├── detection-tool.html    Object detection interface
│   ├── alf-screening.html     AlF-DETECT dashboard
│   ├── vector-search.html     Similarity search
│   ├── batch-processing.html  Batch pipeline
│   ├── quality-control.html   QC metrics
│   └── README.md              Screen documentation
└── styles/                     Medical imaging styles
    ├── isa101-theme.css       ISA-101 base theme
    └── widgets.css            Reusable UI components
```

## AI/ML Algorithms

### Segmentation (`ai/segmentation.js`)
**Purpose:** Medical image segmentation for organs and tumors
**Models:**
- **U-Net:** Fast, accurate organ segmentation
- **Mask R-CNN:** Instance segmentation with bounding boxes
- **DeepLab v3+:** High-resolution semantic segmentation

**Supported Organs:**
- Liver, kidney, lungs, heart, brain, pancreas, spleen, prostate

**Usage:**
```javascript
import { MedicalSegmentation } from '/os/medical/ai/segmentation.js';
const seg = new MedicalSegmentation();

// U-Net segmentation
const result = await seg.unetSegment(imageData, 'liver');
// Returns: { mask, confidence, organType, timestamp }

// Mask R-CNN instance segmentation
const instances = await seg.maskRCNN(imageData, 'tumor');
// Returns: [{ mask, bbox, score, class }]
```

### Classification (`ai/classification.js`)
**Purpose:** Image classification and embedding generation
**Models:**
- **ResNet-50:** General image classification (ImageNet)
- **DenseNet:** Dense connections for medical imaging
- **EfficientNet:** Efficient scaling for mobile deployment
- **BiomedCLIP:** 768-dim multimodal embeddings (biomedical)

**Usage:**
```javascript
import { MedicalClassification } from '/os/medical/ai/classification.js';
const clf = new MedicalClassification();

// Generate BiomedCLIP embedding
const embedding = await clf.biomedclipEmbed(imageData, textPrompt);
// Returns: { embedding: Array(768), dimension: 768, model: 'BiomedCLIP' }

// Classify with ResNet-50
const prediction = await clf.resnet50(imageData);
// Returns: { class, probability, top5 }
```

### Detection (`ai/detection.js`)
**Purpose:** Object detection for nodules, lesions, tumors
**Models:**
- **YOLOv8:** Real-time detection with high accuracy
- **Faster R-CNN:** Two-stage detection for precision
- **RetinaNet:** Focal loss for handling class imbalance

**Detection Targets:**
- Lung nodules, liver lesions, brain tumors, bone fractures

**Usage:**
```javascript
import { MedicalDetection } from '/os/medical/ai/detection.js';
const det = new MedicalDetection();

// YOLOv8 detection
const detections = await det.yolov8Detect(imageData, 'nodule');
// Returns: [{ bbox, confidence, class, objectId }]

// Faster R-CNN with higher precision
const detections = await det.fasterRCNN(imageData, 'tumor');
```

### Preprocessing (`ai/preprocessing.js`)
**Purpose:** Image preprocessing and enhancement
**Techniques:**
- **Window/Level:** CT/MRI contrast adjustment
- **CLAHE:** Contrast Limited Adaptive Histogram Equalization
- **Normalization:** Intensity standardization
- **Denoising:** Noise reduction filters
- **Resampling:** Spatial resolution adjustment

**Usage:**
```javascript
import { MedicalPreprocessing } from '/os/medical/ai/preprocessing.js';
const preprocess = new MedicalPreprocessing();

// CT windowing
const windowed = preprocess.windowLevel(imageData, window=400, level=40);

// CLAHE enhancement
const enhanced = preprocess.clahe(imageData, clipLimit=2.0, tileSize=8);

// Normalization
const normalized = preprocess.normalize(imageData, method='z-score');
```

### AlF-DETECT (`ai/alf-detect.js`)
**Purpose:** Alzheimer's & Autism screening via aluminum detection
**Method:** Dual-energy X-ray analysis of brain aluminum concentration
**Regions:** Hippocampus, cortex, cerebellum, white matter

**Usage:**
```javascript
import { AlfDetect } from '/os/medical/ai/alf-detect.js';
const alf = new AlfDetect();

// Alzheimer's screening
const alzResult = await alf.screenAlzheimers(xrayData);
// Returns: { probability, risk, concentrations, recommendation }

// Autism screening
const autismResult = await alf.screenAutism(xrayData);
// Returns: { probability, risk, concentrations, recommendation }
```

### Vector Search (`ai/vector-search.js`)
**Purpose:** Qdrant integration for similarity search
**Embeddings:** BiomedCLIP 768-dimensional vectors
**Operations:** Index, search, update, delete

**Usage:**
```javascript
import { VectorSearch } from '/os/medical/ai/vector-search.js';
const vs = new VectorSearch('http://localhost:6333');

// Index image
await vs.indexImage(imageId, embedding, metadata);

// Search similar
const results = await vs.search(queryEmbedding, topK=10);
// Returns: [{ id, score, metadata }]
```

## Medical Imaging Screens

### Viewers
**Location:** `/os/medical/screens/`
**Size:** <250 tokens each
**Style:** ISA-101 theme (cream & purple)

**CT Viewer** (`ct-viewer.html`)
- Slice navigation (axial, sagittal, coronal)
- Window/level presets (lung, bone, soft tissue, brain)
- Zoom, pan, measure
- DICOM metadata display

**MRI Viewer** (`mri-viewer.html`)
- Sequence selection (T1, T2, FLAIR, DWI, T1CE)
- Signal intensity measurement
- ROI drawing
- Multi-planar views

### AI Tools
**Segmentation Tool** (`segmentation-tool.html`)
- Model selector dropdown
- Organ type selector
- Upload/load image
- Mask overlay with opacity control
- Export segmentation

**Detection Tool** (`detection-tool.html`)
- Model selector (YOLOv8/Faster R-CNN/RetinaNet)
- Target selector (nodule/lesion/tumor)
- Bounding box visualization
- Confidence threshold slider
- Results table

**AlF-DETECT** (`alf-screening.html`)
- Dual-energy X-ray upload
- Brain region visualization
- Aluminum concentration heatmap
- Risk assessment dashboard
- Treatment recommendations

### Utilities
**Vector Search** (`vector-search.html`)
- Reference image upload
- Embedding generation display
- Similar case results (grid view)
- Metadata comparison
- Export results

**Batch Processing** (`batch-processing.html`)
- Multi-file upload (drag & drop)
- Pipeline configuration (preprocess + AI)
- Progress bar per file
- Batch results table
- Download results (ZIP)

**Quality Control** (`quality-control.html`)
- SNR calculator
- Contrast metrics (Weber, Michelson)
- Artifact detection
- DICOM validation
- Pass/fail indicators

## Data Formats

### Input Formats
- **DICOM** (.dcm) - Primary medical imaging
- **NIfTI** (.nii, .nii.gz) - Neuroimaging
- **JPEG/PNG** - Converted images
- **HDF5** (.h5) - Processed datasets

### Processing Pipeline
```
Raw DICOM/NIfTI
  ↓
Preprocessing (windowing, CLAHE, normalization)
  ↓
AI Analysis (segmentation/detection/classification)
  ↓
Postprocessing (smoothing, refinement)
  ↓
Visualization & Export
```

## Styling

### ISA-101 Theme (`styles/isa101-theme.css`)
**Colors:**
```css
--bg-primary: #2a1a3a;
--bg-secondary: #3d2a52;
--cream: #f5f2e8;
--purple-accent: #b794f4;
--purple-glow: #8b5cf6;
--normal: #90ee90;
--warning: #ffd700;
--alarm: #ff6b6b;
```

**Applies to:** All medical screens
**Size:** 95 lines
**Reusable:** Shared across entire system

### Widgets (`styles/widgets.css`)
Reusable UI components:
- Progress bars
- Toggle switches
- Sliders
- Dropdown menus
- Modal dialogs
- Toast notifications

## Integration Points

### Frontend Portal
**Path:** `/screens/frontend/index.html`
**Integration:** Links to medical screens
**Usage:** Tool selection dashboard

### Examples
**Path:** `/examples/`
**Integration:** Sample data loading
**Usage:** Test medical screens with real datasets

### Qdrant Vector DB
**Endpoint:** http://localhost:6333
**Collections:** `medical_images_xray`, `medical_images_ct`, `medical_images_mri`
**Dimensions:** 768 (BiomedCLIP)

## Performance

### Model Inference Times (CPU)
- **U-Net:** ~500ms per slice
- **Mask R-CNN:** ~2s per image
- **YOLOv8:** ~100ms per image
- **BiomedCLIP:** ~300ms per embedding

### Optimization
- WebGL acceleration (future)
- WebAssembly for preprocessing
- Model quantization (INT8)
- Batching for throughput

## Testing

```bash
# Unit tests
pytest tests/test_medical_ai.py

# Integration tests
pytest tests/test_medical_screens.py

# Load sample data
python examples/download-samples.py --all

# Test screens
python -m http.server 8000
# Open: http://localhost:8000/os/medical/screens/ct-viewer.html
```

## Compliance

### FDA 21 CFR Part 11
- Audit trails (future)
- Electronic signatures (future)
- System validation

### HIPAA
- De-identified data only
- No PHI storage
- Encrypted transmission

### ISO 13485
- Medical device quality management
- Risk management (ISO 14971)
- Clinical evaluation

## Future Enhancements

- **GPU Acceleration:** TensorFlow.js GPU backend
- **Real-time Inference:** WebRTC streaming from devices
- **Federated Learning:** Privacy-preserving model training
- **PACS Integration:** Direct connection to hospital systems
- **3D Visualization:** Volume rendering with VTK.js
- **Workflow Automation:** BPMN-based clinical workflows

See `/screens/frontend/structure.md` for UI integration details.
