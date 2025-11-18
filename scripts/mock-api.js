// Mock API for Demo Mode
// Provides realistic responses without requiring real AI models or backend

class MockAPI {
  constructor(config) {
    this.config = config || window.chazonConfig;
    this.mockLatency = config?.get('dev_tools.mock_latency_ms', 200);
  }

  // Simulate network latency
  async delay(ms = null) {
    const delayMs = ms || this.mockLatency;
    return new Promise(resolve => setTimeout(resolve, delayMs));
  }

  // Generate random value in range
  random(min, max) {
    return Math.random() * (max - min) + min;
  }

  // Mock Segmentation
  async segmentImage(imageData, organType, model = 'unet') {
    const processingTime = this.config?.get('mock_data.ai.segmentation.processing_time_ms', 500);
    const confMin = this.config?.get('mock_data.ai.segmentation.confidence_min', 0.85);
    const confMax = this.config?.get('mock_data.ai.segmentation.confidence_max', 0.98);

    await this.delay(processingTime);

    // Generate mock segmentation mask (binary array)
    const width = 256;
    const height = 256;
    const mask = this.generateMockMask(width, height, organType);

    return {
      success: true,
      model: model,
      organType: organType,
      mask: mask,
      maskDimensions: { width, height },
      confidence: this.random(confMin, confMax),
      processingTimeMs: processingTime,
      timestamp: new Date().toISOString(),
      metadata: {
        pixelCount: mask.filter(p => p === 1).length,
        coverage: (mask.filter(p => p === 1).length / mask.length) * 100
      }
    };
  }

  // Mock Detection
  async detectObjects(imageData, targetType, model = 'yolov8') {
    const processingTime = this.config?.get('mock_data.ai.detection.processing_time_ms', 300);
    const detMin = this.config?.get('mock_data.ai.detection.detections_min', 1);
    const detMax = this.config?.get('mock_data.ai.detection.detections_max', 5);
    const confMin = this.config?.get('mock_data.ai.detection.confidence_min', 0.80);
    const confMax = this.config?.get('mock_data.ai.detection.confidence_max', 0.95);

    await this.delay(processingTime);

    const numDetections = Math.floor(this.random(detMin, detMax + 1));
    const detections = [];

    for (let i = 0; i < numDetections; i++) {
      detections.push({
        id: `det_${i}`,
        class: targetType,
        confidence: this.random(confMin, confMax),
        bbox: {
          x: Math.floor(this.random(50, 450)),
          y: Math.floor(this.random(50, 450)),
          width: Math.floor(this.random(30, 100)),
          height: Math.floor(this.random(30, 100))
        },
        size_mm: this.random(5, 25).toFixed(1)
      });
    }

    return {
      success: true,
      model: model,
      targetType: targetType,
      detections: detections,
      count: detections.length,
      processingTimeMs: processingTime,
      timestamp: new Date().toISOString()
    };
  }

  // Mock Classification
  async classifyImage(imageData, model = 'biomedclip') {
    const processingTime = this.config?.get('mock_data.ai.classification.processing_time_ms', 200);
    const confMin = this.config?.get('mock_data.ai.classification.confidence_min', 0.75);
    const confMax = this.config?.get('mock_data.ai.classification.confidence_max', 0.99);

    await this.delay(processingTime);

    if (model === 'biomedclip') {
      // Generate 768-dim embedding
      const embedding = Array.from({ length: 768 }, () => this.random(-1, 1));

      return {
        success: true,
        model: model,
        embedding: embedding,
        dimension: 768,
        processingTimeMs: processingTime,
        timestamp: new Date().toISOString()
      };
    } else {
      // Classification result
      const classes = ['Normal', 'Abnormal', 'Suspicious', 'Artifact'];
      const topClass = classes[Math.floor(this.random(0, classes.length))];

      return {
        success: true,
        model: model,
        class: topClass,
        confidence: this.random(confMin, confMax),
        top5: classes.map(c => ({
          class: c,
          probability: this.random(0.1, 0.9)
        })).sort((a, b) => b.probability - a.probability).slice(0, 5),
        processingTimeMs: processingTime,
        timestamp: new Date().toISOString()
      };
    }
  }

  // Mock AlF-DETECT Screening
  async screenAlzheimers(xrayData) {
    const processingTime = this.config?.get('mock_data.ai.alf_detect.processing_time_ms', 1000);
    const probability = this.config?.get('mock_data.ai.alf_detect.alzheimers_probability', 0.72);

    await this.delay(processingTime);

    const concentrations = {
      hippocampus: this.random(15, 45),
      cortex: this.random(10, 35),
      cerebellum: this.random(8, 25),
      white_matter: this.random(12, 30)
    };

    return {
      success: true,
      condition: 'alzheimers',
      probability: probability + this.random(-0.1, 0.1),
      risk: probability > 0.7 ? 'high' : probability > 0.5 ? 'medium' : 'low',
      concentrations: concentrations,
      threshold: 0.7,
      recommendation: probability > 0.7
        ? 'Consult neurologist for comprehensive evaluation'
        : 'Monitor and rescreen in 6 months',
      processingTimeMs: processingTime,
      timestamp: new Date().toISOString()
    };
  }

  // Mock Vector Search
  async searchSimilar(queryEmbedding, topK = 10) {
    const processingTime = this.config?.get('mock_data.vector_search.processing_time_ms', 150);
    const simMin = this.config?.get('mock_data.vector_search.similarity_min', 0.75);
    const simMax = this.config?.get('mock_data.vector_search.similarity_max', 0.99);

    await this.delay(processingTime);

    const results = [];
    for (let i = 0; i < topK; i++) {
      results.push({
        id: `case_${1000 + i}`,
        score: this.random(simMin, simMax - (i * 0.02)), // Decreasing scores
        metadata: {
          modality: ['X-Ray', 'CT', 'MRI'][Math.floor(this.random(0, 3))],
          diagnosis: ['Normal', 'Benign', 'Malignant', 'Suspicious'][Math.floor(this.random(0, 4))],
          age: Math.floor(this.random(20, 80)),
          gender: Math.random() > 0.5 ? 'M' : 'F'
        },
        thumbnail: `/examples/thumbnails/case_${1000 + i}.jpg`
      });
    }

    return {
      success: true,
      results: results,
      count: results.length,
      processingTimeMs: processingTime,
      timestamp: new Date().toISOString()
    };
  }

  // Mock Batch Processing
  async processBatch(files, pipeline) {
    const results = [];

    for (let i = 0; i < files.length; i++) {
      const file = files[i];

      // Progress callback
      if (pipeline.onProgress) {
        pipeline.onProgress({
          current: i + 1,
          total: files.length,
          filename: file.name,
          status: 'processing'
        });
      }

      // Simulate processing
      await this.delay(500);

      // Mock result based on pipeline type
      let result;
      if (pipeline.type === 'segmentation') {
        result = await this.segmentImage(file.data, pipeline.organType, pipeline.model);
      } else if (pipeline.type === 'detection') {
        result = await this.detectObjects(file.data, pipeline.targetType, pipeline.model);
      } else {
        result = await this.classifyImage(file.data, pipeline.model);
      }

      results.push({
        filename: file.name,
        fileId: file.id,
        result: result,
        success: true
      });
    }

    return {
      success: true,
      totalFiles: files.length,
      successCount: results.length,
      failedCount: 0,
      results: results,
      timestamp: new Date().toISOString()
    };
  }

  // Generate mock segmentation mask
  generateMockMask(width, height, organType) {
    const mask = new Array(width * height).fill(0);

    // Create elliptical region for organ
    const centerX = width / 2 + this.random(-20, 20);
    const centerY = height / 2 + this.random(-20, 20);
    const radiusX = width * 0.3;
    const radiusY = height * 0.3;

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const dx = (x - centerX) / radiusX;
        const dy = (y - centerY) / radiusY;

        if (dx * dx + dy * dy < 1) {
          mask[y * width + x] = 1;
        }
      }
    }

    return mask;
  }

  // Get mock sample images
  getSampleImages() {
    return this.config?.get('mock_data.sample_images', [
      {
        id: 'xray_chest_001',
        path: '/examples/xray/chest_sample.jpg',
        modality: 'X-Ray',
        description: 'Chest X-ray - Normal'
      },
      {
        id: 'ct_lung_001',
        path: '/examples/ct/lung_sample.dcm',
        modality: 'CT',
        description: 'Lung CT - Nodule present'
      },
      {
        id: 'mri_brain_001',
        path: '/examples/mri/brain_sample.nii.gz',
        modality: 'MRI',
        description: 'Brain MRI - T1 weighted'
      }
    ]);
  }
}

// Export for use in other modules
if (typeof window !== 'undefined') {
  window.MockAPI = MockAPI;
}

export default MockAPI;
