# Test Suite

Comprehensive test suite for the Qdrant Medical Imaging SCADA system.

## Structure

```
tests/
├── unit/           # Unit tests for individual functions
├── integration/    # Integration tests for system components
└── e2e/            # End-to-end workflow tests
```

## Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-asyncio pytest-cov pytest-mock
```

### Run All Tests

```bash
# From project root
pytest

# With coverage
pytest --cov=. --cov-report=html

# Verbose output
pytest -v
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# End-to-end tests only
pytest tests/e2e/
```

## Coverage Goals

- **Minimum**: 70% code coverage
- **Target**: 85% code coverage
- **Critical Paths**: 100% coverage (standards engine, medical workflows, CLI tools)

## Test Priorities

### Priority 1: Core Functionality
- [ ] Standards Instantiation Engine (`standards/engine/standard_instantiation_engine.py`)
- [ ] Template Integration (`standards/engine/template_integration.py`)
- [ ] MSL Parser (`standards/meta-standard/msl_parser.py`)

### Priority 2: Business Logic
- [ ] Medical Workflows (`os/medical/workflows/`)
- [ ] Tag Provider System (`os/controls/tag-providers/`)
- [ ] Generator Scripts (`cli/generators/`)

### Priority 3: CLI Tools
- [ ] Health Check (`cli/health-check.py`)
- [ ] Validate Tags (`cli/validate-tags.py`)
- [ ] Project Stats (`cli/project-stats.py`)

### Priority 4: Integration
- [ ] Backend API (`os/backend/api.py`)
- [ ] Qdrant Integration
- [ ] MQTT/SCADA Integration

## Writing Tests

### Unit Test Example

```python
# tests/unit/test_standard_engine.py
import pytest
from standards.engine.standard_instantiation_engine import StandardInstantiationEngine

def test_load_standard():
    engine = StandardInstantiationEngine('/path/to/standards')
    standard = engine.load_standard('packml-v1.0')
    assert standard is not None
    assert 'states' in standard
    assert len(standard['states']) == 18
```

### Integration Test Example

```python
# tests/integration/test_template_generation.py
import pytest
from standards.engine.standard_instantiation_engine import StandardInstantiationEngine

def test_full_template_generation():
    engine = StandardInstantiationEngine('/path/to/standards')
    instance = engine.instantiate('packml-v1.0', 'test_equipment')
    templates = engine.export_to_templates(instance)
    assert templates is not None
    assert 'tags' in templates
```

### E2E Test Example

```python
# tests/e2e/test_medical_workflow.py
import pytest

def test_complete_dicom_workflow():
    # Test complete DICOM processing pipeline
    # Ingestion → Preprocessing → Analysis → Storage
    pass
```

## CI/CD Integration

Add to `.github/workflows/tests.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Test Configuration

Create `pytest.ini` in project root:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow-running tests
```

## Mocking

For testing without actual resources:

```python
from unittest.mock import Mock, patch

@patch('standards.engine.standard_instantiation_engine.open')
def test_with_mock_file(mock_open):
    mock_open.return_value.__enter__.return_value.read.return_value = '{"test": "data"}'
    # Test code here
```

## Test Data

Create test fixtures:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_standard():
    return {
        "id": "test-standard",
        "states": ["Idle", "Running", "Complete"]
    }

@pytest.fixture
def mock_engine():
    from standards.engine.standard_instantiation_engine import StandardInstantiationEngine
    return StandardInstantiationEngine('/tmp/test-standards')
```

## Current Status

- ✅ Test structure created
- ❌ Test files (0% coverage)
- ❌ pytest.ini configuration
- ❌ CI/CD integration

**Next Steps**: Begin writing unit tests for core functionality.
