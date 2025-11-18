# Medical Imaging Screens

Modular, lightweight screens for medical imaging SCADA system.
Each screen is <250 tokens with separated JS/CSS/HTML.

## Screen Catalog

### Imaging Viewers

**ct-viewer.html**
- CT scan slice viewer
- Window/level controls
- Slice navigation
- Patient info display

**mri-viewer.html**
- MRI sequence viewer
- T1/T2/FLAIR/DWI sequences
- Contrast adjustment
- Multi-plane support

### AI Tools

**segmentation-tool.html**
- U-Net, Mask R-CNN, DeepLab selection
- Real-time segmentation
- Confidence scoring
- Overlay visualization

**detection-tool.html**
- YOLOv8, Faster R-CNN, RetinaNet
- Bounding box visualization
- Object classification
- Detection confidence

**alf-screening.html**
- AlF-DETECT screening interface
- Alzheimer's risk calculation
- Autism risk calculation
- Brain region analysis

### Search & Processing

**vector-search.html**
- Similar image search
- Modality filtering
- BiomedCLIP embeddings
- Qdrant integration

**batch-processing.html**
- Multi-image upload
- Pipeline configuration
- Progress tracking
- Batch operations

### Quality & Metrics

**quality-control.html**
- Image quality scoring
- QC checkpoint status
- Pass/fail metrics
- Daily statistics

## Shared Resources

### Stylesheets

**`../styles/isa101-theme.css`**
- Cream & purple color scheme
- ISA-101 compliant design
- Status color coding
- Base layout

**`../styles/widgets.css`**
- Reusable widget styles
- Metric grid layouts
- Progress bars
- Status indicators

### JavaScript Modules

All screens use ES6 modules from `../ai/`:
- `segmentation.js`
- `classification.js`
- `detection.js`
- `preprocessing.js`
- `alf-detect.js`
- `vector-search.js`

## Design Principles

### ISA-101 Compliance
- High contrast (cream on purple)
- Clear visual hierarchy
- Status color coding
- Minimal cognitive load

### Modularity
- Separate concerns (HTML/CSS/JS)
- Shared stylesheets
- Reusable components
- Small file sizes

### Responsiveness
- Mobile-friendly layouts
- Flexible grids
- Adaptive components

## Integration

### With Docking System
```html
<!-- Load screen into center dock -->
<iframe src="/os/medical/screens/ct-viewer.html"></iframe>
```

### With Templates
```javascript
dockingSystem.loadCustomDock(
  'center',
  '/os/medical/screens/segmentation-tool.html',
  'dock-center'
);
```

## File Sizes

All screens optimized for <250 tokens:
- Minimal inline styles
- Shared CSS files
- Modular JS imports
- Clean HTML structure

## Quick Start

1. Open any screen directly in browser
2. Or load via docking system
3. Shared styles auto-load
4. AI modules import on demand

## See Also

- [AI Algorithms](../ai/README.md)
- [Docking System](/templates/docking/README.md)
- [DICOM Workflows](../workflows/)
