# Standards-as-Tags Framework

## Purpose

Executable industrial standards implementation providing ISA-88, ISA-95, ISA-101, PackML, MQTT, and OPC-UA frameworks for medical imaging SCADA system integration.

## Directory Structure

```
/standards/
├── structure.md               This file
├── index/
│   └── tag.json              Framework metadata
├── packml/                    PackML state machine
│   ├── states.json           18 states definition
│   ├── transitions.json      State transition rules
│   └── implementation.js     State machine executor
├── isa88/                     Batch control (ISA-88)
│   ├── procedural-model.json Physical/procedural/recipe models
│   ├── batch-states.json     Batch state definitions
│   └── recipe-engine.js      Recipe execution
├── isa95/                     Enterprise integration (ISA-95)
│   ├── levels.json           L0-L4 level definitions
│   ├── information-model.json MES data structures
│   └── integration.js        Enterprise system connector
├── isa101/                    High-performance HMI (ISA-101)
│   ├── design-guidelines.json Visual design rules
│   ├── alarm-management.json  ISA-18.2 alarm philosophy
│   └── theme-generator.js    HMI theme builder
├── mqtt/                      MQTT messaging
│   ├── topics.json           Topic hierarchy
│   ├── qos-config.json       QoS policies
│   └── broker-config.json    Broker settings
├── opcua/                     OPC-UA industrial protocol
│   ├── address-space.json    Node definitions
│   ├── methods.json          Callable methods
│   └── client.js             OPC-UA client
├── engine/                    Instantiation engine
│   ├── interpreter.js        Tag→Code generator
│   ├── validator.js          Standard compliance checker
│   └── composer.js           Multi-standard orchestration
└── meta-standard/             Meta-framework
    ├── standard-schema.json  How to define standards
    └── compliance-tests.js   Automated validation
```

## Standards Overview

### PackML (Packaging Machinery Language)
**Purpose:** State machine for equipment control
**States:** 18 defined states (Idle, Starting, Execute, Completing, etc.)
**Transitions:** Event-driven state changes
**Application:** Medical imaging device control, batch workflows

**Key Files:**
- `packml/states.json` - State definitions with entry/exit actions
- `packml/transitions.json` - Valid state transitions and conditions
- `packml/implementation.js` - JavaScript state machine executor

**Usage:**
```javascript
import { PackMLStateMachine } from '/standards/packml/implementation.js';
const sm = new PackMLStateMachine();
sm.transition('Start'); // Idle → Starting → Execute
```

### ISA-88 (Batch Control)
**Purpose:** Hierarchical batch process control
**Models:** Physical, Procedural, Recipe
**Hierarchy:** Enterprise → Site → Area → Process Cell → Unit → Equipment Module

**Key Files:**
- `isa88/procedural-model.json` - Procedure, unit procedure, operation, phase
- `isa88/batch-states.json` - Running, paused, stopping, stopped, complete
- `isa88/recipe-engine.js` - Recipe execution engine

**Application:** Medical imaging batch processing workflows

### ISA-95 (Enterprise Integration)
**Purpose:** Integration between business and control systems
**Levels:** L0 (Physical) → L1 (Control) → L2 (Supervisory) → L3 (MES) → L4 (Business)
**Models:** Equipment, Material, Personnel, Process Segment

**Key Files:**
- `isa95/levels.json` - Level definitions and responsibilities
- `isa95/information-model.json` - Data structures for MES integration
- `isa95/integration.js` - Enterprise system connector (ERP, MES)

**Application:** CHAZON system architecture follows ISA-95 levels

### ISA-101 (High-Performance HMI)
**Purpose:** Effective HMI design for situational awareness
**Principles:** High contrast, minimal chartjunk, ISA-18.2 alarms
**Levels:** 1 (Overview), 2 (Control), 3 (Detail), 4 (Diagnostic)

**Key Files:**
- `isa101/design-guidelines.json` - Visual design rules (colors, fonts, layouts)
- `isa101/alarm-management.json` - Alarm philosophy per ISA-18.2
- `isa101/theme-generator.js` - Generates CSS themes

**Application:** CHAZON uses cream & purple ISA-101 compliant theme

**Color Philosophy:**
- Background: Dark (purple) for operator attention on data
- Normal: Green (#90ee90)
- Warning: Yellow (#ffd700)
- Alarm: Red (#ff6b6b)
- High contrast cream text (#f5f2e8)

### MQTT (Message Queuing Telemetry Transport)
**Purpose:** Lightweight pub/sub messaging for IoT/IIoT
**Topics:** Hierarchical (e.g., `medical/ct/device01/status`)
**QoS:** 0 (at most once), 1 (at least once), 2 (exactly once)

**Key Files:**
- `mqtt/topics.json` - Topic hierarchy for medical imaging
- `mqtt/qos-config.json` - QoS policies per topic
- `mqtt/broker-config.json` - Mosquitto/HiveMQ config

**Application:** Real-time device telemetry, AI result publishing

**Topic Structure:**
```
medical/
├── xray/{deviceId}/{metric}
├── ct/{deviceId}/{metric}
├── mri/{deviceId}/{metric}
├── ai/segmentation/results
├── ai/detection/results
└── alarms/{level}/{source}
```

### OPC-UA (OPC Unified Architecture)
**Purpose:** Industrial interoperability standard
**Features:** Secure, platform-independent, information modeling
**Services:** Read, write, subscribe, method calls, alarms & conditions

**Key Files:**
- `opcua/address-space.json` - Node definitions (Objects, Variables, Methods)
- `opcua/methods.json` - Callable methods on nodes
- `opcua/client.js` - OPC-UA client implementation

**Application:** Integration with medical imaging devices, PACS systems

**Address Space:**
```
Root
└── Medical
    ├── Devices
    │   ├── CT_Scanner_01
    │   ├── MRI_Unit_02
    │   └── XRay_System_03
    ├── AI
    │   ├── Segmentation
    │   ├── Detection
    │   └── Classification
    └── Quality
        └── Metrics
```

## Instantiation Engine

### Purpose
Convert declarative standard definitions (JSON) into executable code.

### Components

**Interpreter** (`engine/interpreter.js`)
- Parses standard definitions
- Generates JavaScript/Python code
- Handles cross-standard dependencies

**Validator** (`engine/validator.js`)
- Checks compliance with standard schemas
- Validates state machines
- Ensures data model consistency

**Composer** (`engine/composer.js`)
- Orchestrates multiple standards
- Resolves conflicts (e.g., ISA-88 + PackML)
- Generates unified system

### Usage

```javascript
import { StandardsEngine } from '/standards/engine/interpreter.js';

// Load PackML standard
const packml = await StandardsEngine.load('/standards/packml/states.json');

// Generate state machine
const code = await StandardsEngine.interpret(packml);

// Execute
eval(code); // Or save to file
```

## Meta-Standard Framework

### Purpose
Define how to define standards (meta-framework).

### Schema (`meta-standard/standard-schema.json`)
```json
{
  "standard": {
    "name": "ExampleStandard",
    "version": "1.0",
    "domain": "medical",
    "components": [
      {
        "type": "state-machine",
        "states": [...],
        "transitions": [...]
      },
      {
        "type": "data-model",
        "entities": [...]
      }
    ]
  }
}
```

### Compliance Tests (`meta-standard/compliance-tests.js`)
- Automated validation of standard implementations
- Test coverage requirements
- Certification reporting

## Integration with CHAZON

### ISA-95 Levels in CHAZON
```
L4: /screens/Enterprise/*.html       (Business planning)
L3: /screens/Enterprise/L3/          (MES operations)
L2: /screens/Enterprise/L3/L2/       (SCADA, HMI)
L1: /screens/Enterprise/L3/L2/L1/    (PLC control)
L0: /screens/Enterprise/L3/L2/L1/L0/ (Physical devices)
```

### ISA-101 Theme in CHAZON
- Theme file: `/theme.yaml`
- Loader: `/scripts/theme-loader.js`
- Base CSS: `/os/medical/styles/isa101-theme.css`
- Colors: Cream & purple per ISA-101 guidelines

### PackML for Batch Processing
- Medical imaging batch workflows
- State tracking for multi-image processing
- Error handling and recovery

### MQTT for Real-time Updates
- Device status publishing
- AI result notifications
- Alarm broadcasting

## Development

### Adding New Standard

1. **Create directory** `/standards/new-standard/`

2. **Define components**
   ```bash
   touch /standards/new-standard/definition.json
   touch /standards/new-standard/implementation.js
   ```

3. **Add to meta-standard**
   Update `/standards/meta-standard/standard-schema.json`

4. **Create tests**
   ```bash
   touch /tests/test_new_standard.py
   ```

5. **Update documentation**
   Add to this `structure.md` file

### Testing Standards

```bash
# Unit tests
pytest tests/test_packml.py
pytest tests/test_isa88.py
pytest tests/test_isa95.py

# Compliance tests
python standards/meta-standard/compliance-tests.js

# Integration tests
pytest tests/test_standards_integration.py
```

## Compliance & Certification

### ISA Standards
- **ISA-88.01-1995:** Batch Control Part 1: Models and Terminology
- **ISA-95.00.01-2010:** Enterprise-Control System Integration
- **ISA-101.01-2015:** Human Machine Interfaces for Process Automation Systems

### OMAC PackML
- **PackML v4.0:** State machine specification
- **PackML Unit/Machine:** Implementation guide

### IEC Standards
- **IEC 62264:** Enterprise-control system integration (equivalent to ISA-95)
- **IEC 61512:** Batch control (equivalent to ISA-88)

## Future Enhancements

- **IEC 61131-3:** PLC programming languages (ST, LD, FBD, SFC, IL)
- **ISA-18.2:** Alarm management lifecycle
- **ISA-106:** Procedure automation
- **WECC:** Wide-area energy control standards
- **HL7 FHIR:** Healthcare interoperability (medical context)
- **DICOM DIMSE:** Medical imaging messaging

See root `/structure.md` for overall project integration.
See `/screens/structure.md` for ISA-95 screen hierarchy.
