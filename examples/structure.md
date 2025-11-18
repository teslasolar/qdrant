# Medical Imaging Examples & Datasets

## Purpose

Repository of open-source medical imaging datasets for testing, development, and validation of the CHAZON Medical Imaging SCADA system.

## Directory Structure

```
/examples/
├── structure.md               This file
├── README.md                  Comprehensive dataset guide (200+ lines)
├── download-samples.py        Python script for fetching samples
├── .gitignore                 Prevents large file commits
├── index/
│   └── tag.json              ISA-95 L4 metadata
├── xray/                      X-ray images
│   └── .gitkeep
├── ct/                        CT scan volumes
│   └── .gitkeep
├── mri/                       MRI scans
│   └── .gitkeep
├── dicom/                     Raw DICOM files
│   └── .gitkeep
└── datasets/                  Downloaded archives
    └── .gitkeep
```

## Dataset Categories

### X-Ray Datasets (3 major sources)
- **MIMIC-CXR:** 377,110 chest X-rays, 227k studies
- **NIH Chest X-Ray:** 112,000+ images, 14 disease labels
- **CANDID-PTX:** 19,237 pneumothorax segmentations

### CT Scan Datasets (3 major sources)
- **NLST:** 26,254 low-dose lung screening scans
- **LIDC-IDRI:** Lung nodule annotations from radiologists
- **BHSD:** Brain hemorrhage segmentation (192+2,200 volumes)

### MRI Datasets (4 major sources)
- **OASIS:** Brain MRI for aging/neuroscience research
- **ADNI:** Alzheimer's Disease Neuroimaging (MR, PET, biomarkers)
- **BraTS:** Brain tumor segmentation (T1, T1ce, T2, FLAIR)
- **ATLAS R2.0:** Stroke lesion segmentation

### Multi-Modal Datasets (3 major sources)
- **TCIA:** The Cancer Imaging Archive (lung, breast, neuro)
- **UMIE:** 1M+ images from 20 datasets (CT, MRI, X-ray)
- **Stanford AIMI:** Annotated datasets for AI research

## Usage

### Download Samples

```bash
# Download all available samples
python examples/download-samples.py --all

# Download specific modalities
python examples/download-samples.py --xray --mri
python examples/download-samples.py --ct --dicom

# Help
python examples/download-samples.py --help
```

### Use with CHAZON Tools

```bash
# Start server
python -m http.server 8000

# Open frontend portal
# http://localhost:8000/screens/frontend/

# Load example into CT viewer
# Select: /examples/ct/lung_sample.dcm

# Run AI segmentation on example
# Tool: AI Segmentation
# Image: /examples/ct/lung_sample.dcm
# Organ: lungs
```

### Access from JavaScript

```javascript
// Load example X-ray
const xrayPath = '/examples/xray/chest_xray_sample.jpg';
const img = await loadImage(xrayPath);

// Load example DICOM
import { loadDICOM } from '/os/medical/utils/dicom-loader.js';
const dcmData = await loadDICOM('/examples/dicom/sample_dicom.dcm');

// Batch process examples
const examples = [
  '/examples/ct/sample1.dcm',
  '/examples/ct/sample2.dcm',
  '/examples/ct/sample3.dcm'
];
for (const path of examples) {
  const result = await processImage(path);
}
```

## Dataset Details

### MIMIC-CXR (X-Ray)
**Source:** https://physionet.org/content/mimic-cxr/
**Size:** 377,110 images (227,835 studies)
**Format:** DICOM, JPG
**Labels:** Free-text radiology reports
**Use Case:** Disease classification, report generation

### NIH Chest X-Ray
**Source:** https://www.nih.gov/news-events/
**Size:** 112,000+ images (30,000+ patients)
**Format:** PNG
**Labels:** 14 disease categories
**Use Case:** Multi-label classification

### NLST (CT)
**Source:** https://cdas.cancer.gov/nlst/
**Size:** 26,254 low-dose CT scans
**Format:** DICOM
**Labels:** Lung cancer screening results
**Use Case:** Nodule detection, cancer screening

### OASIS (MRI)
**Source:** https://www.oasis-brains.org/
**Size:** 416 subjects (aged 18-96)
**Format:** NIfTI
**Modality:** T1-weighted MRI
**Use Case:** Brain aging, dementia research

### BraTS (MRI)
**Source:** http://braintumorsegmentation.org/
**Size:** 369 cases (training)
**Format:** NIfTI
**Sequences:** T1, T1ce, T2, FLAIR
**Labels:** Glioma segmentation masks
**Use Case:** Tumor segmentation, survival prediction

### TCIA (Multi-Modal)
**Source:** https://www.cancerimagingarchive.net/
**Collections:** 200+ curated datasets
**Modalities:** CT, MR, PET, X-ray, ultrasound
**Format:** DICOM
**Use Case:** Cancer imaging research

## Data Formats

### DICOM (.dcm)
- Industry standard for medical imaging
- Contains image + metadata (patient info, acquisition params)
- Supported by all CHAZON tools
- **Privacy:** Use de-identified datasets only

### NIfTI (.nii, .nii.gz)
- Neuroimaging format
- Common in brain MRI research
- Compressed (.gz) to save space
- Convert to DICOM if needed

### JPEG/PNG
- Converted from DICOM for convenience
- Lose metadata and bit depth
- Suitable for visualization only
- Not recommended for AI training

### HDF5 (.h5)
- Processed datasets with arrays
- Includes preprocessed features
- Fast loading for training
- Custom format per project

## File Size Management

### .gitignore Policy
**Prevent commits of:**
- DICOM files (*.dcm) - typically 100KB-10MB each
- NIfTI files (*.nii, *.nii.gz) - typically 5-50MB each
- Archives (*.zip, *.tar.gz) - can be GBs
- HDF5 datasets (*.h5) - typically 100MB-10GB

**Allow commits of:**
- Documentation (README.md, structure.md)
- Scripts (download-samples.py)
- Config files (.gitignore)
- Directory structure (.gitkeep)

### Storage Recommendations
- **Development:** Keep 10-50 sample files locally (~500MB)
- **Testing:** Download specific datasets as needed
- **Production:** Use network storage or cloud buckets
- **CI/CD:** Use lightweight samples (<1MB) for automated tests

## Compliance & Ethics

### HIPAA Compliance
✓ All listed datasets are de-identified
✓ No Protected Health Information (PHI)
✓ Safe for development and research
✗ Not for clinical use without validation

### Data Use Agreements
⚠ Most datasets require registration
⚠ Non-commercial research use only
⚠ Cite original publications
⚠ Follow dataset-specific terms

### Citations Required
When using datasets, cite appropriately:
- **MIMIC-CXR:** Johnson et al. (2019), Scientific Data
- **NIH:** Wang et al. (2017), CVPR
- **OASIS:** Marcus et al. (2007), J. Cognitive Neuroscience
- **BraTS:** Menze et al. (2015), IEEE TMI

See README.md for complete citation information.

## Integration Points

### Frontend Portal
**Path:** `/screens/frontend/index.html`
**Integration:** Sample data dropdown in viewers
**Usage:** Select example files for testing tools

### Medical OS
**Path:** `/os/medical/`
**Integration:** AI algorithms process examples
**Usage:** Validate segmentation, detection, classification

### Batch Processing
**Path:** `/os/medical/screens/batch-processing.html`
**Integration:** Load entire directories
**Usage:** Process multiple examples simultaneously

### Quality Control
**Path:** `/os/medical/screens/quality-control.html`
**Integration:** Validate example datasets
**Usage:** Check SNR, contrast, artifacts

## Future Enhancements

- **Auto-download:** Script fetches full datasets automatically
- **Preprocessing:** Pre-processed versions (normalized, windowed)
- **Embeddings:** Pre-computed BiomedCLIP embeddings
- **Annotations:** Ground truth labels for evaluation
- **Augmentations:** Synthetic variations for training
- **Metadata DB:** SQLite database of all example metadata
- **Cloud Storage:** S3/GCS bucket integration

## Testing

```bash
# Verify directory structure
ls -R examples/

# Download samples
python examples/download-samples.py --all

# Verify downloads
ls -lh examples/xray/
ls -lh examples/ct/
ls -lh examples/mri/
ls -lh examples/dicom/

# Test with CHAZON
python -m http.server 8000
# Open: http://localhost:8000/screens/frontend/
# Load examples in viewers
```

## Troubleshooting

### Download Fails
- Check internet connection
- Some URLs may be down (datasets move)
- Try direct download from source
- Update download-samples.py with new URLs

### File Not Found
- Verify file exists: `ls examples/xray/`
- Check file permissions
- Re-download samples
- Check .gitignore didn't exclude file

### Large Files
- Don't commit DICOM/NIfTI to git
- Use .gitignore to prevent
- Store locally only
- Use git-lfs for tracking (future)

See `/os/medical/structure.md` for AI algorithm integration details.
See `/screens/frontend/structure.md` for UI integration details.
