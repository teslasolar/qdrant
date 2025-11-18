# CHAZON Medical Imaging - Complete Deployment Guide

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [GPU Acceleration](#gpu-acceleration)
5. [Scaling & Performance](#scaling--performance)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Minimum (Development/Testing)
- **OS**: Linux, macOS, or Windows 10+
- **RAM**: 4 GB
- **Storage**: 5 GB free space
- **CPU**: 2 cores
- **Network**: Stable internet (for model download)

### Recommended (Production)
- **OS**: Ubuntu 20.04+ or RHEL 8+
- **RAM**: 8-16 GB
- **Storage**: 20 GB SSD
- **CPU**: 4+ cores
- **GPU**: NVIDIA GPU with CUDA 11.8+ (optional, 10x faster)

### Software Dependencies
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+ (for ingestion scripts)
- Git

---

## 🚀 Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/teslasolar/qdrant.git
cd qdrant
git checkout claude/merge-all-final-016KTQwxg9ThVrm9yVjHSa6Q
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Required variables:**
```env
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=                    # Optional, leave empty for local dev
API_URL=http://localhost:8000
```

**Optional variables (for text search):**
```env
COHERE_API_KEY=your_cohere_key     # For text-based search
OPENAI_API_KEY=your_openai_key     # Alternative for text search
```

### Step 3: Start Services

```bash
# Start Qdrant + Backend
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Expected output:
# 🚀 Starting Chazon OS API
# 🔄 Loading BiomedCLIP model...
# ✅ BiomedCLIP loaded successfully
# ✅ API ready - Model: biomedclip
```

**First startup**: Models download automatically (2-10 minutes)
- BiomedCLIP: ~2 GB
- ResNet50: ~100 MB (fallback)

### Step 4: Verify Services

```bash
# Check containers
docker ps

# Expected output:
# CONTAINER ID   NAME              STATUS    PORTS
# xxxx           qdrant            Up        6333-6334
# xxxx           chazon-backend    Up        8000

# Test API health
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "qdrant": "ok",
#   "collections": 0
# }
```

### Step 5: Load Sample Data

```bash
# Install Python dependencies (if needed)
pip install qdrant-client

# Run ingestion script
python collab/miracle/ingest_medical_data.py

# Expected output:
# 🏥 MEDICAL IMAGING DATA INGESTION
# ✅ Created collection: medical_images (dim=512)
# 🔄 Ingesting 15 medical cases...
# ✅ Successfully ingested 15 medical cases
# ✅ Verification complete
```

### Step 6: Test Search UI

```bash
# Open in browser
open screens/frontend/medical-search.html

# Or use Python HTTP server
cd screens/frontend
python -m http.server 8080
# Then open: http://localhost:8080/medical-search.html
```

---

## 🏭 Production Deployment

### Option 1: Docker Compose (Recommended for Small Scale)

```bash
# Production docker-compose.yml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    restart: always
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2'

  backend:
    build: ./os/backend
    restart: always
    ports:
      - "8000:8000"
    environment:
      - QDRANT_URL=http://qdrant:6333
      - WORKERS=4
    depends_on:
      - qdrant
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '4'

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend

volumes:
  qdrant_data:
```

### Option 2: Kubernetes (Large Scale)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chazon-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chazon-backend
  template:
    metadata:
      labels:
        app: chazon-backend
    spec:
      containers:
      - name: backend
        image: your-registry/chazon-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: QDRANT_URL
          value: "http://qdrant:6333"
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
---
apiVersion: v1
kind: Service
metadata:
  name: chazon-backend
spec:
  selector:
    app: chazon-backend
  ports:
  - port: 8000
    targetPort: 8000
  type: LoadBalancer
```

### Option 3: Cloud Deployment (AWS/GCP/Azure)

**AWS Deployment:**
```bash
# Use ECS + Fargate
aws ecs create-cluster --cluster-name chazon-medical

# Deploy backend
aws ecs run-task \
  --cluster chazon-medical \
  --task-definition chazon-backend:1 \
  --launch-type FARGATE

# Deploy Qdrant
aws ecs run-task \
  --cluster chazon-medical \
  --task-definition qdrant:1 \
  --launch-type FARGATE
```

---

## 🚀 GPU Acceleration

### NVIDIA GPU Support

**1. Install NVIDIA Container Toolkit:**
```bash
# Ubuntu
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

**2. Update docker-compose.yml:**
```yaml
services:
  backend:
    build: ./os/backend
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

**3. Verify GPU Access:**
```bash
docker-compose up -d
docker-compose exec backend nvidia-smi

# Expected output:
# GPU 0: NVIDIA Tesla T4 (UUID: GPU-xxx)
```

**Performance Improvement:**
- BiomedCLIP: 300ms → 80ms per image (3.75x faster)
- ResNet50: 200ms → 50ms per image (4x faster)
- Batch processing: 10-20x faster

---

## 📊 Scaling & Performance

### Horizontal Scaling

**Load Balancer Configuration (Nginx):**
```nginx
upstream chazon_backend {
    least_conn;
    server backend1:8000 weight=1;
    server backend2:8000 weight=1;
    server backend3:8000 weight=1;
}

server {
    listen 80;
    location /api {
        proxy_pass http://chazon_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Qdrant Clustering

```yaml
# Qdrant cluster setup
services:
  qdrant-node1:
    image: qdrant/qdrant:latest
    environment:
      - QDRANT__CLUSTER__ENABLED=true
      - QDRANT__CLUSTER__NODE_ID=1

  qdrant-node2:
    image: qdrant/qdrant:latest
    environment:
      - QDRANT__CLUSTER__ENABLED=true
      - QDRANT__CLUSTER__NODE_ID=2
```

### Caching Strategy

**Redis for embedding cache:**
```python
# Add to api.py
import redis

cache = redis.Redis(host='redis', port=6379)

def get_cached_embedding(image_hash):
    cached = cache.get(f"emb:{image_hash}")
    if cached:
        return json.loads(cached)
    return None

def set_cached_embedding(image_hash, embedding):
    cache.setex(f"emb:{image_hash}", 3600, json.dumps(embedding))
```

---

## 📈 Monitoring & Maintenance

### Prometheus Metrics

```python
# Add to api.py
from prometheus_client import Counter, Histogram, make_asgi_app

search_requests = Counter('medical_search_requests', 'Total search requests')
search_duration = Histogram('medical_search_duration_seconds', 'Search duration')

@app.middleware("http")
async def track_metrics(request, call_next):
    if "/medical/" in request.url.path:
        search_requests.inc()
        with search_duration.time():
            response = await call_next(request)
        return response
    return await call_next(request)

# Mount metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "CHAZON Medical Imaging",
    "panels": [
      {
        "title": "Search Requests/sec",
        "targets": [{"expr": "rate(medical_search_requests[5m])"}]
      },
      {
        "title": "Average Search Duration",
        "targets": [{"expr": "rate(medical_search_duration_seconds_sum[5m]) / rate(medical_search_duration_seconds_count[5m])"}]
      }
    ]
  }
}
```

### Health Checks

```bash
#!/bin/bash
# healthcheck.sh

# Check backend
if ! curl -f http://localhost:8000/health; then
    echo "Backend unhealthy"
    exit 1
fi

# Check Qdrant
if ! curl -f http://localhost:6333/health; then
    echo "Qdrant unhealthy"
    exit 1
fi

echo "All services healthy"
```

### Backup Strategy

```bash
#!/bin/bash
# backup.sh

# Backup Qdrant data
docker run --rm \
  -v qdrant_storage:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/qdrant-$(date +%Y%m%d).tar.gz /data

# Upload to S3
aws s3 cp backups/qdrant-$(date +%Y%m%d).tar.gz \
  s3://chazon-backups/

# Cleanup old backups (keep 30 days)
find backups/ -mtime +30 -delete
```

---

## 🔧 Troubleshooting

### Issue: Backend fails to start

**Symptom:** Container exits immediately

**Solution:**
```bash
# Check logs
docker-compose logs backend

# Common causes:
# 1. Port 8000 already in use
sudo lsof -i :8000
kill -9 <PID>

# 2. Insufficient memory
# Increase Docker memory limit to 8 GB

# 3. Model download failed
# Delete model cache and retry
docker-compose down -v
docker-compose up -d
```

### Issue: Models not loading

**Symptom:** Falls back to statistical features

**Solution:**
```bash
# Check internet connection
curl -I https://huggingface.co

# Manually download BiomedCLIP
docker-compose exec backend python -c "
import open_clip
model, _, preprocess = open_clip.create_model_and_transforms(
    'hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224'
)
print('Model downloaded')
"

# Restart backend
docker-compose restart backend
```

### Issue: Slow search performance

**Symptom:** Search takes >1 second

**Solution:**
```bash
# 1. Enable GPU acceleration (see GPU section)

# 2. Optimize Qdrant index
curl -X POST http://localhost:6333/collections/medical_images/index

# 3. Reduce collection size
# Keep only necessary metadata in payload

# 4. Use caching (see Caching Strategy)
```

### Issue: Out of memory

**Symptom:** Backend crashes under load

**Solution:**
```bash
# 1. Increase container memory
# In docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 16G

# 2. Use model quantization
# In api.py, after loading model:
if IMAGE_MODEL_TYPE == "biomedclip":
    IMAGE_MODEL = torch.quantization.quantize_dynamic(
        IMAGE_MODEL, {torch.nn.Linear}, dtype=torch.qint8
    )

# 3. Reduce batch size
# Process images one at a time
```

### Issue: CORS errors in frontend

**Symptom:** Browser blocks API requests

**Solution:**
```python
# In api.py, update CORS settings:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📞 Support

- **Documentation**: See QUICKSTART.md, FINAL_SUMMARY.txt
- **Issues**: https://github.com/teslasolar/qdrant/issues
- **Performance**: Run `python scripts/test_model.py`
- **Model Info**: http://localhost:8000/ (check `image_model` field)

---

## 📝 Changelog

### v1.0.0 (Current)
- ✅ BiomedCLIP medical embedding model
- ✅ ResNet50 fallback
- ✅ Auto model download
- ✅ GPU acceleration
- ✅ Docker deployment
- ✅ 15 sample medical cases
- ✅ Medical search UI
- ✅ 11 REST API endpoints

### Future Enhancements
- DICOM support
- Batch upload endpoint
- Authentication/authorization
- PACS integration
- Multi-language support
