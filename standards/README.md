# Standards-as-Tags Framework

> Treat industrial standards as executable, instantiable templates

## Overview

The **Standards-as-Tags Framework** transforms industrial automation standards from static documentation into executable, composable code templates. Instead of manually implementing standards, you instantiate them like software classes, generating complete tag structures, state machines, hierarchies, and communication interfaces.

### Philosophy

**Program WITH standards, not just TO standards.**

Traditional approach:
```
1. Read ISA-88 specification (100+ pages)
2. Manually design tag structure
3. Manually implement state machine
4. Hope you got it right
```

Standards-as-Tags approach:
```python
# Instantiate PackML for CT Scanner
packml = engine.instantiate(
    standard_id='packml-v1.0',
    instance_id='ct_scanner_1',
    parameters={'equipmentPath': 'Medical/Radiology/CT_Scanner_1'}
)
# Done! Complete PackML implementation with 18 states, commands, tags
```

## Key Concepts

### 1. Standards are Templates

Each industrial standard is defined as a **JSON template** with:
- **Metadata**: Name, version, description
- **Structure**: States, levels, patterns, protocols
- **Parameters**: Configurable values (equipment paths, names, etc.)
- **Generation Rules**: How to create tags, hierarchies, interfaces
- **Validation Rules**: Ensure correctness

### 2. Instantiation = Code Generation

Instantiating a standard with parameters **generates**:
- Tag structures (tag names, paths, data types)
- State machines (states, transitions, commands)
- Hierarchies (equipment organization, functional levels)
- Communication interfaces (MQTT topics, OPC-UA nodes)
- HMI bindings (screen layouts, component configurations)

### 3. Composition = Integration

Multiple standards can be **composed** to create complete systems:
- ISA-88 (equipment hierarchy) + PackML (state machines)
- PackML (control) + MQTT (communication)
- ISA-95 (architecture) + OPC-UA (interoperability)
- All standards + ISA-101 (visualization)

### 4. Meta-Standard Language (MSL)

A **domain-specific language** for composing standards:

```msl
# Import standards
import packml from "packml/packml-state-machine.json"
import isa88 from "isa-88/equipment-hierarchy.json"

# Instantiate for equipment
instantiate packml as ct_scanner_packml with {
    equipmentPath: "Medical/Radiology/CT_Scanner_1"
}

# Compose with hierarchy
instantiate isa88 as medical_hierarchy with {
    enterpriseName: "Hospital_Boston"
}

# Bind together
bind ct_scanner_packml.tags to medical_hierarchy.tagStructure
```

## Available Standards

### Equipment & Control

#### PackML State Machine (`packml/packml-state-machine.json`)
- **ISA-TR88.00.02** - Packaging Machine Language
- 18 states (Stopped, Idle, Execute, Held, Aborted, etc.)
- Standard commands (Start, Stop, Reset, Abort, etc.)
- Generates: State tags, command tags, indicators
- **Use Case**: Any equipment needing state management

#### ISA-88 Equipment Hierarchy (`isa-88/equipment-hierarchy.json`)
- **ANSI/ISA-88.01** - Batch Control Equipment Model
- 7 levels: Enterprise → Site → Area → Cell → Unit → Module → Control
- Hierarchical tag organization
- Generates: Equipment paths, tag structure, navigation
- **Use Case**: Organizing equipment in standardized hierarchy

#### ISA-88 Procedural Model (`isa-88/procedural-model.json`)
- **ANSI/ISA-88.01** - Batch Control Procedures
- Recipe model (Master & Control recipes)
- 4 procedural levels: Procedure → Unit Procedure → Operation → Phase
- Generates: Recipe structure, execution state machines
- **Use Case**: Batch processes, workflows, multi-step operations

### System Architecture

#### ISA-95 Functional Hierarchy (`isa-95/functional-hierarchy.json`)
- **ANSI/ISA-95.00.01** - Purdue Model
- 5 functional levels (L4 Business → L0 Process)
- Communication paths between levels
- Security zones (Enterprise, DMZ, Control, Field)
- Generates: System architecture, integration points
- **Use Case**: Overall system design, MES/ERP integration

### Visualization

#### ISA-101 HMI Design Patterns (`isa-101/hmi-design-patterns.json`)
- **ANSI/ISA-101.01-2015** - HMI Design
- 4 screen levels (Overview, Group, Detail, Diagnostic)
- High-performance HMI principles
- Color schemes, information density, navigation
- Generates: Screen layouts, component definitions
- **Use Case**: SCADA/HMI design

### Communication Protocols

#### MQTT/Sparkplug B (`protocols/mqtt-sparkplug.json`)
- **MQTT 3.1.1/5.0 + Sparkplug B v1.0**
- Topic namespace (spBv1.0/{group}/{type}/{node}/{device})
- Birth/Death certificates
- Metric definitions
- Generates: MQTT topics, payload structures, publisher configs
- **Use Case**: IIoT, cloud connectivity, edge devices

#### OPC-UA (`protocols/opc-ua.json`)
- **IEC 62541** - OPC Unified Architecture
- Address space organization
- Node definitions (Objects, Variables, Methods)
- Security configurations
- Generates: OPC-UA node structure, server/client configs
- **Use Case**: Interoperability, PLC-SCADA-MES integration

## Installation & Setup

### Prerequisites
- Python 3.8+
- Access to `/home/user/qdrant/standards/` directory

### Quick Start

```python
from pathlib import Path
from standards.engine.standard_instantiation_engine import StandardInstantiationEngine

# Initialize engine
engine = StandardInstantiationEngine('/home/user/qdrant/standards')

# List available standards
standards = engine.list_available_standards()
for std in standards:
    print(f"{std['standardId']}: {std['name']}")

# Instantiate PackML for equipment
ct_packml = engine.instantiate(
    standard_id='packml-v1.0',
    instance_id='ct_scanner_1_packml',
    parameters={
        'equipmentPath': 'Medical/Radiology/CT_Scanner_1',
        'safetyLevel': 'high'
    }
)

# Export generated tags
engine.export_instance('ct_scanner_1_packml',
                      Path('output/ct_scanner_1_packml.json'))
```

## Examples

### Example 1: PackML for CT Scanner
```bash
python standards/examples/01_packml_ct_scanner.py
```

Demonstrates:
- Instantiating PackML state machine
- Generated tag structure
- State definitions and transitions
- Integration with control systems

### Example 2: ISA-88 Recipe for DICOM Processing
```bash
# MSL file - parse and execute
python -m standards.meta-standard.msl_parser standards/examples/02_isa88_dicom_recipe.msl
```

Demonstrates:
- Creating complete ISA-88 recipe
- Multi-level procedural model
- Equipment binding

### Example 3: ISA-95 Functional Hierarchy
```bash
python standards/examples/03_isa95_hierarchy.py
```

Demonstrates:
- 5-level Purdue model
- Communication flows
- Security zones
- System architecture

### Example 4: Multi-Standard Composition
```bash
python standards/examples/04_multi_standard_composition.py
```

Demonstrates:
- Composing 6+ standards
- Complete medical imaging system
- ISA-88 + PackML + MQTT + OPC-UA + ISA-95 + ISA-101
- Full data flow and integration

## Directory Structure

```
/standards/
├── README.md                          # This file
├── packml/
│   └── packml-state-machine.json     # PackML standard definition
├── isa-88/
│   ├── equipment-hierarchy.json       # ISA-88 equipment model
│   └── procedural-model.json          # ISA-88 recipes & procedures
├── isa-95/
│   └── functional-hierarchy.json      # ISA-95 Purdue model
├── isa-101/
│   └── hmi-design-patterns.json       # ISA-101 HMI design
├── protocols/
│   ├── mqtt-sparkplug.json            # MQTT/Sparkplug B
│   └── opc-ua.json                    # OPC-UA
├── engine/
│   ├── standard_instantiation_engine.py  # Core engine
│   └── template_integration.py           # Template system bridge
├── meta-standard/
│   └── msl_parser.py                  # MSL language parser
└── examples/
    ├── 01_packml_ct_scanner.py
    ├── 02_isa88_dicom_recipe.msl
    ├── 03_isa95_hierarchy.py
    ├── 04_multi_standard_composition.py
    └── instances/                     # Generated instances
```

## Core API

### StandardInstantiationEngine

```python
engine = StandardInstantiationEngine(standards_root)

# Load a standard
standard = engine.load_standard('packml/packml-state-machine.json')

# List available standards
standards = engine.list_available_standards()

# Instantiate a standard
instance = engine.instantiate(
    standard_id='packml-v1.0',
    instance_id='my_equipment',
    parameters={'equipmentPath': 'Site/Area/Unit'},
    validate=True
)

# Compose multiple standards
composition = engine.compose_standards(
    composition_id='complete_system',
    standards=[
        {'standardId': 'packml-v1.0', 'instanceId': 'eq1', 'parameters': {...}},
        {'standardId': 'isa88-equipment-v1.0', 'instanceId': 'hierarchy', 'parameters': {...}}
    ]
)

# Export instance
engine.export_instance('my_equipment', Path('output.json'))

# Get instance
instance = engine.get_instance('my_equipment')
```

### Meta-Standard Language (MSL)

```python
from standards.meta_standard.msl_parser import parse_msl, execute_msl

# Parse MSL source
ast = parse_msl(source_code)

# Execute MSL program
results = execute_msl(source_code, engine)
```

### Template Integration

```python
from standards.engine.template_integration import TemplateIntegrationBridge

bridge = TemplateIntegrationBridge(standards_engine, templates_root)

# Convert to tag template
tag_template = bridge.standard_to_tag_template('instance_id')

# Convert to HMI component
hmi_component = bridge.standard_to_hmi_component('instance_id')

# Export to existing template system
path = bridge.export_to_template_system('instance_id', 'tag')
```

## Use Cases

### 1. Greenfield Projects
Start with standards, generate entire system:
- Instantiate ISA-95 for architecture
- Instantiate ISA-88 for equipment organization
- Instantiate PackML for each unit
- Instantiate MQTT for communication
- Instantiate ISA-101 for HMI
- **Result**: Complete, standards-compliant system

### 2. Brownfield Retrofit
Add standards to existing systems:
- Analyze existing equipment
- Instantiate appropriate standards
- Generate integration layer
- Bridge to existing systems
- **Result**: Standards compliance without rebuild

### 3. Multi-Site Standardization
Ensure consistency across facilities:
- Define standard once
- Instantiate for each site/area/unit
- Automatic consistency
- Easy replication
- **Result**: Standardized operations

### 4. Vendor Integration
Enable interoperability:
- Use OPC-UA standard for interface
- PackML for equipment control
- MQTT for data sharing
- **Result**: Vendor-independent integration

### 5. Digital Twin / Simulation
Create virtual replicas:
- Instantiate standards for virtual equipment
- Generate same tag structure
- Test before deployment
- **Result**: Risk-free validation

## Benefits

### 1. Correctness
✓ Standards defined by experts, not manually implemented
✓ Validation built into instantiation
✓ Impossible to violate standard structure

### 2. Consistency
✓ Same standard = same implementation
✓ Automatic naming conventions
✓ Uniform tag structure

### 3. Speed
✓ Instantiate vs. manually implement (hours → seconds)
✓ Generate complete systems
✓ Rapid prototyping

### 4. Maintainability
✓ Standards-based = self-documenting
✓ Clear structure and organization
✓ Easier training and knowledge transfer

### 5. Interoperability
✓ Standards ensure compatibility
✓ OPC-UA, PackML enable vendor independence
✓ Easier integration

### 6. Scalability
✓ Add equipment by instantiating
✓ Expand to new sites easily
✓ Reuse patterns

## Advanced Topics

### Creating Custom Standards

1. **Define Standard JSON**:
```json
{
  "standardId": "my-custom-standard-v1.0",
  "type": "custom-type",
  "metadata": {...},
  "specification": {...},
  "parameters": [...],
  "content": {...}
}
```

2. **Add to standards directory**
3. **Instantiate like any standard**

### Extending Existing Standards

Use MSL `extend` keyword:
```msl
extend packml with {
    additionalStates: [...],
    customCommands: [...]
}
```

### Standard Composition Patterns

**Layered Architecture**:
- ISA-95 (overall architecture)
- ISA-88 (equipment organization)
- PackML (equipment control)
- Protocols (communication)
- ISA-101 (visualization)

**Horizontal Integration**:
- Multiple equipment units
- Same standards
- Integrated via communication protocols

## Integration Points

### With Existing Systems

1. **Tag Templates**: Generate tags compatible with existing template system
2. **HMI Components**: Create ISA-101 compliant screens
3. **OPC-UA Servers**: Generate node structure
4. **MQTT Publishers**: Configure Sparkplug B
5. **Historians**: Standard tag organization for easy trending

### With Development Workflow

1. **Design**: Instantiate standards for system design
2. **Implementation**: Export to PLC/SCADA projects
3. **Testing**: Validate against standard definitions
4. **Deployment**: Generate configuration files
5. **Documentation**: Standards are self-documenting

## Troubleshooting

### Common Issues

**Standard Not Found**:
```python
# Ensure correct path
engine.load_standard('packml/packml-state-machine.json')  # ✓ Correct
engine.load_standard('packml.json')  # ✗ Wrong
```

**Parameter Validation Failed**:
```python
# Check required parameters
standard = engine.loaded_standards['packml-v1.0']
print(standard.parameters)  # See what's required
```

**Template Integration Issues**:
```python
# Verify templates_root path
bridge = TemplateIntegrationBridge(engine, Path('/home/user/qdrant/templates'))
```

## Contributing

To add a new standard:

1. Create JSON definition following standard structure
2. Place in appropriate subdirectory
3. Add validation rules
4. Create example usage
5. Update documentation

## License

Part of the Qdrant Medical Imaging Virtual Factory project.

## References

- **ISA-88**: Batch Control Standard
- **ISA-95**: Enterprise-Control System Integration
- **ISA-101**: Human Machine Interfaces for Process Automation Systems
- **PackML**: ISA-TR88.00.02 - Packaging Machine Language
- **MQTT**: OASIS MQTT Specification
- **Sparkplug B**: Eclipse Sparkplug Specification
- **OPC-UA**: IEC 62541 OPC Unified Architecture

## Support

For questions or issues:
- Review `/standards/examples/` for usage patterns
- Check standard JSON definitions for parameters
- See API documentation in this README

---

**Standards-as-Tags Framework** - Programming WITH Standards Since 2025
