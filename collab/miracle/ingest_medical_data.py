"""
Medical Image Data Ingestion Script
Populates Qdrant with sample medical imaging cases

Usage:
    python ingest_medical_data.py
"""

import os
import asyncio
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
import numpy as np
from datetime import datetime, timedelta

load_dotenv()

# Initialize Qdrant client
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "medical_images"
VECTOR_DIM = 512


def create_collection():
    """Create medical images collection in Qdrant"""
    try:
        # Check if collection exists
        collections = qdrant.get_collections().collections
        if any(col.name == COLLECTION_NAME for col in collections):
            print(f"⚠️  Collection '{COLLECTION_NAME}' already exists. Deleting...")
            qdrant.delete_collection(COLLECTION_NAME)

        # Create new collection
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE)
        )
        print(f"✅ Created collection: {COLLECTION_NAME} (dim={VECTOR_DIM})")
    except Exception as e:
        print(f"❌ Error creating collection: {e}")
        raise


def generate_synthetic_embedding(seed: int, base_pattern: str = "normal") -> list:
    """Generate synthetic medical image embedding

    Args:
        seed: Random seed for reproducibility
        base_pattern: 'normal', 'pneumonia', 'fracture', 'tumor', etc.

    Returns:
        512-dimensional vector
    """
    np.random.seed(seed)

    # Base patterns (simplified medical image features)
    patterns = {
        "normal": np.random.normal(0.5, 0.1, VECTOR_DIM),
        "pneumonia": np.random.normal(0.7, 0.15, VECTOR_DIM),  # Brighter (infiltrates)
        "fracture": np.random.normal(0.4, 0.2, VECTOR_DIM),    # High contrast
        "tumor": np.random.normal(0.6, 0.12, VECTOR_DIM),      # Localized density
        "edema": np.random.normal(0.55, 0.18, VECTOR_DIM),     # Fluid accumulation
        "effusion": np.random.normal(0.65, 0.14, VECTOR_DIM),  # Fluid collection
        "arthritis": np.random.normal(0.5, 0.16, VECTOR_DIM)   # Joint changes
    }

    base = patterns.get(base_pattern, patterns["normal"])

    # Add some noise to make each image unique
    noise = np.random.normal(0, 0.05, VECTOR_DIM)
    embedding = base + noise

    # Normalize to [0, 1] range
    embedding = np.clip(embedding, 0, 1)

    return embedding.tolist()


# Sample medical cases dataset
MEDICAL_CASES = [
    # Chest X-Rays - Normal
    {
        "patient_id": "P001",
        "body_part": "CHEST",
        "modality": "XRAY",
        "diagnosis": "Normal",
        "notes": "Clear lung fields, normal heart size, no acute findings",
        "pattern": "normal",
        "age": 45,
        "sex": "M"
    },
    {
        "patient_id": "P002",
        "body_part": "CHEST",
        "modality": "XRAY",
        "diagnosis": "Normal",
        "notes": "Unremarkable chest radiograph, age-appropriate findings",
        "pattern": "normal",
        "age": 32,
        "sex": "F"
    },

    # Chest X-Rays - Pneumonia
    {
        "patient_id": "P003",
        "body_part": "CHEST",
        "modality": "XRAY",
        "diagnosis": "Pneumonia (Right Lower Lobe)",
        "notes": "Consolidation in right lower lobe consistent with pneumonia. Clinical correlation recommended.",
        "pattern": "pneumonia",
        "age": 67,
        "sex": "M"
    },
    {
        "patient_id": "P004",
        "body_part": "CHEST",
        "modality": "XRAY",
        "diagnosis": "Bilateral Pneumonia",
        "notes": "Bilateral infiltrates, concerning for community-acquired pneumonia or COVID-19",
        "pattern": "pneumonia",
        "age": 54,
        "sex": "F"
    },
    {
        "patient_id": "P005",
        "body_part": "CHEST",
        "modality": "XRAY",
        "diagnosis": "Pneumonia (Left Upper Lobe)",
        "notes": "Left upper lobe consolidation with air bronchograms",
        "pattern": "pneumonia",
        "age": 71,
        "sex": "M"
    },

    # Chest X-Rays - Other pathologies
    {
        "patient_id": "P006",
        "body_part": "CHEST",
        "modality": "XRAY",
        "diagnosis": "Pleural Effusion",
        "notes": "Large right-sided pleural effusion. Thoracentesis recommended.",
        "pattern": "effusion",
        "age": 59,
        "sex": "F"
    },
    {
        "patient_id": "P007",
        "body_part": "CHEST",
        "modality": "XRAY",
        "diagnosis": "Pulmonary Edema",
        "notes": "Bilateral perihilar infiltrates consistent with pulmonary edema. CHF suspected.",
        "pattern": "edema",
        "age": 78,
        "sex": "M"
    },

    # Hand X-Rays
    {
        "patient_id": "P008",
        "body_part": "HAND",
        "modality": "XRAY",
        "diagnosis": "Fracture (Distal Radius)",
        "notes": "Colles fracture of distal radius with dorsal angulation",
        "pattern": "fracture",
        "age": 62,
        "sex": "F"
    },
    {
        "patient_id": "P009",
        "body_part": "HAND",
        "modality": "XRAY",
        "diagnosis": "Arthritis (Rheumatoid)",
        "notes": "Erosive changes in MCP joints, joint space narrowing",
        "pattern": "arthritis",
        "age": 56,
        "sex": "F"
    },
    {
        "patient_id": "P010",
        "body_part": "HAND",
        "modality": "XRAY",
        "diagnosis": "Normal",
        "notes": "Normal hand radiograph, no fracture or dislocation",
        "pattern": "normal",
        "age": 28,
        "sex": "M"
    },

    # Head CT Scans
    {
        "patient_id": "P011",
        "body_part": "HEAD",
        "modality": "CT",
        "diagnosis": "Normal",
        "notes": "No acute intracranial abnormality, normal brain parenchyma",
        "pattern": "normal",
        "age": 42,
        "sex": "M"
    },
    {
        "patient_id": "P012",
        "body_part": "HEAD",
        "modality": "CT",
        "diagnosis": "Brain Tumor (Glioblastoma)",
        "notes": "Large heterogeneous mass in right frontal lobe with surrounding edema",
        "pattern": "tumor",
        "age": 58,
        "sex": "M"
    },

    # Abdomen CT
    {
        "patient_id": "P013",
        "body_part": "ABDOMEN",
        "modality": "CT",
        "diagnosis": "Normal",
        "notes": "Normal abdominal CT, no acute abnormality",
        "pattern": "normal",
        "age": 39,
        "sex": "F"
    },
    {
        "patient_id": "P014",
        "body_part": "ABDOMEN",
        "modality": "CT",
        "diagnosis": "Kidney Stone (Left)",
        "notes": "4mm calculus in left proximal ureter causing mild hydronephrosis",
        "pattern": "normal",  # Using normal pattern as base
        "age": 47,
        "sex": "M"
    },

    # Knee MRI
    {
        "patient_id": "P015",
        "body_part": "KNEE",
        "modality": "MRI",
        "diagnosis": "Meniscal Tear (Medial)",
        "notes": "Vertical tear of medial meniscus posterior horn",
        "pattern": "fracture",  # Similar feature pattern
        "age": 34,
        "sex": "M"
    },
]


def ingest_medical_cases():
    """Ingest medical cases into Qdrant"""
    print(f"\n🔄 Ingesting {len(MEDICAL_CASES)} medical cases...")

    points = []

    for idx, case in enumerate(MEDICAL_CASES):
        # Generate embedding based on pathology pattern
        embedding = generate_synthetic_embedding(
            seed=1000 + idx,
            base_pattern=case.get("pattern", "normal")
        )

        # Create point
        point_id = str(uuid.uuid4())

        # Add metadata
        metadata = {
            "id": point_id,
            "patient_id": case["patient_id"],
            "body_part": case["body_part"],
            "modality": case["modality"],
            "diagnosis": case["diagnosis"],
            "notes": case["notes"],
            "age": case.get("age", 0),
            "sex": case.get("sex", "U"),
            "upload_date": (datetime.now() - timedelta(days=idx)).isoformat(),
            "filename": f"{case['patient_id']}_{case['body_part'].lower()}.dcm"
        }

        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload=metadata
        )

        points.append(point)

        print(f"  ✓ {case['patient_id']}: {case['body_part']} - {case['diagnosis']}")

    # Upsert all points
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"\n✅ Successfully ingested {len(points)} medical cases")


def verify_ingestion():
    """Verify data was ingested correctly"""
    print("\n🔍 Verifying ingestion...")

    try:
        # Get collection info
        collection_info = qdrant.get_collection(COLLECTION_NAME)
        vectors_count = collection_info.points_count

        print(f"  Collection: {COLLECTION_NAME}")
        print(f"  Total vectors: {vectors_count}")
        print(f"  Dimension: {collection_info.config.params.vectors.size}")
        print(f"  Distance: {collection_info.config.params.vectors.distance}")

        # Get sample points
        points = qdrant.scroll(
            collection_name=COLLECTION_NAME,
            limit=5
        )[0]

        # Count by body part and diagnosis
        all_points = qdrant.scroll(
            collection_name=COLLECTION_NAME,
            limit=1000
        )[0]

        body_parts = {}
        modalities = {}
        diagnoses = {}

        for point in all_points:
            bp = point.payload.get("body_part", "UNKNOWN")
            mod = point.payload.get("modality", "UNKNOWN")
            diag = point.payload.get("diagnosis", "UNKNOWN")

            body_parts[bp] = body_parts.get(bp, 0) + 1
            modalities[mod] = modalities.get(mod, 0) + 1
            diagnoses[diag] = diagnoses.get(diag, 0) + 1

        print(f"\n  Body Parts:")
        for bp, count in sorted(body_parts.items()):
            print(f"    {bp}: {count}")

        print(f"\n  Modalities:")
        for mod, count in sorted(modalities.items()):
            print(f"    {mod}: {count}")

        print(f"\n  Diagnoses:")
        for diag, count in sorted(diagnoses.items()):
            print(f"    {diag}: {count}")

        print(f"\n✅ Verification complete")

    except Exception as e:
        print(f"❌ Verification failed: {e}")


def test_search():
    """Test similarity search"""
    print("\n🔎 Testing similarity search...")

    try:
        # Generate query embedding for pneumonia case
        query_vector = generate_synthetic_embedding(seed=5000, base_pattern="pneumonia")

        # Search
        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )

        print(f"\n  Query: Pneumonia-like pattern")
        print(f"  Top 3 similar cases:\n")

        for i, hit in enumerate(results, 1):
            print(f"  {i}. Score: {hit.score:.3f}")
            print(f"     Patient: {hit.payload['patient_id']}")
            print(f"     Diagnosis: {hit.payload['diagnosis']}")
            print(f"     Body Part: {hit.payload['body_part']}")
            print()

        print(f"✅ Search test complete")

    except Exception as e:
        print(f"❌ Search test failed: {e}")


def main():
    """Main ingestion pipeline"""
    print("=" * 60)
    print("🏥 MEDICAL IMAGING DATA INGESTION")
    print("=" * 60)

    try:
        # Step 1: Create collection
        create_collection()

        # Step 2: Ingest data
        ingest_medical_cases()

        # Step 3: Verify
        verify_ingestion()

        # Step 4: Test search
        test_search()

        print("\n" + "=" * 60)
        print("✅ INGESTION COMPLETE!")
        print("=" * 60)
        print(f"\nCollection '{COLLECTION_NAME}' is ready for use.")
        print(f"Total medical cases: {len(MEDICAL_CASES)}")
        print("\nYou can now:")
        print("  1. Start the backend API: python api.py")
        print("  2. Test search: curl http://localhost:8000/medical/stats")
        print("  3. Open the medical viewer UI")

    except Exception as e:
        print(f"\n❌ INGESTION FAILED: {e}")
        raise


if __name__ == "__main__":
    main()
