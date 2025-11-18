# Medical Imaging API Documentation

FastAPI backend for medical image similarity search with Qdrant.

---

## Base URL

**Local:** `http://localhost:8000`
**Production:** Your deployed URL

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check backend and Qdrant connection status.

**Response:**
```json
{
  "status": "healthy",
  "qdrant": "ok",
  "collections": 1
}
```

---

### 2. Analyze Medical Image

**POST** `/medical/analyze`

Upload and analyze a medical image, finding similar cases.

**Request Body:**
```json
{
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "metadata": {
    "body_part": "CHEST",
    "modality": "XRAY",
    "notes": "Optional notes"
  },
  "collection": "medical_images"
}
```

**Response:**
```json
{
  "success": true,
  "analyzed_image": {
    "embedding_dim": 512,
    "metadata": {...}
  },
  "similar_cases": [
    {
      "id": "uuid-here",
      "score": 0.876,
      "patient_id": "P003",
      "body_part": "CHEST",
      "modality": "XRAY",
      "diagnosis": "Pneumonia",
      "notes": "Right lower lobe consolidation..."
    }
  ],
  "count": 5
}
```

---

### 3. Search Medical Images

**POST** `/medical/search`

Search by text query or image.

**Request Body (Text Search):**
```json
{
  "query": "chest x-ray pneumonia",
  "limit": 5,
  "body_part": "CHEST",
  "modality": "XRAY",
  "collection": "medical_images"
}
```

**Request Body (Image Search):**
```json
{
  "image_base64": "data:image/jpeg;base64,...",
  "limit": 5,
  "body_part": "CHEST"
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "uuid",
      "score": 0.92,
      "payload": {
        "patient_id": "P001",
        "diagnosis": "Pneumonia",
        ...
      }
    }
  ],
  "count": 5
}
```

---

### 4. Upload Medical Image

**POST** `/medical/upload`

Upload and index a new medical image.

**Request (multipart/form-data):**
```
file: <image file>
patient_id: P123
body_part: CHEST
modality: XRAY
diagnosis: Pneumonia
notes: Right lower lobe infiltrate
```

**Response:**
```json
{
  "success": true,
  "id": "uuid-here",
  "metadata": {...},
  "embedding_dim": 512
}
```

---

### 5. Get Statistics

**GET** `/medical/stats`

Get database statistics.

**Response:**
```json
{
  "total_images": 15,
  "vector_dimension": 512,
  "body_parts": {
    "CHEST": 7,
    "HEAD": 2,
    "HAND": 3,
    "ABDOMEN": 2,
    "KNEE": 1
  },
  "modalities": {
    "XRAY": 10,
    "CT": 3,
    "MRI": 2
  }
}
```

---

### 6. Create Collection

**POST** `/collections/{name}/create?dimension=512`

Create a new Qdrant collection.

**Response:**
```json
{
  "collection": "medical_images",
  "dimension": 512,
  "created": true
}
```

---

### 7. List Collections

**GET** `/collections`

List all Qdrant collections.

**Response:**
```json
{
  "collections": [
    {
      "name": "medical_images",
      "vectors_count": 15
    }
  ]
}
```

---

## Data Models

### Metadata Schema

```typescript
{
  id: string,              // UUID
  patient_id: string,      // Patient identifier
  body_part: string,       // CHEST, HEAD, ABDOMEN, HAND, KNEE, etc.
  modality: string,        // XRAY, CT, MRI, US
  diagnosis: string,       // Clinical diagnosis
  notes: string,           // Additional notes
  filename: string,        // Original filename
  upload_date: string,     // ISO timestamp
  age?: number,            // Patient age
  sex?: string,            // M, F, U
  image_base64?: string    // Base64 encoded image
}
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- **200** - Success
- **400** - Bad request (invalid input)
- **500** - Server error

**Error Response:**
```json
{
  "detail": "Error message here"
}
```

---

## Rate Limiting

Currently no rate limiting. Add for production:

```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/search")
@limiter.limit("10/minute")
async def search_vectors(...):
    ...
```

---

## Authentication

No authentication in demo. For production, add API key:

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(401, "Invalid API key")
```

---

## CORS

CORS is enabled for all origins (development only):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"]
)
```

---

## Deployment

### Railway.app
```bash
cd os/backend
railway up
```

### Fly.io
```bash
cd os/backend
fly deploy
```

### Docker
```bash
docker-compose up -d
```

---

## Examples

### Python
```python
import requests
import base64

# Read image
with open('xray.jpg', 'rb') as f:
    img_base64 = base64.b64encode(f.read()).decode()

# Analyze
response = requests.post(
    'http://localhost:8000/medical/analyze',
    json={
        'image_base64': f'data:image/jpeg;base64,{img_base64}',
        'metadata': {'body_part': 'CHEST', 'modality': 'XRAY'}
    }
)

results = response.json()
print(f"Found {results['count']} similar cases")
```

### JavaScript
```javascript
// Analyze image
const response = await fetch('http://localhost:8000/medical/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    image_base64: imageDataURL,
    metadata: {body_part: 'CHEST', modality: 'XRAY'}
  })
});

const data = await response.json();
console.log('Similar cases:', data.similar_cases);
```

### cURL
```bash
# Search by text
curl -X POST http://localhost:8000/medical/search \
  -H "Content-Type: application/json" \
  -d '{"query": "pneumonia", "body_part": "CHEST", "limit": 3}'
```

---

**API Version:** 1.0.0
**Powered by:** FastAPI + Qdrant
