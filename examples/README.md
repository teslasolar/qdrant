# Medical Imaging Examples & Datasets

This directory contains example medical imaging data and links to open-source datasets for testing the CHAZON Medical Imaging SCADA system.

## Directory Structure

```
/examples/
├── xray/       - X-ray images (JPEG, PNG, DICOM)
├── ct/         - CT scan volumes and slices
├── mri/        - MRI scans (T1, T2, FLAIR, DWI)
├── dicom/      - Raw DICOM files for various modalities
└── datasets/   - Downloaded dataset archives
```

## Open Source Medical Imaging Datasets

### 🏥 Multi-Modal Datasets

**UMIE Dataset** (1M+ images)
- **Content:** CT, MRI, and X-ray images from 20+ open-source datasets
- **Use:** Classification and segmentation
- **Link:** https://medium.com/thelion-ai/umie-datasets-83c04305b069

**The Cancer Imaging Archive (TCIA)**
- **Content:** Lung, Breast, Neuro, CT Colonoscopy, PET/CT scans
- **Format:** DICOM primary format
- **Link:** https://www.cancerimagingarchive.net/
- **Collections:** LIDC-IDRI (Lung), Breast MR, Lung PET/CT, Neuro MRI

**Stanford AIMI Shared Datasets**
- **Content:** Annotated medical imaging for AI research
- **Use:** Non-commercial research
- **Link:** https://aimi.stanford.edu/shared-datasets

### 📷 X-Ray Datasets

**MIMIC-CXR** (377,110 images)
- **Content:** 227,835 chest X-ray radiographic studies
- **Format:** JPG and DICOM
- **Features:** Structured labels from free-text reports
- **Link:** https://physionet.org/content/mimic-cxr/

**NIH Chest X-Ray Dataset** (112,000+ images)
- **Content:** 30,000+ unique patients
- **Annotations:** 14 disease labels
- **Link:** https://www.nih.gov/news-events/news-releases/nih-clinical-center-provides-one-largest-publicly-available-chest-x-ray-datasets-scientific-community

**CANDID-PTX** (19,237 images)
- **Content:** Chest X-ray DICOM images
- **Annotations:** Pneumothorax, rib fractures, chest tubes (segmentation)
- **Link:** https://physionet.org/content/candid-ptx/

### 🧠 CT Scan Datasets

**NLST - National Lung Screening Trial** (26,254 scans)
- **Content:** Low-dose CT scans for lung cancer screening
- **Link:** https://cdas.cancer.gov/nlst/

**Brain Hemorrhage Segmentation Dataset (BHSD)**
- **Content:** 192 volumes (pixel-level) + 2,200 volumes (slice-level)
- **Annotations:** Hemorrhage segmentation masks
- **Link:** Available through medical imaging repositories

**Lung Image Database Consortium (LIDC-IDRI)**
- **Content:** Thoracic CT scans with lung nodule annotations
- **Annotations:** Expert radiologist markings
- **Link:** https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI

### 🧠 MRI Datasets

**ATLAS R2.0** (Stroke MRI)
- **Content:** T1w MRIs with lesion segmentation masks
- **Population:** Stroke patients
- **Link:** https://fcon_1000.projects.nitrc.org/indi/retro/atlas.html

**OASIS - Open Access Series of Imaging Studies**
- **Content:** Brain MRI datasets
- **Use:** Neuroscience and aging research
- **Link:** https://www.oasis-brains.org/

**ADNI - Alzheimer's Disease Neuroimaging Initiative**
- **Content:** MR and PET images, genetics, cognitive tests
- **Biomarkers:** CSF and blood biomarkers
- **Link:** https://adni.loni.usc.edu/

**BraTS - Brain Tumor Segmentation**
- **Content:** Multi-institutional pre-operative MRI scans
- **Modalities:** T1, T1ce, T2, FLAIR
- **Annotations:** Glioma segmentation
- **Link:** http://braintumorsegmentation.org/

## Recommended Datasets by Use Case

### For AlF-DETECT Screening (Alzheimer's/Autism)
- **ADNI** - Alzheimer's imaging + biomarkers
- **OASIS** - Brain MRI for aging studies
- **ABIDE** - Autism Brain Imaging Data Exchange

### For Tumor Detection
- **BraTS** - Brain tumor segmentation (MRI)
- **LIDC-IDRI** - Lung nodule detection (CT)
- **TCIA Collections** - Various cancer types

### For General Medical Imaging AI
- **MIMIC-CXR** - Large-scale chest X-rays with reports
- **NIH Chest X-Ray** - Multi-label disease classification
- **UMIE** - Multi-modal mega-dataset

### For Segmentation Tasks
- **BHSD** - Brain hemorrhage segmentation
- **CANDID-PTX** - Pneumothorax segmentation
- **ATLAS R2.0** - Stroke lesion segmentation

## Data Format Support

The CHAZON system supports:
- **DICOM** (.dcm) - Primary medical imaging format
- **NIfTI** (.nii, .nii.gz) - Neuroimaging format
- **JPEG/PNG** - Converted medical images
- **HDF5** (.h5) - Processed imaging datasets

## Download Instructions

### Using Python (pydicom, nibabel)
```python
# Install dependencies
pip install pydicom nibabel requests

# Example: Load DICOM
import pydicom
ds = pydicom.dcmread('examples/dicom/sample.dcm')

# Example: Load NIfTI
import nibabel as nib
img = nib.load('examples/mri/brain_t1.nii.gz')
```

### Using wget/curl
```bash
# Download example datasets
cd examples/datasets

# Example: TCIA collection
wget https://wiki.cancerimagingarchive.net/download/...

# Extract archives
unzip dataset.zip
```

## Ethical & Legal Considerations

⚠️ **Important:**
- Most datasets require registration and data use agreements
- **Non-commercial research use only** for most datasets
- Follow HIPAA and privacy regulations
- Do not re-distribute without permission
- Cite datasets appropriately in publications

## Dataset Citations

When using these datasets, please cite appropriately:

**MIMIC-CXR:**
Johnson et al. (2019). MIMIC-CXR, a de-identified publicly available database of chest radiographs with free-text reports. Scientific Data, 6, 317.

**NIH Chest X-Ray:**
Wang et al. (2017). ChestX-ray8: Hospital-scale Chest X-ray Database and Benchmarks on Weakly-Supervised Classification and Localization of Common Thorax Diseases. CVPR 2017.

**OASIS:**
Marcus et al. (2007). Open Access Series of Imaging Studies (OASIS): Cross-sectional MRI Data in Young, Middle Aged, Nondemented, and Demented Older Adults. Journal of Cognitive Neuroscience, 19, 1498-1507.

## Integration with CHAZON

Place downloaded examples in appropriate subdirectories:

```bash
# X-rays
cp chest_xray.jpg examples/xray/

# CT scans
cp lung_ct_*.dcm examples/ct/

# MRI
cp brain_t1.nii.gz examples/mri/

# Test with CHAZON tools
# Access via frontend: /screens/frontend/index.html
```

## Additional Resources

- **GitHub Medical Imaging Datasets List:** https://github.com/sfikas/medical-imaging-datasets
- **Aylward.org Repository List:** https://www.aylward.org/notes/open-access-medical-image-repositories
- **radRounds Dataset List:** https://radrounds.com/radiology-news/list-of-open-access-medical-imaging-datasets/
- **Aliza DICOM Viewer Datasets:** https://www.aliza-dicom-viewer.com/download/datasets

## Contributing

To add new example datasets:
1. Place files in appropriate modality subdirectory
2. Update this README with source and citation
3. Ensure compliance with dataset license
4. Add to .gitignore if files are large (>10MB)

## License

Example datasets retain their original licenses. Refer to source repositories for specific terms. This directory structure and documentation are MIT licensed.
