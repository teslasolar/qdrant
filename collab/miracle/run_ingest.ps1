# Helper: run_ingest.ps1
# Sets environment variables and runs the ingestion script for Qdrant Cloud.

param(
  [Parameter(Mandatory=$false)]
  [string]$QdrantUrl = $env:QDRANT_URL,

  [Parameter(Mandatory=$false)]
  [string]$QdrantApiKey = $env:QDRANT_API_KEY
)

if (-not $QdrantUrl) {
  Write-Host "Provide Qdrant URL via -QdrantUrl or set QDRANT_URL env var" -ForegroundColor Yellow
  exit 1
}

Set-Location -Path (Join-Path $PSScriptRoot '.')

$env:QDRANT_URL = $QdrantUrl
if ($QdrantApiKey) { $env:QDRANT_API_KEY = $QdrantApiKey }

Write-Host "Using QDRANT_URL=$env:QDRANT_URL" -ForegroundColor Green
if ($env:QDRANT_API_KEY) { Write-Host "Using QDRANT_API_KEY=***" -ForegroundColor Green }

python .\ingest_medical_data.py

if ($LASTEXITCODE -ne 0) {
  Write-Host "Ingestion failed (exit code $LASTEXITCODE)" -ForegroundColor Red
  exit $LASTEXITCODE
}

Write-Host "Ingestion finished" -ForegroundColor Green
