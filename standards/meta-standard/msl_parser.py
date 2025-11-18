#!/usr/bin/env python3
"""
Meta-Standard Language (MSL) Parser
DSL for composing and programming with industrial standards
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class MSLToken:
    """Token in MSL"""
    type: str
    value: str
    line: int
    column: int


@dataclass
class MSLNode:
    """AST Node for MSL"""
    type: str
    value: Any
    children: List['MSLNode'] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.metadata is None:
            self.metadata = {}


class MSLLexer:
    """Lexical analyzer for MSL"""

    TOKEN_PATTERNS = [
        ('COMMENT', r'#.*'),
        ('IMPORT', r'\bimport\b'),
        ('INSTANTIATE', r'\binstantiate\b'),
        ('COMPOSE', r'\bcompose\b'),
        ('BIND', r'\bbind\b'),
        ('EXTEND', r'\bextend\b'),
        ('WITH', r'\bwith\b'),
        ('AS', r'\bas\b'),
        ('FROM', r'\bfrom\b'),
        ('TO', r'\bto\b'),
        ('MAP', r'\bmap\b'),
        ('VALIDATE', r'\bvalidate\b'),
        ('GENERATE', r'\bgenerate\b'),
        ('ARROW', r'->'),
        ('COLON', r':'),
        ('SEMICOLON', r';'),
        ('COMMA', r','),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        ('STRING', r'"[^"]*"'),
        ('NUMBER', r'\d+\.?\d*'),
        ('BOOLEAN', r'\b(true|false)\b'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_.-]*'),
        ('NEWLINE', r'\n'),
        ('WHITESPACE', r'[ \t]+'),
    ]

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[MSLToken] = []
        self.line = 1
        self.column = 1

    def tokenize(self) -> List[MSLToken]:
        """Tokenize source code"""
        pos = 0

        while pos < len(self.source):
            match_found = False

            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source, pos)

                if match:
                    value = match.group(0)

                    # Skip whitespace and comments
                    if token_type not in ['WHITESPACE', 'COMMENT']:
                        if token_type != 'NEWLINE':  # Keep newlines for statement separation
                            token = MSLToken(
                                type=token_type,
                                value=value,
                                line=self.line,
                                column=self.column
                            )
                            self.tokens.append(token)

                    # Update position
                    pos = match.end()
                    if token_type == 'NEWLINE':
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += len(value)

                    match_found = True
                    break

            if not match_found:
                raise SyntaxError(f"Unexpected character '{self.source[pos]}' "
                                f"at line {self.line}, column {self.column}")

        return self.tokens


class MSLParser:
    """Parser for MSL"""

    def __init__(self, tokens: List[MSLToken]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None

    def parse(self) -> MSLNode:
        """Parse tokens into AST"""
        root = MSLNode(type='Program', value=None)

        while self.current_token:
            if self.current_token.type == 'NEWLINE':
                self.advance()
                continue

            stmt = self.parse_statement()
            if stmt:
                root.children.append(stmt)

        return root

    def parse_statement(self) -> Optional[MSLNode]:
        """Parse a single statement"""
        if not self.current_token:
            return None

        token_type = self.current_token.type

        if token_type == 'IMPORT':
            return self.parse_import()
        elif token_type == 'INSTANTIATE':
            return self.parse_instantiate()
        elif token_type == 'COMPOSE':
            return self.parse_compose()
        elif token_type == 'BIND':
            return self.parse_bind()
        elif token_type == 'EXTEND':
            return self.parse_extend()
        elif token_type == 'MAP':
            return self.parse_map()
        elif token_type == 'VALIDATE':
            return self.parse_validate()
        elif token_type == 'GENERATE':
            return self.parse_generate()
        else:
            raise SyntaxError(f"Unexpected token: {token_type} at line {self.current_token.line}")

    def parse_import(self) -> MSLNode:
        """Parse import statement: import standard from "path" """
        node = MSLNode(type='Import', value=None)
        self.expect('IMPORT')

        standard_id = self.expect('IDENTIFIER').value
        self.expect('FROM')
        path = self.expect('STRING').value.strip('"')

        node.metadata = {
            'standardId': standard_id,
            'path': path
        }

        self.skip_newlines()
        return node

    def parse_instantiate(self) -> MSLNode:
        """Parse instantiate: instantiate standard_id as instance_id with { params } """
        node = MSLNode(type='Instantiate', value=None)
        self.expect('INSTANTIATE')

        standard_id = self.expect('IDENTIFIER').value
        self.expect('AS')
        instance_id = self.expect('IDENTIFIER').value
        self.expect('WITH')

        parameters = self.parse_object()

        node.metadata = {
            'standardId': standard_id,
            'instanceId': instance_id,
            'parameters': parameters
        }

        self.skip_newlines()
        return node

    def parse_compose(self) -> MSLNode:
        """Parse compose: compose composition_id { instantiate statements } """
        node = MSLNode(type='Compose', value=None)
        self.expect('COMPOSE')

        composition_id = self.expect('IDENTIFIER').value
        self.expect('LBRACE')
        self.skip_newlines()

        instances = []
        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.type == 'NEWLINE':
                self.advance()
                continue

            if self.current_token.type == 'INSTANTIATE':
                instances.append(self.parse_instantiate())
            else:
                break

        self.expect('RBRACE')

        node.metadata = {
            'compositionId': composition_id,
            'instances': instances
        }

        self.skip_newlines()
        return node

    def parse_bind(self) -> MSLNode:
        """Parse bind: bind instance1.output to instance2.input """
        node = MSLNode(type='Bind', value=None)
        self.expect('BIND')

        source = self.parse_reference()
        self.expect('TO')
        target = self.parse_reference()

        node.metadata = {
            'source': source,
            'target': target
        }

        self.skip_newlines()
        return node

    def parse_extend(self) -> MSLNode:
        """Parse extend: extend standard_id with { overrides } """
        node = MSLNode(type='Extend', value=None)
        self.expect('EXTEND')

        standard_id = self.expect('IDENTIFIER').value
        self.expect('WITH')
        overrides = self.parse_object()

        node.metadata = {
            'standardId': standard_id,
            'overrides': overrides
        }

        self.skip_newlines()
        return node

    def parse_map(self) -> MSLNode:
        """Parse map: map source_path -> target_path """
        node = MSLNode(type='Map', value=None)
        self.expect('MAP')

        source = self.parse_reference()
        self.expect('ARROW')
        target = self.parse_reference()

        node.metadata = {
            'source': source,
            'target': target
        }

        self.skip_newlines()
        return node

    def parse_validate(self) -> MSLNode:
        """Parse validate: validate instance_id """
        node = MSLNode(type='Validate', value=None)
        self.expect('VALIDATE')

        instance_id = self.expect('IDENTIFIER').value

        node.metadata = {
            'instanceId': instance_id
        }

        self.skip_newlines()
        return node

    def parse_generate(self) -> MSLNode:
        """Parse generate: generate instance_id """
        node = MSLNode(type='Generate', value=None)
        self.expect('GENERATE')

        instance_id = self.expect('IDENTIFIER').value

        node.metadata = {
            'instanceId': instance_id
        }

        self.skip_newlines()
        return node

    def parse_reference(self) -> str:
        """Parse dotted reference: instance.property.subproperty"""
        parts = [self.expect('IDENTIFIER').value]

        while self.current_token and self.current_token.value == '.':
            self.advance()  # skip '.'
            # Handle dot as part of identifier pattern
            if self.current_token and self.current_token.type == 'IDENTIFIER':
                parts.append(self.current_token.value)
                self.advance()
            else:
                break

        return '.'.join(parts)

    def parse_object(self) -> Dict[str, Any]:
        """Parse object literal: { key: value, ... } """
        self.expect('LBRACE')
        self.skip_newlines()

        obj = {}

        while self.current_token and self.current_token.type != 'RBRACE':
            if self.current_token.type == 'NEWLINE':
                self.advance()
                continue

            # Parse key
            key = self.expect('IDENTIFIER').value
            self.expect('COLON')

            # Parse value
            value = self.parse_value()
            obj[key] = value

            # Optional comma
            if self.current_token and self.current_token.type == 'COMMA':
                self.advance()

            self.skip_newlines()

        self.expect('RBRACE')
        return obj

    def parse_value(self) -> Any:
        """Parse a value (string, number, boolean, object, array)"""
        if not self.current_token:
            raise SyntaxError("Unexpected end of input")

        token = self.current_token

        if token.type == 'STRING':
            value = token.value.strip('"')
            self.advance()
            return value
        elif token.type == 'NUMBER':
            value = float(token.value) if '.' in token.value else int(token.value)
            self.advance()
            return value
        elif token.type == 'BOOLEAN':
            value = token.value == 'true'
            self.advance()
            return value
        elif token.type == 'LBRACE':
            return self.parse_object()
        elif token.type == 'LBRACKET':
            return self.parse_array()
        elif token.type == 'IDENTIFIER':
            # Could be a reference
            return self.parse_reference()
        else:
            raise SyntaxError(f"Unexpected token in value: {token.type}")

    def parse_array(self) -> List[Any]:
        """Parse array: [ value1, value2, ... ] """
        self.expect('LBRACKET')
        self.skip_newlines()

        arr = []

        while self.current_token and self.current_token.type != 'RBRACKET':
            if self.current_token.type == 'NEWLINE':
                self.advance()
                continue

            value = self.parse_value()
            arr.append(value)

            if self.current_token and self.current_token.type == 'COMMA':
                self.advance()

            self.skip_newlines()

        self.expect('RBRACKET')
        return arr

    def advance(self):
        """Move to next token"""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def expect(self, token_type: str) -> MSLToken:
        """Expect a specific token type"""
        if not self.current_token or self.current_token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'} "
                f"at line {self.current_token.line if self.current_token else 'EOF'}"
            )

        token = self.current_token
        self.advance()
        return token

    def skip_newlines(self):
        """Skip any newline tokens"""
        while self.current_token and self.current_token.type == 'NEWLINE':
            self.advance()


class MSLInterpreter:
    """Interpreter for MSL - executes the AST"""

    def __init__(self, engine):
        """
        Initialize interpreter with a StandardInstantiationEngine

        Args:
            engine: StandardInstantiationEngine instance
        """
        self.engine = engine
        self.context = {}  # Store instances and bindings

    def execute(self, ast: MSLNode) -> Dict[str, Any]:
        """Execute MSL AST"""
        if ast.type != 'Program':
            raise ValueError("Expected Program node")

        results = {}

        for stmt in ast.children:
            result = self.execute_statement(stmt)
            if result:
                results.update(result)

        return results

    def execute_statement(self, node: MSLNode) -> Optional[Dict[str, Any]]:
        """Execute a single statement"""
        if node.type == 'Import':
            return self.execute_import(node)
        elif node.type == 'Instantiate':
            return self.execute_instantiate(node)
        elif node.type == 'Compose':
            return self.execute_compose(node)
        elif node.type == 'Bind':
            return self.execute_bind(node)
        elif node.type == 'Extend':
            return self.execute_extend(node)
        elif node.type == 'Map':
            return self.execute_map(node)
        elif node.type == 'Validate':
            return self.execute_validate(node)
        elif node.type == 'Generate':
            return self.execute_generate(node)
        else:
            raise ValueError(f"Unknown statement type: {node.type}")

    def execute_import(self, node: MSLNode) -> Dict[str, Any]:
        """Execute import statement"""
        standard_id = node.metadata['standardId']
        path = node.metadata['path']

        self.engine.load_standard(path)

        return {'import': standard_id}

    def execute_instantiate(self, node: MSLNode) -> Dict[str, Any]:
        """Execute instantiate statement"""
        instance = self.engine.instantiate(
            standard_id=node.metadata['standardId'],
            instance_id=node.metadata['instanceId'],
            parameters=node.metadata['parameters']
        )

        self.context[node.metadata['instanceId']] = instance

        return {node.metadata['instanceId']: instance.to_dict()}

    def execute_compose(self, node: MSLNode) -> Dict[str, Any]:
        """Execute compose statement"""
        composition_id = node.metadata['compositionId']
        instances = []

        for inst_node in node.metadata['instances']:
            result = self.execute_instantiate(inst_node)
            instances.append(result)

        return {
            composition_id: {
                'type': 'composition',
                'instances': instances
            }
        }

    def execute_bind(self, node: MSLNode) -> Dict[str, Any]:
        """Execute bind statement - connect outputs to inputs"""
        binding = {
            'source': node.metadata['source'],
            'target': node.metadata['target']
        }

        if 'bindings' not in self.context:
            self.context['bindings'] = []

        self.context['bindings'].append(binding)

        return {'bind': binding}

    def execute_extend(self, node: MSLNode) -> Dict[str, Any]:
        """Execute extend statement - create derived standard"""
        # This would create a new standard definition based on existing one
        return {'extend': node.metadata}

    def execute_map(self, node: MSLNode) -> Dict[str, Any]:
        """Execute map statement - map between naming schemes"""
        mapping = {
            'source': node.metadata['source'],
            'target': node.metadata['target']
        }

        if 'mappings' not in self.context:
            self.context['mappings'] = []

        self.context['mappings'].append(mapping)

        return {'map': mapping}

    def execute_validate(self, node: MSLNode) -> Dict[str, Any]:
        """Execute validate statement"""
        instance_id = node.metadata['instanceId']

        if instance_id not in self.context:
            raise ValueError(f"Instance not found: {instance_id}")

        # Validation logic would go here
        return {'validate': instance_id, 'result': 'valid'}

    def execute_generate(self, node: MSLNode) -> Dict[str, Any]:
        """Execute generate statement - output final artifacts"""
        instance_id = node.metadata['instanceId']

        if instance_id not in self.context:
            raise ValueError(f"Instance not found: {instance_id}")

        instance = self.context[instance_id]

        return {'generate': instance_id, 'output': instance.to_dict()}


def parse_msl(source: str) -> MSLNode:
    """Parse MSL source code into AST"""
    lexer = MSLLexer(source)
    tokens = lexer.tokenize()
    parser = MSLParser(tokens)
    return parser.parse()


def execute_msl(source: str, engine) -> Dict[str, Any]:
    """Parse and execute MSL source code"""
    ast = parse_msl(source)
    interpreter = MSLInterpreter(engine)
    return interpreter.execute(ast)


# Example MSL programs
EXAMPLE_MSL = """
# Import standards
import packml from "packml/packml-state-machine.json"
import isa88 from "isa-88/equipment-hierarchy.json"
import mqtt from "protocols/mqtt-sparkplug.json"

# Instantiate PackML for CT Scanner
instantiate packml as ct_scanner_packml with {
    equipmentPath: "Medical/Radiology/CT_Scanner_1",
    enableManualMode: true,
    safetyLevel: "high"
}

# Instantiate ISA-88 hierarchy
instantiate isa88 as medical_hierarchy with {
    enterpriseName: "MedTech_Industries",
    siteName: "Hospital_Boston",
    includeMetrics: true
}

# Instantiate MQTT interface
instantiate mqtt as ct_scanner_mqtt with {
    groupId: "Hospital_Boston",
    edgeNodeId: "Gateway_Radiology",
    deviceId: "CT_Scanner_1",
    brokerUrl: "mqtt://broker.hospital.local:1883"
}

# Bind PackML state to MQTT publishing
bind ct_scanner_packml.tags.stateName to ct_scanner_mqtt.metricNaming

# Map ISA-88 paths to MQTT topics
map medical_hierarchy.tagGeneration.pathFormat to mqtt.topicDesign

# Validate and generate
validate ct_scanner_packml
generate ct_scanner_packml
"""


if __name__ == '__main__':
    print("Meta-Standard Language (MSL) Parser")
    print("=" * 80)
    print("\nExample MSL Program:")
    print(EXAMPLE_MSL)
    print("\n" + "=" * 80)
    print("\nParsing...")

    try:
        ast = parse_msl(EXAMPLE_MSL)
        print(f"✓ Parsed successfully!")
        print(f"  Statements: {len(ast.children)}")

        for i, stmt in enumerate(ast.children):
            print(f"    {i+1}. {stmt.type}: {stmt.metadata}")

    except Exception as e:
        print(f"✗ Parse error: {e}")
