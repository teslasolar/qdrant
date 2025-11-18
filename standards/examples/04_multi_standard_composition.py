#!/usr/bin/env python3
"""
Example 4: Multi-Standard Composition
Compose ISA-88 + PackML + MQTT + OPC-UA + ISA-101 for Complete System

This example shows the power of composing multiple standards:
1. ISA-88 equipment hierarchy for organization
2. PackML state machines for equipment control
3. MQTT/Sparkplug for IIoT communication
4. OPC-UA for interoperability
5. ISA-101 HMI for visualization

Result: Complete, standards-based medical imaging system
"""

import sys
from pathlib import Path
import json

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'engine'))

from standard_instantiation_engine import StandardInstantiationEngine


def main():
    print("=" * 80)
    print("Example 4: Complete Multi-Standard System Composition")
    print("Medical Imaging Facility - Standards-Based Architecture")
    print("=" * 80)

    # Initialize engine
    standards_root = Path(__file__).parent.parent
    engine = StandardInstantiationEngine(standards_root)

    # Define the complete system
    print("\n1. System Definition:")
    print("-" * 80)
    print("""
System: Medical Imaging Radiology Department
Location: Hospital Boston, Radiology Area

Equipment:
  - CT Scanner 1 (Primary)
  - CT Scanner 2 (Backup)
  - MRI Scanner 1
  - X-Ray Room 1
  - X-Ray Room 2

Standards Applied:
  1. ISA-88: Equipment hierarchy and procedural control
  2. PackML: State machine for each imaging device
  3. ISA-95: Functional architecture (Level 0-4)
  4. MQTT/Sparkplug: IIoT communication to cloud
  5. OPC-UA: Interoperability between systems
  6. ISA-101: High-performance HMI design
    """)

    # Compose the system
    print("\n2. Composing Standards...")
    print("-" * 80)

    composition = engine.compose_standards(
        composition_id='radiology_department_complete',
        standards=[
            # ISA-88 Equipment Hierarchy
            {
                'standardId': 'isa-88-equipment-v1.0',
                'instanceId': 'radiology_equipment',
                'parameters': {
                    'enterpriseName': 'MedTech_Healthcare',
                    'siteName': 'Hospital_Boston',
                    'includeMetrics': True,
                    'maxDepth': 7,
                    'tagSeparator': '/'
                }
            },
            # PackML for CT Scanner 1
            {
                'standardId': 'packml-v1.0',
                'instanceId': 'ct_scanner_1_packml',
                'parameters': {
                    'equipmentPath': 'MedTech_Healthcare/Hospital_Boston/Radiology/CT_Imaging/CT_Scanner_1',
                    'enableManualMode': True,
                    'autoComplete': True,
                    'safetyLevel': 'high'
                }
            },
            # PackML for CT Scanner 2
            {
                'standardId': 'packml-v1.0',
                'instanceId': 'ct_scanner_2_packml',
                'parameters': {
                    'equipmentPath': 'MedTech_Healthcare/Hospital_Boston/Radiology/CT_Imaging/CT_Scanner_2',
                    'enableManualMode': True,
                    'autoComplete': True,
                    'safetyLevel': 'high'
                }
            },
            # PackML for MRI Scanner
            {
                'standardId': 'packml-v1.0',
                'instanceId': 'mri_scanner_1_packml',
                'parameters': {
                    'equipmentPath': 'MedTech_Healthcare/Hospital_Boston/Radiology/MRI_Suite/MRI_Scanner_1',
                    'enableManualMode': True,
                    'autoComplete': True,
                    'safetyLevel': 'sil2'
                }
            },
            # ISA-95 Functional Hierarchy
            {
                'standardId': 'isa-95-functional-v1.0',
                'instanceId': 'hospital_isa95',
                'parameters': {
                    'enterpriseName': 'MedTech_Healthcare',
                    'includeSecurityZones': True,
                    'includeCommunicationPaths': True,
                    'levels': [0, 1, 2, 3, 4]
                }
            },
            # MQTT/Sparkplug for CT Scanner 1
            {
                'standardId': 'mqtt-sparkplug-v1.0',
                'instanceId': 'ct_scanner_1_mqtt',
                'parameters': {
                    'groupId': 'Hospital_Boston',
                    'edgeNodeId': 'Gateway_Radiology',
                    'deviceId': 'CT_Scanner_1',
                    'brokerUrl': 'mqtt://iot.medtech.com:8883',
                    'qos': 1,
                    'useTls': True
                }
            },
            # OPC-UA for CT Scanner 1
            {
                'standardId': 'opc-ua-v1.0',
                'instanceId': 'ct_scanner_1_opcua',
                'parameters': {
                    'serverUrl': 'opc.tcp://ct-scanner-1.local:4840',
                    'namespaceIndex': 2,
                    'securityMode': 'SignAndEncrypt',
                    'authenticationMode': 'Certificate',
                    'organizationByISA88': True
                }
            },
            # ISA-101 HMI Screen for Overview
            {
                'standardId': 'isa-101-hmi-v1.0',
                'instanceId': 'radiology_overview_screen',
                'parameters': {
                    'screenLevel': 'overview',
                    'scope': 'Radiology_Department',
                    'colorScheme': 'highPerformance',
                    'includeAlarms': True,
                    'includeTrends': False
                }
            },
            # ISA-101 HMI Screen for CT Scanner 1 Detail
            {
                'standardId': 'isa-101-hmi-v1.0',
                'instanceId': 'ct_scanner_1_detail_screen',
                'parameters': {
                    'screenLevel': 'detail',
                    'scope': 'CT_Scanner_1',
                    'colorScheme': 'highPerformance',
                    'includeAlarms': True,
                    'includeTrends': True
                }
            }
        ]
    )

    print(f"✓ Composition created: {composition['compositionId']}")
    print(f"  Standards instantiated: {len(composition['standards'])}")
    print(f"  Created: {composition['created']}")

    # Display composition structure
    print("\n3. Composition Structure:")
    print("-" * 80)

    for std in composition['standards']:
        instance = composition['instances'][std['instanceId']]
        print(f"\n{std['instanceId']}:")
        print(f"  Standard: {std['standardId']}")
        print(f"  Type: {instance['metadata'].get('standardType', 'N/A')}")
        print(f"  Parameters: {len(instance['parameters'])} configured")

    # Show how standards integrate
    print("\n4. Standard Integration Map:")
    print("-" * 80)
    print("""
┌─────────────────────────────────────────────────────────────────┐
│                     ISA-95 Functional Architecture              │
│  Defines: System layers, communication paths, security zones   │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──> Level 4: HIS/RIS (Hospital/Radiology Info System)
         │
         ├──> Level 3: PACS, Worklist Management, MES
         │
         ├──> Level 2: SCADA/HMI ◄──── ISA-101 HMI Design
         │                               │
         │                               ├─ Overview Screen
         │                               ├─ CT Scanner 1 Detail
         │                               └─ Alarm Management
         │
         ├──> Level 1: Device Controllers
         │
         └──> Level 0: Sensors/Actuators

┌─────────────────────────────────────────────────────────────────┐
│              ISA-88 Equipment & Procedural Model                │
│  Defines: Equipment organization, recipes, procedures           │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──> Enterprise: MedTech Healthcare
         │      └──> Site: Hospital Boston
         │            └──> Area: Radiology
         │                  ├──> Cell: CT Imaging
         │                  │     ├──> Unit: CT Scanner 1 ◄──┐
         │                  │     └──> Unit: CT Scanner 2    │
         │                  ├──> Cell: MRI Suite              │
         │                  │     └──> Unit: MRI Scanner 1    │
         │                  └──> Cell: X-Ray Rooms            │
         │                                                     │
         └─────────────────────────────────────────────────────┘
                                                               │
┌──────────────────────────────────────────────────────────────┴──┐
│                   PackML State Machines                          │
│  Defines: Equipment states, commands, transitions               │
└────────┬─────────────────────────────────────────────────────────┘
         │
         ├──> CT Scanner 1 PackML ◄──┐
         │    States: Stopped, Idle, Execute, Complete, etc.
         │    Commands: Start, Stop, Hold, Abort, etc.
         │                             │
         ├──> CT Scanner 2 PackML     │
         │                             │
         └──> MRI Scanner 1 PackML    │
                                       │
┌──────────────────────────────────────┴───────────────────────────┐
│               Communication Protocols                            │
│  Defines: How data flows between systems                        │
└────────┬─────────────────────────────────────────────────────────┘
         │
         ├──> MQTT/Sparkplug B ────> Cloud/IIoT Platform
         │    Topics: spBv1.0/Hospital_Boston/DDATA/Gateway/CT_1
         │    Metrics: PackML state, process values, alarms
         │    Birth/Death: Equipment online/offline notifications
         │
         └──> OPC-UA ────> SCADA, MES, Other Systems
              Address Space: Objects/Hospital/Radiology/CT_1
              Variables: PackML.State, Process.*, Commands.*
              Methods: Start(), Stop(), LoadProtocol()
    """)

    # Show data flow example
    print("\n5. Example Data Flow: Patient Scan Workflow:")
    print("-" * 80)
    print("""
1. Order Created (Level 4 - HIS):
   → RIS receives imaging order
   → Patient scheduled for CT scan

2. Worklist Updated (Level 3 - RIS/PACS):
   → Scan appears on modality worklist
   → Protocol selected (head, chest, etc.)

3. Technologist Prepares (Level 2 - HMI):
   → Opens ISA-101 Overview Screen
   → Sees CT Scanner 1 is "Idle" (PackML state)
   → Clicks to open Detail Screen
   → Selects patient from worklist
   → Loads protocol

4. Equipment Ready (Level 1 - Controller):
   → CT Scanner receives parameters
   → PackML transitions: Idle → Starting
   → Safety checks performed
   → Equipment initialized

5. Scan Execution (Level 0-1):
   → Operator sends Start command
   → PackML transitions: Starting → Execute
   → X-ray generator activates
   → Gantry rotates, table moves
   → Detector captures images
   → Real-time monitoring on HMI

6. State Published (Communication):
   → OPC-UA: CT Scanner State = "Execute"
   → MQTT: spBv1.0/.../DDATA/CT_1 with state metric
   → Cloud dashboard shows scanner in use
   → SCADA trend shows scanner runtime

7. Scan Complete (Level 1):
   → Scan completes successfully
   → PackML transitions: Execute → Completing → Complete
   → Images reconstructed
   → Data sent to PACS

8. Report Generated (Level 3):
   → Images available in PACS
   → Radiologist reviews
   → Report created
   → Results sent to HIS

9. Equipment Reset (Level 1-2):
   → Operator sends Reset command
   → PackML transitions: Complete → Resetting → Idle
   → Scanner ready for next patient
   → HMI shows "Available"

Throughout workflow:
  - All state changes logged by historian
  - Alarms managed per ISA-101 design
  - Metrics published via MQTT
  - OPC-UA provides interoperability
  - ISA-88 procedural model tracks recipe execution
    """)

    # Export complete composition
    print("\n6. Exporting Complete Composition...")
    print("-" * 80)

    output_path = Path(__file__).parent / 'instances' / 'radiology_department_complete.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(composition, f, indent=2)

    print(f"✓ Exported to: {output_path}")
    print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")

    # Summary
    print("\n7. Benefits of Standards-Based Approach:")
    print("-" * 80)
    print("""
✓ Interoperability:
  - OPC-UA enables vendor-independent communication
  - PackML provides standard equipment interface
  - Any PackML client can control any PackML server

✓ Consistency:
  - All equipment uses same state model
  - Standardized naming via ISA-88 hierarchy
  - Consistent HMI design via ISA-101

✓ Scalability:
  - Add new equipment by instantiating standards
  - Same patterns work for CT, MRI, X-Ray, etc.
  - Easy to expand to new sites

✓ Maintainability:
  - Clear architecture via ISA-95
  - Documented standards-based design
  - Easier training and troubleshooting

✓ Integration:
  - MQTT enables cloud connectivity
  - OPC-UA enables MES/ERP integration
  - Standards-based = easier vendor integration

✓ Future-Proof:
  - Based on international standards
  - Not locked to specific vendor
  - Easier to upgrade/replace components
    """)

    print("\n" + "=" * 80)
    print("Example Complete!")
    print("Generated complete standards-based medical imaging system")
    print("=" * 80)


if __name__ == '__main__':
    main()
