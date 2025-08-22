# Trigger Vectorization Pipeline

## 🎯 Overview
Command-line tool that initiates the vectorization pipeline by sending requests to the vectorization service.

## 🏗️ Features
- **Pipeline Initiation** - Triggers vectorization and orchestration

- **Simplified Interface** - Clean command-line interface

## 🚀 Quick Start

### Basic Usage
```powershell
python trigger_vectorization.py \
  --vectorizationServiceUrl http://localhost:5001 \
  --url ..\vectorization-service\metadata-test.json \
  --jobId test_job_123 \
  --clientsList '["client1"]' \
  --studyId study_12345
```

### Parameters
- `--vectorizationServiceUrl` - Vectorization service endpoint
- `--url` - Dataset path (local file or URL)
- `--jobId` - Unique identifier for the job
- `--clientsList` - List of client identifiers as JSON array (e.g., '["client1", "client2", "client3"]') - REQUIRED JSON FORMAT
- `--studyId` - Study identifier *(required, used for Feature Extraction Tool API)*