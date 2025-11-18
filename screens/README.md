# Screens Directory

This directory contains all the main application screens and interfaces for the Chazon Medical Imaging Virtual Factory.

## Contents

### Enterprise Management Screens
- **enterprise-portal.html** - Main enterprise management portal
- **asset-management.html** - Asset tracking and management system
- **analytics-reporting.html** - Analytics and reporting dashboards
- **configuration.html** - System configuration interface

### Production Management Screens
- **production-planning.html** - Production planning and scheduling
- **quality-management.html** - Quality control and management system
- **maintenance-planning.html** - Maintenance planning and scheduling

### Operations Control Screens
- **scada.html** - SCADA (Supervisory Control and Data Acquisition) gateway
- **hmi.html** - HMI (Human Machine Interface) control panel
- **plc.html** - PLC (Programmable Logic Controller) logic interface

## Architecture

These screens implement ISA-95 Level 4 (Business Planning & Logistics) interfaces. They provide:
- Real-time monitoring and control
- Business process management
- Data acquisition and analysis
- Integration with lower-level control systems

## Access

All screens are accessible from the main index.html gateway or directly via their URLs:
- `/screens/[filename].html`