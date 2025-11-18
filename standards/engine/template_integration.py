#!/usr/bin/env python3
"""
Template System Integration
Bridges Standards-as-Tags framework with existing HMI/SCADA template system
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from standard_instantiation_engine import StandardInstantiationEngine, StandardInstance


class TemplateIntegrationBridge:
    """
    Bridges standards instances to existing template system
    Converts standard instances to template-compatible formats
    """

    def __init__(self,
                 standards_engine: StandardInstantiationEngine,
                 templates_root: Path):
        """
        Initialize integration bridge

        Args:
            standards_engine: StandardInstantiationEngine instance
            templates_root: Path to existing /templates/ directory
        """
        self.engine = standards_engine
        self.templates_root = Path(templates_root)

    def standard_to_tag_template(self, instance_id: str) -> Dict[str, Any]:
        """
        Convert a standard instance to tag template format

        Args:
            instance_id: ID of standard instance

        Returns:
            Tag template in existing template format
        """
        instance = self.engine.get_instance(instance_id)
        if not instance:
            raise ValueError(f"Instance not found: {instance_id}")

        # Generate tag template based on standard type
        if 'packml' in instance.standard_id.lower():
            return self._packml_to_tag_template(instance)
        elif 'isa-88' in instance.standard_id.lower() and 'equipment' in instance.standard_id.lower():
            return self._isa88_equipment_to_tag_template(instance)
        elif 'isa-95' in instance.standard_id.lower():
            return self._isa95_to_tag_template(instance)
        else:
            return self._generic_to_tag_template(instance)

    def _packml_to_tag_template(self, instance: StandardInstance) -> Dict[str, Any]:
        """Convert PackML instance to tag template"""
        equipment_path = instance.parameters.get('equipmentPath', 'Equipment')

        tags = []

        # Status tags
        tags.append({
            "uuid": f"tag-{instance.instance_id}-state",
            "type": "tag",
            "category": "status",
            "metadata": {
                "name": f"{equipment_path} - State",
                "description": "PackML current state",
                "standard": "PackML ISA-TR88.00.02",
                "version": "1.0.0",
                "tags": ["packml", "state", "status"]
            },
            "config": {
                "dataType": "Integer",
                "accessMode": "Read",
                "scanRate": 500,
                "path": f"{equipment_path}/Status/CurrentState"
            }
        })

        tags.append({
            "uuid": f"tag-{instance.instance_id}-state-name",
            "type": "tag",
            "category": "status",
            "metadata": {
                "name": f"{equipment_path} - State Name",
                "description": "PackML current state name",
                "standard": "PackML ISA-TR88.00.02",
                "version": "1.0.0",
                "tags": ["packml", "state", "status"]
            },
            "config": {
                "dataType": "String",
                "accessMode": "Read",
                "scanRate": 500,
                "path": f"{equipment_path}/Status/StateName"
            }
        })

        # Command tags
        commands = instance.generated_content.get('commands', {})
        for cmd_name in commands.keys():
            tags.append({
                "uuid": f"tag-{instance.instance_id}-cmd-{cmd_name}",
                "type": "tag",
                "category": "command",
                "metadata": {
                    "name": f"{equipment_path} - {cmd_name.title()} Command",
                    "description": f"PackML {cmd_name} command",
                    "standard": "PackML ISA-TR88.00.02",
                    "version": "1.0.0",
                    "tags": ["packml", "command", cmd_name]
                },
                "config": {
                    "dataType": "Boolean",
                    "accessMode": "Write",
                    "scanRate": 100,
                    "path": f"{equipment_path}/Commands/{cmd_name.title()}"
                }
            })

        return {
            "templateType": "packml-tags",
            "instanceId": instance.instance_id,
            "equipmentPath": equipment_path,
            "tags": tags
        }

    def _isa88_equipment_to_tag_template(self, instance: StandardInstance) -> Dict[str, Any]:
        """Convert ISA-88 equipment hierarchy to tag template"""
        enterprise = instance.parameters.get('enterpriseName', 'Enterprise')

        # Generate hierarchical tag structure
        hierarchy_tags = []

        levels = instance.generated_content.get('levels', {})

        # Create tags for each level
        for level_key, level_def in levels.items():
            if 'tagStructure' in level_def:
                tag_structure = level_def['tagStructure']
                path = tag_structure.get('path', '')

                for tag_name, tag_path in tag_structure.get('tags', {}).items():
                    hierarchy_tags.append({
                        "uuid": f"tag-{instance.instance_id}-{level_key}-{tag_name}",
                        "type": "tag",
                        "category": "hierarchy",
                        "metadata": {
                            "name": f"{level_def['name']} - {tag_name}",
                            "description": f"ISA-88 {level_def['name']} level tag",
                            "standard": "ISA-88 ANSI/ISA-88.01",
                            "level": level_def['level'],
                            "tags": ["isa-88", "hierarchy", level_key]
                        },
                        "config": {
                            "dataType": "String",
                            "accessMode": "Read",
                            "scanRate": 1000,
                            "path": f"{path}/{tag_path}"
                        }
                    })

        return {
            "templateType": "isa88-hierarchy-tags",
            "instanceId": instance.instance_id,
            "enterpriseName": enterprise,
            "tags": hierarchy_tags
        }

    def _isa95_to_tag_template(self, instance: StandardInstance) -> Dict[str, Any]:
        """Convert ISA-95 functional hierarchy to tag template"""
        # Similar pattern to ISA-88 but for functional levels
        return {
            "templateType": "isa95-functional-tags",
            "instanceId": instance.instance_id,
            "tags": []  # Would generate L0-L4 functional tags
        }

    def _generic_to_tag_template(self, instance: StandardInstance) -> Dict[str, Any]:
        """Generic conversion for other standard types"""
        return {
            "templateType": "generic-standard-tags",
            "instanceId": instance.instance_id,
            "standardId": instance.standard_id,
            "tags": []
        }

    def standard_to_hmi_component(self, instance_id: str) -> Dict[str, Any]:
        """
        Convert a standard instance to HMI component template

        Args:
            instance_id: ID of standard instance

        Returns:
            HMI component template
        """
        instance = self.engine.get_instance(instance_id)
        if not instance:
            raise ValueError(f"Instance not found: {instance_id}")

        # Generate HMI component based on standard type
        if 'packml' in instance.standard_id.lower():
            return self._packml_to_hmi_component(instance)
        elif 'isa-101' in instance.standard_id.lower():
            return self._isa101_to_hmi_screen(instance)
        else:
            return self._generic_to_hmi_component(instance)

    def _packml_to_hmi_component(self, instance: StandardInstance) -> Dict[str, Any]:
        """Convert PackML instance to HMI component"""
        equipment_path = instance.parameters.get('equipmentPath', 'Equipment')

        return {
            "uuid": f"component-{instance.instance_id}",
            "type": "component",
            "category": "status-panel",
            "metadata": {
                "name": "PackML Status Panel",
                "description": "Standard PackML equipment status display",
                "version": "1.0.0",
                "standard": "PackML ISA-TR88.00.02",
                "tags": ["packml", "status", "hmi"]
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
                    "binding": f"{equipment_path}/Status/StateName",
                    "colorMapping": {
                        "Stopped": "#E53E3E",
                        "Idle": "#48BB78",
                        "Execute": "#38B2AC",
                        "Complete": "#805AD5",
                        "Aborted": "#C53030"
                    }
                },
                {
                    "type": "ButtonPanel",
                    "buttons": [
                        {"label": "Start", "command": f"{equipment_path}/Commands/Start"},
                        {"label": "Stop", "command": f"{equipment_path}/Commands/Stop"},
                        {"label": "Reset", "command": f"{equipment_path}/Commands/Reset"},
                        {"label": "Abort", "command": f"{equipment_path}/Commands/Abort"}
                    ]
                }
            ]
        }

    def _isa101_to_hmi_screen(self, instance: StandardInstance) -> Dict[str, Any]:
        """Convert ISA-101 instance to HMI screen"""
        screen_level = instance.parameters.get('screenLevel', 'detail')
        scope = instance.parameters.get('scope', 'Equipment')

        screen_def = instance.generated_content.get('screenHierarchy', {}).get(f"level1_{screen_level}", {})

        return {
            "uuid": f"screen-{instance.instance_id}",
            "type": "screen",
            "category": screen_level,
            "metadata": {
                "name": f"{scope} - {screen_level.title()} View",
                "description": f"ISA-101 {screen_level} level screen",
                "version": "1.0.0",
                "standard": "ISA-101 ANSI/ISA-101.01-2015",
                "tags": ["isa-101", "hmi", screen_level]
            },
            "layout": screen_def.get('layout', {}),
            "components": screen_def.get('components', []),
            "colorScheme": instance.parameters.get('colorScheme', 'highPerformance')
        }

    def _generic_to_hmi_component(self, instance: StandardInstance) -> Dict[str, Any]:
        """Generic conversion for other standard types"""
        return {
            "uuid": f"component-{instance.instance_id}",
            "type": "component",
            "standardId": instance.standard_id
        }

    def export_to_template_system(self,
                                  instance_id: str,
                                  template_type: str = 'tag') -> Path:
        """
        Export standard instance to existing template system

        Args:
            instance_id: ID of standard instance
            template_type: Type of template ('tag' or 'component')

        Returns:
            Path to exported template file
        """
        if template_type == 'tag':
            template = self.standard_to_tag_template(instance_id)
            output_dir = self.templates_root / 'tags' / 'standards'
            filename = f"{instance_id}.json"
        elif template_type == 'component':
            template = self.standard_to_hmi_component(instance_id)
            output_dir = self.templates_root / 'components' / 'standards'
            filename = f"{instance_id}.json"
        else:
            raise ValueError(f"Unknown template type: {template_type}")

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename

        with open(output_path, 'w') as f:
            json.dump(template, f, indent=2)

        return output_path

    def import_from_template_system(self,
                                    template_path: Path) -> Optional[str]:
        """
        Import existing template and convert to standard instance

        Args:
            template_path: Path to existing template

        Returns:
            Instance ID if successfully converted
        """
        with open(template_path, 'r') as f:
            template = json.load(f)

        # Detect template type and convert
        # This is a placeholder - would need specific conversion logic
        return None


def main():
    """Example usage of template integration"""
    print("=" * 80)
    print("Template System Integration Example")
    print("=" * 80)

    # Initialize engines
    standards_root = Path('/home/user/qdrant/standards')
    templates_root = Path('/home/user/qdrant/templates')

    standards_engine = StandardInstantiationEngine(standards_root)
    bridge = TemplateIntegrationBridge(standards_engine, templates_root)

    # Create a PackML instance
    print("\n1. Creating PackML instance...")
    instance = standards_engine.instantiate(
        standard_id='packml-v1.0',
        instance_id='demo_packml',
        parameters={
            'equipmentPath': 'Demo/Equipment/Unit1',
            'enableManualMode': True,
            'safetyLevel': 'standard'
        }
    )

    print(f"✓ Created instance: {instance.instance_id}")

    # Convert to tag template
    print("\n2. Converting to tag template format...")
    tag_template = bridge.standard_to_tag_template('demo_packml')
    print(f"✓ Generated {len(tag_template['tags'])} tags")

    # Convert to HMI component
    print("\n3. Converting to HMI component...")
    hmi_component = bridge.standard_to_hmi_component('demo_packml')
    print(f"✓ Generated HMI component: {hmi_component['type']}")

    # Export to template system
    print("\n4. Exporting to template system...")
    tag_path = bridge.export_to_template_system('demo_packml', 'tag')
    component_path = bridge.export_to_template_system('demo_packml', 'component')

    print(f"✓ Tag template: {tag_path}")
    print(f"✓ Component template: {component_path}")

    print("\n" + "=" * 80)
    print("Integration Complete!")
    print("=" * 80)


if __name__ == '__main__':
    main()
