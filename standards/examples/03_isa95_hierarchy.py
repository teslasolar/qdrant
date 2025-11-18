#!/usr/bin/env python3
"""
Example 3: Generate ISA-95 Functional Hierarchy

This example shows how to:
1. Load the ISA-95 functional hierarchy standard
2. Instantiate it for a medical facility
3. Generate the 5-level Purdue model
4. Show communication paths between levels
"""

import sys
from pathlib import Path
import json

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'engine'))

from standard_instantiation_engine import StandardInstantiationEngine


def main():
    print("=" * 80)
    print("Example 3: ISA-95 Functional Hierarchy")
    print("=" * 80)

    # Initialize engine
    standards_root = Path(__file__).parent.parent
    engine = StandardInstantiationEngine(standards_root)

    # Instantiate ISA-95 hierarchy
    print("\n1. Instantiating ISA-95 Functional Hierarchy...")
    print("-" * 80)

    isa95_hierarchy = engine.instantiate(
        standard_id='isa-95-functional-v1.0',
        instance_id='hospital_isa95',
        parameters={
            'enterpriseName': 'MedTech_Healthcare',
            'includeSecurityZones': True,
            'includeCommunicationPaths': True,
            'levels': [0, 1, 2, 3, 4]
        }
    )

    print(f"✓ Instance created: {isa95_hierarchy.instance_id}")

    # Display the 5 levels
    print("\n2. ISA-95 / Purdue Model Levels:")
    print("-" * 80)

    levels = isa95_hierarchy.generated_content.get('levels', {})

    for level_key in ['level4', 'level3', 'level2', 'level1', 'level0']:
        if level_key in levels:
            level = levels[level_key]
            print(f"\nLevel {level['level']}: {level['name']}")
            print(f"  Purdue Name: {level['purdueName']}")
            print(f"  Timeframe: {level['timeframe']}")
            print(f"  Description: {level['description']}")
            print(f"  Systems: {', '.join(level['systems'][:3])}")

            if 'connectivity' in level:
                conn = level['connectivity']
                print(f"  Connects To: {', '.join(conn['connectsTo'])}")
                print(f"  Protocol: {conn['protocol']}")
                print(f"  Update Freq: {conn['updateFrequency']}")

    # Display communication flows
    print("\n3. Information Flows Between Levels:")
    print("-" * 80)

    integration = isa95_hierarchy.generated_content.get('integrationModel', {})
    if 'informationFlows' in integration:
        flows = integration['informationFlows']

        for flow_name, flow_info in flows.items():
            print(f"\n{flow_name}:")
            print(f"  Data: {', '.join(flow_info['data'][:3])}")
            print(f"  Frequency: {flow_info['frequency']}")
            print(f"  Protocol: {flow_info['protocol']}")

    # Display security zones
    print("\n4. Security Zones (Cybersecurity):")
    print("-" * 80)

    security_zones = isa95_hierarchy.generated_content.get('securityZones', {})

    for zone_key in ['zone4', 'zone3', 'zone2', 'zone1', 'zone0']:
        if zone_key in security_zones:
            zone = security_zones[zone_key]
            print(f"\nZone {zone['level']}: {zone['name']}")
            print(f"  Security: {zone['security']}")
            print(f"  Access: {zone['access']}")
            print(f"  Protocols: {zone['protocols']}")

    # Show mapping to ISA-88
    print("\n5. Mapping to ISA-88 Equipment Hierarchy:")
    print("-" * 80)

    mapping = isa95_hierarchy.generated_content.get('mappingToISA88', {})
    if 'mappings' in mapping:
        print("\nISA-95 Level -> ISA-88 Equipment Level:")
        for level, equipment in mapping['mappings'].items():
            print(f"  {level:4s} -> {equipment}")

    # Generate system architecture diagram (as text)
    print("\n6. System Architecture:")
    print("-" * 80)
    print("""
┌─────────────────────────────────────────────────────────────────┐
│ Level 4: Business Planning & Logistics (Enterprise Network)    │
│ Systems: ERP, SCM, PLM, Financial Systems                      │
│ Example: SAP, Oracle, Patient Management System                │
│ Security Zone: Enterprise DMZ                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTPS/REST, Database (Minutes-Hours)
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ Level 3: Manufacturing Operations (MES/Site Operations)        │
│ Systems: MES, LIMS, QMS, Production Tracking                   │
│ Example: Ignition MES, Lab System, Quality Management          │
│ Security Zone: Manufacturing DMZ                                │
└────────────────────┬────────────────────────────────────────────┘
                     │ OPC-UA, MQTT, Database (Seconds-Minutes)
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ Level 2: Supervisory Control (SCADA/HMI)                       │
│ Systems: SCADA, HMI, Historian, Alarm Management               │
│ Example: Ignition SCADA, Wonderware, Medical Device Monitors   │
│ Security Zone: Control System LAN                              │
└────────────────────┬────────────────────────────────────────────┘
                     │ OPC-UA, Modbus TCP, Ethernet/IP (100ms-Sec)
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ Level 1: Basic Control (PLC/DCS)                               │
│ Systems: PLCs, DCS, PACs, Controllers                          │
│ Example: Allen-Bradley PLC, Siemens S7, Medical Device PLCs    │
│ Security Zone: Control Network                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │ Ethernet/IP, Profinet, I/O (1ms-100ms)
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ Level 0: Physical Process (Field Devices)                      │
│ Systems: Sensors, Actuators, Instruments                       │
│ Example: Temperature sensors, Valves, Motors, Medical Sensors  │
│ Security Zone: Field Device Network                            │
└─────────────────────────────────────────────────────────────────┘
    """)

    # Show practical example for medical facility
    print("\n7. Example: Medical Imaging Facility Architecture:")
    print("-" * 80)
    print("""
Level 4 (ERP/HIS):
  - Hospital Information System (HIS)
  - Patient Scheduling
  - Billing & Insurance
  - Resource Planning

Level 3 (MES/RIS):
  - Radiology Information System (RIS)
  - PACS (Picture Archiving)
  - Worklist Management
  - Quality Metrics & Reporting
  - Equipment Utilization Tracking

Level 2 (SCADA/Monitoring):
  - Medical Device Monitoring Dashboard
  - CT Scanner HMI
  - MRI Scanner Interface
  - Equipment Status Displays
  - Alarm Management
  - Real-time Trending

Level 1 (Device Control):
  - CT Scanner Controller
  - MRI System Controller
  - X-Ray Generator Controller
  - Table/Gantry Motion Control
  - Radiation Dose Monitoring

Level 0 (Sensors/Actuators):
  - X-Ray Detectors
  - RF Coils (MRI)
  - Patient Position Sensors
  - Radiation Monitors
  - Temperature Sensors
  - Motion Encoders
    """)

    # Export the hierarchy
    print("\n8. Exporting ISA-95 Hierarchy...")
    print("-" * 80)

    output_path = Path(__file__).parent / 'instances' / 'hospital_isa95.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    engine.export_instance('hospital_isa95', output_path)
    print(f"✓ Exported to: {output_path}")

    print("\n" + "=" * 80)
    print("Example Complete!")
    print("=" * 80)


if __name__ == '__main__':
    main()
