// Qdrant Vector Search for Medical Imaging
// ISA-95 Level 3 - MES Operations

class VectorSearch {
  constructor(qdrantUrl = 'http://localhost:6333') {
    this.url = qdrantUrl;
    this.collection = 'medical_images';
  }

  // Search similar images
  async searchSimilar(embedding, limit = 5, filter = null) {
    const payload = {
      vector: embedding,
      limit: limit,
      with_payload: true,
      with_vector: false
    };

    if (filter) payload.filter = filter;

    const response = await fetch(`${this.url}/collections/${this.collection}/points/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    return await response.json();
  }

  // Upload image vector
  async uploadVector(id, embedding, metadata) {
    const point = {
      id: id,
      vector: embedding,
      payload: metadata
    };

    const response = await fetch(`${this.url}/collections/${this.collection}/points`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ points: [point] })
    });

    return await response.json();
  }

  // Filter by modality
  async searchByModality(embedding, modality, limit = 5) {
    return await this.searchSimilar(embedding, limit, {
      must: [{ key: 'modality', match: { value: modality } }]
    });
  }

  // Get collection stats
  async getStats() {
    const response = await fetch(`${this.url}/collections/${this.collection}`);
    return await response.json();
  }
}

export default VectorSearch;
