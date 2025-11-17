/**
 * CHAZON Medical OS Loader
 * Tag-based module loading system for GitHub Pages (static hosting)
 *
 * Loads medical imaging OS modules dynamically from /os directory
 * Uses tag system for module discovery and dependency resolution
 */

class CHAZONOSLoader {
  constructor() {
    this.modules = new Map();
    this.registry = null;
    this.loaded = new Set();
    this.loading = new Map();
    this.basePath = '/os';
  }

  /**
   * Initialize the OS loader by fetching module registry
   */
  async init() {
    try {
      const response = await fetch('/os/modules.json');
      this.registry = await response.json();
      console.log('✓ CHAZON OS Registry loaded:', this.registry.registry.total_modules, 'modules');
      return true;
    } catch (error) {
      console.error('✗ Failed to load OS registry:', error);
      return false;
    }
  }

  /**
   * Load a module by path or UUID
   * @param {string} identifier - Module path or UUID
   * @returns {Promise<Object>} Loaded module
   */
  async loadModule(identifier) {
    // Check if already loaded
    if (this.modules.has(identifier)) {
      return this.modules.get(identifier);
    }

    // Check if currently loading (prevent duplicate requests)
    if (this.loading.has(identifier)) {
      return this.loading.get(identifier);
    }

    // Find module in registry
    const moduleInfo = this.findModule(identifier);
    if (!moduleInfo) {
      throw new Error(`Module not found: ${identifier}`);
    }

    // Create loading promise
    const loadPromise = this._loadModuleInternal(moduleInfo);
    this.loading.set(identifier, loadPromise);

    try {
      const module = await loadPromise;
      this.modules.set(identifier, module);
      this.modules.set(moduleInfo.uuid, module);
      this.loaded.add(identifier);
      this.loading.delete(identifier);
      return module;
    } catch (error) {
      this.loading.delete(identifier);
      throw error;
    }
  }

  /**
   * Internal module loading with dependency resolution
   */
  async _loadModuleInternal(moduleInfo) {
    console.log(`Loading module: ${moduleInfo.name} (${moduleInfo.path})`);

    // Load dependencies first
    if (moduleInfo.dependencies && moduleInfo.dependencies.length > 0) {
      console.log(`  Dependencies: ${moduleInfo.dependencies.join(', ')}`);
      await Promise.all(
        moduleInfo.dependencies.map(dep => this.loadModule(dep))
      );
    }

    // Load the module script
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.type = 'module';
      script.src = moduleInfo.path;

      script.onload = () => {
        console.log(`✓ Loaded: ${moduleInfo.name}`);
        resolve({
          info: moduleInfo,
          exports: window[moduleInfo.exports[0]] // Assume first export is main class
        });
      };

      script.onerror = () => {
        console.error(`✗ Failed to load: ${moduleInfo.name}`);
        reject(new Error(`Failed to load module: ${moduleInfo.path}`));
      };

      document.head.appendChild(script);
    });
  }

  /**
   * Find module in registry by path, UUID, or name
   */
  findModule(identifier) {
    if (!this.registry) {
      throw new Error('Registry not loaded. Call init() first.');
    }

    // Search in modules
    for (const category in this.registry.modules) {
      for (const key in this.registry.modules[category]) {
        const module = this.registry.modules[category][key];
        if (module.uuid === identifier ||
            module.path === identifier ||
            module.name === identifier ||
            key === identifier) {
          return module;
        }
      }
    }

    // Search in controls
    for (const key in this.registry.controls) {
      const control = this.registry.controls[key];
      if (control.uuid === identifier ||
          control.path === identifier ||
          control.name === identifier ||
          key === identifier) {
        return control;
      }
    }

    return null;
  }

  /**
   * Query modules by tag
   * @param {string|string[]} tags - Single tag or array of tags
   * @returns {Array} Matching modules
   */
  queryByTag(tags) {
    if (!this.registry) {
      throw new Error('Registry not loaded. Call init() first.');
    }

    const tagArray = Array.isArray(tags) ? tags : [tags];
    const results = [];

    // Search modules
    for (const category in this.registry.modules) {
      for (const key in this.registry.modules[category]) {
        const module = this.registry.modules[category][key];
        if (module.tags && tagArray.some(tag => module.tags.includes(tag))) {
          results.push(module);
        }
      }
    }

    // Search controls
    for (const key in this.registry.controls) {
      const control = this.registry.controls[key];
      if (control.tags && tagArray.some(tag => control.tags.includes(tag))) {
        results.push(control);
      }
    }

    return results;
  }

  /**
   * Query modules by category
   */
  queryByCategory(category) {
    if (!this.registry) {
      throw new Error('Registry not loaded. Call init() first.');
    }

    const results = [];

    if (this.registry.modules[category]) {
      for (const key in this.registry.modules[category]) {
        results.push(this.registry.modules[category][key]);
      }
    }

    return results;
  }

  /**
   * Get all AI modules
   */
  getAIModules() {
    return this.queryByCategory('ai');
  }

  /**
   * Get all data modules
   */
  getDataModules() {
    return this.queryByCategory('data');
  }

  /**
   * Get all visualization modules
   */
  getVisualizationModules() {
    return this.queryByCategory('visualization');
  }

  /**
   * Get module info without loading
   */
  getModuleInfo(identifier) {
    return this.findModule(identifier);
  }

  /**
   * Preload commonly used modules
   */
  async preloadCommon() {
    console.log('Preloading common modules...');
    const commonModules = [
      'dicom-loader',
      'image-processor',
      'windowing'
    ];

    await Promise.all(
      commonModules.map(m => this.loadModule(m).catch(err => {
        console.warn(`Could not preload ${m}:`, err.message);
      }))
    );

    console.log('✓ Common modules preloaded');
  }

  /**
   * Load modules for a specific screen/control
   * Based on screen configuration
   */
  async loadForScreen(screenType) {
    const screenModules = {
      'ct-workstation': ['segmentation', 'dicom-loader', 'dicom-viewer', 'windowing'],
      'mri-workstation': ['segmentation', 'dicom-loader', 'mpr-viewer', 'windowing'],
      'xray-workstation': ['detection', 'dicom-loader', 'dicom-viewer'],
      'pacs-dashboard': ['dicom-loader', 'pacs-client'],
      'alf-screening': ['alf-detect', 'biomedclip', 'dicom-loader', 'qdrant-client']
    };

    const modules = screenModules[screenType] || [];

    if (modules.length === 0) {
      console.warn(`No modules configured for screen: ${screenType}`);
      return [];
    }

    console.log(`Loading ${modules.length} modules for ${screenType}...`);

    const loaded = await Promise.all(
      modules.map(m => this.loadModule(m).catch(err => {
        console.warn(`Could not load ${m}:`, err.message);
        return null;
      }))
    );

    return loaded.filter(m => m !== null);
  }

  /**
   * Get registry statistics
   */
  getStats() {
    return {
      totalModules: this.registry?.registry?.total_modules || 0,
      totalControls: this.registry?.registry?.total_controls || 0,
      loadedModules: this.loaded.size,
      categories: this.registry?.registry?.categories || {}
    };
  }

  /**
   * List all available modules
   */
  listModules() {
    if (!this.registry) {
      return [];
    }

    const allModules = [];

    for (const category in this.registry.modules) {
      for (const key in this.registry.modules[category]) {
        allModules.push({
          ...this.registry.modules[category][key],
          category
        });
      }
    }

    return allModules;
  }

  /**
   * Create a tag-based control interface
   * Maps control tags to OS modules
   */
  async createControl(controlId) {
    const control = this.registry?.controls?.[controlId];
    if (!control) {
      throw new Error(`Control not found: ${controlId}`);
    }

    console.log(`Creating control: ${control.name}`);

    // Load modules with matching tags
    const matchingModules = this.queryByTag(control.tags);
    console.log(`  Found ${matchingModules.length} matching modules by tag`);

    // Load all matching modules
    const loaded = await Promise.all(
      matchingModules
        .filter(m => m.type === 'module')
        .map(m => this.loadModule(m.uuid).catch(err => {
          console.warn(`Could not load ${m.name}:`, err.message);
          return null;
        }))
    );

    return {
      control,
      modules: loaded.filter(m => m !== null)
    };
  }
}

// Create global instance
window.chazonOS = new CHAZONOSLoader();

// Auto-initialize on load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', async () => {
    await window.chazonOS.init();
  });
} else {
  window.chazonOS.init();
}

// Export for module usage
export default CHAZONOSLoader;
