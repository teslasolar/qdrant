"""
Chazon OS Backend API
FastAPI service for Qdrant and embeddings - Medical Imaging Focus
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import io
import base64
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Qdrant client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

# Embeddings (choose one)
try:
    import cohere
    COHERE_AVAILABLE = True
except ImportError:
    COHERE_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Image processing
try:
    from PIL import Image
    import numpy as np
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

load_dotenv()

app = FastAPI(title="Chazon OS API", version="1.0.0")

# CORS for GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY")
)

if COHERE_AVAILABLE:
    cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

if OPENAI_AVAILABLE:
    openai.api_key = os.getenv("OPENAI_API_KEY")


# Models
class SearchRequest(BaseModel):
    query: str
    collection: str = "medical_images"
    limit: int = 5
    filter: Optional[Dict[str, Any]] = None

class IndexRequest(BaseModel):
    text: str
    collection: str
    metadata: dict

class EmbedRequest(BaseModel):
    text: str
    model: str = "cohere"  # or "openai"

class MedicalImageRequest(BaseModel):
    image_base64: str
    metadata: Dict[str, Any]
    collection: str = "medical_images"

class MedicalSearchRequest(BaseModel):
    query: Optional[str] = None
    image_base64: Optional[str] = None
    collection: str = "medical_images"
    limit: int = 5
    body_part: Optional[str] = None
    modality: Optional[str] = None


# Endpoints

@app.get("/")
async def root():
    return {
        "name": "Chazon OS API",
        "version": "1.0.0",
        "qdrant": "connected",
        "cohere": COHERE_AVAILABLE,
        "openai": OPENAI_AVAILABLE
    }

@app.get("/health")
async def health():
    try:
        collections = qdrant.get_collections()
        return {
            "status": "healthy",
            "qdrant": "ok",
            "collections": len(collections.collections)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.post("/collections/{name}/create")
async def create_collection(name: str, dimension: int = 512):
    """Create a Qdrant collection"""
    try:
        qdrant.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
        )
        return {"collection": name, "dimension": dimension, "created": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed")
async def generate_embedding(request: EmbedRequest):
    """Generate text embedding"""
    try:
        if request.model == "cohere" and COHERE_AVAILABLE:
            response = cohere_client.embed(
                texts=[request.text],
                model="embed-english-v3.0"
            )
            return {
                "embedding": response.embeddings[0],
                "dimension": len(response.embeddings[0]),
                "model": "cohere"
            }

        elif request.model == "openai" and OPENAI_AVAILABLE:
            response = openai.Embedding.create(
                input=request.text,
                model="text-embedding-3-large"
            )
            return {
                "embedding": response['data'][0]['embedding'],
                "dimension": len(response['data'][0]['embedding']),
                "model": "openai"
            }

        else:
            raise HTTPException(status_code=400, detail="Model not available")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_vectors(request: SearchRequest):
    """Search Qdrant collection"""
    try:
        # Generate embedding for query
        if COHERE_AVAILABLE:
            embed_response = cohere_client.embed(
                texts=[request.query],
                model="embed-english-v3.0"
            )
            query_vector = embed_response.embeddings[0]
        else:
            raise HTTPException(status_code=400, detail="No embedding model available")

        # Search Qdrant
        results = qdrant.search(
            collection_name=request.collection,
            query_vector=query_vector,
            limit=request.limit
        )

        return {
            "results": [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload
                }
                for hit in results
            ],
            "count": len(results)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index")
async def index_document(request: IndexRequest):
    """Index document in Qdrant"""
    try:
        # Generate embedding
        if COHERE_AVAILABLE:
            embed_response = cohere_client.embed(
                texts=[request.text],
                model="embed-english-v3.0"
            )
            vector = embed_response.embeddings[0]
        else:
            raise HTTPException(status_code=400, detail="No embedding model available")

        # Generate UUID
        import uuid
        point_id = str(uuid.uuid4())

        # Upsert to Qdrant
        qdrant.upsert(
            collection_name=request.collection,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=request.metadata
                )
            ]
        )

        return {
            "id": point_id,
            "indexed": True,
            "collection": request.collection
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/collections")
async def list_collections():
    """List all Qdrant collections"""
    try:
        collections = qdrant.get_collections()
        return {
            "collections": [
                {
                    "name": col.name,
                    "vectors_count": qdrant.count(col.name).count
                }
                for col in collections.collections
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Medical Imaging Endpoints

def process_medical_image(image_base64: str) -> np.ndarray:
    """Process base64 image to numpy array"""
    if not PIL_AVAILABLE:
        raise HTTPException(status_code=500, detail="PIL not available - install: pip install pillow")

    # Remove data URL prefix if present
    if ',' in image_base64:
        image_base64 = image_base64.split(',')[1]

    # Decode base64
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes))

    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Resize to standard size (224x224 for CLIP)
    image = image.resize((224, 224))

    # Convert to numpy array
    image_array = np.array(image)

    return image_array


def generate_image_embedding(image_array: np.ndarray, model: str = "clip") -> List[float]:
    """Generate embedding from image array

    Note: This is a placeholder using text-based embeddings.
    For production, integrate actual image embedding models:
    - CLIP (OpenAI)
    - BiomedCLIP (Microsoft)
    - MedCLIP (Stanford)
    """

    # For now, create a simple feature vector from image statistics
    # In production, use actual image embeddings
    features = []

    # Color channels mean
    features.extend(image_array.mean(axis=(0, 1)).tolist())

    # Color channels std
    features.extend(image_array.std(axis=(0, 1)).tolist())

    # Histogram features (simplified)
    for channel in range(3):
        hist, _ = np.histogram(image_array[:, :, channel], bins=10, range=(0, 256))
        features.extend((hist / hist.sum()).tolist())

    # Pad to 512 dimensions (standard for CLIP)
    while len(features) < 512:
        features.append(0.0)

    return features[:512]


@app.post("/medical/upload")
async def upload_medical_image(
    file: UploadFile = File(...),
    patient_id: str = Form("UNKNOWN"),
    body_part: str = Form("CHEST"),
    modality: str = Form("XRAY"),
    diagnosis: str = Form(""),
    notes: str = Form("")
):
    """Upload and index medical image"""
    try:
        # Read image file
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode('utf-8')

        # Process image
        image_array = process_medical_image(image_base64)

        # Generate embedding
        embedding = generate_image_embedding(image_array)

        # Generate unique ID
        image_id = str(uuid.uuid4())

        # Metadata
        metadata = {
            "id": image_id,
            "patient_id": patient_id,
            "body_part": body_part.upper(),
            "modality": modality.upper(),
            "diagnosis": diagnosis,
            "notes": notes,
            "filename": file.filename,
            "upload_date": datetime.now().isoformat(),
            "image_base64": f"data:image/jpeg;base64,{image_base64}"
        }

        # Index in Qdrant
        qdrant.upsert(
            collection_name="medical_images",
            points=[
                PointStruct(
                    id=image_id,
                    vector=embedding,
                    payload=metadata
                )
            ]
        )

        return {
            "success": True,
            "id": image_id,
            "metadata": metadata,
            "embedding_dim": len(embedding)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/medical/analyze")
async def analyze_medical_image(request: MedicalImageRequest):
    """Analyze medical image and find similar cases"""
    try:
        # Process image
        image_array = process_medical_image(request.image_base64)

        # Generate embedding
        query_vector = generate_image_embedding(image_array)

        # Build filter if metadata provided
        filter_conditions = None
        if request.metadata.get('body_part'):
            filter_conditions = Filter(
                must=[
                    FieldCondition(
                        key="body_part",
                        match=MatchValue(value=request.metadata['body_part'].upper())
                    )
                ]
            )

        # Search for similar images
        results = qdrant.search(
            collection_name=request.collection,
            query_vector=query_vector,
            limit=5,
            query_filter=filter_conditions
        )

        # Format results
        similar_cases = [
            {
                "id": hit.id,
                "score": hit.score,
                "patient_id": hit.payload.get("patient_id"),
                "body_part": hit.payload.get("body_part"),
                "modality": hit.payload.get("modality"),
                "diagnosis": hit.payload.get("diagnosis"),
                "notes": hit.payload.get("notes"),
                "image_url": hit.payload.get("image_base64", "")
            }
            for hit in results
        ]

        return {
            "success": True,
            "analyzed_image": {
                "embedding_dim": len(query_vector),
                "metadata": request.metadata
            },
            "similar_cases": similar_cases,
            "count": len(similar_cases)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/medical/search")
async def search_medical_images(request: MedicalSearchRequest):
    """Search medical images by text query or image similarity"""
    try:
        query_vector = None

        # Generate embedding from image if provided
        if request.image_base64:
            image_array = process_medical_image(request.image_base64)
            query_vector = generate_image_embedding(image_array)

        # Generate embedding from text if provided
        elif request.query:
            if COHERE_AVAILABLE:
                embed_response = cohere_client.embed(
                    texts=[request.query],
                    model="embed-english-v3.0"
                )
                query_vector = embed_response.embeddings[0]
            else:
                raise HTTPException(status_code=400, detail="No embedding model available")

        else:
            raise HTTPException(status_code=400, detail="Either query or image_base64 must be provided")

        # Build filter
        filter_conditions = None
        must_conditions = []

        if request.body_part:
            must_conditions.append(
                FieldCondition(
                    key="body_part",
                    match=MatchValue(value=request.body_part.upper())
                )
            )

        if request.modality:
            must_conditions.append(
                FieldCondition(
                    key="modality",
                    match=MatchValue(value=request.modality.upper())
                )
            )

        if must_conditions:
            filter_conditions = Filter(must=must_conditions)

        # Search Qdrant
        results = qdrant.search(
            collection_name=request.collection,
            query_vector=query_vector,
            limit=request.limit,
            query_filter=filter_conditions
        )

        return {
            "results": [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload
                }
                for hit in results
            ],
            "count": len(results)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/medical/stats")
async def get_medical_stats():
    """Get statistics about medical image collection"""
    try:
        collection_info = qdrant.get_collection("medical_images")

        # Get all points to calculate stats
        points = qdrant.scroll(
            collection_name="medical_images",
            limit=1000
        )[0]

        # Count by body part
        body_parts = {}
        modalities = {}

        for point in points:
            bp = point.payload.get("body_part", "UNKNOWN")
            mod = point.payload.get("modality", "UNKNOWN")

            body_parts[bp] = body_parts.get(bp, 0) + 1
            modalities[mod] = modalities.get(mod, 0) + 1

        return {
            "total_images": len(points),
            "vector_dimension": collection_info.config.params.vectors.size,
            "body_parts": body_parts,
            "modalities": modalities
        }

    except Exception as e:
        return {
            "total_images": 0,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
