# 🏥 Medical Imaging with Qdrant - Quick Start

**5-Minute Setup Guide**

---

## 🎯 What This Does

AI-powered medical image similarity search using **Qdrant vector database**. Upload an X-ray or CT scan and instantly find similar cases from your database.

### Key Features
- 🔍 Vector similarity search with Qdrant
- 🏥 Multi-modal support (X-Ray, CT, MRI)
- 🎯 Metadata filtering (body part, modality)
- ⚡ Real-time results
- 🎨 Beautiful UI

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker (for Qdrant)
- Modern web browser

### Step 1: Start Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```
✅ Qdrant running at `http://localhost:6333`

### Step 2: Install Dependencies
```bash
cd os/backend
pip install -r requirements.txt
```

### Step 3: Populate Database
```bash
cd ../../collab/miracle
python ingest_medical_data.py
```

Expected output:
```
✅ Created collection: medical_images (dim=512)
✅ Successfully ingested 15 medical cases
```

### Step 4: Start Backend
```bash
cd ../../os/backend
python api.py
```
✅ API running at `http://localhost:8000`

### Step 5: Open Viewer
```bash
# From project root
open collab/miracle/medical-viewer.html
```

**Done! 🎉**

---

## 🎮 Using the Application

1. **Upload Image** - Drag & drop or click to upload
2. **Select Metadata** - Choose body part and modality
3. **Find Similar** - Get instant results ranked by similarity

---

## 📊 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Analyze Image
```bash
curl -X POST http://localhost:8000/medical/analyze \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "data:image/jpeg;base64,...", "metadata": {"body_part": "CHEST"}}'
```

### Search Cases
```bash
curl -X POST http://localhost:8000/medical/search \
  -H "Content-Type: application/json" \
  -d '{"query": "chest x-ray pneumonia", "limit": 5}'
```

### Get Statistics
```bash
curl http://localhost:8000/medical/stats
```

---

## 🗄️ Sample Dataset

15 medical cases across:
- **7 Chest X-Rays** (2 normal, 3 pneumonia, 1 effusion, 1 edema)
- **3 Hand X-Rays** (1 normal, 1 fracture, 1 arthritis)
- **2 Head CT** (1 normal, 1 tumor)
- **2 Abdomen CT** (1 normal, 1 kidney stone)
- **1 Knee MRI** (meniscal tear)

---

## 🔬 How It Works

```
Image → Feature Extraction → 512-D Vector → Qdrant Search → Ranked Results
```

**Features extracted:**
- Color channel statistics
- Histogram distributions
- Normalized to 512 dimensions

**Search:**
- Cosine similarity in Qdrant
- Metadata filtering (body part, modality)
- Real-time results

---

## 🎨 Architecture

```
Medical Viewer UI (HTML/JS)
           ↓
   FastAPI Backend (Python)
           ↓
   Qdrant Vector Database
```

---

## 🚀 Next Steps

1. **Add Your Data** - Upload your medical images
2. **Customize** - Integrate CLIP/BiomedCLIP models
3. **Deploy** - Use Railway/Fly.io for production
4. **Scale** - Deploy to Qdrant Cloud

---

## 🔧 Troubleshooting

**Backend won't start:**
```bash
pip install -r os/backend/requirements.txt
```

**Qdrant connection failed:**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**No results found:**
```bash
cd collab/miracle
python ingest_medical_data.py
```

---

## 📚 Documentation

- [API Documentation](API.md)
- [Project Plan](../PROJECT_PLAN.md)
- [Backend Setup](../../../docs/guides/BACKEND_SETUP.md)

---

**Built with Qdrant Vector Database for lablab.ai Challenge 2025**
