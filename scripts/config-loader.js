// Configuration Loader for CHAZON Medical Imaging SCADA
// Loads config.yaml and exposes settings to application

class ConfigLoader {
  constructor() {
    this.config = null;
    this.environment = null;
  }

  async load() {
    try {
      // Load config.yaml (convert to JSON via server or use js-yaml)
      const response = await fetch('/config.json');  // Server converts YAML to JSON
      this.config = await response.json();

      // Get current environment
      this.environment = this.config.environment || 'demo';

      console.log(`[Config] Loaded environment: ${this.environment}`);
      console.log(`[Config] Mode: ${this.getEnvConfig().name}`);

      return this.config;
    } catch (error) {
      console.warn('[Config] Failed to load config, using defaults:', error);
      return this.getDefaultConfig();
    }
  }

  getEnvConfig() {
    if (!this.config) return this.getDefaultConfig().environments.demo;
    return this.config.environments[this.environment];
  }

  get(path, defaultValue = null) {
    if (!this.config) return defaultValue;

    const keys = path.split('.');
    let value = this.config;

    for (const key of keys) {
      if (value && typeof value === 'object' && key in value) {
        value = value[key];
      } else {
        return defaultValue;
      }
    }

    return value;
  }

  getEnv(path, defaultValue = null) {
    const envConfig = this.getEnvConfig();
    const keys = path.split('.');
    let value = envConfig;

    for (const key of keys) {
      if (value && typeof value === 'object' && key in value) {
        value = value[key];
      } else {
        return defaultValue;
      }
    }

    return value;
  }

  isDemo() {
    return this.environment === 'demo';
  }

  isDev() {
    return this.environment === 'dev';
  }

  isProd() {
    return this.environment === 'prod';
  }

  useMockAI() {
    return this.getEnv('features.use_mock_ai', true);
  }

  useSampleData() {
    return this.getEnv('features.use_sample_data', true);
  }

  showWatermark() {
    return this.getEnv('features.show_watermark', false);
  }

  getApiUrl(endpoint = '') {
    const baseUrl = this.getEnv('api.base_url', '/api/mock');
    return `${baseUrl}${endpoint}`;
  }

  getQdrantUrl() {
    return this.getEnv('api.qdrant_url', 'http://localhost:6333');
  }

  getMaxUploadSize() {
    return this.getEnv('limits.max_upload_size_mb', 10);
  }

  getMaxBatchFiles() {
    return this.getEnv('limits.max_batch_files', 5);
  }

  getSampleData(modality) {
    return this.getEnv(`sample_data.${modality}`, null);
  }

  getDefaultConfig() {
    // Fallback config if loading fails
    return {
      environment: 'demo',
      environments: {
        demo: {
          name: 'Demo Mode',
          features: {
            use_mock_ai: true,
            use_sample_data: true,
            enable_enterprise: true,
            show_watermark: true
          },
          api: {
            base_url: '/api/mock'
          },
          limits: {
            max_upload_size_mb: 10,
            max_batch_files: 5
          }
        }
      }
    };
  }

  applyUIConfig() {
    const envConfig = this.getEnvConfig();

    // Add watermark if demo mode
    if (this.showWatermark()) {
      this.addDemoWatermark();
    }

    // Apply lablab.ai banner
    if (this.get('lablab.show_banner', false)) {
      this.addLabLabBanner();
    }

    // Set CSS variables from config
    document.documentElement.style.setProperty('--max-upload-mb', this.getMaxUploadSize());
  }

  addDemoWatermark() {
    const watermark = document.createElement('div');
    watermark.id = 'demo-watermark';
    watermark.textContent = 'DEMO MODE';
    watermark.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: rgba(255, 215, 0, 0.9);
      color: #2a1a3a;
      padding: 5px 15px;
      border-radius: 5px;
      font-weight: bold;
      font-size: 0.9em;
      z-index: 9999;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    `;
    document.body.appendChild(watermark);
  }

  addLabLabBanner() {
    const banner = document.createElement('div');
    banner.id = 'lablab-banner';
    banner.innerHTML = `
      <span>🚀 ${this.get('lablab.banner_text', 'Built for lablab.ai Hackathon')}</span>
    `;
    banner.style.cssText = `
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(135deg, #b794f4, #8b5cf6);
      color: #f5f2e8;
      padding: 8px;
      text-align: center;
      font-size: 0.9em;
      z-index: 9998;
      box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
    `;
    document.body.appendChild(banner);
  }
}

// Global config instance
window.chazonConfig = new ConfigLoader();

// Auto-load on page ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', async () => {
    await window.chazonConfig.load();
    window.chazonConfig.applyUIConfig();
  });
} else {
  window.chazonConfig.load().then(() => {
    window.chazonConfig.applyUIConfig();
  });
}

export default ConfigLoader;
