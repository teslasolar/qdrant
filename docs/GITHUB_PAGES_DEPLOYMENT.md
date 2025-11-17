# GitHub Pages Deployment Guide
**CHAZON Medical Imaging SCADA - Static Hosting Architecture**

## Overview

CHAZON is designed to run entirely on **GitHub Pages** (static hosting) using a tag-based module loading system. No backend server required!

## 🏗️ Architecture

### Tag-Based OS Module System

Instead of a traditional backend, CHAZON uses:

```
┌─────────────────────────────────────────────────────┐
│  GitHub Pages (Static Files)                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  📄 /os/modules.json                                │
│      └── Module Registry (all OS components)        │
│                                                      │
│  🔧 /scripts/os-loader.js                           │
│      └── Client-side module loader                  │
│                                                      │
│  🏷️  Tag System                                     │
│      ├── Controls tagged with ["AI", "Medical"]     │
│      ├── Modules tagged with ["AI", "Medical"]      │
│      └── Loader matches tags → loads modules        │
│                                                      │
│  📦 /os/medical/ai/*.js                             │
│      └── Actual AI/ML modules (JavaScript)          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### How It Works

1. **Module Registry (`/os/modules.json`)**
   - JSON file listing all OS modules
   - Each module has: path, tags, dependencies, exports
   - 16 modules registered (AI, data, visualization, etc.)

2. **OS Loader (`/scripts/os-loader.js`)**
   - Client-side JavaScript class
   - Loads modules dynamically based on tags
   - Handles dependencies automatically
   - Works entirely in browser (no backend)

3. **Control Files (generated from templates)**
   - Each control (plc.html, hmi.html, scada.html) has tags
   - OS loader queries modules by tags
   - Modules loaded on-demand when needed
   - Example: `["Medical", "L3"]` → loads all medical AI modules

## 🚀 Quick Start

### 1. Enable GitHub Pages

```bash
# In your repository settings:
Settings → Pages → Source: main branch → /root
```

Your site will be at: `https://yourusername.github.io/qdrant/`

### 2. Deploy Structure

```
your-repo/
├── index.html              # Entry point
├── os/
│   ├── modules.json        # Module registry (CRITICAL)
│   └── medical/
│       └── ai/
│           ├── segmentation.js
│           ├── detection.js
│           └── ...
├── scripts/
│   ├── os-loader.js        # OS module loader (CRITICAL)
│   ├── config-loader.js
│   └── theme-loader.js
├── screens/
│   └── frontend/
│       ├── index.html
│       ├── ct-workstation.html
│       └── ...
└── templates/
    └── controls/
        └── control-template.html
```

### 3. Generate Control Files

```bash
# Generate all control files from template
python3 cli/generators/generate_controls_from_template.py --all

# Or just for one section
python3 cli/generators/generate_controls_from_template.py --section medical

# Preview without creating files
python3 cli/generators/generate_controls_from_template.py --all --dry-run
```

This creates plc.html, hmi.html, scada.html files that:
- ✅ Load OS modules based on tags
- ✅ Work entirely client-side
- ✅ No backend needed

### 4. Test Locally

```bash
# Start local server
./start.sh

# Or use Python
python3 -m http.server 8000

# Visit: http://localhost:8000
```

## 📦 Module Loading Example

### In a Control File (`/os/medical/hmi.html`)

```html
<script src="/scripts/os-loader.js"></script>

<script>
// Configuration
const CONTROL_CONFIG = {
  name: 'Medical HMI',
  section: 'Medical',
  tags: ["Medical", "Imaging", "L3"],
  isaLevel: 'L3_MES'
};

// Wait for OS to initialize
async function initControl() {
  await window.chazonOS.init();

  // Query modules by tag
  const medicalModules = window.chazonOS.queryByTag("Medical");
  console.log('Found', medicalModules.length, 'medical modules');

  // Load specific module
  const segmentation = await window.chazonOS.loadModule('segmentation');

  // Use the module
  const seg = new segmentation.exports.MedicalSegmentation();
  const result = await seg.unetSegment(imageData, 'liver');
}

initControl();
</script>
```

### Module Registry Entry (`/os/modules.json`)

```json
{
  "modules": {
    "ai": {
      "segmentation": {
        "uuid": "os-ai-seg-001",
        "name": "Medical Segmentation",
        "path": "/os/medical/ai/segmentation.js",
        "tags": ["AI", "Segmentation", "Medical"],
        "exports": ["MedicalSegmentation"],
        "dependencies": []
      }
    }
  }
}
```

### Module Implementation (`/os/medical/ai/segmentation.js`)

```javascript
// Medical segmentation module
export class MedicalSegmentation {
  async unetSegment(imageData, organType) {
    // Implementation here
    return { mask, confidence, processingTimeMs };
  }

  async maskRCNNSegment(imageData, config) {
    // Implementation here
    return { instances, masks, boxes, scores };
  }
}

// Also export as global for non-module contexts
window.MedicalSegmentation = MedicalSegmentation;
```

## 🏷️ Tag System

### How Tags Work

1. **Modules are tagged** in `/os/modules.json`:
   ```json
   {
     "tags": ["AI", "Segmentation", "Medical", "U-Net"]
   }
   ```

2. **Controls are tagged** in generated files:
   ```javascript
   tags: ["Medical", "Imaging", "L3"]
   ```

3. **OS Loader matches tags**:
   ```javascript
   // Find all modules tagged "Medical"
   const modules = window.chazonOS.queryByTag("Medical");

   // Find modules tagged with any of multiple tags
   const aiModules = window.chazonOS.queryByTag(["AI", "ML", "DeepLearning"]);
   ```

### Tag Categories

| Category | Tags | Purpose |
|----------|------|---------|
| **ISA-95 Levels** | L0, L1, L2, L3, L4 | Automation hierarchy |
| **Medical Imaging** | Medical, Imaging, DICOM, PACS | Medical domain |
| **AI/ML** | AI, ML, DeepLearning, Classification | AI functionality |
| **Modalities** | CT, MRI, XRay, Ultrasound | Imaging types |
| **Subsystems** | Boot, Backend, Frontend | System components |

## 🔧 Configuration Files

### 1. Module Registry (`/os/modules.json`)

**Purpose:** Central registry of all OS modules

**Structure:**
```json
{
  "metadata": {
    "version": "1.0.0",
    "description": "Medical Imaging OS Module Registry"
  },
  "modules": {
    "category": {
      "module-id": {
        "uuid": "unique-id",
        "name": "Module Name",
        "path": "/path/to/module.js",
        "tags": ["tag1", "tag2"],
        "exports": ["ClassName"],
        "dependencies": ["other-module"]
      }
    }
  }
}
```

**Categories:**
- `ai` - AI/ML modules (segmentation, detection, classification)
- `data` - Data loaders (DICOM, NIfTI, PACS)
- `visualization` - Viewers (DICOM viewport, MPR)
- `vector` - Vector search (Qdrant client)
- `utils` - Utilities (image processing, windowing)

### 2. Config (`/config.yaml`)

**Purpose:** Environment configuration (demo/dev/prod)

```yaml
environment: demo

environments:
  demo:
    features:
      use_mock_ai: true
      use_sample_data: true
  dev:
    features:
      use_mock_ai: false
      enable_gpu: true
  prod:
    features:
      use_real_data: true
```

**Converted to JSON for browser:**
```bash
./start.sh  # Auto-converts config.yaml → config.json
```

### 3. Theme (`/theme.yaml`)

**Purpose:** ISA-101 HMI color scheme

```yaml
colors:
  purple:
    accent: "#b794f4"
  cream:
    primary: "#f5f2e8"
  status:
    normal: "#90ee90"
    warning: "#ffd700"
    alarm: "#ff6b6b"
```

## 📊 Database System (Browser-Compatible)

### Using sql.js (SQLite in Browser)

CHAZON can use **sql.js** for client-side SQLite:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/sql-wasm.js"></script>
<script src="/scripts/database.js"></script>

<script>
// Initialize database
await window.chazonDB.init();

// Query tags
const tags = window.chazonDB.getAllTags();

// Query samples by modality
const ctScans = window.chazonDB.getSamplesByModality('CT');
</script>
```

### Database File

```bash
# Create database locally
python3 database/migrate.py

# Commit database/chazon.db
git add database/chazon.db
git commit -m "Add database"
git push

# Database is served as static file on GitHub Pages
# Browser loads it with sql.js
```

**Size:** ~850 KB (consolidated from 367 tag.json files)

## 🎨 Template System

### Template-Based Generation

All screens and controls are generated from templates:

```bash
# Generate medical screens
python3 cli/generators/generate_from_templates.py --medical

# Generate control files
python3 cli/generators/generate_controls_from_template.py --all
```

### Benefits

- **Consistency:** All files use same structure
- **Maintainability:** Change template once, regenerate all
- **Size Reduction:** 75% less code duplication
- **Theme Integration:** Auto-loads theme.yaml
- **Config Integration:** Auto-loads config.yaml

## ⚡ Performance Optimization

### 1. Module Loading Strategy

```javascript
// Preload common modules on app init
await window.chazonOS.preloadCommon();

// Load screen-specific modules on demand
await window.chazonOS.loadForScreen('ct-workstation');
```

### 2. Caching

- **Browser caching:** All modules cached by browser
- **Service Worker:** Can add for offline support
- **LocalStorage:** Cache module registry

### 3. Lazy Loading

```javascript
// Only load when user navigates to screen
document.getElementById('ct-scan-btn').onclick = async () => {
  const modules = await window.chazonOS.loadForScreen('ct-workstation');
  // Modules loaded, open screen
  window.location.href = '/screens/frontend/ct-workstation.html';
};
```

## 🔒 Security Considerations

### Content Security Policy (CSP)

Add to `index.html`:

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;
               style-src 'self' 'unsafe-inline';
               img-src 'self' data:;
               connect-src 'self';">
```

### Module Validation

```javascript
// In os-loader.js
async _loadModuleInternal(moduleInfo) {
  // Validate module path
  if (!moduleInfo.path.startsWith('/os/')) {
    throw new Error('Invalid module path');
  }

  // Validate against registry
  if (!this.findModule(moduleInfo.uuid)) {
    throw new Error('Module not in registry');
  }

  // Load module
  // ...
}
```

## 📱 Progressive Web App (PWA)

### Make it an App

Add `manifest.json`:

```json
{
  "name": "CHAZON Medical Imaging",
  "short_name": "CHAZON",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#2a1a3a",
  "theme_color": "#b794f4",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

Add Service Worker for offline:

```javascript
// sw.js
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open('chazon-v1').then(cache => {
      return cache.addAll([
        '/',
        '/os/modules.json',
        '/scripts/os-loader.js',
        '/scripts/config-loader.js',
        '/scripts/theme-loader.js'
      ]);
    })
  );
});
```

## 🧪 Testing Locally

### 1. Local HTTP Server

```bash
# Python 3
python3 -m http.server 8000

# Or use start.sh (converts YAML → JSON first)
./start.sh
```

### 2. Test Module Loading

```javascript
// In browser console
await window.chazonOS.init();
const modules = window.chazonOS.listModules();
console.table(modules);

// Load specific module
const seg = await window.chazonOS.loadModule('segmentation');
console.log('Exports:', seg.exports);
```

### 3. Test Tag Queries

```javascript
// Find all AI modules
const aiModules = window.chazonOS.queryByTag('AI');
console.log('AI modules:', aiModules.map(m => m.name));

// Find all L3 controls
const l3Controls = window.chazonOS.queryByTag('L3');
console.log('L3 controls:', l3Controls);
```

## 🚀 Deployment Checklist

- [ ] Generate all screens from templates
- [ ] Generate all control files from templates
- [ ] Convert config.yaml to config.json
- [ ] Test module loading locally
- [ ] Verify theme integration
- [ ] Check all navigation links
- [ ] Test database loading (if using sql.js)
- [ ] Enable GitHub Pages in repository settings
- [ ] Push to `main` branch
- [ ] Wait 2-3 minutes for deployment
- [ ] Visit `https://yourusername.github.io/qdrant/`
- [ ] Test in multiple browsers
- [ ] Check browser console for errors

## 📈 Size Optimization

### Before Template System
```
280 control files × 3 KB = 840 KB
17 medical screens × 15 KB = 255 KB
Total: ~1.1 MB of duplicate code
```

### After Template System
```
1 control template × 5 KB = 5 KB
280 loader files × 200 bytes = 56 KB
17 generated screens = 350 KB (with external CSS)
Total: ~411 KB (-63% reduction)
```

## 🔧 Troubleshooting

### Module not loading

**Check:**
1. Is module listed in `/os/modules.json`?
2. Does file exist at specified path?
3. Is path correct (absolute from root)?
4. Check browser console for errors

### Tags not matching

**Check:**
1. Tags are case-sensitive: `"Medical"` ≠ `"medical"`
2. Use exact tag strings from registry
3. Query with array: `queryByTag(["Medical", "AI"])`

### Database not loading

**Check:**
1. Did you run `database/migrate.py`?
2. Is `database/chazon.db` committed to git?
3. Is sql.js loaded before database.js?
4. Check browser console for loading errors

## 🎯 Best Practices

1. **Tag Consistently**
   - Use same tag names across modules and controls
   - Follow ISA-95 level naming (L0, L1, L2, L3, L4)

2. **Minimize Dependencies**
   - Keep modules independent where possible
   - Use dependency field for required modules only

3. **Test Locally First**
   - Always test with local server before pushing
   - Check browser console for errors

4. **Use Templates**
   - Generate files from templates, don't hand-write
   - Regenerate after template changes

5. **Keep Registry Updated**
   - Add new modules to `/os/modules.json`
   - Update when paths or tags change

## 📚 Additional Resources

- **ISA-95 Standards:** Enterprise-Control System Integration
- **ISA-101 HMI:** High Performance HMI Design
- **sql.js Documentation:** https://sql.js.org/
- **GitHub Pages Guide:** https://pages.github.com/

---

**Last Updated:** 2025-11-17
**Version:** 1.0.0
