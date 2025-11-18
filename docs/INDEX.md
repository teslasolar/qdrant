# Documentation Index

Complete documentation navigation for the Qdrant Medical Imaging SCADA System.

## 📚 Quick Start

- [README](../README.md) - Project overview
- [QUICKSTART](user-guide/QUICKSTART.md) - 5-minute setup guide
- [CHANGELOG](../CHANGELOG.md) - Version history

## 👤 User Documentation

### Getting Started
- [Installation Guide](user-guide/INSTALLATION.md)
- [Quick Start](user-guide/QUICKSTART.md)
- [User Interface Guide](user-guide/UI_GUIDE.md)

### Medical Workflows
- [DICOM Processing](user-guide/DICOM_WORKFLOW.md)
- [AlF-DETECT Screening](../os/medical/ALF-DETECT-ENHANCEMENT-GUIDE.md)
- [Patient Study Management](user-guide/STUDY_MANAGEMENT.md)

### ISA-95 Architecture
- [Architecture Overview](user-guide/ISA95_ARCHITECTURE.md)
- [L4 Business Layer](user-guide/L4_BUSINESS.md)
- [L3 MES Layer](user-guide/L3_MES.md)
- [L2 Supervisory Layer](user-guide/L2_SUPERVISORY.md)
- [L1 Control Layer](user-guide/L1_CONTROL.md)

## 🔧 Developer Documentation

### Development Setup
- [Development Environment](developer-guide/DEVELOPMENT_SETUP.md)
- [Build Process](developer-guide/BUILD.md)
- [Testing](../tests/README.md)

### Core Systems
- [Standards Framework](../standards/README.md)
- [Template System](../templates/README.md)
- [Generator Scripts](developer-guide/GENERATORS.md)
- [CLI Tools](../cli/README.md)

### Standards
- [Standards-as-Tags Framework](../standards/FRAMEWORK_SUMMARY.md)
- [PackML](../standards/packml/packml-state-machine.json)
- [ISA-88](../standards/isa-88/)
- [ISA-95](../standards/isa-95/)
- [ISA-101](../standards/isa-101/)
- [Protocols](../standards/protocols/)

### Integration
- [Template Integration](../standards/INTEGRATION_GUIDE.md)
- [Standards Composition](developer-guide/STANDARDS_COMPOSITION.md)
- [Meta-Standard Language (MSL)](developer-guide/MSL_GUIDE.md)

## 📡 API Documentation

- [API Overview](api/README.md)
- [Endpoints Reference](api/ENDPOINTS.md)
- [Authentication](api/AUTHENTICATION.md)
- [Examples](api/EXAMPLES.md)
- [FastAPI Docs](http://localhost:8000/docs) (when running)

## 🔒 Security & Compliance

- [Security Policy](security/README.md)
- [HIPAA Compliance](security/HIPAA.md)
- [FDA 21 CFR Part 11](security/FDA_21_CFR.md)
- [EU Annex 11](security/EU_ANNEX_11.md)
- [ISO 13485](security/ISO_13485.md)
- [Audit Logging](security/AUDIT.md)

## 📊 Standards Documentation

### ISA Standards
- [ISA-88: Batch Control](standards/isa/isa-88/README.md)
- [ISA-95: Enterprise-Control Integration](standards/isa/isa-95/README.md)
- [ISA-101: HMI Design](standards/isa/isa-101/README.md)

### Protocols
- [MQTT/Sparkplug B](standards/protocols/mqtt/README.md)
- [Modbus](standards/protocols/modbus/README.md)
- [OPC-UA](standards/protocols/opc-ua/README.md)

### PackML
- [PackML State Machine](../os/modules/packml/README.md)
- [PackML Baton](../os/modules/packml/packml-baton.md)

## 🏥 Medical Imaging

### Workflows
- [DICOM Workflow System](../os/medical/workflows/README.md)
- [Multi-Modal Analysis](../os/medical/workflows/multi-modal-analysis.json)
- [Batch Screening](../os/medical/workflows/batch-screening.json)

### AlF-DETECT System
- [Enhancement Guide](../os/medical/ALF-DETECT-ENHANCEMENT-GUIDE.md)
- [Enhancement Summary](../os/medical/ENHANCEMENT-SUMMARY.md)
- [Configuration](../os/medical/config.yaml)

### Quality Control
- [QC Checkpoints](../os/medical/workflows/qc/quality-control-checkpoints.yaml)
- [Image Enhancement](../os/medical/workflows/processing/enhancement-pipeline.yaml)

## 🎛️ SCADA & Controls

- [Tag Providers](../os/controls/tag-providers/)
- [Medical Tags](../os/controls/tag-providers/medical.json)
- [PLC Areas](../README.md#8-plc-areas)

## 🛠️ Maintenance

### CLI Tools
- [Health Check](../cli/health-check.py)
- [Validate Tags](../cli/validate-tags.py)
- [Project Stats](../cli/project-stats.py)
- [Find Unused Files](../cli/find-unused-files.py)
- [Backup/Restore](../cli/backup-restore.py)

### Monitoring
- [System Health](../cli/README.md#health-check)
- [Performance Metrics](../cli/README.md#project-statistics)

## 📖 Reference

- [Complete Hierarchy](ISA-95-COMPLETE-HIERARCHY.md)
- [Equipment Model](../os/equipment/README.md)
- [Module Registry](../os/modules/REGISTRY.md)
- [Project Manifest](../MANIFEST.md)

## 🔍 Search & Navigation

### By Topic
- **Medical Imaging**: AlF-DETECT, DICOM, Modalities, Workflows
- **Standards**: ISA-88, ISA-95, ISA-101, PackML
- **Protocols**: MQTT, Modbus, OPC-UA
- **Templates**: Screens, Components, Tags
- **Testing**: Unit, Integration, E2E
- **Security**: HIPAA, FDA, ISO, Audit

### By ISA-95 Level
- **L4 Business**: Enterprise Portal, Production, Quality, Analytics
- **L3 MES**: SCADA Gateway, Workflows, Coordination
- **L2 Supervisory**: Tag Providers, SCADA, HMI
- **L1 Control**: PLCs, Control Logic
- **L0 Physical**: Sensors, Actuators, Equipment

## 📝 Contributing

- [Contributing Guide](guides/CONTRIBUTING.md)
- [Code Style](developer-guide/CODE_STYLE.md)
- [Pull Request Process](developer-guide/PR_PROCESS.md)

## 📞 Support

- **Documentation Issues**: File an issue with label `documentation`
- **Technical Support**: support@chazon.ai
- **Security Issues**: security@chazon.ai (private)

---

**Last Updated**: 2025-01-17
**Documentation Version**: 2.1
