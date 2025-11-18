# Chazon CLI Tools

**Markdown-executable** command-line interface tools for managing the Chazon Medical Imaging SCADA System.

All CLI tools are **markdown files (.md)** that follow the system's markdown-first architecture.

## Three Access Methods

Every CLI command is accessible via **three interfaces**:

| Method | Example | Port |
|--------|---------|------|
| **CLI** (Direct) | `./cli/boot.md` | N/A |
| **API** (REST) | `POST http://localhost:8001/cli/boot` | 8001 |
| **MCP** (Tool) | `cli_boot` tool via MCP server | stdio |

### Start Wrappers

```bash
# Start API wrapper (port 8001)
python3 cli/api-wrapper.md

# Start MCP wrapper (stdio)
python3 cli/mcp-wrapper.md

# Or configure MCP in Claude Desktop (see mcp-wrapper.md)
```

---

## Quick Reference

### System Management
```bash
./cli/boot.md           # Boot the OS (6-phase sequence)
./cli/start.md          # Start all services
./cli/stop.md           # Stop all services
./cli/restart.md        # Restart all services
./cli/health.md         # System health check
./cli/logs.md [area]    # View logs (backend|http|system|all)
./cli/deploy.md         # Deploy to GitHub Pages
```

### Development
```bash
./cli/dev/setup.md      # Setup development environment
./cli/dev/test.md       # Run all tests
```

### Models
```bash
./cli/models/download.md    # Download AI models
./cli/models/list.md        # List available models
```

---

## Complete Examples (All 3 Methods)

### Boot OS
```bash
# CLI
./cli/boot.md

# API
curl -X POST http://localhost:8001/cli/boot

# MCP (natural language in Claude Desktop)
"Boot the Chazon OS"
```

### Start Services
```bash
# CLI
./cli/start.md

# API
curl -X POST http://localhost:8001/cli/start

# MCP
"Start all services"
```

### Health Check
```bash
# CLI
./cli/health.md

# API
curl http://localhost:8001/cli/health

# MCP
"Check system health"
```

### View Logs
```bash
# CLI
./cli/logs.md backend

# API
curl -X POST http://localhost:8001/cli/logs \
  -H "Content-Type: application/json" \
  -d '{"args": ["backend"]}'

# MCP
"Show me the backend logs"
```

### Run Tests
```bash
# CLI
./cli/dev/test.md

# API
curl -X POST http://localhost:8001/cli/dev/test

# MCP
"Run all tests"
```

### List Models
```bash
# CLI
./cli/models/list.md

# API
curl http://localhost:8001/cli/models/list

# MCP
"List all AI models"
```

---

## API & MCP Wrappers

### api-wrapper.md
FastAPI server that exposes all CLI commands as REST endpoints.

**Features:**
- All CLI commands available via HTTP POST/GET
- JSON responses with stdout/stderr/exit codes
- CORS enabled
- 5-minute timeout per command
- `/cli/commands` endpoint lists all available commands

**Endpoints:**
- `GET /health` - API health check
- `GET /cli/commands` - List all commands
- `POST /cli/boot` - Boot OS
- `POST /cli/start` - Start services
- `POST /cli/stop` - Stop services
- `POST /cli/restart` - Restart services
- `GET /cli/health` - System health
- `POST /cli/logs` - View logs
- `POST /cli/deploy` - Deploy
- `POST /cli/dev/setup` - Dev setup
- `POST /cli/dev/test` - Run tests
- `POST /cli/models/download` - Download models
- `GET /cli/models/list` - List models
- `POST /cli/exec` - Execute any command

### mcp-wrapper.md
Model Context Protocol server for Claude Desktop and other MCP clients.

**Features:**
- 12 MCP tools (one per CLI command)
- Natural language interface
- Async execution
- 5-minute timeout per command
- Works with Claude Desktop, IDEs, etc.

**Tools:**
- `cli_boot` - Boot OS
- `cli_start` - Start services
- `cli_stop` - Stop services
- `cli_restart` - Restart services
- `cli_health` - Health check
- `cli_logs` - View logs (with area parameter)
- `cli_deploy` - Deploy
- `cli_dev_setup` - Dev setup
- `cli_dev_test` - Run tests
- `cli_models_download` - Download models
- `cli_models_list` - List models
- `cli_exec` - Execute any command

---

## System Management Scripts

### boot.md
Runs the 6-phase boot sequence to initialize the Chazon OS.

**Phases:**
1. Phase 0: Core Infrastructure (OS, Compiler, PackML)
2. Phase 1: AI Models (ONNX, WebGPU)
3. Phase 2: Multi-Agent System (Swarm, Conway, GPT)
4. Phase 3: Medical Imaging (DICOM, Qdrant, AlF-DETECT)
5. Phase 4: UI Components (Modules, Icons, Screens)
6. Phase 5: Templates (ISA, Views, Medical)

**Usage:**
```bash
./cli/boot.md
```

**Output:**
- ✅ Status for each phase
- 🟢 System ready indicators
- 📊 Access points for SCADA/HMI/PLC

---

### start.md
Starts all backend services required for full system operation.

**Services Started:**
1. **Qdrant** - Vector database on port 6333 (Docker)
2. **Backend API** - FastAPI server on port 8000 (Python)
3. **HTTP Server** - Development server on port 8080 (Python)

**Requirements:**
- Docker (for Qdrant)
- Python 3.8+ (for Backend API)

**Usage:**
```bash
./cli/start.md
```

**Logs:**
- Backend API: `cli/logs/backend.log`
- HTTP Server: `cli/logs/httpserver.log`

**PID Files:**
- Backend API: `cli/logs/backend.pid`
- HTTP Server: `cli/logs/httpserver.pid`

---

### stop.md
Stops all running services gracefully.

**Stops:**
- Backend API (kills process, removes PID file)
- HTTP Server (kills process, removes PID file)
- Qdrant (stops and removes Docker container)

**Usage:**
```bash
./cli/stop.md
```

---

### restart.md
Convenience script that stops and starts all services.

**Usage:**
```bash
./cli/restart.md
```

Equivalent to:
```bash
./cli/stop.md && sleep 2 && ./cli/start.md
```

---

### health.md
Comprehensive system health check for all services and resources.

**Checks:**
1. **Qdrant** - Container status and HTTP response
2. **Backend API** - Process status and health endpoint
3. **HTTP Server** - Process status and serving files
4. **Disk Usage** - Warns if >80% full
5. **File System** - Counts modules, models, logs

**Status Indicators:**
- 🟢 HEALTHY - Service responding normally
- 🟡 DEGRADED - Service running but not responding
- 🔴 DOWN - Service not running

**Usage:**
```bash
./cli/health.md
```

**Example Output:**
```
🟢 Qdrant: HEALTHY (http://localhost:6333)
🟢 Backend API: HEALTHY (http://localhost:8000)
🟢 HTTP Server: HEALTHY (http://localhost:8080)
🟢 Disk Usage: 45% (healthy)
📦 Modules: 114
🤖 Models: 4
📋 Log Files: 12
```

---

### logs.md
View system logs for different areas.

**Usage:**
```bash
./cli/logs.md [area]
```

**Areas:**
- `backend` - Backend API logs
- `http` - HTTP server logs
- `system` - OS system logs
- `all` - All logs (default, shows last 10 lines of each)

**Examples:**
```bash
# View all logs (summary)
./cli/logs.md

# Tail backend logs
./cli/logs.md backend

# Tail HTTP server logs
./cli/logs.md http

# View system logs
./cli/logs.md system
```

**Live Monitoring:**
For live log monitoring, the script will run `tail -f` for single areas.

---

### deploy.md
Deploy the application to GitHub Pages.

**Process:**
1. Checks for git repository
2. Warns about uncommitted changes
3. Gets current branch name
4. Pushes to origin

**Usage:**
```bash
./cli/deploy.md
```

**Deployment URL:**
https://teslasolar.github.io/qdrant/

**Note:** GitHub Pages may take a few minutes to update after deployment.

---

## Development Scripts

### dev/setup.md
Sets up the complete development environment.

**Actions:**
1. Checks Python 3.8+ availability
2. Creates backend virtual environment
3. Installs backend dependencies (requirements.txt)
4. Checks Node.js (optional)
5. Installs frontend dependencies if package.json exists
6. Creates log directories
7. Creates .env from .env.example

**Usage:**
```bash
./cli/dev/setup.md
```

**Requirements:**
- Python 3.8+
- Node.js (optional, for frontend development)
- Docker (for Qdrant)

**Post-Setup:**
1. Update `.env` with your API keys
2. Run `./cli/start.md`
3. Open http://localhost:8080

---

### dev/test.md
Runs all available test suites.

**Test Suites:**
1. Module tests (os/test-modules with pytest)
2. Backend API tests (os/backend/test_api.py)

**Usage:**
```bash
./cli/dev/test.md
```

**Requirements:**
- pytest (`pip install pytest`)

**Example Output:**
```
🧪 Running Chazon Tests
=======================

Running module tests...
  ✅ Module tests passed

Running backend tests...
  ✅ Backend tests passed

=======================
✅ All tests completed
```

---

## Model Management Scripts

### models/download.md
Downloads AI models for inference.

**Models:**
- **BERT Tiny** - Text embeddings
- **MobileNet V2** - Image classification
- **ResNet18** - Image classification
- **SqueezeNet** - Lightweight image classification

**Usage:**
```bash
./cli/models/download.md
```

**Download Locations:**
Models are downloaded to their respective directories:
- `os/models/bert-tiny/`
- `os/models/mobilenet-v2/`
- `os/models/resnet18/`
- `os/models/squeezenet/`

---

### models/list.md
Lists all available AI models and their sizes.

**Usage:**
```bash
./cli/models/list.md
```

**Example Output:**
```
🤖 Available AI Models
======================

📦 bert-tiny
   ✅ model.onnx (45MB)

📦 mobilenet-v2
   ✅ mobilenetv2-7.onnx (14MB)

📦 resnet18
   ✅ resnet18-v1-7.onnx (46MB)

📦 squeezenet
   ✅ squeezenet1.1-7.onnx (5.0MB)

======================
Total models: 4
```

---

## Directory Structure

```
cli/
├── README.md               # This file
├── api-wrapper.md          # REST API wrapper (port 8001)
├── mcp-wrapper.md          # MCP server wrapper (stdio)
├── boot.md                 # Boot OS
├── start.md                # Start services
├── stop.md                 # Stop services
├── restart.md              # Restart services
├── health.md               # Health check
├── logs.md                 # View logs
├── deploy.md               # Deploy to GitHub Pages
├── dev/                    # Development tools
│   ├── setup.md            # Dev environment setup
│   └── test.md             # Run tests
├── models/                 # Model management
│   ├── download.md         # Download models
│   └── list.md             # List models
├── backup/                 # Backup tools (future)
└── logs/                   # Service logs
    ├── backend.log         # Backend API logs
    ├── backend.pid         # Backend API PID
    ├── httpserver.log      # HTTP server logs
    └── httpserver.pid      # HTTP server PID
```

---

## Environment Variables

Create a `.env` file in the root directory (use `.env.example` as template):

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
COHERE_API_KEY=...

# Qdrant
QDRANT_URL=https://xyz.qdrant.io
QDRANT_API_KEY=...

# Application
DEBUG=false
LOG_LEVEL=INFO
PORT=8000
```

---

## Typical Workflow

### First-Time Setup
```bash
# 1. Setup development environment
./cli/dev/setup.md

# 2. Update .env with API keys
nano .env

# 3. Download AI models (optional)
./cli/models/download.md

# 4. Boot the OS
./cli/boot.md

# 5. Start all services
./cli/start.md

# 6. Check health
./cli/health.md

# 7. Open browser
open http://localhost:8080
```

### Daily Development
```bash
# Start services
./cli/start.md

# Make changes...

# Run tests
./cli/dev/test.md

# Check logs
./cli/logs.md backend

# Restart if needed
./cli/restart.md

# Stop when done
./cli/stop.md
```

### Deployment
```bash
# Run tests
./cli/dev/test.md

# Health check
./cli/health.md

# Deploy
./cli/deploy.md
```

---

## Troubleshooting

### Services Won't Start
```bash
# Check if ports are already in use
lsof -i :6333  # Qdrant
lsof -i :8000  # Backend API
lsof -i :8080  # HTTP Server

# Kill processes using ports
kill -9 <PID>

# Restart services
./cli/restart.md
```

### Docker Issues
```bash
# Check Docker is running
docker info

# Remove old Qdrant container
docker stop qdrant && docker rm qdrant

# Restart services
./cli/start.md
```

### Python Virtual Environment Issues
```bash
# Remove and recreate venv
cd os/backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Issues
```bash
# Make scripts executable
chmod +x cli/*.md
chmod +x cli/dev/*.md
chmod +x cli/models/*.md
```

---

## Advanced Usage

### Custom Health Checks
Add your own health checks to `health.md`:

```bash
# Check custom service
echo "Checking My Service..."
if curl -s http://localhost:9000/health > /dev/null 2>&1; then
    echo "  🟢 My Service: HEALTHY"
else
    echo "  🔴 My Service: DOWN"
fi
```

### Custom Log Monitoring
Add custom log areas to `logs.md`:

```bash
myservice)
    echo "My Service Logs:"
    tail -f "$ROOT_DIR/cli/logs/myservice.log"
    ;;
```

### Automated Deployment
Set up GitHub Actions to automatically deploy:

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: ./cli/deploy.md
```

---

## Maintenance & Utility Scripts

The CLI includes powerful maintenance and utility scripts for managing the project:

### health-check.py
Comprehensive health check that validates the entire project structure.

**Usage:**
```bash
python3 cli/health-check.py [--verbose] [--fix]
```

**What it checks:**
- Required directories exist
- Critical files present
- All tag.json files valid
- Index directories properly structured
- No duplicate UUIDs
- ISA-95 hierarchy integrity
- Controls structure (HMI/PLC/SCADA)
- JSON syntax validity
- Broken symbolic links

**Exit codes:**
- 0: All checks passed
- 1: Warnings found
- 2: Errors found

**Example output:**
```
Checking Required Directories
==============================================================
✓ Directory exists: cli/
✓ Directory exists: collab/
✓ Directory exists: docs/
✓ Directory exists: index/
✓ Directory exists: os/

Validating tag.json Files
==============================================================
✓ All 127 tag.json files are valid

Health Check Summary
==============================================================
Successes: 45
Warnings:  2
Errors:    0

Health check PASSED with 2 warnings
```

---

### validate-tags.py
Specialized validator for tag.json files with auto-fix capabilities.

**Usage:**
```bash
python3 cli/validate-tags.py [--fix] [--verbose] [--export report.json]
```

**Validations:**
- Required fields present (UUID, ISA_Level, Directory_Path, Title, Description)
- UUID format valid (RFC 4122)
- ISA Level valid
- Directory paths match actual locations
- Child/parent relationships correct
- No duplicate UUIDs
- Breadcrumb trails valid
- File references exist

**Options:**
- `--fix`: Automatically fix common issues (invalid UUIDs, incorrect paths)
- `--verbose`: Show validation details for each file
- `--export FILE`: Export validation report to JSON

**Example with fixes:**
```bash
python3 cli/validate-tags.py --fix --verbose

Validating Individual Files
==============================================================
ℹ Validating: docs/index/tag.json
✓ docs/index/tag.json: Valid

✗ collab/test/index/tag.json: Invalid UUID format: abc123
🔧 Generated new UUID: d4cffc59-a266-42d2-82c6-bb9cf206ec65

Validation Report
==============================================================
Total tag.json files:  127
Valid files:           126
Files with errors:     1
Fixes applied:         1
```

---

### find-unused-files.py
Find and report unused, temporary, or orphaned files in the project.

**Usage:**
```bash
python3 cli/find-unused-files.py [--delete] [--report unused.txt]
```

**What it finds:**
- Temporary/backup files (.bak, .tmp, ~, .swp)
- Empty directories
- Duplicate files (same content)
- Old log files (>30 days)
- Orphaned files (not referenced anywhere)
- Large files (>10MB)

**Options:**
- `--delete`: Delete unused files (with confirmation)
- `--extensions .py,.js`: Only check specific extensions
- `--exclude-dirs tests,docs`: Exclude additional directories
- `--report FILE`: Save detailed report to file

**Example output:**
```
Finding Temporary/Backup Files
==============================================================
⚠ Found 3 temporary/backup files:
  - old_script.py~ (1.2KB)
  - backup.bak (45KB)
  - .DS_Store (6.0KB)

Finding Duplicate Files
==============================================================
⚠ Found 2 sets of duplicate files:

  Duplicate set (4.5KB):
    - index/controls/index.html
    - os/controls/index.html

Summary Report
==============================================================
Temporary/Backup Files: 3
Empty Directories:      2
Duplicate Files:        2
Old Log Files:          5
Orphaned Files:         1
Large Files:            3

Total items found:      16
Potential space savings: 156.3KB
```

---

### project-stats.py
Generate comprehensive statistics about the project.

**Usage:**
```bash
python3 cli/project-stats.py [--output FORMAT] [--export FILE] [--chart]
```

**Output formats:**
- `text`: Human-readable terminal output (default)
- `json`: Structured JSON data
- `markdown`: Markdown report
- `html`: HTML report (planned)

**Statistics collected:**
- File counts by type
- Directory structure depth
- Code metrics (lines by language)
- ISA-95 tag distribution
- Controls statistics (HMI screens, templates)
- Size analysis
- Recent activity (files modified)
- Largest files and directories

**Options:**
- `--output FORMAT`: Choose output format
- `--export FILE`: Save report to file
- `--detailed`: Show detailed breakdown
- `--chart`: Generate ASCII charts (text mode)

**Example output:**
```
==============================================================
  Qdrant Project Statistics
==============================================================

Overview
==============================================================
Total Files:           1,247
Total Directories:     456
Total Size:            45.3MB
Total Lines of Code:   12,345

File Types
==============================================================
.json                    387 files      8.2MB
.py                      142 files     12.1MB
.md                       89 files      3.4MB
.html                     67 files      5.6MB

Code Statistics
==============================================================
Python               142 files    8,234 lines      12.1MB
JavaScript            45 files    2,145 lines       1.8MB
HTML                  67 files    1,890 lines       5.6MB

Tag Statistics
==============================================================
Total tag.json files:  127
Valid tags:            125
Invalid tags:          2

ISA-95 Level Distribution:
  L4_Business             45 tags
  L3_Site                 32 tags
  L2_Area                 28 tags
  L1_ProcessCell          18 tags
  L0_Unit                  4 tags

Controls Statistics
==============================================================
HMI Screens:           15
HMI Templates:         8
PLC Files:             23
SCADA Files:           12

Recent Activity
==============================================================
Modified in last 24h:  8
Modified in last week: 23
Modified in last month:67
```

**Export to JSON:**
```bash
python3 cli/project-stats.py --output json --export stats.json
```

**Generate markdown report:**
```bash
python3 cli/project-stats.py --output markdown --export STATS.md
```

---

### backup-restore.py
Complete backup and restore solution with versioning.

**Usage:**
```bash
# Create backup
python3 cli/backup-restore.py backup [--name NAME] [--compress]

# List backups
python3 cli/backup-restore.py list

# Show backup details
python3 cli/backup-restore.py info BACKUP_ID

# Restore backup
python3 cli/backup-restore.py restore BACKUP_ID [--force]

# Delete backup
python3 cli/backup-restore.py delete BACKUP_ID

# Clean old backups
python3 cli/backup-restore.py clean [--keep 5]
```

**Features:**
- Full project backups with metadata
- Gzip compression support
- Backup verification (checksums)
- Incremental backups (planned)
- Keep N most recent backups
- Backup integrity checking

**Backup locations:**
- Archives: `cli/backup/archives/`
- Metadata: `cli/backup/archives/metadata.json`

**Example - Create backup:**
```bash
python3 cli/backup-restore.py backup --name "pre-refactor" --compress

Creating Backup
==============================================================
ℹ Backup ID: backup_20251117_143022
ℹ Name: pre-refactor
ℹ Destination: backup_20251117_143022.tar.gz
  Backed up 1247 files...
✓ Backed up 1247 files (45.3MB)
✓ Archive size: 12.8MB
ℹ Compression ratio: 71.8%
✓ Backup created successfully: backup_20251117_143022
```

**Example - List backups:**
```bash
python3 cli/backup-restore.py list

Available Backups
================================================================================
ID                        Name                 Date                 Size       Files
--------------------------------------------------------------------------------
backup_20251117_143022    pre-refactor        2025-11-17 14:30     12.8MB     1247
backup_20251117_120000    daily-backup        2025-11-17 12:00     13.2MB     1245
backup_20251116_180000    before-cleanup      2025-11-16 18:00     42.1MB     1285

Total backups: 3
```

**Example - Restore:**
```bash
python3 cli/backup-restore.py restore backup_20251117_143022

Restoring Backup
==============================================================
Backup ID:       backup_20251117_143022
Name:            pre-refactor
Created:         2025-11-17 14:30:22
Files:           1,247
Size:            12.8MB
ℹ Verifying backup integrity...
✓ Checksum verified

WARNING: This will overwrite existing files!
Continue? (yes/no): yes

ℹ Extracting backup...
✓ Restored 1,247 files
✓ Backup restored successfully!
```

**Example - Clean old backups:**
```bash
python3 cli/backup-restore.py clean --keep 3

Cleaning Old Backups
==============================================================
Keeping 3 most recent backups
Deleting 2 old backups:
  - backup_20251115_120000 (daily-backup)
  - backup_20251114_120000 (daily-backup)

Continue? (yes/no): yes

✓ Deleted 2 backups
✓ Freed 89.4MB of space
```

**Automated daily backups:**
Add to cron:
```bash
# Daily backup at 2 AM
0 2 * * * cd /path/to/qdrant && python3 cli/backup-restore.py backup --name "daily-$(date +\%Y\%m\%d)" --compress

# Weekly cleanup, keep last 7 backups
0 3 * * 0 cd /path/to/qdrant && python3 cli/backup-restore.py clean --keep 7
```

---

## Maintenance Workflow

### Daily Maintenance
```bash
# 1. Check project health
python3 cli/health-check.py

# 2. Validate tags
python3 cli/validate-tags.py --verbose

# 3. Check for unused files
python3 cli/find-unused-files.py --report daily-unused.txt

# 4. Generate statistics
python3 cli/project-stats.py --export stats-$(date +%Y%m%d).json
```

### Weekly Maintenance
```bash
# 1. Deep health check with fixes
python3 cli/health-check.py --verbose --fix

# 2. Validate and fix all tags
python3 cli/validate-tags.py --fix --export tag-validation.json

# 3. Find and clean unused files
python3 cli/find-unused-files.py --delete --report unused-cleaned.txt

# 4. Create backup
python3 cli/backup-restore.py backup --name "weekly-$(date +%Y%m%d)" --compress

# 5. Clean old backups
python3 cli/backup-restore.py clean --keep 4
```

### Before Major Changes
```bash
# 1. Create named backup
python3 cli/backup-restore.py backup --name "pre-${CHANGE_NAME}" --compress

# 2. Full validation
python3 cli/health-check.py --verbose
python3 cli/validate-tags.py --verbose --export pre-change-validation.json

# 3. Generate baseline stats
python3 cli/project-stats.py --output json --export pre-change-stats.json
```

### After Major Changes
```bash
# 1. Health check
python3 cli/health-check.py

# 2. Validate tags (with auto-fix)
python3 cli/validate-tags.py --fix

# 3. Compare statistics
python3 cli/project-stats.py --output json --export post-change-stats.json

# 4. Find new unused files
python3 cli/find-unused-files.py --report post-change-unused.txt
```

### Emergency Recovery
```bash
# 1. List available backups
python3 cli/backup-restore.py list

# 2. Check backup integrity
python3 cli/backup-restore.py info BACKUP_ID

# 3. Restore
python3 cli/backup-restore.py restore BACKUP_ID

# 4. Verify restoration
python3 cli/health-check.py --verbose
```

---

## Script Reference Summary

| Script | Purpose | Common Usage |
|--------|---------|--------------|
| `health-check.py` | Validate project structure | `python3 cli/health-check.py` |
| `validate-tags.py` | Validate tag.json files | `python3 cli/validate-tags.py --fix` |
| `find-unused-files.py` | Find unused files | `python3 cli/find-unused-files.py --report unused.txt` |
| `project-stats.py` | Generate statistics | `python3 cli/project-stats.py --chart` |
| `backup-restore.py` | Backup/restore project | `python3 cli/backup-restore.py backup --compress` |

---

## Related Documentation

- **Main README:** `/README.md`
- **Architecture:** `/docs/ISA-95-COMPLETE-HIERARCHY.md`
- **Equipment:** `/os/equipment/README.md`
- **Boot System:** `/os/boot/README.md`

---

**Version:** 2.0
**Last Updated:** 2025-11-17
**Maintained By:** Chazon Development Team
