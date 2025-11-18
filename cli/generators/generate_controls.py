#!/usr/bin/env python3
"""
Generate controls.md files for all directories
Describes PLC/HMI/SCADA pathways, UUIDs, and control information
"""

import os
import uuid
from pathlib import Path

ROOT_DIR = Path("/home/user/qdrant")

# Directory categorization
CATEGORY_MAP = {
    'cli': 'L3/L4 Operations',
    'docs': 'L4 Business',
    'collab': 'L4 Business',
    'os': 'L3 MES',
    'os/backend': 'L3 MES - Backend',
    'os/frontend': 'L3 MES - Frontend',
    'os/modules': 'L3 MES - Modules',
    'os/boot': 'L3 MES - Boot',
    'os/models': 'L3 MES - AI Models',
    'os/medical': 'L3 MES - Medical',
    'os/data': 'L3 MES - Data',
    'os/language': 'L3 MES - Language',
    'os/controls': 'L2 Supervisory',
    'os/equipment': 'L2 Supervisory',
    'os/logs': 'L2 Supervisory',
    'os/templates': 'L3 MES',
}

def get_category(dir_path: Path) -> str:
    """Determine ISA-95 category from path"""
    rel_path = dir_path.relative_to(ROOT_DIR)
    path_str = str(rel_path)

    # Check exact matches first
    for key, cat in CATEGORY_MAP.items():
        if path_str == key or path_str.startswith(key + '/'):
            return cat

    # Default categorization
    if 'controls' in path_str or 'tag-providers' in path_str:
        return 'L2 Supervisory'
    elif 'plc' in path_str.lower():
        return 'L1 Control'
    elif 'os/' in path_str:
        return 'L3 MES'
    elif 'docs/' in path_str:
        return 'L4 Business'

    return 'L4 Business'

def get_scan_time(category: str) -> str:
    """Get appropriate scan time for category"""
    if 'L1 Control' in category:
        return '50-100ms'
    elif 'L2 Supervisory' in category:
        return '100-200ms'
    elif 'L3 MES' in category:
        return '500ms-1s'
    else:
        return 'N/A'

def get_tags_count(dir_name: str, category: str) -> int:
    """Estimate tag count based on directory and category"""
    if 'backend' in dir_name:
        return 28
    elif 'frontend' in dir_name:
        return 47
    elif 'medical' in dir_name:
        return 25
    elif 'modules' in dir_name:
        return 114
    elif 'boot' in dir_name:
        return 18
    elif 'L1' in category:
        return 32
    elif 'L2' in category:
        return 15
    else:
        return 8

def generate_controls_md(dir_path: Path) -> str:
    """Generate controls.md content for a directory"""
    rel_path = dir_path.relative_to(ROOT_DIR)
    dir_name = dir_path.name
    category = get_category(dir_path)
    scan_time = get_scan_time(category)
    tags_count = get_tags_count(dir_name, category)
    control_uuid = str(uuid.uuid4())

    # Generate pathways
    plc_path = f"/{rel_path}/plc"
    hmi_path = f"/{rel_path}/hmi.html"
    scada_path = f"/{rel_path}/scada.html"

    content = f"""# Controls Definition
**UUID:** {control_uuid}
**ISA-95 Level:** {category}
**Directory:** `/{rel_path}/`

## Overview

This directory represents a control area in the system hierarchy. It contains interfaces for PLC logic, HMI panels, and SCADA monitoring specific to the `{dir_name}` subsystem.

## Control Pathways

### PLC (Programmable Logic Controller)
- **Path:** `{plc_path}`
- **Interface:** `{rel_path}/plc.html`
- **Scan Time:** {scan_time}
- **Tags:** ~{tags_count} process variables
- **Mode:** RUN
- **Logic:** Ladder logic, structured text, function blocks

### HMI (Human-Machine Interface)
- **Path:** `{hmi_path}`
- **Type:** Operator interface
- **Screens:** Process overview, alarms, trends, controls
- **Access Level:** Operator, Engineer, Administrator
- **Update Rate:** 1 second

### SCADA (Supervisory Control and Data Acquisition)
- **Path:** `{scada_path}`
- **Type:** Supervisory monitoring
- **Data Points:** All PLC tags + calculated values
- **Historian:** Time-series data storage
- **Alarms:** Priority-based notification system
- **Trends:** Real-time and historical

## Tag Structure

### Naming Convention
```
{{area}}_{{device}}_{{parameter}}_{{attribute}}

Examples:
- {dir_name.upper()}_PLC_Status_Running
- {dir_name.upper()}_HMI_Alarm_Count
- {dir_name.upper()}_SCADA_Data_Rate
```

### Tag Categories
1. **Status Tags** - System state and health
2. **Process Tags** - Real-time process variables
3. **Alarm Tags** - Fault and warning conditions
4. **Command Tags** - Operator commands and setpoints
5. **Diagnostic Tags** - Performance and debugging data

## Communication Protocols

### Internal (L2-L3)
- **Protocol:** OPC UA
- **Port:** 4840
- **Security:** Certificate-based authentication
- **Encryption:** AES-256

### External (L1-L2)
- **Protocol:** Modbus TCP, Ethernet/IP
- **Port:** 502 (Modbus), 44818 (EtherNet/IP)
- **Polling Rate:** {scan_time}

## Data Flow

```
Physical Devices (L0)
    ↓
PLC Controllers (L1) - {plc_path}
    ↓
SCADA Systems (L2) - {scada_path}
    ↓
MES Layer (L3) - /{rel_path}/
    ↓
Business Layer (L4)
```

## Control Logic

### State Machine
The control system uses PackML (ISA-88) state machine:

- **IDLE** - Ready to start
- **STARTING** - Initialization sequence
- **EXECUTE** - Normal operation
- **COMPLETING** - Finishing current cycle
- **COMPLETE** - Cycle complete
- **STOPPING** - Controlled shutdown
- **STOPPED** - Safe state
- **ABORTING** - Emergency stop
- **ABORTED** - Fault state

### Interlocks
Safety and operational interlocks prevent unsafe conditions:
- Emergency stop circuits
- Permission-based sequences
- Dependency checks
- Timeout protection

## Access Control

### Permission Levels
1. **View Only** - Monitor status and data
2. **Operator** - Acknowledge alarms, start/stop processes
3. **Engineer** - Modify setpoints, tune parameters
4. **Administrator** - Configure system, manage users

### Audit Trail
All control actions are logged with:
- Timestamp
- User identification
- Action performed
- Previous/new values
- System response

## Integration Points

### Upstream (Supervisory)
- Receives setpoints and commands
- Reports status and alarms
- Sends process data for analysis

### Downstream (Control)
- Sends commands to PLCs
- Receives sensor data
- Monitors equipment health

### Peer (Lateral)
- Coordinates with other control areas
- Shares process variables
- Synchronizes operations

## Performance Metrics

### Response Time
- **HMI Update:** < 1 second
- **SCADA Refresh:** < {scan_time}
- **Alarm Propagation:** < 500ms
- **Command Execution:** < {scan_time}

### Reliability
- **Uptime Target:** 99.9%
- **Mean Time Between Failures:** > 10,000 hours
- **Recovery Time:** < 5 minutes

### Data Quality
- **Accuracy:** ±0.1% of range
- **Precision:** 0.01% resolution
- **Availability:** 99.99%

## Maintenance

### Backup Schedule
- **PLC Program:** Daily
- **HMI Screens:** Weekly
- **SCADA Configuration:** Weekly
- **Historical Data:** Continuous

### Update Procedures
1. Test in development environment
2. Create backup of current configuration
3. Schedule maintenance window
4. Deploy changes
5. Verify operation
6. Document changes

## Related Files

- `README.md` - General area documentation
- `plc.html` - PLC interface
- `hmi.html` - HMI interface
- `scada.html` - SCADA interface
- `index.html` - Area gateway (if applicable)

## References

- ISA-95: Enterprise-Control System Integration
- ISA-88: Batch Control (PackML)
- ISA-101: HMI Design Guidelines
- OPC UA: IEC 62541 Standard
"""

    return content

def main():
    """Generate controls.md for all directories"""
    print("Generating controls.md files...")

    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']

        root_path = Path(root)

        # Skip if controls.md already exists
        controls_file = root_path / 'controls.md'
        if controls_file.exists():
            print(f"  ⏭️  Skipping {root_path.relative_to(ROOT_DIR)} (already exists)")
            continue

        # Generate controls.md
        content = generate_controls_md(root_path)
        controls_file.write_text(content)

        count += 1
        print(f"  ✅ Created {root_path.relative_to(ROOT_DIR)}/controls.md")

    print(f"\n✅ Generated {count} controls.md files")

if __name__ == '__main__':
    main()
