"""
Pytest configuration and shared fixtures
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def project_root_path():
    """Return path to project root"""
    return Path(__file__).parent.parent


@pytest.fixture
def standards_path(project_root_path):
    """Return path to standards directory"""
    return project_root_path / "standards"


@pytest.fixture
def templates_path(project_root_path):
    """Return path to templates directory"""
    return project_root_path / "templates"


@pytest.fixture
def sample_packml_standard():
    """Sample PackML standard for testing"""
    return {
        "id": "packml-v1.0",
        "name": "PackML State Machine",
        "version": "1.0",
        "states": [
            "Stopped", "Starting", "Idle", "Running", "Suspending",
            "Suspended", "Unsuspending", "Holding", "Held", "Unholding",
            "Completing", "Complete", "Clearing", "Stopping", "Aborting",
            "Aborted", "Resetting", "Execute"
        ],
        "commands": [
            "Start", "Stop", "Hold", "Unhold", "Suspend",
            "Unsuspend", "Abort", "Clear", "Reset", "StateChange"
        ]
    }


@pytest.fixture
def sample_isa88_hierarchy():
    """Sample ISA-88 equipment hierarchy for testing"""
    return {
        "id": "isa-88-hierarchy",
        "levels": [
            "Enterprise",
            "Site",
            "Area",
            "ProcessCell",
            "Unit",
            "EquipmentModule",
            "ControlModule"
        ]
    }


@pytest.fixture
def mock_medical_study():
    """Sample medical study for testing"""
    return {
        "study_id": "ST001",
        "patient_id": "PT001",
        "patient_name": "Test Patient",
        "modality": "CT",
        "status": "Pending",
        "priority": "High",
        "body_part": "Chest",
        "date": "2025-01-17"
    }
