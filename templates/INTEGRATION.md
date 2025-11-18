# Template System Integration Guide

This guide explains how to integrate the JSON template system with existing HMI files in the qdrant project.

## Overview

The template system provides:
- **JSON-based screen templates** - Define HMI screens in declarative JSON format
- **Reusable components** - Build libraries of buttons, gauges, charts, and indicators
- **UUID-based navigation** - Navigate between screens using UUIDs instead of file paths
- **Tag-based organization** - Organize and filter screens by tags
- **Dynamic screen generation** - Generate static HTML files from templates

## Quick Start

### 1. Include the Template Loader

Add the template loader script to your HTML file:

```html
<script src="/templates/template-loader.js"></script>
```

### 2. Load a Screen by UUID

```javascript
// Load a screen by its UUID
await loadScreen('550e8400-e29b-41d4-a716-446655440000', 'hmi-container');
```

### 3. Load a Screen by Tag

```javascript
// Load the first screen with the 'overview' tag
await loadScreenByTag('overview', 'hmi-container');
```

### 4. Load a Screen by Name

```javascript
// Load a screen by its name
await loadScreenByName('System Overview', 'hmi-container');
```

## Integration Points

### Main HMI File (/home/user/qdrant/hmi.html)

The main HMI control panel has been updated with:

1. **Template Loader Script**
   ```html
   <script src="templates/template-loader.js"></script>
   ```

2. **Template Screens Button**
   - Added "Template Screens" button to footer
   - Opens modal showing all available template screens
   - Supports loading by UUID or tag

3. **Template Modal**
   - Browse available template screens
   - Search by tag
   - Click to load screen in new window

**Usage:**
1. Open `/home/user/qdrant/hmi.html`
2. Click "Template Screens" button in footer
3. Browse or search for screens
4. Click a screen to load it

### HMI Control System (/home/user/qdrant/index/controls/HMI/)

The existing HMI control system has been enhanced with:

1. **Template Loader Integration**
   ```html
   <script src="../../../templates/template-loader.js"></script>
   ```

2. **Enhanced Navigation System**
   - Added `navigateToTemplate(uuid)` method
   - Added `navigateToScreenByTag(tag)` method
   - Automatic template screen loading

3. **Template Screens Section**
   - Dynamically loads and displays template screens
   - Click any template screen to open it in new window

**Usage:**
1. Open `/home/user/qdrant/index/controls/HMI/index.html`
2. Scroll to "Template-Based Screens" section
3. Click any template screen card to open it

## Screen Generator

### Node.js Script

Generate static HTML files from templates:

```bash
# Generate all screens
node /home/user/qdrant/templates/generate-screens.js --all

# Generate specific screen by UUID
node /home/user/qdrant/templates/generate-screens.js --uuid 550e8400-e29b-41d4-a716-446655440000

# Generate screens by tag
node /home/user/qdrant/templates/generate-screens.js --tag overview

# Specify output directory
node /home/user/qdrant/templates/generate-screens.js --all --output ./build/screens
```

### Web-Based Generator

For browser-based generation:

1. Open `/home/user/qdrant/templates/screen-generator-web.html`
2. Select screens to generate
3. Click "Generate Selected"
4. HTML files will download automatically

## API Reference

### Template Loader

#### `loadScreen(uuid, containerId)`
Load and render a screen by UUID.

```javascript
await loadScreen('550e8400-e29b-41d4-a716-446655440000', 'hmi-container');
```

#### `loadScreenByTag(tag, containerId)`
Load the first screen matching a tag.

```javascript
await loadScreenByTag('overview', 'hmi-container');
```

#### `loadScreenByName(name, containerId)`
Load a screen by its name.

```javascript
await loadScreenByName('System Overview', 'hmi-container');
```

#### `window.templateLoader.loadScreensByTag(tag)`
Get all screens with a specific tag.

```javascript
const screens = await window.templateLoader.loadScreensByTag('alarm');
console.log(`Found ${screens.length} alarm screens`);
```

#### `window.templateLoader.searchTemplates(query, type)`
Search for templates.

```javascript
const results = await window.templateLoader.searchTemplates('equipment', 'screen');
```

### HMI Navigation

#### `hmiNav.navigateToTemplate(uuid, newWindow)`
Navigate to a template screen.

```javascript
await hmiNav.navigateToTemplate('550e8400-e29b-41d4-a716-446655440000', true);
```

#### `hmiNav.navigateToScreenByTag(tag, newWindow)`
Navigate to a screen by tag.

```javascript
await hmiNav.navigateToScreenByTag('overview', true);
```

## Available Template Screens

The following template screens are currently available:

| UUID | Name | Category | Tags |
|------|------|----------|------|
| `550e8400-e29b-41d4-a716-446655440000` | System Overview | overview | overview, master, dashboard |
| `660e8400-e29b-41d4-a716-446655440001` | Equipment Detail | detail | detail, equipment, control |
| `770e8400-e29b-41d4-a716-446655440002` | Alarm Management | alarm | alarm, management, notification |
| `880e8400-e29b-41d4-a716-446655440003` | Historical Trend | trend | trend, historical, analysis |

## Examples

### Example 1: UUID-Based Navigation

See: `/home/user/qdrant/templates/examples/uuid-navigation-example.html`

This example demonstrates:
- Direct UUID navigation
- Tag-based navigation
- Search and navigate
- Dynamic screen loading
- URL parameter loading

### Example 2: Tag-Based Navigation

See: `/home/user/qdrant/templates/examples/tag-navigation-example.html`

This example demonstrates:
- Tag cloud visualization
- Single tag filtering
- Multi-tag filtering
- Tag statistics
- Screen categorization

## Directory Structure

```
/home/user/qdrant/
├── hmi.html                          # Main HMI (integrated)
├── templates/
│   ├── template-loader.js            # Template loader library
│   ├── example-hmi.html              # Example template viewer
│   ├── generate-screens.js           # Node.js screen generator
│   ├── screen-generator-web.html     # Web-based generator
│   ├── screens/
│   │   ├── index.json                # Screen index
│   │   ├── overview/
│   │   ├── detail/
│   │   ├── alarm/
│   │   └── trend/
│   ├── components/
│   │   ├── index.json                # Component index
│   │   ├── buttons/
│   │   ├── gauges/
│   │   └── indicators/
│   ├── tags/
│   │   └── index.json                # Tag index
│   └── examples/
│       ├── uuid-navigation-example.html
│       └── tag-navigation-example.html
└── index/controls/HMI/
    ├── index.html                    # HMI control system (integrated)
    └── js/
        ├── navigation.js             # Enhanced navigation
        ├── template-loader.js        # Legacy template loader
        └── screen-renderer.js
```

## Best Practices

### 1. Use UUIDs for Navigation

Instead of hardcoding file paths, use UUIDs:

```javascript
// ✅ Good - UUID-based
hmiNav.navigateToTemplate('550e8400-e29b-41d4-a716-446655440000');

// ❌ Avoid - File path-based
window.location.href = 'screens/overview/system-overview.html';
```

### 2. Tag Your Screens

Use descriptive tags for better organization:

```json
{
  "tags": ["overview", "dashboard", "master", "production"]
}
```

### 3. Leverage Tag-Based Navigation

For category-based navigation:

```javascript
// Load any "alarm" screen
await loadScreenByTag('alarm');

// Filter by multiple tags
const screens = allScreens.filter(s =>
  s.tags.includes('overview') && s.tags.includes('dashboard')
);
```

### 4. Reuse Components

Build component libraries and reuse them across screens:

```json
{
  "components": [
    {
      "uuid": "component-uuid",
      "config": {
        "label": "Tank 1",
        "tagPath": "site/tank1/level"
      }
    }
  ]
}
```

### 5. Generate Static HTML for Production

For production deployment, generate static HTML:

```bash
node generate-screens.js --all --output ./dist/screens
```

## Troubleshooting

### Template Loader Not Found

**Problem:** `window.templateLoader is undefined`

**Solution:** Ensure template-loader.js is loaded before use:
```html
<script src="/templates/template-loader.js"></script>
```

### Screen Not Found

**Problem:** `Screen with UUID ${uuid} not found`

**Solution:** Verify the UUID exists in `/templates/screens/index.json`

### Path Issues

**Problem:** Template files not loading

**Solution:** Check the base path configuration:
```javascript
const loader = new TemplateLoader('/templates');
```

### CORS Issues

**Problem:** `Failed to fetch` errors

**Solution:** Serve files through a web server (not `file://` protocol):
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx http-server
```

## Migration Guide

### Migrating from Static HTML to Templates

1. **Extract Screen Structure**
   - Identify grid layout (columns, rows, gap)
   - Identify components and their positions
   - Extract component configurations

2. **Create Template JSON**
   ```json
   {
     "uuid": "unique-uuid",
     "type": "screen",
     "metadata": { ... },
     "layout": { ... },
     "components": [ ... ]
   }
   ```

3. **Update Index**
   - Add entry to `/templates/screens/index.json`
   - Specify category and tags

4. **Update Navigation**
   - Replace file paths with UUIDs
   - Use `navigateToTemplate()` instead of direct links

## Support

For questions or issues:
- See README.md in `/templates/` directory
- Check example files in `/templates/examples/`
- Review template schemas in `/templates/README.md`

## Version History

### v1.0.0 (2025-11-17)
- Initial integration with qdrant project
- Added template loader to main HMI
- Enhanced HMI navigation system
- Created screen generator tools
- Added UUID and tag-based examples
- Integrated with existing HMI infrastructure
