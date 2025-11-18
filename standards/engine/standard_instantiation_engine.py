#!/usr/bin/env python3
"""
Standard Instantiation Engine
Loads and instantiates industrial standards as executable templates
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import copy


@dataclass
class StandardDefinition:
    """Loaded standard definition"""
    standard_id: str
    type: str
    metadata: Dict[str, Any]
    specification: Dict[str, Any]
    content: Dict[str, Any]
    parameters: List[Dict[str, Any]]
    validation: Dict[str, Any]
    instantiation: Dict[str, Any]
    source_path: Path

    @classmethod
    def from_file(cls, file_path: Path) -> 'StandardDefinition':
        """Load standard definition from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)

        return cls(
            standard_id=data['standardId'],
            type=data['type'],
            metadata=data['metadata'],
            specification=data['specification'],
            content={k: v for k, v in data.items()
                    if k not in ['standardId', 'type', 'metadata', 'specification',
                                'parameters', 'validation', 'instantiation']},
            parameters=data.get('parameters', []),
            validation=data.get('validation', {}),
            instantiation=data.get('instantiation', {}),
            source_path=file_path
        )


@dataclass
class StandardInstance:
    """Instantiated standard with bound parameters"""
    standard_id: str
    instance_id: str
    parameters: Dict[str, Any]
    generated_content: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert instance to dictionary"""
        return {
            'standardId': self.standard_id,
            'instanceId': self.instance_id,
            'parameters': self.parameters,
            'generatedContent': self.generated_content,
            'createdAt': self.created_at,
            'metadata': self.metadata
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert instance to JSON string"""
        return json.dumps(self.to_dict(), indent=indent)


class ParameterValidator:
    """Validates parameters against standard definition"""

    @staticmethod
    def validate(parameters: Dict[str, Any],
                 param_definitions: List[Dict[str, Any]]) -> tuple[bool, List[str]]:
        """
        Validate parameters against definitions
        Returns: (is_valid, errors)
        """
        errors = []

        # Check required parameters
        required_params = {p['name'] for p in param_definitions if p.get('required', False)}
        provided_params = set(parameters.keys())
        missing = required_params - provided_params

        if missing:
            errors.append(f"Missing required parameters: {', '.join(missing)}")

        # Validate each provided parameter
        param_map = {p['name']: p for p in param_definitions}

        for name, value in parameters.items():
            if name not in param_map:
                errors.append(f"Unknown parameter: {name}")
                continue

            param_def = param_map[name]

            # Type validation
            expected_type = param_def.get('type')
            if expected_type:
                if not ParameterValidator._check_type(value, expected_type):
                    errors.append(f"Parameter '{name}' has wrong type. "
                                f"Expected {expected_type}, got {type(value).__name__}")

            # Enum validation
            if 'enum' in param_def:
                if value not in param_def['enum']:
                    errors.append(f"Parameter '{name}' must be one of {param_def['enum']}")

            # Range validation for numbers
            if expected_type in ['integer', 'number']:
                if 'min' in param_def and value < param_def['min']:
                    errors.append(f"Parameter '{name}' must be >= {param_def['min']}")
                if 'max' in param_def and value > param_def['max']:
                    errors.append(f"Parameter '{name}' must be <= {param_def['max']}")

        return len(errors) == 0, errors

    @staticmethod
    def _check_type(value: Any, expected_type: str) -> bool:
        """Check if value matches expected type"""
        type_map = {
            'string': str,
            'integer': int,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict
        }

        expected_python_type = type_map.get(expected_type)
        if expected_python_type is None:
            return True  # Unknown type, skip validation

        return isinstance(value, expected_python_type)


class TemplateEngine:
    """Simple template engine for parameter substitution"""

    @staticmethod
    def substitute(template: Any, parameters: Dict[str, Any]) -> Any:
        """
        Recursively substitute {{parameter}} placeholders with values
        """
        if isinstance(template, str):
            # Replace {{param}} with value
            def replacer(match):
                param_name = match.group(1)
                value = parameters.get(param_name, match.group(0))
                return str(value)

            return re.sub(r'\{\{(\w+)\}\}', replacer, template)

        elif isinstance(template, dict):
            return {k: TemplateEngine.substitute(v, parameters)
                   for k, v in template.items()}

        elif isinstance(template, list):
            return [TemplateEngine.substitute(item, parameters)
                   for item in template]

        else:
            return template


class StandardInstantiationEngine:
    """Main engine for loading and instantiating standards"""

    def __init__(self, standards_root: Path):
        """
        Initialize engine with root directory of standards

        Args:
            standards_root: Path to /standards/ directory
        """
        self.standards_root = Path(standards_root)
        self.loaded_standards: Dict[str, StandardDefinition] = {}
        self.instances: Dict[str, StandardInstance] = {}

    def load_standard(self, standard_path: str) -> StandardDefinition:
        """
        Load a standard definition from file

        Args:
            standard_path: Relative path to standard JSON (e.g., 'packml/packml-state-machine.json')

        Returns:
            Loaded StandardDefinition
        """
        full_path = self.standards_root / standard_path

        if not full_path.exists():
            raise FileNotFoundError(f"Standard not found: {full_path}")

        standard = StandardDefinition.from_file(full_path)
        self.loaded_standards[standard.standard_id] = standard

        return standard

    def list_available_standards(self) -> List[Dict[str, str]]:
        """
        List all available standards in the standards directory

        Returns:
            List of standard metadata
        """
        standards = []

        for json_file in self.standards_root.rglob('*.json'):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                if 'standardId' in data and 'metadata' in data:
                    standards.append({
                        'standardId': data['standardId'],
                        'name': data['metadata'].get('name', ''),
                        'type': data.get('type', ''),
                        'description': data['metadata'].get('description', ''),
                        'path': str(json_file.relative_to(self.standards_root))
                    })
            except (json.JSONDecodeError, KeyError):
                continue

        return standards

    def instantiate(self,
                   standard_id: str,
                   instance_id: str,
                   parameters: Dict[str, Any],
                   validate: bool = True) -> StandardInstance:
        """
        Instantiate a standard with parameters

        Args:
            standard_id: ID of standard to instantiate
            instance_id: Unique ID for this instance
            parameters: Parameter values
            validate: Whether to validate parameters

        Returns:
            StandardInstance with generated content
        """
        # Load standard if not already loaded
        if standard_id not in self.loaded_standards:
            # Try to find and load it
            standards = self.list_available_standards()
            matching = [s for s in standards if s['standardId'] == standard_id]

            if not matching:
                raise ValueError(f"Standard not found: {standard_id}")

            self.load_standard(matching[0]['path'])

        standard = self.loaded_standards[standard_id]

        # Validate parameters
        if validate:
            is_valid, errors = ParameterValidator.validate(parameters, standard.parameters)
            if not is_valid:
                raise ValueError(f"Parameter validation failed:\n" + "\n".join(errors))

        # Add defaults for missing optional parameters
        full_parameters = self._apply_defaults(parameters, standard.parameters)

        # Create instance
        instance = StandardInstance(
            standard_id=standard_id,
            instance_id=instance_id,
            parameters=full_parameters,
            metadata={
                'standardType': standard.type,
                'standardName': standard.metadata['name'],
                'standardVersion': standard.metadata['version']
            }
        )

        # Generate content by substituting parameters
        instance.generated_content = TemplateEngine.substitute(
            copy.deepcopy(standard.content),
            full_parameters
        )

        # Store instance
        self.instances[instance_id] = instance

        return instance

    def _apply_defaults(self,
                       parameters: Dict[str, Any],
                       param_definitions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply default values for missing optional parameters"""
        result = parameters.copy()

        for param_def in param_definitions:
            name = param_def['name']
            if name not in result and 'default' in param_def:
                result[name] = param_def['default']

        return result

    def compose_standards(self,
                         composition_id: str,
                         standards: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compose multiple standards together

        Args:
            composition_id: ID for the composition
            standards: List of {standardId, instanceId, parameters} dicts

        Returns:
            Composed result with all instances
        """
        composition = {
            'compositionId': composition_id,
            'created': datetime.utcnow().isoformat(),
            'standards': [],
            'instances': {}
        }

        for std_config in standards:
            instance = self.instantiate(
                standard_id=std_config['standardId'],
                instance_id=std_config['instanceId'],
                parameters=std_config['parameters']
            )

            composition['standards'].append({
                'standardId': std_config['standardId'],
                'instanceId': std_config['instanceId']
            })

            composition['instances'][std_config['instanceId']] = instance.to_dict()

        return composition

    def export_instance(self, instance_id: str, output_path: Path) -> None:
        """Export an instance to JSON file"""
        if instance_id not in self.instances:
            raise ValueError(f"Instance not found: {instance_id}")

        instance = self.instances[instance_id]

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(instance.to_json())

    def get_instance(self, instance_id: str) -> Optional[StandardInstance]:
        """Get an instance by ID"""
        return self.instances.get(instance_id)

    def list_instances(self) -> List[str]:
        """List all instance IDs"""
        return list(self.instances.keys())


def main():
    """Example usage"""
    # Initialize engine
    engine = StandardInstantiationEngine('/home/user/qdrant/standards')

    # List available standards
    print("Available Standards:")
    print("=" * 80)
    for std in engine.list_available_standards():
        print(f"  {std['standardId']}")
        print(f"    Name: {std['name']}")
        print(f"    Type: {std['type']}")
        print(f"    Path: {std['path']}")
        print()

    # Example: Instantiate PackML for CT Scanner
    print("\nInstantiating PackML for CT Scanner...")
    print("=" * 80)

    packml_instance = engine.instantiate(
        standard_id='packml-v1.0',
        instance_id='ct-scanner-1-packml',
        parameters={
            'equipmentPath': 'Medical/Radiology/CT_Scanner_1',
            'enableManualMode': True,
            'autoComplete': False,
            'safetyLevel': 'high'
        }
    )

    print(f"Instance created: {packml_instance.instance_id}")
    print(f"Generated tags:")
    for tag_type, tag_path in packml_instance.generated_content.get('tags', {}).items():
        if isinstance(tag_path, str):
            print(f"  {tag_type}: {tag_path}")

    # Export instance
    export_path = Path('/home/user/qdrant/standards/examples/instances/ct-scanner-1-packml.json')
    engine.export_instance('ct-scanner-1-packml', export_path)
    print(f"\nExported to: {export_path}")


if __name__ == '__main__':
    main()
