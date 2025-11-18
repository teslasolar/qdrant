// CHAZON Medical Imaging SCADA - Database Accessor
// Uses sql.js (SQLite compiled to WebAssembly) for browser-side database access

class Database {
  constructor(dbPath = '/database/chazon.db') {
    this.dbPath = dbPath;
    this.db = null;
    this.SQL = null;
    this.ready = false;
  }

  async init() {
    try {
      // Load sql.js library from CDN
      if (!window.initSqlJs) {
        await this.loadSqlJs();
      }

      // Initialize SQL.js
      this.SQL = await initSqlJs({
        locateFile: file => `https://sql.js.org/dist/${file}`
      });

      // Load database file
      const response = await fetch(this.dbPath);
      const buffer = await response.arrayBuffer();
      const arr = new Uint8Array(buffer);

      this.db = new this.SQL.Database(arr);
      this.ready = true;

      console.log('[Database] Initialized successfully');
      return true;

    } catch (error) {
      console.warn('[Database] Failed to initialize:', error);
      console.warn('[Database] Falling back to JSON mode');
      this.ready = false;
      return false;
    }
  }

  async loadSqlJs() {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'https://sql.js.org/dist/sql-wasm.js';
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  // ========================================================================
  // TAG QUERIES
  // ========================================================================

  getTag(directoryPath) {
    if (!this.ready) return null;

    const stmt = this.db.prepare(`
      SELECT * FROM tags WHERE directory_path = ?
    `);
    stmt.bind([directoryPath]);

    if (!stmt.step()) {
      stmt.free();
      return null;
    }

    const row = stmt.getAsObject();
    stmt.free();

    // Get related data
    const tag = this.buildTagObject(row.id);
    return tag;
  }

  buildTagObject(tagId) {
    const tag = this.db.exec(`SELECT * FROM tags WHERE id = ${tagId}`)[0];
    if (!tag) return null;

    const data = this.rowToObject(tag);

    // Get features
    data.Features = this.query(`
      SELECT title, description, icon
      FROM tag_features
      WHERE tag_id = ${tagId}
      ORDER BY sort_order
    `);

    // Get child directories
    data.Child_Directories = this.query(`
      SELECT path, title, description, icon, page_count
      FROM tag_child_directories
      WHERE tag_id = ${tagId}
      ORDER BY sort_order
    `);

    // Get sibling directories
    data.Sibling_Directories = this.query(`
      SELECT path, title, description, icon
      FROM tag_sibling_directories
      WHERE tag_id = ${tagId}
      ORDER BY sort_order
    `);

    // Get page links
    data.Page_Links = this.query(`
      SELECT path, name, icon, size
      FROM tag_page_links
      WHERE tag_id = ${tagId}
      ORDER BY sort_order
    `);

    // Get quick actions
    data.Quick_Actions = this.query(`
      SELECT label, path, type
      FROM tag_quick_actions
      WHERE tag_id = ${tagId}
      ORDER BY sort_order
    `);

    // Get related files
    data.Related_Files = this.query(`
      SELECT path, name, type
      FROM tag_related_files
      WHERE tag_id = ${tagId}
      ORDER BY sort_order
    `);

    // Get breadcrumb trail
    data.Breadcrumb_Trail = this.query(`
      SELECT path, title, icon
      FROM tag_breadcrumb_trail
      WHERE tag_id = ${tagId}
      ORDER BY sort_order
    `);

    // Convert snake_case to PascalCase for JSON compatibility
    return this.toPascalCase(data);
  }

  getAllTags() {
    if (!this.ready) return [];

    return this.query(`
      SELECT uuid, directory_path, title, isa_level, color_scheme
      FROM tags
      ORDER BY directory_path
    `);
  }

  getTagsByLevel(isaLevel) {
    if (!this.ready) return [];

    return this.query(`
      SELECT uuid, directory_path, title, description, icon
      FROM tags
      WHERE isa_level = ?
      ORDER BY directory_path
    `, [isaLevel]);
  }

  // ========================================================================
  // SAMPLE QUERIES
  // ========================================================================

  getSample(sampleId) {
    if (!this.ready) return null;

    const results = this.query(`
      SELECT * FROM samples WHERE sample_id = ?
    `, [sampleId]);

    return results.length > 0 ? results[0] : null;
  }

  getSamplesByModality(modality) {
    if (!this.ready) return [];

    return this.query(`
      SELECT sample_id, file_path, file_name, description, body_part
      FROM samples
      WHERE modality = ?
      ORDER BY sample_id
    `, [modality]);
  }

  getAllSamples() {
    if (!this.ready) return [];

    return this.query(`
      SELECT sample_id, modality, file_path, description
      FROM samples
      ORDER BY modality, sample_id
    `);
  }

  // ========================================================================
  // MODEL QUERIES
  // ========================================================================

  getModel(modelName) {
    if (!this.ready) return null;

    const results = this.query(`
      SELECT * FROM models WHERE model_name = ?
    `, [modelName]);

    return results.length > 0 ? results[0] : null;
  }

  getModelsByType(modelType) {
    if (!this.ready) return [];

    return this.query(`
      SELECT model_name, description, precision, enabled
      FROM models
      WHERE model_type = ? AND enabled = 1
      ORDER BY model_name
    `, [modelType]);
  }

  // ========================================================================
  // STATISTICS QUERIES
  // ========================================================================

  getTagsStats() {
    if (!this.ready) return null;

    return this.query(`
      SELECT
        COUNT(*) as total_tags,
        COUNT(DISTINCT isa_level) as levels,
        SUM(CASE WHEN has_plc THEN 1 ELSE 0 END) as with_plc,
        SUM(CASE WHEN has_hmi THEN 1 ELSE 0 END) as with_hmi,
        SUM(CASE WHEN has_scada THEN 1 ELSE 0 END) as with_scada
      FROM tags
    `)[0];
  }

  getSampleStats() {
    if (!this.ready) return null;

    return this.query(`
      SELECT * FROM v_samples_by_modality
    `);
  }

  // ========================================================================
  // HELPER METHODS
  // ========================================================================

  query(sql, params = []) {
    if (!this.ready) return [];

    try {
      const stmt = this.db.prepare(sql);
      stmt.bind(params);

      const results = [];
      while (stmt.step()) {
        results.push(stmt.getAsObject());
      }
      stmt.free();

      return results;
    } catch (error) {
      console.error('[Database] Query error:', error);
      return [];
    }
  }

  exec(sql) {
    if (!this.ready) return [];

    try {
      return this.db.exec(sql);
    } catch (error) {
      console.error('[Database] Exec error:', error);
      return [];
    }
  }

  rowToObject(result) {
    if (!result || !result.values || result.values.length === 0) {
      return null;
    }

    const obj = {};
    const columns = result.columns;
    const values = result.values[0];

    for (let i = 0; i < columns.length; i++) {
      obj[columns[i]] = values[i];
    }

    return obj;
  }

  toPascalCase(obj) {
    const newObj = {};

    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        // Convert snake_case to PascalCase
        const pascalKey = key.split('_')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join('_');

        newObj[pascalKey] = obj[key];
      }
    }

    return newObj;
  }

  close() {
    if (this.db) {
      this.db.close();
      this.db = null;
      this.ready = false;
      console.log('[Database] Closed');
    }
  }
}

// ============================================================================
// DATABASE FALLBACK - Use JSON files if database not available
// ============================================================================

class DatabaseFallback {
  async getTag(directoryPath) {
    try {
      const tagPath = directoryPath + '/index/tag.json';
      const response = await fetch(tagPath);
      return await response.json();
    } catch (error) {
      console.error('[Database Fallback] Error loading tag:', error);
      return null;
    }
  }

  async getSample(sampleId) {
    // Return hardcoded sample data
    const samples = {
      'xray_chest_001': {
        sample_id: 'xray_chest_001',
        modality: 'XRay',
        file_path: '/examples/xray/chest_sample.jpg',
        description: 'Chest X-ray - Normal'
      },
      'ct_lung_001': {
        sample_id: 'ct_lung_001',
        modality: 'CT',
        file_path: '/examples/ct/lung_sample.dcm',
        description: 'Lung CT - Nodule present'
      },
      'mri_brain_001': {
        sample_id: 'mri_brain_001',
        modality: 'MRI',
        file_path: '/examples/mri/brain_sample.nii.gz',
        description: 'Brain MRI - T1 weighted'
      }
    };

    return samples[sampleId] || null;
  }

  async getAllSamples() {
    return [
      await this.getSample('xray_chest_001'),
      await this.getSample('ct_lung_001'),
      await this.getSample('mri_brain_001')
    ].filter(s => s !== null);
  }

  async getModel(modelName) {
    const models = {
      'unet': { model_name: 'unet', model_type: 'segmentation', description: 'U-Net' },
      'yolov8': { model_name: 'yolov8', model_type: 'detection', description: 'YOLOv8' },
      'biomedclip': { model_name: 'biomedclip', model_type: 'classification', description: 'BiomedCLIP' }
    };

    return models[modelName] || null;
  }
}

// ============================================================================
// GLOBAL DATABASE INSTANCE
// ============================================================================

window.chazonDB = new Database();
window.chazonDBFallback = new DatabaseFallback();

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
  const success = await window.chazonDB.init();

  if (!success) {
    console.log('[Database] Using fallback JSON mode');
  } else {
    console.log('[Database] Using SQLite mode (faster!)');
  }
});

export default Database;
