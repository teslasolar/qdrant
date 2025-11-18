# Templates System

JSON-based templating system for HMI screens, components, tags, and controls.

## Directory Structure

```
templates/
├── screens/          # Complete HMI screen templates
│   ├── overview/     # System overview screens
│   ├── detail/       # Detailed equipment screens
│   ├── alarm/        # Alarm management screens
│   ├── trend/        # Trending/historical data screens
│   └── process/      # Process control screens
├── components/       # Reusable UI components
│   ├── buttons/      # Button components
│   ├── gauges/       # Gauge/meter components
│   ├── charts/       # Chart/graph components
│   ├── indicators/   # Status indicator components
│   └── inputs/       # Input control components
├── tags/             # Tag definition templates
├── controls/         # Control logic templates
└── layouts/          # Layout templates
```

## Template Structure

### Screen Template Schema
```json
{
  "uuid": "unique-identifier",
  "type": "screen",
  "category": "overview|detail|alarm|trend|process",
  "metadata": {
    "name": "Screen Name",
    "description": "Description",
    "version": "1.0.0",
    "author": "Author Name",
    "created": "2025-01-01T00:00:00Z",
    "modified": "2025-01-01T00:00:00Z",
    "tags": ["tag1", "tag2"]
  },
  "layout": {
    "grid": {
      "columns": 12,
      "rows": 8,
      "gap": 10
    },
    "theme": "dark|light",
    "colorScheme": "blue|green|red|yellow"
  },
  "components": [
    {
      "uuid": "component-uuid",
      "type": "gauge|chart|button|indicator|input",
      "position": {
        "x": 0,
        "y": 0,
        "width": 2,
        "height": 2
      },
      "config": {},
      "bindings": {
        "tags": ["tag-path"]
      }
    }
  ],
  "actions": [
    {
      "trigger": "onLoad|onClick|onChange",
      "action": "navigate|writeTag|showModal"
    }
  ]
}
```

### Component Template Schema
```json
{
  "uuid": "unique-identifier",
  "type": "component",
  "category": "button|gauge|chart|indicator|input",
  "metadata": {
    "name": "Component Name",
    "description": "Description",
    "version": "1.0.0"
  },
  "template": {
    "html": "<div>...</div>",
    "css": "...",
    "js": "..."
  },
  "properties": [
    {
      "name": "label",
      "type": "string",
      "default": "Button"
    }
  ],
  "bindings": {
    "tags": []
  }
}
```

### Tag Template Schema
```json
{
  "uuid": "unique-identifier",
  "type": "tag",
  "category": "analog|digital|string",
  "metadata": {
    "name": "Tag Name",
    "description": "Description",
    "dataType": "Float|Int|Bool|String",
    "engUnits": "°C|PSI|RPM",
    "minValue": 0,
    "maxValue": 100,
    "alarmLow": 10,
    "alarmHigh": 90
  },
  "historization": {
    "enabled": true,
    "sampleRate": 1000,
    "deadband": 0.1
  }
}
```

## Usage

### Loading a Screen by UUID
```javascript
async function loadScreen(uuid) {
  const response = await fetch(`/templates/screens/index.json`);
  const index = await response.json();
  const screenPath = index.screens.find(s => s.uuid === uuid).path;
  const screen = await fetch(screenPath).then(r => r.json());
  return screen;
}
```

### Loading a Screen by Tag
```javascript
async function loadScreenByTag(tag) {
  const response = await fetch(`/templates/screens/index.json`);
  const index = await response.json();
  const screens = index.screens.filter(s => s.tags.includes(tag));
  return screens;
}
```

## Template Categories

### Screen Templates
- **overview**: High-level system overview screens
- **detail**: Detailed equipment/process screens
- **alarm**: Alarm management and acknowledgment
- **trend**: Historical trending and analytics
- **process**: Process control and setpoint management

### Component Templates
- **buttons**: Start/stop, reset, acknowledge buttons
- **gauges**: Analog gauges, meters, progress bars
- **charts**: Line charts, bar charts, pie charts
- **indicators**: Status lights, boolean indicators
- **inputs**: Numeric input, text input, sliders

## Examples

See individual template files for complete examples.
