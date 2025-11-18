# Qdrant Client
**Real Vector DB Connection** | Backend Integration

Client for connecting Chazon OS to real Qdrant backend API.

```javascript
const QdrantClient = {
  baseURL: 'http://localhost:8000',
  timeout: 30000, // 30s timeout

  async _fetch(url, options = {}) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return response.json();
    } catch (err) {
      clearTimeout(timeoutId);
      if (err.name === 'AbortError') {
        throw new Error('Request timeout - backend may be offline');
      }
      throw err;
    }
  },

  async createCollection(name, dimension = 512) {
    return this._fetch(`${this.baseURL}/collections/${name}/create?dimension=${dimension}`, {
      method: 'POST'
    });
  },

  async embed(text, model = 'cohere') {
    return this._fetch(`${this.baseURL}/embed`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, model })
    });
  },

  async search(query, collection = 'medical_images', limit = 5) {
    return this._fetch(`${this.baseURL}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, collection, limit })
    });
  },

  async index(text, collection, metadata) {
    return this._fetch(`${this.baseURL}/index`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, collection, metadata })
    });
  },

  async listCollections() {
    return this._fetch(`${this.baseURL}/collections`);
  },

  async health() {
    return this._fetch(`${this.baseURL}/health`);
  },

  // Medical imaging endpoints
  async analyzeMedicalImage(imageBase64, metadata) {
    return this._fetch(`${this.baseURL}/medical/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_base64: imageBase64, metadata, collection: 'medical_images' })
    });
  },

  async searchMedicalImages(query, bodyPart, modality, limit = 5) {
    return this._fetch(`${this.baseURL}/medical/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, body_part: bodyPart, modality, limit, collection: 'medical_images' })
    });
  },

  async getMedicalStats() {
    return this._fetch(`${this.baseURL}/medical/stats`);
  },

  configure(url) {
    this.baseURL = url;
    console.log(`🔌 Qdrant client: ${url}`);
  }
};

window.QdrantClient = QdrantClient;
```
