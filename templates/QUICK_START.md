# Template System - Quick Start Guide

Get started with the template system in 5 minutes.

## Installation

No installation required! The template system is already integrated.

## Basic Usage

### 1. View Available Screens

**Option A: Main HMI**
1. Open `/home/user/qdrant/hmi.html`
2. Click "Template Screens" button
3. Browse available screens

**Option B: HMI Control System**
1. Open `/home/user/qdrant/index/controls/HMI/index.html`
2. Scroll to "Template-Based Screens" section
3. Click any screen card

**Option C: Template Viewer**
1. Open `/home/user/qdrant/templates/example-hmi.html`
2. Select screen from dropdown
3. Click "Load Screen"

### 2. Load a Screen

```html
<!DOCTYPE html>
<html>
<head>
  <script src="/templates/template-loader.js"></script>
</head>
<body>
  <div id="hmi-container"></div>

  <script>
    // Load System Overview screen
    loadScreen('550e8400-e29b-41d4-a716-446655440000', 'hmi-container');
  </script>
</body>
</html>
```

### 3. Navigate by Tag

```javascript
// Load first "overview" screen
await loadScreenByTag('overview', 'hmi-container');
```

### 4. Search Screens

```javascript
// Search for screens
const results = await window.templateLoader.searchTemplates('alarm', 'screen');
console.log('Found', results.length, 'screens');
```

## Available Screens

| Screen | UUID | Tag |
|--------|------|-----|
| System Overview | `550e8400-e29b-41d4-a716-446655440000` | `overview` |
| Equipment Detail | `660e8400-e29b-41d4-a716-446655440001` | `detail` |
| Alarm Management | `770e8400-e29b-41d4-a716-446655440002` | `alarm` |
| Historical Trend | `880e8400-e29b-41d4-a716-446655440003` | `trend` |

## Common Tasks

### Open a Screen in New Window

```javascript
// Using HMI navigation
hmiNav.navigateToTemplate('550e8400-e29b-41d4-a716-446655440000', true);

// Or directly
window.open('templates/example-hmi.html?uuid=550e8400-e29b-41d4-a716-446655440000');
```

### Filter Screens by Tag

```javascript
await window.templateLoader.loadIndexes();
const screens = window.templateLoader.indexes.screens.screens;

const alarmScreens = screens.filter(s => s.tags.includes('alarm'));
console.log('Alarm screens:', alarmScreens);
```

### Generate Static HTML

```bash
# Generate all screens
node templates/generate-screens.js --all

# Generate specific screen
node templates/generate-screens.js --uuid 550e8400-e29b-41d4-a716-446655440000

# Or use web interface
# Open: templates/screen-generator-web.html
```

## Examples

### UUID Navigation
See: `/templates/examples/uuid-navigation-example.html`
- Direct UUID navigation
- URL parameter loading
- Dynamic loading

### Tag Navigation
See: `/templates/examples/tag-navigation-example.html`
- Tag cloud
- Multi-tag filtering
- Tag statistics

## Next Steps

1. **Read Full Documentation**
   - `/templates/INTEGRATION.md` - Complete integration guide
   - `/templates/README.md` - Template system overview

2. **Explore Examples**
   - `/templates/example-hmi.html` - Basic template viewer
   - `/templates/examples/` - Advanced examples

3. **Create Custom Templates**
   - See template schemas in README.md
   - Add to `/templates/screens/` directory
   - Update `/templates/screens/index.json`

## Tips

- Use UUIDs instead of file paths for navigation
- Tag screens for better organization
- Generate static HTML for production
- Reuse components across screens
- Search by tag for quick access

## Troubleshooting

**Template loader not found?**
```html
<script src="/templates/template-loader.js"></script>
```

**Screen not loading?**
- Check UUID in `/templates/screens/index.json`
- Verify path is correct
- Use web server (not `file://`)

**Need help?**
- Check `/templates/INTEGRATION.md`
- Review examples in `/templates/examples/`
- See `/templates/README.md` for schemas
