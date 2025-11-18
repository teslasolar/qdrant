# Medical Imaging AI/ML/CV Algorithms

AI/CV algorithms for medical imaging organized by ISA-95 architecture levels.

## ISA-95 Level 3 - MES Operations

All AI/ML/CV algorithms operate at Level 3 (Manufacturing Execution Systems), processing medical images in real-time and providing analysis results to operators and higher-level systems.

## Algorithm Modules

### Segmentation (`segmentation.js`)
**Purpose**: Segment anatomical structures and abnormalities

**Models**:
- **U-Net**: Organ segmentation (liver, kidney, brain regions)
- **Mask R-CNN**: Instance segmentation for tumors
- **DeepLab v3+**: Semantic segmentation

**Use Cases**:
- Organ volume measurement
- Tumor boundary delineation
- Multi-organ segmentation

### Classification (`classification.js`)
**Purpose**: Classify medical images and generate embeddings

**Models**:
- **ResNet-50**: General pathology classification
- **DenseNet**: Dense feature extraction
- **EfficientNet**: Efficient classification
- **BiomedCLIP**: Medical image-text embeddings (768-dim)

**Use Cases**:
- Normal vs abnormal classification
- Disease type classification
- Vector embeddings for search

### Detection (`detection.js`)
**Purpose**: Detect and localize abnormalities

**Models**:
- **YOLOv8**: Real-time nodule/lesion detection
- **Faster R-CNN**: Accurate tumor detection
- **RetinaNet**: Small object detection

**Use Cases**:
- Lung nodule detection
- Breast lesion detection
- Multi-class abnormality detection

### Preprocessing (`preprocessing.js`)
**Purpose**: Prepare images for analysis

**Methods**:
- **Window/Level**: HU windowing for CT/MRI
- **CLAHE**: Contrast enhancement
- **Normalize**: Statistical normalization
- **Resize**: Interpolation-based resizing
- **Denoise**: Gaussian/median filtering

**Use Cases**:
- CT windowing (lung: W=1500, L=-600)
- MRI contrast enhancement
- Image quality improvement

### AlF-DETECT (`alf-detect.js`)
**Purpose**: Alzheimer's & Autism screening via dual-energy X-ray

**Methods**:
- **Dual-Energy Subtraction**: Isolate aluminum signal
- **Region Analysis**: Brain region concentration measurement
- **Risk Scoring**: Probability calculation

**Brain Regions**:
- Hippocampus
- Frontal Cortex
- Temporal Lobe
- Cerebellum

**Thresholds**:
- Alzheimer's: >65% probability
- Autism: >60% probability

### Vector Search (`vector-search.js`)
**Purpose**: Qdrant integration for similarity search

**Features**:
- Similar image search by embedding
- Filter by modality (CT, MRI, X-Ray)
- Upload vectors with metadata
- Collection statistics

**Integration**:
- Qdrant URL: `http://localhost:6333`
- Collection: `medical_images`
- Vector dimension: 768 (BiomedCLIP)

## Screen Modules

Modular screens in `/screens/` directory:

- **ct-viewer.html**: CT scan visualization
- **mri-viewer.html**: MRI scan viewer with sequences
- **segmentation-tool.html**: AI segmentation interface
- **detection-tool.html**: Object detection interface
- **alf-screening.html**: AlF-DETECT screening tool
- **vector-search.html**: Similar image search
- **batch-processing.html**: Batch image processing
- **quality-control.html**: Image quality dashboard

## Shared Styles

Modular CSS in `/styles/` directory:

- **isa101-theme.css**: Cream & purple ISA-101 color scheme
- **widgets.css**: Reusable widget components

## Usage Examples

### Segmentation
```javascript
import MedicalSegmentation from './ai/segmentation.js';

const seg = new MedicalSegmentation();
const result = await seg.unetSegment(imageData, 'liver');
console.log('Confidence:', result.confidence);
```

### Classification
```javascript
import MedicalClassification from './ai/classification.js';

const classifier = new MedicalClassification();
const embedding = await classifier.biomedclipEmbed(imageData);
// 768-dimensional vector for Qdrant
```

### Detection
```javascript
import MedicalDetection from './ai/detection.js';

const detector = new MedicalDetection();
const detections = await detector.yoloDetect(imageData);
// Returns bounding boxes and scores
```

### AlF-DETECT Screening
```javascript
import AlfDetect from './ai/alf-detect.js';

const alfDetect = new AlfDetect();
const alzResult = await alfDetect.screenAlzheimers(xrayData);
console.log('Risk:', alzResult.probability);
```

### Vector Search
```javascript
import VectorSearch from './ai/vector-search.js';

const search = new VectorSearch();
const results = await search.searchSimilar(embedding, 5);
// Returns 5 most similar images
```

## File Size Optimization

All modules kept under 250 tokens:
- Separated JS/CSS/HTML
- Modular components
- Shared stylesheets
- Minimal inline code

## Integration with ISA-95

**Level 4 (Business)**:
- Analytics on detection/classification results
- ROI analysis from AI predictions
- Quality metrics aggregation

**Level 3 (MES)**:
- Real-time AI inference
- Workflow orchestration
- Result validation

**Level 2 (SCADA)**:
- Equipment monitoring
- Processing status
- Alert generation

**Level 1 (Control)**:
- Image acquisition triggers
- Scanner parameter control
- Quality checkpoints

## Performance

- **Segmentation**: ~500ms per image
- **Classification**: ~200ms per image
- **Detection**: ~300ms per image
- **Vector Search**: <50ms query latency

## See Also

- [DICOM Workflows](/os/medical/workflows/)
- [Template System](/templates/)
- [Standards Framework](/standards/)
