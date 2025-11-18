# DICOM Workflow System - Comprehensive Documentation

## Overview

The DICOM Workflow System is a comprehensive automation framework for medical imaging processing, built on ISA-95 Level 3 (MES) architecture. It provides end-to-end automation for ingesting, processing, analyzing, and archiving DICOM medical studies with integrated AI screening and vector similarity search.

## Architecture

### ISA-95 Level 3 - Manufacturing Execution System (MES)

The workflow system operates at ISA-95 Level 3, providing:
- Work order management (study processing jobs)
- Production tracking (workflow progress)
- Quality assurance (QC checkpoints)
- Performance analysis (metrics and KPIs)
- Resource allocation (GPU, CPU, storage)

### Key Technologies

- **DICOM Protocol**: Medical imaging standard communication
- **Qdrant Vector Database**: 512-dimensional BiomedCLIP embeddings for similarity search
- **AlF-DETECT AI**: Alzheimer's and Autism screening
- **ISA-95 Architecture**: Manufacturing execution system framework
- **MQTT**: Real-time event messaging
- **Modbus**: Industrial control integration

## Workflow Structure

```
/os/medical/workflows/
├── ingestion/              # Data ingestion workflows
│   ├── pacs-ingestion.yaml
│   ├── file-upload-ingestion.yaml
│   └── c-store-ingestion.yaml
├── processing/             # Image processing pipelines
│   ├── anonymization-pipeline.yaml
│   ├── normalization-pipeline.yaml
│   └── enhancement-pipeline.yaml
├── analysis/               # AI analysis workflows
│   ├── alf-detect-analysis.yaml
│   └── embedding-generation.yaml
├── storage/                # Storage and archival
│   └── storage-archival.yaml
├── profiles/               # Modality-specific processing
│   ├── ct-profile.yaml
│   ├── mr-profile.yaml
│   └── xray-profile.yaml
├── queue/                  # Batch processing system
│   └── batch-processing-queue.yaml
├── routing/                # Intelligent routing rules
│   └── study-routing-rules.yaml
├── qc/                     # Quality control
│   └── quality-control-checkpoints.yaml
├── workflow-dashboard.html # Visualization dashboard
└── README.md              # This file
```

## Complete Workflow Pipeline

### 1. Ingestion Phase

**Purpose**: Acquire DICOM studies from multiple sources

**Sources**:
- **PACS Integration** (`pacs-ingestion.yaml`)
  - Automated DICOM C-FIND/C-MOVE queries
  - Scheduled polling every 5 minutes
  - Duplicate detection and deduplication
  - Connection: Port 11112, AE Title: CHAZON_MES

- **File Upload** (`file-upload-ingestion.yaml`)
  - Web interface uploads (max 2GB per file)
  - Watched folder monitoring
  - Batch upload support (up to 1000 files)
  - Format validation and metadata extraction

- **C-STORE Receiver** (`c-store-ingestion.yaml`)
  - DICOM Storage SCP (Service Class Provider)
  - Port 11112, supports 10 concurrent associations
  - Multiple transfer syntax support
  - Real-time instance reception

**Key Features**:
- Automatic duplicate detection
- Study completeness validation
- Metadata extraction and validation
- Quarantine for invalid files
- MQTT notifications on completion

**Monitoring Tags**:
- `PACS_STUDIES_RETRIEVED`
- `UPLOAD_FILES_PROCESSED`
- `CSTORE_INSTANCES_RECEIVED`

---

### 2. Anonymization Phase

**Purpose**: HIPAA/GDPR compliant PHI removal

**Workflow**: `processing/anonymization-pipeline.yaml`

**Compliance Standards**:
- HIPAA Safe Harbor method
- GDPR pseudonymization
- DICOM PS 3.15 compliance

**Anonymization Steps**:
1. **Backup Original Study** - Encrypted backup with 365-day retention
2. **Create Anonymization Mapping** - Reversible mapping stored in vault
3. **Remove PHI Tags** - 40+ DICOM tags removed including:
   - Patient Name, DOB, Address
   - Physician names and contacts
   - Institution information
   - Private tags and curves
4. **Replace Identifiers** - Generate anonymous IDs (ANON{8-digit})
5. **Shift Dates** - Random offset ±365 days, preserve intervals
6. **Regenerate UIDs** - New Study/Series/SOP Instance UIDs
7. **Detect Burned-in PHI** - OCR scan for text in images
8. **Validate Anonymization** - Verify no PHI remains

**Quality Control**:
- PHI pattern detection (names, SSNs, MRNs)
- Audit trail logging (7-year retention)
- Validation before proceeding

**Monitoring Tags**:
- `ANONYMIZATION_STUDIES_PROCESSED`
- `ANONYMIZATION_PHI_REMOVED`
- `ANONYMIZATION_FAILURES`

---

### 3. Normalization Phase

**Purpose**: Standardize DICOM format and quality

**Workflow**: `processing/normalization-pipeline.yaml`

**Normalization Steps**:
1. **Decompress Transfers** - Convert to ExplicitVRLittleEndian
2. **Standardize Metadata** - Fix invalid tags, VRs, lengths
3. **Convert Photometric** - Target MONOCHROME2 for grayscale
4. **Normalize Intensities** - Modality-specific normalization
5. **Standardize Orientation** - Target LPS orientation
6. **Validate Geometry** - Check spacing, thickness, position
7. **Organize Series** - Sort by instance number, detect missing
8. **Apply Modality Profile** - Route to CT/MR/X-Ray profiles

**Modality-Specific**:
- **CT**: HU normalization, rescale application
- **MR**: Intensity normalization, bias correction
- **CR/DX**: VOI LUT application, inversion if needed

**Quality Control**:
- Pixel data validation
- Geometry consistency checks
- Metadata completeness

**Monitoring Tags**:
- `NORMALIZATION_STUDIES_PROCESSED`
- `NORMALIZATION_GEOMETRY_ISSUES`

---

### 4. Enhancement Phase

**Purpose**: Improve image quality for analysis

**Workflow**: `processing/enhancement-pipeline.yaml`

**Enhancement Techniques**:
1. **Quality Assessment** - Calculate SNR, CNR, sharpness
2. **Adaptive Enhancement** - Route by quality score
3. **Denoising** - Non-local means, bilateral filtering
4. **Contrast Enhancement** - CLAHE with modality-specific settings
5. **Sharpening** - Unsharp masking with adaptive strength
6. **Artifact Removal**:
   - CT: Beam hardening, metal artifacts
   - MR: Bias field correction, ghosting
   - CR/DX: Grid lines, scatter
7. **Modality-Specific Enhancement** - Apply specialized profiles
8. **Generate Thumbnails** - Multiple sizes for preview

**Quality Control**:
- Quality improvement metrics (PSNR, SSIM)
- No over-enhancement detection
- Diagnostic feature preservation

**Monitoring Tags**:
- `ENHANCEMENT_STUDIES_PROCESSED`
- `ENHANCEMENT_QUALITY_IMPROVEMENT`

---

### 5. AI Analysis Phase

**Purpose**: AI-powered screening and biomarker detection

#### AlF-DETECT Analysis

**Workflow**: `analysis/alf-detect-analysis.yaml`

**AI Model**: AlF-DETECT v2.1.0
- Framework: PyTorch
- Input: 256³ voxels, 1mm spacing
- GPU: CUDA, mixed precision
- Modalities: MR (primary), CT, PET

**Detection Capabilities**:

**Alzheimer's Detection**:
- Amyloid plaques
- Neurofibrillary tangles
- Hippocampal atrophy
- Cortical thinning
- White matter lesions
- Risk scoring: Preclinical → MCI → Mild → Moderate → Severe

**Autism Detection**:
- Structural abnormalities
- Connectivity patterns
- Volumetric differences
- Cortical thickness variations
- Severity: Low → Medium → High

**ROI Analysis**:
- Hippocampus
- Entorhinal cortex
- Amygdala
- Temporal/Parietal/Frontal lobes
- Cerebellum
- Corpus callosum

**Biomarker Extraction**:
- Hippocampal volume
- Cortex thickness
- Brain atrophy rate
- CSF space enlargement
- White matter hyperintensity volume
- Age-normalized percentiles

**Outputs**:
- Risk scores with confidence intervals
- Detection heatmaps and segmentations
- Comprehensive PDF/HTML/JSON reports
- DICOM Structured Reports

**Routing by Findings**:
- **High Risk** (≥0.7): Immediate radiologist notification
- **Medium Risk** (≥0.4): Schedule follow-up
- **Low Risk** (<0.4): Routine processing

#### Embedding Generation

**Workflow**: `analysis/embedding-generation.yaml`

**Model**: BiomedCLIP v1.0.0
- Architecture: Vision Transformer (ViT)
- Embedding dimension: 512
- Text encoder: BERT base

**Process**:
1. **Key Frame Selection** - Intelligent sampling (max 50/series)
2. **Preprocessing** - Resize to 224×224, RGB conversion
3. **Generate Embeddings** - Normalized 512-D vectors
4. **Generate Text Embeddings** - From descriptions and captions
5. **Upload to Qdrant** - Vector database indexing

**Qdrant Configuration**:
- Collection: `medical_image_embeddings`
- Distance: Cosine similarity
- HNSW indexing (m=16, ef=100)
- Payload: Study/Series metadata, AI results

**Similarity Search**:
- Find similar studies by image content
- Cross-modal text-to-image search
- Clinical context filtering
- Default top-10 results, threshold 0.7

**Monitoring Tags**:
- `ALF_DETECT_STUDIES_ANALYZED`
- `ALF_DETECT_HIGH_RISK_DETECTED`
- `EMBEDDINGS_GENERATED`
- `SIMILARITY_SEARCHES`
- `QDRANT_COLLECTION_SIZE`

---

### 6. Storage & Archival Phase

**Purpose**: Long-term storage with lifecycle management

**Workflow**: `storage/storage-archival.yaml`

**Storage Tiers**:

| Tier | Retention | Storage | Access | Backup |
|------|-----------|---------|--------|--------|
| **Hot** | 90 days | SSD RAID10 | <1 min | Daily |
| **Warm** | 365 days | HDD RAID6 | <5 min | Weekly |
| **Cold** | 7 years | Tape | <1 hour | Monthly |
| **Glacier** | 10 years | Cloud | <24 hours | Quarterly |

**Lifecycle Policies**:
- Automatic tier transitions based on age and access
- 90 days → Warm
- 365 days → Cold
- 7 years → Glacier
- 10 years → Eligible for deletion (if no hold)

**Features**:
- Compression (zstd level 6) for Warm/Cold/Glacier
- AES-256 encryption for Cold/Glacier
- SHA-256 checksums for integrity
- Deduplication and thin provisioning
- Geographic replication for disaster recovery

**Compliance**:
- HIPAA: 7-year minimum retention
- FDA 21 CFR Part 11 compliant
- Legal hold support
- Complete audit trail

**Monitoring Tags**:
- `STUDIES_ARCHIVED`
- `STORAGE_USED_GB`
- `BACKUP_STATUS`

---

## Modality-Specific Processing Profiles

### CT Profile

**File**: `profiles/ct-profile.yaml`

**Specialized Processing**:
- Hounsfield Unit (HU) conversion and validation
- 10+ window presets (brain, lung, bone, soft tissue, etc.)
- Gantry tilt correction
- Artifact removal (beam hardening, metal, ring)
- Body part detection for optimal windowing
- MPR (Multi-Planar Reconstruction) generation
- Dose monitoring (CTDIvol, DLP)

**Protocol Detection**:
- Head CT: Brain windowing, bone removal
- Chest CT: Lung/mediastinum windowing, nodule detection
- CT Angiography: Vessel enhancement, MIP generation
- HR-CT Lung: High-resolution processing

### MRI Profile

**File**: `profiles/mr-profile.yaml`

**Sequence Detection**:
- T1, T2, FLAIR, DWI, SWI, TOF, and more
- Automatic parameter-based identification

**Specialized Processing**:
- N4ITK bias field correction
- Motion and distortion correction
- Intensity normalization (histogram matching)
- Brain extraction (skull stripping)
- Tissue segmentation (GM, WM, CSF)
- Multi-sequence co-registration
- Lesion detection and quantification

**Sequence-Specific**:
- **FLAIR**: Lesion enhancement, CSF suppression validation
- **DWI**: ADC map generation, stroke detection
- **SWI**: Susceptibility mapping, venography
- **TOF**: MIP generation, aneurysm detection

**Advanced Processing**:
- fMRI: Activation detection, connectivity analysis
- DTI: Tractography, FA/MD maps
- Perfusion: CBF, CBV, MTT calculation
- MRS: Metabolite quantification

### X-Ray Profile

**File**: `profiles/xray-profile.yaml`

**Applicable to**: CR (Computed Radiography), DX (Digital X-Ray)

**Processing**:
- Photometric interpretation correction
- VOI LUT application
- Grid line and scatter removal
- Collimator detection and cropping
- Body part and view detection

**Chest X-Ray Specific**:
- Lung field segmentation
- 9+ pathology detection:
  - Pneumonia, pleural effusion, pneumothorax
  - Cardiomegaly, pulmonary edema
  - Mass, nodule, atelectasis, consolidation
- Cardiothoracic ratio measurement
- Tube/line detection and positioning verification
- Rib fracture detection

**Extremity X-Ray**:
- Bone segmentation
- Fracture detection
- Joint space analysis
- Bone density estimation

**Spine X-Ray**:
- Vertebra detection and labeling
- Cobb angle measurement (scoliosis)
- Disk space analysis
- Compression fracture detection

---

## Batch Processing Queue System

**File**: `queue/batch-processing-queue.yaml`

### Queue Types

| Queue | Priority | Concurrency | Timeout | Use Case |
|-------|----------|-------------|---------|----------|
| **High Priority** | 1 | 10 | 1 hour | STAT/Emergency studies |
| **Standard** | 5 | 20 | 2 hours | Routine processing |
| **AI Analysis** | 3 | 2 (GPU) | 30 min | AlF-DETECT screening |
| **Embedding** | 4 | 3 (GPU) | 15 min | BiomedCLIP embeddings |
| **Storage** | 8 | 10 | 1 hour | Archival operations |
| **Low Priority** | 10 | 5 | 4 hours | Bulk reprocessing |

### Worker Pool

- **Auto-scaling**: 5-50 workers based on queue utilization
- **Resource allocation**: Dynamic CPU/Memory, Exclusive GPU
- **Load balancing**: Weighted round-robin
- **Time-based scheduling**: Peak hours vs off-hours optimization

### Job Lifecycle

States: Pending → Scheduled → Running → Completed/Failed/Timeout
- Retry policy: Exponential backoff, max 3 attempts
- Dead letter queue for permanent failures
- Circuit breaker for cascading failures

### Monitoring

- Real-time queue metrics (length, wait time, throughput)
- Job execution tracking
- Resource utilization (CPU, GPU, Memory, Storage I/O)
- SLA compliance monitoring

**Monitoring Tags**:
- `QUEUE_JOBS_PENDING`
- `QUEUE_JOBS_RUNNING`
- `QUEUE_THROUGHPUT_PER_HOUR`
- `QUEUE_AVG_WAIT_TIME`

---

## Intelligent Study Routing

**File**: `routing/study-routing-rules.yaml`

### Routing Decision Tree

**Priority-based rule evaluation**:

1. **Emergency Fast Track** (Priority 1)
   - Conditions: STAT/URGENT, Stroke, Trauma
   - Actions: Critical priority, skip enhancement, immediate notification
   - Path: Ingestion → Normalization → AI → Embedding → Storage

2. **Research Studies** (Priority 2)
   - Conditions: Research study type
   - Actions: Enhanced anonymization, low priority
   - Path: Full pipeline with strict anonymization

3. **AI Screening Required** (Priority 3)
   - Conditions: Alzheimer's/Dementia/Autism/Brain keywords
   - Actions: Enable AlF-DETECT, high priority
   - Path: Full pipeline with AI analysis

4. **Standard Workflow** (Priority 10)
   - Conditions: Routine urgency
   - Actions: Normal priority, complete pipeline
   - Path: All 7 phases

### Modality-Specific Routing

- **CT Brain**: AlF-DETECT screening, brain/bone windows
- **CT Chest**: Lung/mediastinum windows, nodule detection
- **MRI Brain**: AlF-DETECT, tissue segmentation, lesion detection
- **Chest X-Ray**: Pathology detection, CTR measurement

### AI-Based Post-Analysis Routing

- **High Risk** (≥0.7): Immediate notification, urgent flag
- **Medium Risk** (0.4-0.7): Routine flag, schedule follow-up
- **Low Risk** (<0.4): Routine processing, direct archive

### Quality-Based Routing

- **High Quality** (≥0.8): Standard processing, training set inclusion
- **Medium Quality** (0.5-0.8): Enhanced preprocessing
- **Low Quality** (<0.5): Aggressive enhancement, rescan consideration

### Time-Based Routing

- **Peak Hours** (8AM-6PM weekdays): Defer heavy processing, prioritize urgent
- **Off Hours**: Full processing, run batch jobs

**Monitoring Tags**:
- `ROUTING_STUDIES_PROCESSED`
- `ROUTING_EMERGENCY_COUNT`
- `ROUTING_AI_FLAGGED`

---

## Quality Control System

**File**: `qc/quality-control-checkpoints.yaml`

### QC Framework

- **7 Checkpoints** throughout pipeline
- **3 Severity Levels**: Critical (fail), Warning (flag), Info (log)
- **Auto-remediation** for common issues
- **Manual review** for scores <0.6

### Quality Checkpoints

1. **Post-Ingestion**
   - DICOM conformance
   - File integrity (checksums)
   - Metadata completeness
   - Study completeness

2. **Post-Anonymization**
   - PHI removal verification (OCR scan)
   - UID regeneration validation
   - Date shifting verification
   - Burned-in PHI detection

3. **Post-Normalization**
   - Pixel data validation
   - Geometry consistency
   - Intensity range validation
   - Modality-specific checks (HU for CT)

4. **Post-Enhancement**
   - Quality improvement metrics (PSNR, SSIM)
   - No over-enhancement
   - Diagnostic feature preservation

5. **Post-AI-Analysis**
   - AI results completeness
   - Confidence threshold validation
   - Result consistency
   - Uncertainty assessment

6. **Post-Embedding**
   - Embedding validation (512-D, normalized)
   - Qdrant upload verification
   - Similarity sanity check

7. **Pre-Storage**
   - Pipeline completion verification
   - Data integrity (checksums)
   - Metadata completeness

### Quality Scoring

**Weighted average** (0.0-1.0):
- DICOM conformance: 20%
- Data integrity: 20%
- Image quality: 15%
- Processing quality: 15%
- AI confidence: 10%
- Embedding quality: 10%
- Completeness: 10%

**Score Interpretation**:
- 0.9-1.0: Excellent → Proceed, include in training
- 0.8-0.9: Good → Proceed
- 0.6-0.8: Acceptable → Proceed, flag for monitoring
- 0.4-0.6: Needs Review → Manual review, hold storage
- 0.0-0.4: Unacceptable → Quarantine, reprocess, notify admin

### Remediation Strategies

- **Missing metadata**: Attempt recovery, inference, manual entry
- **Poor quality**: Reprocess with aggressive enhancement, flag for rescan
- **Processing errors**: Retry with alternative algorithms
- **AI uncertainty**: Ensemble models, expert review

**Monitoring Tags**:
- `QC_STUDIES_CHECKED`
- `QC_PASS_RATE_PERCENT`
- `QC_MANUAL_REVIEW_COUNT`
- `QC_AVG_SCORE`

---

## Workflow Dashboard

**File**: `workflow-dashboard.html`

### Features

**Real-time Metrics**:
- Images processed (daily total)
- Similarity searches (Qdrant queries)
- Embedding model (BiomedCLIP)
- Average process time per study
- Cache size (Qdrant storage)
- Queue length (pending studies)

**Pipeline Visualization**:
- 7-stage workflow diagram
- Stage status indicators (Active/Idle/Error)
- Real-time progress tracking

**Queue Status**:
- Per-queue metrics (pending, running, capacity)
- Concurrency utilization
- GPU queue status

**AI Analysis**:
- Alzheimer's detection statistics
- Autism detection statistics
- Confidence scores and processing times

**Tag Provider**:
- All ISA-95 tag values
- Real-time updates
- MQTT integration

### Access

```bash
# Open dashboard
open /home/user/qdrant/os/medical/workflows/workflow-dashboard.html

# Or via web server
# Navigate to: http://localhost:8080/os/medical/workflows/workflow-dashboard.html
```

---

## Configuration and Customization

### Environment Variables

```bash
# PACS Configuration
export PACS_HOST=pacs.hospital.local
export PACS_PORT=11112
export PACS_AE_TITLE=PACS_SCP

# Qdrant Configuration
export QDRANT_HOST=localhost
export QDRANT_PORT=6333
export QDRANT_API_KEY=your_api_key

# Processing Configuration
export PACS_INTEGRATION_ENABLED=true
export GPU_DEVICES=0,1
```

### Workflow Customization

Each workflow YAML file supports:
- **Conditional execution**: Enable/disable steps
- **Parameter tuning**: Adjust thresholds, timeouts
- **Custom routing**: Modify decision rules
- **Integration**: Add custom MQTT topics, Modbus registers

### Adding Custom Workflows

```yaml
# custom-workflow.yaml
workflow:
  id: custom-workflow-001
  name: Custom Processing
  version: "1.0.0"

steps:
  - id: custom-step
    name: Custom Processing Step
    type: custom
    action: custom_function
    on_success: next-step
```

---

## Monitoring and Observability

### MQTT Topics

**Workflow Events**:
- `chazon/os/medical/workflow/study-received`
- `chazon/os/medical/workflow/study-uploaded`
- `chazon/os/medical/workflow/study-received-complete`

**Processing Events**:
- `chazon/os/medical/anonymization/*`
- `chazon/os/medical/normalization/*`
- `chazon/os/medical/enhancement/*`

**AI Events**:
- `chazon/os/medical/alf-detect/results-available`
- `chazon/os/medical/alf-detect/high-risk-detected`
- `chazon/os/medical/embeddings/generated`

**Queue Events**:
- `chazon/os/medical/queue/job-submitted`
- `chazon/os/medical/queue/job-completed`

**QC Events**:
- `chazon/os/medical/qc/checkpoint-passed`
- `chazon/os/medical/qc/checkpoint-failed`

### Modbus Registers

| Address | Tag Name | Description |
|---------|----------|-------------|
| 40100-40102 | PACS_* | PACS ingestion metrics |
| 40110-40112 | UPLOAD_* | File upload metrics |
| 40120-40122 | CSTORE_* | C-STORE receiver metrics |
| 40200-40202 | ANONYMIZATION_* | Anonymization metrics |
| 40210-40211 | NORMALIZATION_* | Normalization metrics |
| 40220-40222 | ENHANCEMENT_* | Enhancement metrics |
| 40300-40302 | ALF_DETECT_* | AI analysis metrics |
| 40310-40313 | EMBEDDINGS_* | Embedding metrics |
| 40400-40402 | STORAGE_* | Storage metrics |
| 40500-40504 | QUEUE_* | Queue system metrics |
| 40600-40602 | ROUTING_* | Routing metrics |
| 40700-40703 | QC_* | Quality control metrics |

### Logging

**Log Locations**:
```
/var/log/medical/workflows/
├── pacs-ingestion.log
├── file-upload-ingestion.log
├── c-store-ingestion.log
├── anonymization.log
├── normalization.log
├── enhancement.log
├── alf-detect-analysis.log
├── embedding-generation.log
├── storage-archival.log
├── routing.log
├── qc.log
└── batch-processing.log
```

**Log Retention**:
- Standard logs: 90 days
- Audit logs: 7 years (compliance)
- Anonymization logs: 7 years (compliance)

---

## Performance Optimization

### Throughput

- **Target**: 3-5 studies/minute average
- **Peak**: Up to 10 studies/minute with scaling
- **Bottlenecks**: GPU-based AI analysis (2 concurrent)

### Resource Requirements

**Minimum**:
- CPU: 16 cores
- Memory: 64GB RAM
- GPU: 2x NVIDIA GPU with 8GB+ VRAM
- Storage: 200TB total (tiered)
- Network: 1 Gbps

**Recommended**:
- CPU: 32 cores
- Memory: 128GB RAM
- GPU: 4x NVIDIA GPU with 16GB+ VRAM
- Storage: 500TB total (tiered)
- Network: 10 Gbps

### Optimization Strategies

- **Parallel Processing**: Multiple studies simultaneously
- **GPU Batching**: Batch AI inference for efficiency
- **Caching**: Model caching, result caching
- **Progressive Loading**: Stream large studies
- **Time-based Scheduling**: Heavy processing during off-hours

---

## Security and Compliance

### Data Security

- **Encryption at Rest**: AES-256 for cold/glacier tiers
- **Encryption in Transit**: TLS for DICOM, HTTPS for uploads
- **Access Control**: OAuth2 authentication, RBAC authorization
- **Audit Logging**: All access and modifications logged

### Compliance

- **HIPAA**: Safe Harbor anonymization, 7-year retention
- **GDPR**: Right to erasure, data portability, pseudonymization
- **FDA 21 CFR Part 11**: Electronic records and signatures
- **DICOM PS 3.15**: Security and privacy profiles

### Privacy

- **Anonymization**: Comprehensive PHI removal
- **Burned-in PHI Detection**: OCR-based text detection
- **Reversible Mapping**: Secure vault for re-identification (if authorized)
- **No PHI in Logs**: Privacy-safe logging

---

## Troubleshooting

### Common Issues

**1. PACS Connection Failures**
- Check network connectivity
- Verify AE titles and ports
- Check firewall rules
- Review `/var/log/medical/workflows/pacs-ingestion.log`

**2. GPU Out of Memory**
- Reduce batch size in AI workflows
- Reduce concurrent AI jobs
- Check GPU memory with `nvidia-smi`

**3. Qdrant Upload Failures**
- Verify Qdrant service is running
- Check network connectivity
- Validate collection exists
- Review `/var/log/medical/workflows/embedding-generation.log`

**4. QC Checkpoint Failures**
- Review specific checkpoint in QC logs
- Check quarantine directory for failed studies
- Run manual remediation

**5. Queue Stalling**
- Check worker availability
- Review resource utilization
- Check for circuit breaker activation
- Restart queue service if needed

### Support

For issues and support:
- Check logs in `/var/log/medical/workflows/`
- Review workflow dashboard for status
- Monitor MQTT topics for error events
- Contact: medical-imaging-team@organization.com

---

## Future Enhancements

### Planned Features

1. **Advanced AI Models**
   - Tumor detection and characterization
   - Stroke detection and ASPECTS scoring
   - Fracture detection across all modalities

2. **Workflow Extensions**
   - 3D printing workflow for surgical planning
   - Radiation therapy planning integration
   - Interventional radiology support

3. **Enhanced Analytics**
   - Longitudinal study comparison
   - Population health analytics
   - Predictive maintenance for imaging equipment

4. **Integration Expansion**
   - HL7 FHIR interface
   - RIS/PACS integration
   - EHR system connectivity

5. **Cloud Migration**
   - Hybrid cloud storage tiers
   - Cloud-based AI inference
   - Multi-site federation

---

## Version History

- **v1.0.0** (2025-11-17): Initial comprehensive workflow system
  - Complete 7-phase pipeline
  - AlF-DETECT AI integration
  - BiomedCLIP embeddings with Qdrant
  - Batch queue system
  - Intelligent routing
  - Quality control framework
  - Workflow dashboard

---

## License and Usage

This workflow system is designed for medical imaging factories using ISA-95 architecture. All processing complies with HIPAA, GDPR, and DICOM standards.

**Disclaimer**: AI analysis results are for screening purposes only and should be interpreted by qualified healthcare professionals. Not a substitute for professional medical diagnosis.

---

## Quick Start

```bash
# 1. View workflow dashboard
open /home/user/qdrant/os/medical/workflows/workflow-dashboard.html

# 2. Check system status
tail -f /var/log/medical/workflows/*.log

# 3. Monitor MQTT events
mosquitto_sub -t 'chazon/os/medical/#' -v

# 4. Check Qdrant status
curl http://localhost:6333/collections/medical_image_embeddings

# 5. Review queue status
curl http://localhost:8080/api/queue/stats
```

---

**Medical Imaging Virtual Factory**
**ISA-95 Level 3 - Manufacturing Execution System**
**DICOM Workflow Automation v1.0.0**
