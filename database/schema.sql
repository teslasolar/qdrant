-- CHAZON Medical Imaging SCADA - SQLite Database Schema
-- Reduces file count by consolidating JSON files into databases

-- ============================================================================
-- TAGS DATABASE - Consolidates all index/tag.json files
-- ============================================================================

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE NOT NULL,
    directory_path TEXT UNIQUE NOT NULL,
    directory_name TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    color_scheme TEXT,
    isa_level TEXT,
    parent_path TEXT,
    has_plc BOOLEAN DEFAULT 0,
    has_hmi BOOLEAN DEFAULT 0,
    has_scada BOOLEAN DEFAULT 0,
    plc_path TEXT,
    hmi_path TEXT,
    scada_path TEXT,
    readme_path TEXT,
    controls_path TEXT,
    status_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_path) REFERENCES tags(directory_path)
);

CREATE TABLE IF NOT EXISTS tag_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tag_child_directories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    page_count INTEGER DEFAULT 0,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tag_sibling_directories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tag_page_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    name TEXT NOT NULL,
    icon TEXT,
    size INTEGER DEFAULT 0,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tag_quick_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER NOT NULL,
    label TEXT NOT NULL,
    path TEXT NOT NULL,
    type TEXT DEFAULT 'primary',
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tag_related_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tag_breadcrumb_trail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    title TEXT NOT NULL,
    icon TEXT,
    sort_order INTEGER NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tags_directory_path ON tags(directory_path);
CREATE INDEX IF NOT EXISTS idx_tags_uuid ON tags(uuid);
CREATE INDEX IF NOT EXISTS idx_tags_parent_path ON tags(parent_path);
CREATE INDEX IF NOT EXISTS idx_tags_isa_level ON tags(isa_level);
CREATE INDEX IF NOT EXISTS idx_tag_features_tag_id ON tag_features(tag_id);
CREATE INDEX IF NOT EXISTS idx_tag_child_directories_tag_id ON tag_child_directories(tag_id);

-- ============================================================================
-- SAMPLES DATABASE - Medical imaging sample metadata
-- ============================================================================

CREATE TABLE IF NOT EXISTS samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT UNIQUE NOT NULL,
    modality TEXT NOT NULL,  -- XRay, CT, MRI, DICOM
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_size INTEGER,
    file_format TEXT,  -- dcm, nii, nii.gz, jpg, png
    description TEXT,

    -- Clinical metadata
    body_part TEXT,
    study_type TEXT,
    diagnosis TEXT,

    -- Imaging parameters
    image_width INTEGER,
    image_height INTEGER,
    image_depth INTEGER,
    bits_per_pixel INTEGER,

    -- Dataset source
    dataset_name TEXT,  -- MIMIC-CXR, NIH, OASIS, etc.
    dataset_url TEXT,
    license TEXT,

    -- Processing metadata
    is_processed BOOLEAN DEFAULT 0,
    has_segmentation BOOLEAN DEFAULT 0,
    has_detection BOOLEAN DEFAULT 0,
    has_embedding BOOLEAN DEFAULT 0,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sample_embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id INTEGER NOT NULL,
    model_name TEXT NOT NULL,  -- biomedclip, resnet50, etc.
    dimension INTEGER NOT NULL,
    embedding BLOB NOT NULL,  -- Store as binary blob
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sample_annotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id INTEGER NOT NULL,
    annotation_type TEXT NOT NULL,  -- segmentation, detection, classification
    annotation_data TEXT NOT NULL,  -- JSON string
    confidence REAL,
    model_name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sample_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_samples_modality ON samples(modality);
CREATE INDEX IF NOT EXISTS idx_samples_body_part ON samples(body_part);
CREATE INDEX IF NOT EXISTS idx_samples_dataset_name ON samples(dataset_name);
CREATE INDEX IF NOT EXISTS idx_sample_embeddings_sample_id ON sample_embeddings(sample_id);
CREATE INDEX IF NOT EXISTS idx_sample_embeddings_model ON sample_embeddings(model_name);
CREATE INDEX IF NOT EXISTS idx_sample_annotations_sample_id ON sample_annotations(sample_id);
CREATE INDEX IF NOT EXISTS idx_sample_tags_sample_id ON sample_tags(sample_id);
CREATE INDEX IF NOT EXISTS idx_sample_tags_tag ON sample_tags(tag);

-- ============================================================================
-- STANDARDS DATABASE - Consolidates standards definitions
-- ============================================================================

CREATE TABLE IF NOT EXISTS standards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_name TEXT UNIQUE NOT NULL,  -- PackML, ISA-88, ISA-95, etc.
    version TEXT,
    description TEXT,
    domain TEXT,
    enabled BOOLEAN DEFAULT 1,
    config_data TEXT,  -- JSON string for complex config
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS standard_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id INTEGER NOT NULL,
    state_name TEXT NOT NULL,
    state_value INTEGER,
    description TEXT,
    entry_action TEXT,
    exit_action TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (standard_id) REFERENCES standards(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS standard_transitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id INTEGER NOT NULL,
    from_state_id INTEGER NOT NULL,
    to_state_id INTEGER NOT NULL,
    event_name TEXT,
    condition TEXT,
    action TEXT,
    FOREIGN KEY (standard_id) REFERENCES standards(id) ON DELETE CASCADE,
    FOREIGN KEY (from_state_id) REFERENCES standard_states(id),
    FOREIGN KEY (to_state_id) REFERENCES standard_states(id)
);

CREATE TABLE IF NOT EXISTS standard_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    standard_id INTEGER NOT NULL,
    model_name TEXT NOT NULL,
    model_type TEXT,  -- physical, procedural, recipe, etc.
    model_data TEXT NOT NULL,  -- JSON string
    FOREIGN KEY (standard_id) REFERENCES standards(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_standards_name ON standards(standard_name);
CREATE INDEX IF NOT EXISTS idx_standard_states_standard_id ON standard_states(standard_id);
CREATE INDEX IF NOT EXISTS idx_standard_transitions_standard_id ON standard_transitions(standard_id);

-- ============================================================================
-- MOCK DATA DATABASE - Demo mode mock responses
-- ============================================================================

CREATE TABLE IF NOT EXISTS mock_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT NOT NULL,  -- /api/mock/segment, /api/mock/detect, etc.
    request_params TEXT,  -- JSON string of request params
    response_data TEXT NOT NULL,  -- JSON string of response
    processing_time_ms INTEGER DEFAULT 500,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mock_embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mock_id TEXT UNIQUE NOT NULL,
    dimension INTEGER NOT NULL,
    embedding BLOB NOT NULL,
    metadata TEXT,  -- JSON string
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_mock_responses_endpoint ON mock_responses(endpoint);
CREATE INDEX IF NOT EXISTS idx_mock_embeddings_dimension ON mock_embeddings(dimension);

-- ============================================================================
-- CONFIGURATION CACHE - Cache for config.yaml
-- ============================================================================

CREATE TABLE IF NOT EXISTS config_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,  -- JSON string
    environment TEXT,  -- demo, dev, prod
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_config_cache_key ON config_cache(key);
CREATE INDEX IF NOT EXISTS idx_config_cache_environment ON config_cache(environment);

-- ============================================================================
-- MODELS DATABASE - AI/ML model metadata
-- ============================================================================

CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT UNIQUE NOT NULL,
    model_type TEXT NOT NULL,  -- segmentation, detection, classification
    description TEXT,
    version TEXT,
    file_path TEXT,
    file_size INTEGER,
    precision TEXT DEFAULT 'float32',
    input_shape TEXT,  -- JSON array
    output_shape TEXT,  -- JSON array
    supported_organs TEXT,  -- JSON array for segmentation
    supported_targets TEXT,  -- JSON array for detection
    performance_metrics TEXT,  -- JSON object
    enabled BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_models_type ON models(model_type);
CREATE INDEX IF NOT EXISTS idx_models_name ON models(model_name);

-- ============================================================================
-- USAGE STATISTICS - Track API usage for analytics
-- ============================================================================

CREATE TABLE IF NOT EXISTS usage_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT NOT NULL,
    model_name TEXT,
    processing_time_ms INTEGER,
    success BOOLEAN DEFAULT 1,
    error_message TEXT,
    user_agent TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usage_stats_endpoint ON usage_stats(endpoint);
CREATE INDEX IF NOT EXISTS idx_usage_stats_model ON usage_stats(model_name);
CREATE INDEX IF NOT EXISTS idx_usage_stats_created_at ON usage_stats(created_at);

-- ============================================================================
-- VIEWS - Convenient queries
-- ============================================================================

-- View: All tags with feature count
CREATE VIEW IF NOT EXISTS v_tags_summary AS
SELECT
    t.id,
    t.uuid,
    t.directory_path,
    t.title,
    t.isa_level,
    COUNT(DISTINCT f.id) as feature_count,
    COUNT(DISTINCT c.id) as child_count,
    COUNT(DISTINCT p.id) as page_count
FROM tags t
LEFT JOIN tag_features f ON t.id = f.tag_id
LEFT JOIN tag_child_directories c ON t.id = c.tag_id
LEFT JOIN tag_page_links p ON t.id = p.tag_id
GROUP BY t.id;

-- View: Sample statistics by modality
CREATE VIEW IF NOT EXISTS v_samples_by_modality AS
SELECT
    modality,
    COUNT(*) as total_samples,
    SUM(CASE WHEN has_embedding THEN 1 ELSE 0 END) as with_embeddings,
    SUM(CASE WHEN has_segmentation THEN 1 ELSE 0 END) as with_segmentation,
    SUM(CASE WHEN has_detection THEN 1 ELSE 0 END) as with_detection,
    AVG(file_size) as avg_file_size
FROM samples
GROUP BY modality;

-- View: Model usage statistics
CREATE VIEW IF NOT EXISTS v_model_usage AS
SELECT
    model_name,
    COUNT(*) as usage_count,
    AVG(processing_time_ms) as avg_processing_time,
    SUM(CASE WHEN success THEN 1 ELSE 0 END) as success_count,
    SUM(CASE WHEN NOT success THEN 1 ELSE 0 END) as error_count
FROM usage_stats
WHERE model_name IS NOT NULL
GROUP BY model_name;

-- ============================================================================
-- TRIGGERS - Auto-update timestamps
-- ============================================================================

CREATE TRIGGER IF NOT EXISTS update_tags_timestamp
AFTER UPDATE ON tags
BEGIN
    UPDATE tags SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_samples_timestamp
AFTER UPDATE ON samples
BEGIN
    UPDATE samples SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_standards_timestamp
AFTER UPDATE ON standards
BEGIN
    UPDATE standards SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_models_timestamp
AFTER UPDATE ON models
BEGIN
    UPDATE models SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- ============================================================================
-- INITIAL DATA - Seed with ISA-95 levels
-- ============================================================================

INSERT OR IGNORE INTO standards (standard_name, version, description, domain) VALUES
('PackML', '4.0', '18-state equipment control state machine', 'automation'),
('ISA-88', '1995', 'Batch control models and terminology', 'batch'),
('ISA-95', '2010', 'Enterprise-control system integration', 'enterprise'),
('ISA-101', '2015', 'High-performance HMI design', 'hmi'),
('MQTT', '5.0', 'Message queuing telemetry transport', 'messaging'),
('OPC-UA', '1.05', 'OPC unified architecture', 'interoperability');

-- ============================================================================
-- VACUUM AND OPTIMIZE
-- ============================================================================

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;  -- 64MB cache
PRAGMA temp_store = MEMORY;
PRAGMA mmap_size = 268435456;  -- 256MB mmap
