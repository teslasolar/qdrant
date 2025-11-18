# Integration Guide: Standards-as-Tags ↔ Existing Systems

## Overview

This guide shows how the Standards-as-Tags framework integrates with the existing Qdrant project template system.

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Standards-as-Tags Framework                     │
│  /home/user/qdrant/standards/                                   │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Standard   │  │   Standard   │  │    Engine    │          │
│  │  Definitions │→ │  Instances   │→ │              │          │
│  │    (JSON)    │  │  (Runtime)   │  │  Generators  │          │
│  └──────────────┘  └──────────────┘  └──────┬───────┘          │
│                                              │                   │
└──────────────────────────────────────────────┼───────────────────┘
                                               │
                            TemplateIntegrationBridge
                                               │
┌──────────────────────────────────────────────┼───────────────────┐
│                 Existing Template System     ▼                   │
│  /home/user/qdrant/templates/                                    │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │     Tags     │  │  Components  │  │   Screens    │          │
│  │   Templates  │  │  Templates   │  │  Templates   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
                          ┌────────────────────────────────┐
                          │   Industrial Control Systems   │
                          │   (PLC, SCADA, HMI, MES)      │
                          └────────────────────────────────┘
```

## Integration Points

### 1. Standard → Tag Template

**Source**: Standards framework generates tag definitions
**Destination**: `/templates/tags/standards/`

**Example**:
```python
from standards.engine.template_integration import TemplateIntegrationBridge
from standards.engine.standard_instantiation_engine import StandardInstantiationEngine

# Create standard instance
engine = StandardInstantiationEngine('/home/user/qdrant/standards')
instance = engine.instantiate(
    standard_id='packml-v1.0',
    instance_id='ct_scanner_1',
    parameters={'equipmentPath': 'Medical/Radiology/CT_Scanner_1'}
)

# Convert to tag template
bridge = TemplateIntegrationBridge(
    engine,
    Path('/home/user/qdrant/templates')
)

tag_template = bridge.standard_to_tag_template('ct_scanner_1')

# Export to existing template system
output_path = bridge.export_to_template_system('ct_scanner_1', 'tag')
# Result: /templates/tags/standards/ct_scanner_1.json
```

**Generated Tag Template Structure**:
```json
{
  "templateType": "packml-tags",
  "instanceId": "ct_scanner_1",
  "equipmentPath": "Medical/Radiology/CT_Scanner_1",
  "tags": [
    {
      "uuid": "tag-ct_scanner_1-state",
      "type": "tag",
      "category": "status",
      "metadata": {
        "name": "CT Scanner 1 - State",
        "standard": "PackML ISA-TR88.00.02"
      },
      "config": {
        "dataType": "Integer",
        "path": "Medical/Radiology/CT_Scanner_1/Status/CurrentState"
      }
    }
    // ... more tags
  ]
}
```

### 2. Standard → HMI Component

**Source**: Standards framework generates HMI components
**Destination**: `/templates/components/standards/`

**Example**:
```python
# Convert PackML instance to HMI component
hmi_component = bridge.standard_to_hmi_component('ct_scanner_1')

# Export to component templates
output_path = bridge.export_to_template_system('ct_scanner_1', 'component')
# Result: /templates/components/standards/ct_scanner_1.json
```

**Generated HMI Component**:
```json
{
  "uuid": "component-ct_scanner_1",
  "type": "component",
  "category": "status-panel",
  "metadata": {
    "name": "PackML Status Panel",
    "standard": "PackML ISA-TR88.00.02"
  },
  "layout": {
    "type": "panel",
    "width": 400,
    "height": 300
  },
  "components": [
    {
      "type": "StatusIndicator",
      "label": "Equipment State",
      "binding": "Medical/Radiology/CT_Scanner_1/Status/StateName",
      "colorMapping": {
        "Stopped": "#E53E3E",
        "Idle": "#48BB78",
        "Execute": "#38B2AC"
      }
    },
    {
      "type": "ButtonPanel",
      "buttons": [
        {"label": "Start", "command": ".../Commands/Start"},
        {"label": "Stop", "command": ".../Commands/Stop"}
      ]
    }
  ]
}
```

### 3. Standard → HMI Screen (ISA-101)

**Source**: ISA-101 standard instances
**Destination**: `/templates/screens/standards/`

**Example**:
```python
# Instantiate ISA-101 HMI screen
screen = engine.instantiate(
    standard_id='isa-101-hmi-v1.0',
    instance_id='radiology_overview',
    parameters={
        'screenLevel': 'overview',
        'scope': 'Radiology_Department',
        'colorScheme': 'highPerformance'
    }
)

# Convert to HMI screen template
hmi_screen = bridge.standard_to_hmi_component('radiology_overview')

# This generates a complete ISA-101 compliant screen layout
# Compatible with existing /templates/screens/ structure
```

## Workflow Examples

### Workflow 1: Standards-First Development

```python
# 1. Define equipment structure using ISA-88
hierarchy = engine.instantiate(
    standard_id='isa-88-equipment-v1.0',
    instance_id='facility_hierarchy',
    parameters={'enterpriseName': 'MedTech', 'siteName': 'Boston'}
)

# 2. Add PackML to each unit
for unit in ['CT_Scanner_1', 'CT_Scanner_2', 'MRI_Scanner_1']:
    packml = engine.instantiate(
        standard_id='packml-v1.0',
        instance_id=f'{unit}_packml',
        parameters={'equipmentPath': f'MedTech/Boston/Radiology/{unit}'}
    )

    # 3. Export to template system
    bridge.export_to_template_system(f'{unit}_packml', 'tag')
    bridge.export_to_template_system(f'{unit}_packml', 'component')

# Result: Complete tag structure and HMI components for all equipment
```

### Workflow 2: Retrofit Existing System

```python
# 1. Analyze existing tags in /templates/tags/
# 2. Identify which standards apply
# 3. Instantiate matching standards
# 4. Compare generated vs. existing
# 5. Migrate to standards-based approach incrementally

# Example: Existing motor control → PackML
existing_motor = load_existing_template('/templates/tags/motor-running.json')

# Instantiate PackML for motor
motor_packml = engine.instantiate(
    standard_id='packml-v1.0',
    instance_id='motor_1',
    parameters={'equipmentPath': existing_motor['path']}
)

# Generate enhanced tags with PackML states
enhanced_tags = bridge.standard_to_tag_template('motor_1')
```

### Workflow 3: Multi-Standard System

```python
# Complete system with all standards
composition = engine.compose_standards(
    composition_id='radiology_complete',
    standards=[
        # Organization
        {'standardId': 'isa-88-equipment-v1.0',
         'instanceId': 'hierarchy',
         'parameters': {'enterpriseName': 'Hospital'}},

        # Equipment control
        {'standardId': 'packml-v1.0',
         'instanceId': 'ct1_packml',
         'parameters': {'equipmentPath': '...'}},

        # Architecture
        {'standardId': 'isa-95-functional-v1.0',
         'instanceId': 'architecture',
         'parameters': {}},

        # Communication
        {'standardId': 'mqtt-sparkplug-v1.0',
         'instanceId': 'ct1_mqtt',
         'parameters': {'groupId': 'Hospital'}},

        {'standardId': 'opc-ua-v1.0',
         'instanceId': 'ct1_opcua',
         'parameters': {'serverUrl': 'opc.tcp://...'}},

        # Visualization
        {'standardId': 'isa-101-hmi-v1.0',
         'instanceId': 'overview_screen',
         'parameters': {'screenLevel': 'overview'}}
    ]
)

# Export entire composition to template system
for instance_id in composition['instances']:
    bridge.export_to_template_system(instance_id, 'tag')
    bridge.export_to_template_system(instance_id, 'component')
```

## Directory Mapping

### Standards Framework → Template System

```
/standards/                          /templates/
├── packml/                    →    ├── tags/standards/
│   └── instances/             →    │   └── packml-*.json
├── isa-88/                    →    ├── components/standards/
│   └── instances/             →    │   └── isa88-*.json
├── isa-101/                   →    └── screens/standards/
│   └── instances/             →        └── isa101-*.json
```

### Standards Framework → HMI Templates

```
/standards/                          /index/controls/HMI/templates/
├── isa-101/                   →    ├── components/
│   └── hmi-design-patterns    →    │   └── Standards*.json
└── packml/                    →    └── base/
    └── packml-state-machine   →        └── PackMLBase.json
```

## Usage in Existing Project

### In PLC Programming

```python
# 1. Generate PackML tags for PLC
packml_tags = bridge.standard_to_tag_template('equipment_packml')

# 2. Export to PLC tag database format
# (Custom exporter would convert to PLC-specific format)
export_to_plc(packml_tags, format='Allen-Bradley')

# Result: PLC program with standard PackML tag structure
```

### In SCADA/HMI Development

```python
# 1. Generate ISA-101 compliant screens
overview = engine.instantiate('isa-101-hmi-v1.0', 'plant_overview', {...})
detail = engine.instantiate('isa-101-hmi-v1.0', 'ct_detail', {...})

# 2. Export to Ignition-compatible format
export_to_ignition(overview, 'PlantOverview.json')
export_to_ignition(detail, 'CTDetail.json')

# Result: Ignition screens following ISA-101 design principles
```

### In MES Integration

```python
# 1. Generate ISA-95 architecture
architecture = engine.instantiate('isa-95-functional-v1.0', 'facility', {...})

# 2. Generate OPC-UA interface
opcua = engine.instantiate('opc-ua-v1.0', 'mes_interface', {...})

# 3. Use for MES configuration
mes_config = {
    'levels': architecture.generated_content['levels'],
    'opcua_nodes': opcua.generated_content['addressSpace']
}

# Result: MES system configured per ISA-95 architecture
```

### In IIoT/Cloud Integration

```python
# 1. Generate MQTT/Sparkplug configuration
mqtt = engine.instantiate('mqtt-sparkplug-v1.0', 'equipment_mqtt', {
    'groupId': 'Hospital',
    'edgeNodeId': 'Gateway1',
    'deviceId': 'CT_Scanner_1'
})

# 2. Configure edge gateway
gateway_config = {
    'topics': mqtt.generated_content['topicNamespace'],
    'metrics': mqtt.generated_content['metricNaming'],
    'birth_death': mqtt.generated_content['birthDeathSequence']
}

# Result: Edge gateway publishing data to cloud
```

## Compatibility

### With Existing Templates

The TemplateIntegrationBridge ensures compatibility:

- **Tag Templates**: Generates same structure as `/templates/tags/*.json`
- **Components**: Compatible with `/templates/components/*.json`
- **Screens**: Works with `/templates/screens/*.json`

### Custom Adapters

Create custom adapters for specific systems:

```python
class IgnitionAdapter(TemplateIntegrationBridge):
    def to_ignition_view(self, instance_id):
        """Convert to Ignition Perspective view"""
        instance = self.engine.get_instance(instance_id)
        # Convert to Ignition JSON format
        return ignition_view

class RockwellAdapter(TemplateIntegrationBridge):
    def to_rslogix_tags(self, instance_id):
        """Convert to RSLogix tag database"""
        instance = self.engine.get_instance(instance_id)
        # Convert to L5X format
        return rslogix_tags
```

## Best Practices

1. **Start with Standards**: Design using standards first, then export
2. **Version Control**: Keep standard instances in version control
3. **Validate**: Always validate parameters during instantiation
4. **Document**: Standards are self-documenting - reference standard IDs
5. **Compose**: Use multiple standards together for complete systems
6. **Export Often**: Generate output files to verify results

## Migration Path

### Phase 1: New Development
- Use standards for all new equipment
- Export to template system
- Build alongside existing templates

### Phase 2: Gradual Migration
- Identify existing equipment that matches standards
- Instantiate matching standards
- Replace manual templates with generated ones

### Phase 3: Full Adoption
- All equipment uses standards
- Template system becomes output of standards
- Standards are source of truth

## Support

- **Examples**: See `/standards/examples/` for integration patterns
- **API Docs**: See `/standards/README.md` for complete API
- **Bridge Code**: Review `/standards/engine/template_integration.py`

---

**Integration Status**: Fully compatible with existing Qdrant template system
