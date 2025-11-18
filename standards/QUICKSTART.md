# Standards-as-Tags Quick Start Guide

Get up and running in 5 minutes.

## 1. Basic Instantiation (30 seconds)

```python
from pathlib import Path
from standards.engine.standard_instantiation_engine import StandardInstantiationEngine

# Initialize
engine = StandardInstantiationEngine('/home/user/qdrant/standards')

# Instantiate PackML for equipment
instance = engine.instantiate(
    standard_id='packml-v1.0',
    instance_id='my_equipment',
    parameters={'equipmentPath': 'Factory/Line1/Machine1'}
)

# Use generated content
print(f"State tag: {instance.generated_content['tags']['stateName']}")
# Output: Factory/Line1/Machine1.Status.StateName
```

## 2. List Available Standards (15 seconds)

```python
standards = engine.list_available_standards()

for std in standards:
    print(f"{std['name']} ({std['standardId']})")
```

Output:
```
PackML State Machine (packml-v1.0)
ISA-88 Equipment Hierarchy (isa-88-equipment-v1.0)
ISA-88 Procedural Model (isa-88-procedural-v1.0)
ISA-95 Functional Hierarchy (isa-95-functional-v1.0)
ISA-101 HMI Design Patterns (isa-101-hmi-v1.0)
MQTT Sparkplug B Protocol (mqtt-sparkplug-v1.0)
OPC Unified Architecture (opc-ua-v1.0)
```

## 3. Compose Multiple Standards (2 minutes)

```python
composition = engine.compose_standards(
    composition_id='complete_line',
    standards=[
        {
            'standardId': 'isa-88-equipment-v1.0',
            'instanceId': 'equipment_hierarchy',
            'parameters': {
                'enterpriseName': 'MyFactory',
                'siteName': 'Plant_A'
            }
        },
        {
            'standardId': 'packml-v1.0',
            'instanceId': 'machine1_packml',
            'parameters': {
                'equipmentPath': 'MyFactory/Plant_A/Line1/Machine1'
            }
        },
        {
            'standardId': 'mqtt-sparkplug-v1.0',
            'instanceId': 'machine1_mqtt',
            'parameters': {
                'groupId': 'Plant_A',
                'edgeNodeId': 'Line1_Gateway',
                'deviceId': 'Machine1',
                'brokerUrl': 'mqtt://broker.factory.com:1883'
            }
        }
    ]
)

print(f"Created composition with {len(composition['instances'])} instances")
```

## 4. Export to Template System (1 minute)

```python
from standards.engine.template_integration import TemplateIntegrationBridge

# Create bridge
bridge = TemplateIntegrationBridge(
    engine,
    Path('/home/user/qdrant/templates')
)

# Convert standard instance to tag template
tag_template = bridge.standard_to_tag_template('machine1_packml')

# Export to template system
output_path = bridge.export_to_template_system('machine1_packml', 'tag')

print(f"Exported to: {output_path}")
```

## 5. Use Meta-Standard Language (1 minute)

Create file `my_system.msl`:
```msl
# Import standards
import packml from "packml/packml-state-machine.json"
import isa88 from "isa-88/equipment-hierarchy.json"

# Instantiate
instantiate packml as machine1 with {
    equipmentPath: "Factory/Line1/Machine1"
}

instantiate isa88 as factory_hierarchy with {
    enterpriseName: "MyFactory"
}

# Generate
generate machine1
```

Execute:
```python
from standards.meta_standard.msl_parser import execute_msl

with open('my_system.msl', 'r') as f:
    source = f.read()

results = execute_msl(source, engine)
print(results)
```

## Common Patterns

### Pattern 1: Single Equipment with PackML

```python
# For CT Scanner, Filler, Reactor, etc.
equipment = engine.instantiate(
    standard_id='packml-v1.0',
    instance_id='ct_scanner_1',
    parameters={
        'equipmentPath': 'Hospital/Radiology/CT_Scanner_1',
        'safetyLevel': 'high',
        'enableManualMode': True
    }
)
```

### Pattern 2: Complete Facility Hierarchy

```python
# Organization structure
hierarchy = engine.instantiate(
    standard_id='isa-88-equipment-v1.0',
    instance_id='facility',
    parameters={
        'enterpriseName': 'ACME_Corp',
        'siteName': 'Plant_Boston',
        'includeMetrics': True,
        'maxDepth': 7
    }
)
```

### Pattern 3: Recipe/Batch Process

```python
# For batch manufacturing
recipe = engine.instantiate(
    standard_id='isa-88-procedural-v1.0',
    instance_id='product_a_recipe',
    parameters={
        'recipeName': 'Product_A_Master',
        'recipeType': 'master',
        'includeStateManagement': True
    }
)
```

### Pattern 4: IIoT Communication

```python
# MQTT/Sparkplug for cloud connectivity
mqtt = engine.instantiate(
    standard_id='mqtt-sparkplug-v1.0',
    instance_id='line1_mqtt',
    parameters={
        'groupId': 'Factory_A',
        'edgeNodeId': 'Line1_Gateway',
        'deviceId': 'Machine1',
        'brokerUrl': 'mqtt://iot.company.com:8883',
        'useTls': True
    }
)
```

### Pattern 5: System Architecture

```python
# Overall system design
architecture = engine.instantiate(
    standard_id='isa-95-functional-v1.0',
    instance_id='facility_architecture',
    parameters={
        'enterpriseName': 'ACME_Corp',
        'includeSecurityZones': True,
        'levels': [0, 1, 2, 3, 4]
    }
)
```

### Pattern 6: HMI Screen Design

```python
# High-performance HMI
overview_screen = engine.instantiate(
    standard_id='isa-101-hmi-v1.0',
    instance_id='plant_overview',
    parameters={
        'screenLevel': 'overview',
        'scope': 'Plant_Overview',
        'colorScheme': 'highPerformance',
        'includeAlarms': True
    }
)
```

## Next Steps

1. **Run Examples**:
   ```bash
   cd /home/user/qdrant/standards/examples
   python 01_packml_ct_scanner.py
   python 03_isa95_hierarchy.py
   python 04_multi_standard_composition.py
   ```

2. **Read Full Documentation**:
   - `/standards/README.md` - Complete framework documentation
   - Individual standard JSON files for parameter details

3. **Create Your Own**:
   - Start with single equipment + PackML
   - Add hierarchy with ISA-88
   - Add communication with MQTT or OPC-UA
   - Design HMI with ISA-101
   - Compose into complete system

## Tips

- **Start Simple**: Begin with one standard for one piece of equipment
- **Validate Parameters**: Use `validate=True` when instantiating
- **Check Examples**: All patterns demonstrated in `/standards/examples/`
- **Compose Gradually**: Build up multi-standard compositions incrementally
- **Export Often**: Generate output files to see what's created

## Common Questions

**Q: Which standard should I start with?**
A: Start with PackML for equipment control or ISA-88 for organization.

**Q: Can I modify generated content?**
A: Yes! Instances are JSON - modify as needed after generation.

**Q: How do I know what parameters are required?**
A: Check the standard JSON file's `parameters` array or call with `validate=True`.

**Q: Can I use this in production?**
A: Yes! Generated structures are standards-compliant and production-ready.

**Q: How do I integrate with existing systems?**
A: Use `TemplateIntegrationBridge` to convert to your template format.

---

**Ready to go!** Pick a pattern above and start instantiating standards.
