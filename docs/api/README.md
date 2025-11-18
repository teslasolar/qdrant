# API Documentation

Comprehensive API documentation for the Qdrant Medical Imaging SCADA system.

## Quick Links

- **FastAPI Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (Alternative documentation)
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Base URL

```
Development: http://localhost:8000
Production: https://teslasolar.github.io/qdrant/api
```

## Authentication

```python
# Example: Bearer token authentication
headers = {
    "Authorization": "Bearer YOUR_API_KEY"
}
```

## Core Endpoints

### Health Check
```http
GET /api/health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-17T12:00:00Z"
}
```

### Medical Image Search
```http
POST /api/medical/search
Content-Type: application/json

{
  "image_url": "...",
  "modality": "CT",
  "limit": 5
}
```

**Response**:
```json
{
  "results": [
    {
      "study_id": "ST001",
      "similarity_score": 0.95,
      "metadata": {...}
    }
  ]
}
```

### Vector Embeddings
```http
POST /api/embeddings/generate
Content-Type: application/json

{
  "text": "chest x-ray pneumonia",
  "model": "BiomedCLIP"
}
```

### Qdrant Integration
```http
POST /api/qdrant/search
Content-Type: application/json

{
  "query_vector": [...],
  "collection": "medical_images",
  "limit": 10
}
```

## Standard Instantiation API
```http
POST /api/standards/instantiate
Content-Type: application/json

{
  "standard_id": "packml-v1.0",
  "instance_id": "ct_scanner_1",
  "parameters": {
    "equipmentPath": "Medical/CT_Scanner_1"
  }
}
```

## AlF-DETECT Screening
```http
POST /api/alf-detect/screen
Content-Type: multipart/form-data

image: <file>
modality: X-Ray
```

**Response**:
```json
{
  "alzheimers_probability": 0.73,
  "autism_probability": 0.12,
  "confidence": 0.89,
  "brain_regions": {
    "hippocampus": 0.85,
    "frontal_cortex": 0.67
  }
}
```

## Error Handling

All errors follow this format:
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Detailed error message",
    "details": {...}
  }
}
```

## Rate Limiting

- Default: 100 requests/minute per IP
- Authenticated: 1000 requests/minute per API key

## Examples

See `docs/api/EXAMPLES.md` for complete code examples in Python, JavaScript, and cURL.

## SDK Support

- Python: `pip install qdrant-client`
- JavaScript/TypeScript: `npm install @qdrant/js-client-rest`
