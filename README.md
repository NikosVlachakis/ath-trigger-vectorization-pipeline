# Trigger Vectorization Pipeline

## 🎯 Overview
Command-line tool that initiates the vectorization pipeline by sending requests to the vectorization service.

## 🏗️ Features
- **Dataset Processing** - Supports local files and URLs
- **Pipeline Initiation** - Triggers vectorization and orchestration
- **Centralized Logging** - All activities logged with clear identification
- **Simplified Interface** - Clean command-line interface (no more orchestratorUrl parameter!)

## 🚀 Quick Start

### Basic Usage
```powershell
python trigger_vectorization.py \
  --vectorizationServiceUrl http://localhost:5001 \
  --url ..\vectorization-service\metadata-test.json \
  --jobId test_job_123 \
  --clientsList client1 \
  --studyId study_12345
```

### Parameters
- `--vectorizationServiceUrl` - Vectorization service endpoint
- `--url` - Dataset path (local file or URL) *(required in development mode)*
- `--jobId` - Unique identifier for the job
- `--clientsList` - List of client identifiers (e.g., client1 client2 client3)
- `--studyId` - Study identifier *(required, used for Feature Extraction Tool API in production mode)*

**✅ New Features**:
- **Feature Extraction Tool Integration** - Production mode API support via `studyId`
- **API Endpoint**: `https://localhost/dt4h/feast/api/Dataset?featureSetId={studyId}`
- **Development/Production Modes** - Configurable via `PRODUCTION_MODE` environment variable

**✅ Architecture Improvements**:
- `orchestratorUrl` is now configured via environment variable (cleaner API!)
- `totalClients` replaced with `clientsList` (more explicit, prevents mismatches)

## 📊 Example Datasets
- `../vectorization-service/metadata-test.json` - Employee dataset (1000 records)
- URL-based datasets supported
- Local file paths supported

## 🧪 Testing

### Centralized Logging Tests
```powershell
cd tests
python test_centralized_logging.py
```
**Expected**: 10/10 tests pass ✅

**Test Coverage:**
- Log directory creation and permissions
- Logging configuration validation
- Script execution logging (parameters, HTTP requests)
- Response handling logging (status codes, response bodies)
- Error handling and logging (connection failures, validation errors)
- Log format validation (timestamps, service identification)
- Log persistence verification
- Integration testing with other services

### Example Test Scenarios
```powershell
# Test with valid dataset (Development Mode)
python trigger_vectorization.py \
  --vectorizationServiceUrl http://localhost:5001 \
  --url ../vectorization-service/metadata-test.json \
  --jobId test_valid \
  --clientsList client1 \
  --studyId study_dev_123

# Test error handling
python trigger_vectorization.py \
  --vectorizationServiceUrl http://invalid:9999 \
  --url nonexistent.json \
  --jobId test_error \
  --clientsList client1 \
  --studyId study_error_123

# Test Production Mode (requires PRODUCTION_MODE=true in vectorization-service)
python trigger_vectorization.py \
  --vectorizationServiceUrl http://localhost:5001 \
  --studyId study_prod_123 \
  --jobId test_production \
  --clientsList client1
```

## 📄 Centralized Logging

### Log Location
**File**: `../logs/trigger-vectorization-pipeline.log` (when running as container)
**Console**: Standard output for local execution

### What Gets Logged
- ✅ Script startup with parameters
- ✅ HTTP request preparation and execution
- ✅ Response handling (status codes, response bodies)
- ✅ Success/failure outcomes
- ✅ Error conditions with full context
- ✅ Parameter validation and processing

### Sample Log Output
```
2025-07-30 17:30:25,123 INFO [trigger-vectorization-pipeline] === TRIGGER-VECTORIZATION-PIPELINE SERVICE STARTED ===
2025-07-30 17:30:26,456 INFO [trigger-vectorization-pipeline] ACTION: Starting Vectorization Pipeline Trigger
2025-07-30 17:30:27,789 INFO [trigger-vectorization-pipeline] Sending POST to http://localhost:5001/vectorize
2025-07-30 17:30:28,012 INFO [trigger-vectorization-pipeline] Response code: 200
2025-07-30 17:30:29,345 INFO [trigger-vectorization-pipeline] Vectorization trigger request succeeded
```

## 🔧 Configuration

### Dependencies
- Python 3.9+
- `requests` library
- Access to vectorization service

### Error Handling
- ✅ Connection failures logged and reported
- ✅ Invalid parameters validated
- ✅ HTTP errors properly handled
- ✅ File not found errors managed

### Environment
- **Local execution**: Standard logging to console
- **Container execution**: Centralized logging to host files

---
✅ **Simple, reliable pipeline trigger with comprehensive logging**