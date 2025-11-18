# 🚀 CHAZON Medical Imaging - Quick Start Guide

Get the complete medical imaging vector search system running in **3 steps**!

---

## ⚡ Quick Start (3 Commands)

```bash
# 1. Start Qdrant + Backend (with auto-download of models)
docker-compose up -d

# 2. Load 15 medical sample cases
python collab/miracle/ingest_medical_data.py

# 3. Open the medical search UI
open screens/frontend/medical-search.html
```

**That's it!** Your medical imaging search system is live! 🎉

---

## 🎯 What You Get

### **Automatic Model Download**

The backend automatically downloads and loads one of these models:

**1. BiomedCLIP** (Best - Medical-specific)
- Microsoft's medical imaging model
- 512-D embeddings
- Best accuracy for medical images
- Auto-downloads from HuggingFace (~2 GB)

**2. ResNet50** (Good - General purpose)
- PyTorch pre-trained on ImageNet
- 2048-D → 512-D embeddings
- Fast and reliable
- Auto-downloads from PyTorch (~100 MB)

**3. Statistical Features** (Fallback)
- Color histograms + edge detection
- No download needed
- Works offline
- Good for testing

### **Complete System**

✅ **Backend API** (11 endpoints)
- `POST /medical/upload` - Upload medical images
- `POST /medical/analyze` - Find similar cases
- `POST /medical/search` - Search with filters
- `GET /medical/stats` - Database statistics

✅ **Vector Database** (Qdrant)
- 512-D COSINE similarity
- Metadata filtering
- Fast search (<500ms)

✅ **Sample Dataset** (15 medical cases)
- 5 body parts (CHEST, HEAD, HAND, ABDOMEN, KNEE)
- 3 modalities (XRAY, CT, MRI)
- 12+ diagnoses (Pneumonia, Fractures, Tumors...)

✅ **Web UI** (Medical search interface)
- Drag & drop upload
- Three search modes
- Real-time results
- Beautiful purple theme

---

## 📋 Prerequisites

**Required:**
- Docker & Docker Compose
- Python 3.11+
- 4 GB RAM minimum

**Optional (for better performance):**
- NVIDIA GPU with CUDA (for GPU acceleration)
- 8 GB RAM (for BiomedCLIP)
- Fast internet (for model download)

---

## 🔧 Detailed Setup

### Step 1: Start Services

```bash
# Start Qdrant + Backend
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Expected output:
# 🚀 Starting Chazon OS API
# 🔄 Loading BiomedCLIP model...  (or ResNet50)
# ✅ BiomedCLIP loaded successfully
# ✅ API ready - Model: biomedclip
```

**First run:** Model download takes 2-10 minutes depending on your internet speed.

**Services running:**
- Qdrant: http://localhost:6333
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Step 2: Load Sample Data

```bash
# Navigate to repo root
cd /path/to/qdrant

# Run ingestion script
python collab/miracle/ingest_medical_data.py

# Expected output:
# 🏥 MEDICAL IMAGING DATA INGESTION
# ✅ Created collection: medical_images (dim=512)
# 🔄 Ingesting 15 medical cases...
#   ✓ P001: CHEST - Normal
#   ✓ P002: CHEST - Normal
#   ✓ P003: CHEST - Pneumonia (Right Lower Lobe)
#   ...
# ✅ Successfully ingested 15 medical cases
# ✅ Verification complete
```

**Data stored in:**
- Qdrant: `qdrant_storage:/qdrant/storage`
- Persistent across restarts

### Step 3: Open UI & Test

```bash
# Option 1: Open medical search interface
open screens/frontend/medical-search.html

# Option 2: Open compressed database viewer
open screens/frontend/medical-db-compressed.html
```

**Test the search:**
1. Check connection status (should be green)
2. View database statistics (15 cases)
3. Try filter search (Body Part: CHEST)
4. Upload a test medical image
5. View similar cases with similarity scores

---

## 🧪 Testing the API

### Health Check
```bash
curl http://localhost:8000/health

# Response:
# {
#   "status": "healthy",
#   "qdrant": "ok",
#   "collections": 1
# }
```

### Get Statistics
```bash
curl http://localhost:8000/medical/stats

# Response:
# {
#   "total_images": 15,
#   "vector_dimension": 512,
#   "body_parts": {
#     "CHEST": 7,
#     "HAND": 3,
#     "HEAD": 2,
#     "ABDOMEN": 2,
#     "KNEE": 1
#   },
#   "modalities": {
#     "XRAY": 10,
#     "CT": 4,
#     "MRI": 1
#   }
# }
```

### Check Model Type
```bash
curl http://localhost:8000/

# Response:
# {
#   "name": "Chazon OS API",
#   "version": "1.0.0",
#   "qdrant": "connected",
#   "image_model": "biomedclip",  # or "resnet50" or "statistical"
#   "gpu_available": false
# }
```

### Upload Medical Image
```bash
# Upload a test image
curl -X POST http://localhost:8000/medical/upload \
  -F "file=@/path/to/chest_xray.jpg" \
  -F "patient_id=P999" \
  -F "body_part=CHEST" \
  -F "modality=XRAY" \
  -F "diagnosis=Test Case"

# Response:
# {
#   "success": true,
#   "id": "uuid-here",
#   "embedding_dim": 512
# }
```

---

## 🎨 UI Features

### Medical Search Interface

**Three Search Modes:**

1. **Image Upload Search**
   - Drag & drop medical image
   - Finds similar cases
   - Shows top 5 results with scores

2. **Text Query Search**
   - Natural language search
   - Example: "chest x-ray with pneumonia"
   - Uses Cohere/OpenAI embeddings

3. **Filter Search**
   - Filter by body part
   - Filter by modality
   - Filter by diagnosis
   - Combined filters supported

**Features:**
- Real-time connection status
- Database statistics dashboard
- Similarity scores (0-100%)
- Case metadata display
- Loading states & error handling

---

## 🚨 Troubleshooting

### Backend won't start
```bash
# Check Docker containers
docker ps

# View logs
docker-compose logs backend

# Common issues:
# - Port 8000 already in use → Change port in docker-compose.yml
# - Model download failed → Check internet connection
# - Out of memory → Reduce model size or add more RAM
```

### Model not loading
```bash
# Check backend logs
docker-compose logs backend | grep -i "model"

# If BiomedCLIP fails, it falls back to ResNet50
# If ResNet50 fails, it falls back to statistical features

# Force specific model by editing os/backend/api.py
```

### Qdrant connection failed
```bash
# Check Qdrant is running
curl http://localhost:6333/collections

# Restart services
docker-compose restart

# Check volumes
docker volume ls | grep qdrant
```

### No search results
```bash
# Verify data was loaded
curl http://localhost:8000/medical/stats

# Re-run ingestion
python collab/miracle/ingest_medical_data.py

# Check collection exists
curl http://localhost:6333/collections
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file:
```bash
# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# Optional: Embedding models for text search
COHERE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# API
API_URL=http://localhost:8000
```

### GPU Support (Optional)

If you have NVIDIA GPU:

```yaml
# Edit docker-compose.yml
services:
  backend:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

---

## 📊 Performance Expectations

### With BiomedCLIP (Medical-specific)
- **Index time**: ~300ms per image (~80ms with GPU)
- **Search time**: <500ms for 1000 images
- **Memory**: ~2 GB (model) + 10 MB per 1000 images
- **Accuracy**: 🔥 Excellent for medical images

### With ResNet50 (General purpose)
- **Index time**: ~200ms per image (~50ms with GPU)
- **Search time**: <500ms for 1000 images
- **Memory**: ~500 MB (model) + 10 MB per 1000 images
- **Accuracy**: ✅ Good for general images

### With Statistical Features (Fallback)
- **Index time**: ~50ms per image
- **Search time**: <100ms for 1000 images
- **Memory**: ~10 MB per 1000 images
- **Accuracy**: ⚠️ Limited (color-based only)

---

## 🔗 Useful Links

- **API Documentation**: http://localhost:8000/docs
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **BiomedCLIP Model**: https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224
- **Project Issues**: https://github.com/teslasolar/qdrant/issues

---

## 📝 Next Steps

### Add More Medical Images

```python
# Upload via API
import requests

files = {'file': open('chest_xray.jpg', 'rb')}
data = {
    'patient_id': 'P100',
    'body_part': 'CHEST',
    'modality': 'XRAY',
    'diagnosis': 'Pneumonia'
}

response = requests.post(
    'http://localhost:8000/medical/upload',
    files=files,
    data=data
)
```

### Batch Upload Script

```python
import os
import requests

image_dir = '/path/to/medical/images'

for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.png', '.dcm')):
        with open(os.path.join(image_dir, filename), 'rb') as f:
            files = {'file': f}
            data = {
                'patient_id': filename.split('_')[0],
                'body_part': 'CHEST',
                'modality': 'XRAY'
            }
            requests.post('http://localhost:8000/medical/upload', files=files, data=data)
            print(f'✅ Uploaded {filename}')
```

### Integrate with PACS System

```python
# Example: Query PACS and index in Qdrant
from pydicom import dcmread

dicom_file = dcmread('study.dcm')
pixel_array = dicom_file.pixel_array

# Convert to PNG and upload
from PIL import Image
image = Image.fromarray(pixel_array)
image.save('temp.png')

# Upload to Qdrant via API
# ...
```

---

## 🎓 Learn More

- Check `QDRANT_INTEGRATION_CHECKLIST.md` for feature checklist
- Check `AUDIT_UPDATE.md` for detailed audit results
- Check `os/backend/api.py` for API implementation
- Check `collab/miracle/ingest_medical_data.py` for data examples

---

**Happy searching! 🔍⚕️**

Questions? Check the [Issues](https://github.com/teslasolar/qdrant/issues) or [Discussions](https://github.com/teslasolar/qdrant/discussions)
