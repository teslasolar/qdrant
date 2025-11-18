#!/usr/bin/env python3
"""
Example 1: Instantiate PackML State Machine for CT Scanner

This example shows how to:
1. Load the PackML standard
2. Instantiate it for a CT Scanner
3. Generate tag structure
4. Export the instance
"""

import sys
from pathlib import Path

# Add engine to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'engine'))

from standard_instantiation_engine import StandardInstantiationEngine
import json


def main():
    print("=" * 80)
    print("Example 1: PackML State Machine for CT Scanner")
    print("=" * 80)

    # Initialize engine
    standards_root = Path(__file__).parent.parent
    engine = StandardInstantiationEngine(standards_root)

    # Instantiate PackML for CT Scanner
    print("\n1. Instantiating PackML for CT Scanner...")
    print("-" * 80)

    ct_scanner_packml = engine.instantiate(
        standard_id='packml-v1.0',
        instance_id='ct_scanner_1_packml',
        parameters={
            'equipmentPath': 'Medical/Radiology/CT_Scanner_1',
            'enableManualMode': True,
            'autoComplete': False,
            'safetyLevel': 'high'
        }
    )

    print(f"✓ Instance created: {ct_scanner_packml.instance_id}")
    print(f"  Standard: {ct_scanner_packml.standard_id}")
    print(f"  Created: {ct_scanner_packml.created_at}")

    # Display generated tags
    print("\n2. Generated Tag Structure:")
    print("-" * 80)

    tags = ct_scanner_packml.generated_content.get('tags', {})

    print("\nStatus Tags:")
    for tag_name, tag_path in tags.items():
        if tag_name in ['status', 'stateName', 'stateCategory']:
            print(f"  {tag_name:20s} -> {tag_path}")

    print("\nCommand Tags:")
    if 'commands' in tags and isinstance(tags['commands'], dict):
        for cmd_name, cmd_path in tags['commands'].items():
            print(f"  {cmd_name:20s} -> {cmd_path}")

    print("\nIndicator Tags:")
    if 'indicators' in tags and isinstance(tags['indicators'], dict):
        for ind_name, ind_path in tags['indicators'].items():
            print(f"  {ind_name:20s} -> {ind_path}")

    # Display state definitions
    print("\n3. State Machine States:")
    print("-" * 80)

    states = ct_scanner_packml.generated_content.get('states', {})
    print(f"\nTotal States: {len(states)}")

    # Show key states
    key_states = ['stopped', 'idle', 'execute', 'held', 'aborted']
    for state_name in key_states:
        if state_name in states:
            state = states[state_name]
            print(f"\n{state['name']} (ID: {state['id']})")
            print(f"  Description: {state['description']}")
            print(f"  Category: {state['category']}")
            print(f"  Color: {state['color']}")
            print(f"  Allowed Transitions: {', '.join(state['allowedTransitions'])}")

    # Display commands
    print("\n4. Available Commands:")
    print("-" * 80)

    commands = ct_scanner_packml.generated_content.get('commands', {})
    for cmd_name, cmd_def in commands.items():
        print(f"\n{cmd_name}:")
        print(f"  Description: {cmd_def['description']}")
        print(f"  Source States: {', '.join(cmd_def['sourceStates'])}")
        print(f"  Target State: {cmd_def['targetState']}")

    # Export instance
    print("\n5. Exporting Instance...")
    print("-" * 80)

    output_path = Path(__file__).parent / 'instances' / 'ct_scanner_1_packml.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    engine.export_instance('ct_scanner_1_packml', output_path)
    print(f"✓ Exported to: {output_path}")

    # Show how this integrates with controls
    print("\n6. Integration with Control System:")
    print("-" * 80)

    print("""
This PackML instance generates tags that can be used in:

1. PLC Programming:
   - Read PackML state to know equipment status
   - Write commands to control equipment
   - Use indicators for HMI binding

2. SCADA/HMI:
   - Bind status tags to status indicators
   - Bind command tags to operator buttons
   - Show state name and category on screens

3. MES Integration:
   - Report equipment state changes
   - Track uptime/downtime by state
   - Trigger MES actions on state transitions

4. OPC-UA Server:
   - Expose PackML object with standard interface
   - Enable interoperable equipment control
   - Support OPC UA for PackML companion spec

5. MQTT Publishing:
   - Publish state changes via Sparkplug B
   - Enable IIoT monitoring
   - Cloud connectivity

Example Tag Usage:
  - Read: Medical/Radiology/CT_Scanner_1.Status.CurrentState
  - Write: Medical/Radiology/CT_Scanner_1.Commands.Start
  - Monitor: Medical/Radiology/CT_Scanner_1.Status.IsExecuting
    """)

    # Show state transition example
    print("\n7. Example State Transition Sequence:")
    print("-" * 80)

    print("""
Typical CT Scanner Operation:

1. Power On -> Undefined
   - Equipment initializes

2. Clear/Reset -> Clearing -> Stopped
   - Clear any faults
   - Move to stopped state

3. Reset -> Resetting -> Idle
   - Reset to home position
   - Load default parameters
   - Ready for operation

4. Start -> Starting -> Execute
   - Perform safety checks
   - Enable systems
   - Begin scanning

5. During Scan -> Execute
   - Normal operation
   - Acquiring images
   - Monitoring patient

6. Pause (if needed) -> Holding -> Held
   - Pause scan temporarily
   - Maintain safe state
   - Can resume

7. Resume -> Unholding -> Execute
   - Resume scanning

8. Complete Scan -> Completing -> Complete
   - Finish current scan
   - Process final images
   - Prepare for next patient

9. Reset for Next -> Resetting -> Idle
   - Ready for next patient

Emergency Scenarios:
- Patient issue -> Abort -> Aborting -> Aborted
- Equipment fault -> Abort -> Aborting -> Aborted
- After abort -> Clear -> Clearing -> Stopped -> Reset -> Idle
    """)

    print("\n" + "=" * 80)
    print("Example Complete!")
    print("=" * 80)


if __name__ == '__main__':
    main()
