/**
 * Qdrant Vector Database Client
 * Medical Imaging Similarity Search
 *
 * Implements vector search for medical images using Qdrant backend
 */

class QdrantClient {
  constructor(config = {}) {
    this.baseURL = config.baseURL || this.getAPIURL();
    this.timeout = config.timeout || 30000;
    this.collection = config.collection || 'medical_images';
    this.retries = config.retries || 3;
    this.connected = false;
  }

  /**
   * Get API URL from environment config
   */
  getAPIURL() {
    // Check if config is loaded
    if (window.chazonConfig) {
      const apiURL = window.chazonConfig.getEnv('api.base_url');
      if (apiURL) return apiURL;
    }

    // Check environment variable (Vercel runtime)
    if (typeof process !== 'undefined' && process.env.API_URL) {
      return process.env.API_URL;
    }

    // Default to localhost
    return 'http://localhost:8000';
  }

  /**
   * Fetch with timeout and retries
   */
  async _fetch(url, options = {}, attempt = 1) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        }
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (err) {
      clearTimeout(timeoutId);

      // Retry on network errors
      if (attempt < this.retries && (err.name === 'AbortError' || err.name === 'TypeError')) {
        console.warn(`Retry ${attempt}/${this.retries} for ${url}`);
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
        return this._fetch(url, options, attempt + 1);
      }

      if (err.name === 'AbortError') {
        throw new Error('Request timeout - Qdrant backend may be offline');
      }

      throw err;
    }
  }

  /**
   * Health check
   */
  async health() {
    try {
      const result = await this._fetch(`${this.baseURL}/health`);
      this.connected = true;
      return result;
    } catch (err) {
      this.connected = false;
      throw err;
    }
  }

  /**
   * List all collections
   */
  async listCollections() {
    return this._fetch(`${this.baseURL}/collections`);
  }

  /**
   * Create a new collection
   */
  async createCollection(name, dimension = 512) {
    return this._fetch(`${this.baseURL}/collections/${name}/create?dimension=${dimension}`, {
      method: 'POST'
    });
  }

  /**
   * Get collection info
   */
  async getCollectionInfo(name = this.collection) {
    return this._fetch(`${this.baseURL}/collections/${name}`);
  }

  /**
   * Generate text embedding
   */
  async embed(text, model = 'cohere') {
    return this._fetch(`${this.baseURL}/embed`, {
      method: 'POST',
      body: JSON.stringify({ text, model })
    });
  }

  /**
   * Generic vector search
   */
  async search(query, collection = this.collection, limit = 5, filter = null) {
    return this._fetch(`${this.baseURL}/search`, {
      method: 'POST',
      body: JSON.stringify({
        query,
        collection,
        limit,
        filter
      })
    });
  }

  /**
   * Index text into collection
   */
  async index(text, collection, metadata) {
    return this._fetch(`${this.baseURL}/index`, {
      method: 'POST',
      body: JSON.stringify({
        text,
        collection,
        metadata
      })
    });
  }

  // ========================================
  // Medical Imaging Specific Methods
  // ========================================

  /**
   * Analyze medical image (generate embedding + metadata)
   */
  async analyzeMedicalImage(imageBase64, metadata = {}) {
    return this._fetch(`${this.baseURL}/medical/analyze`, {
      method: 'POST',
      body: JSON.stringify({
        image_base64: imageBase64,
        metadata,
        collection: this.collection
      })
    });
  }

  /**
   * Search similar medical images
   */
  async searchMedicalImages(params = {}) {
    const {
      query = null,
      imageBase64 = null,
      bodyPart = null,
      modality = null,
      diagnosis = null,
      limit = 5
    } = params;

    return this._fetch(`${this.baseURL}/medical/search`, {
      method: 'POST',
      body: JSON.stringify({
        query,
        image_base64: imageBase64,
        body_part: bodyPart,
        modality,
        diagnosis,
        limit,
        collection: this.collection
      })
    });
  }

  /**
   * Get medical imaging statistics
   */
  async getMedicalStats() {
    return this._fetch(`${this.baseURL}/medical/stats`);
  }

  /**
   * Search by body part
   */
  async searchByBodyPart(bodyPart, limit = 10) {
    return this.searchMedicalImages({ bodyPart, limit });
  }

  /**
   * Search by modality (CT, MRI, XRAY, etc.)
   */
  async searchByModality(modality, limit = 10) {
    return this.searchMedicalImages({ modality, limit });
  }

  /**
   * Search by diagnosis
   */
  async searchByDiagnosis(diagnosis, limit = 10) {
    return this.searchMedicalImages({ diagnosis, limit });
  }

  /**
   * Find similar cases to uploaded image
   */
  async findSimilarCases(imageFile, options = {}) {
    try {
      // Convert file to base64
      const base64 = await this.fileToBase64(imageFile);

      // Search
      return this.searchMedicalImages({
        imageBase64: base64,
        bodyPart: options.bodyPart,
        modality: options.modality,
        limit: options.limit || 5
      });
    } catch (err) {
      throw new Error(`Failed to find similar cases: ${err.message}`);
    }
  }

  /**
   * Upload and index medical image
   */
  async uploadMedicalImage(imageFile, metadata = {}) {
    try {
      // Convert to base64
      const base64 = await this.fileToBase64(imageFile);

      // Analyze and index
      return this.analyzeMedicalImage(base64, {
        filename: imageFile.name,
        size: imageFile.size,
        upload_date: new Date().toISOString(),
        ...metadata
      });
    } catch (err) {
      throw new Error(`Failed to upload medical image: ${err.message}`);
    }
  }

  /**
   * Search with text query (natural language)
   */
  async searchWithQuery(queryText, options = {}) {
    return this.searchMedicalImages({
      query: queryText,
      bodyPart: options.bodyPart,
      modality: options.modality,
      limit: options.limit || 5
    });
  }

  // ========================================
  // Utility Methods
  // ========================================

  /**
   * Convert File to base64
   */
  fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        // Remove data:image/...;base64, prefix
        const base64 = reader.result.split(',')[1];
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  /**
   * Configure client
   */
  configure(config) {
    if (config.baseURL) this.baseURL = config.baseURL;
    if (config.collection) this.collection = config.collection;
    if (config.timeout) this.timeout = config.timeout;

    console.log(`🔌 Qdrant client configured: ${this.baseURL}`);
  }

  /**
   * Get connection status
   */
  isConnected() {
    return this.connected;
  }

  /**
   * Test connection with health check
   */
  async testConnection() {
    try {
      const health = await this.health();
      console.log('✓ Qdrant backend connected:', health);
      return true;
    } catch (err) {
      console.error('✗ Qdrant backend offline:', err.message);
      return false;
    }
  }

  /**
   * Get backend info
   */
  getInfo() {
    return {
      baseURL: this.baseURL,
      collection: this.collection,
      timeout: this.timeout,
      connected: this.connected,
      retries: this.retries
    };
  }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = QdrantClient;
}

// Global instance
window.QdrantClient = QdrantClient;

// Create default instance
window.qdrantClient = new QdrantClient();

// Auto-test connection on load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', async () => {
    await window.qdrantClient.testConnection();
  });
} else {
  window.qdrantClient.testConnection();
}

export default QdrantClient;
