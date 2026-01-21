# TraceFinder API Documentation

## Overview

TraceFinder provides a RESTful API for forensic scanner identification. This document describes all available endpoints, request/response formats, and usage examples.

## Base URL

```
http://localhost:5000
```

For production, replace with your deployed URL.

## Endpoints

### 1. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /health`

**Response:**
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "timestamp": "2026-01-21T12:00:00.000000"
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

---

### 2. Upload and Analyze Document

Upload a scanned document for forensic analysis.

**Endpoint:** `POST /upload`

**Content-Type:** `multipart/form-data`

**Parameters:**
- `file` (required): The scanned document file
  - Supported formats: JPG, JPEG, PNG, TIFF, TIF, PDF
  - Maximum size: 16 MB

**Success Response (200):**
```json
{
    "success": true,
    "results": {
        "success": true,
        "scanner_brand": "Canon",
        "scanner_model": "CanoScan LiDE",
        "confidence": 0.87,
        "confidence_level": "High",
        "analysis_date": "2026-01-21T12:00:00.000000",
        "features_summary": {
            "PRNU Characteristics": "STD: 0.0234, Pattern Strength: 1.2345",
            "Texture Quality": "Energy: 0.0876, Homogeneity: 0.7654",
            "Frequency Analysis": "Low/High Ratio: 3.45",
            "Noise Level": "SNR: 25.34 dB",
            "Image Entropy": "7.23 bits"
        },
        "metadata": {
            "exif_data": {
                "Make": "Canon",
                "Model": "CanoScan LiDE 220"
            },
            "file_info": {
                "size": 1234567,
                "created": "2026-01-20T10:30:00",
                "modified": "2026-01-20T10:30:00"
            }
        },
        "detailed_analysis": {
            "primary_indicators": [
                "PRNU pattern matches Canon signature",
                "Texture characteristics consistent with Canon scanners",
                "Frequency domain analysis indicates Canon sensor type"
            ],
            "secondary_indicators": [
                "Noise profile: 0.0145",
                "Wavelet energy distribution consistent with flatbed scanner",
                "No signs of digital manipulation detected"
            ],
            "anomalies": [
                "No anomalies detected"
            ]
        }
    },
    "filename": "document.jpg",
    "timestamp": "20260121_120000"
}
```

**Error Response (400):**
```json
{
    "error": "No file provided"
}
```

**Error Response (400):**
```json
{
    "error": "Invalid file type. Allowed: PNG, JPG, TIFF, PDF"
}
```

**Error Response (500):**
```json
{
    "error": "Analysis failed: [error message]"
}
```

**Example (curl):**
```bash
curl -X POST \
  http://localhost:5000/upload \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/document.jpg'
```

**Example (Python):**
```python
import requests

url = 'http://localhost:5000/upload'
files = {'file': open('document.jpg', 'rb')}
response = requests.post(url, files=files)
result = response.json()

if result['success']:
    print(f"Scanner: {result['results']['scanner_brand']}")
    print(f"Confidence: {result['results']['confidence']:.2%}")
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Scanner:', data.results.scanner_brand);
        console.log('Confidence:', data.results.confidence);
    }
});
```

---

### 3. Detailed Analysis

Perform comprehensive forensic analysis on an already uploaded image.

**Endpoint:** `POST /analyze`

**Content-Type:** `application/json`

**Request Body:**
```json
{
    "image_path": "/path/to/image.jpg"
}
```

**Success Response (200):**
```json
{
    "success": true,
    "analysis": {
        "success": true,
        "scanner_brand": "Epson",
        "scanner_model": "Perfection V",
        "confidence": 0.82,
        "confidence_level": "High",
        "analysis_date": "2026-01-21T12:00:00.000000",
        "advanced_analysis": {
            "noise_pattern_analysis": {
                "pattern_type": "Gaussian",
                "uniformity": 0.85,
                "spatial_correlation": 0.23
            },
            "periodic_artifact_detection": {
                "periodic_artifacts_detected": false,
                "artifact_strength": 1.23
            },
            "compression_artifacts": {
                "compression_detected": false,
                "quality_estimate": "High",
                "blocking_artifacts": "None detected"
            },
            "color_interpolation": {
                "interpolation_method": "Linear",
                "cfa_pattern": "Not applicable (grayscale analysis)",
                "artifacts": "None"
            },
            "forensic_markers": {
                "tampering_detected": false,
                "authenticity_score": 0.95,
                "markers": [
                    "Original scan",
                    "No splicing detected",
                    "Consistent noise pattern"
                ]
            }
        }
    }
}
```

**Example:**
```bash
curl -X POST \
  http://localhost:5000/analyze \
  -H 'Content-Type: application/json' \
  -d '{"image_path": "/path/to/image.jpg"}'
```

---

### 4. Generate PDF Report

Generate a PDF report of analysis results.

**Endpoint:** `POST /generate_report`

**Content-Type:** `application/json`

**Request Body:**
```json
{
    "results": {
        "scanner_brand": "Canon",
        "scanner_model": "CanoScan LiDE",
        "confidence": 0.87,
        "features_summary": {...},
        "detailed_analysis": {...}
    }
}
```

**Success Response (200):**
- Content-Type: `application/pdf`
- Binary PDF data
- Filename: `tracefinder_report.pdf`

**Error Response (500):**
```json
{
    "error": "Report generation failed: [error message]"
}
```

**Example:**
```bash
curl -X POST \
  http://localhost:5000/generate_report \
  -H 'Content-Type: application/json' \
  -d @results.json \
  -o report.pdf
```

---

## Data Models

### AnalysisResult

```typescript
interface AnalysisResult {
    success: boolean;
    scanner_brand: string;
    scanner_model: string;
    confidence: number;  // 0.0 to 1.0
    confidence_level: string;  // "Very Low" | "Low" | "Medium" | "High" | "Very High"
    analysis_date: string;  // ISO 8601 format
    features_summary: FeaturesSummary;
    metadata: Metadata;
    detailed_analysis: DetailedAnalysis;
}
```

### FeaturesSummary

```typescript
interface FeaturesSummary {
    "PRNU Characteristics": string;
    "Texture Quality": string;
    "Frequency Analysis": string;
    "Noise Level": string;
    "Image Entropy": string;
}
```

### Metadata

```typescript
interface Metadata {
    exif_data: Record<string, string>;
    file_info: {
        size: number;
        created: string;
        modified: string;
    };
}
```

### DetailedAnalysis

```typescript
interface DetailedAnalysis {
    primary_indicators: string[];
    secondary_indicators: string[];
    anomalies: string[];
}
```

---

## Error Handling

All endpoints follow a consistent error response format:

```json
{
    "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid input or missing required parameters
- `404 Not Found`: Endpoint not found
- `500 Internal Server Error`: Server-side error during processing

---

## Rate Limiting

Currently, there are no rate limits. For production use, implement rate limiting based on your requirements.

---

## Authentication

The current version does not require authentication. For production deployment, implement appropriate authentication mechanisms:

- API Keys
- OAuth 2.0
- JWT tokens

---

## CORS

Cross-Origin Resource Sharing (CORS) is not enabled by default. To enable CORS for frontend applications:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

---

## Best Practices

### 1. File Size Optimization

Compress images before uploading to reduce processing time:
- Use JPEG with quality 85-95
- Resize to maximum 2000x2000 pixels if larger

### 2. Error Handling

Always check the `success` field in responses:

```python
response = requests.post(url, files=files)
data = response.json()

if data.get('success'):
    # Process results
    results = data['results']
else:
    # Handle error
    error = data.get('error', 'Unknown error')
    print(f"Error: {error}")
```

### 3. Timeout Configuration

Set appropriate timeouts for long-running analyses:

```python
response = requests.post(url, files=files, timeout=30)
```

---

## SDK Examples

### Python SDK

```python
class TraceFinderClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
    
    def health_check(self):
        response = requests.get(f'{self.base_url}/health')
        return response.json()
    
    def analyze_document(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f'{self.base_url}/upload',
                files=files,
                timeout=30
            )
        return response.json()
    
    def generate_report(self, results, output_path='report.pdf'):
        response = requests.post(
            f'{self.base_url}/generate_report',
            json={'results': results}
        )
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        return False

# Usage
client = TraceFinderClient()
result = client.analyze_document('scan.jpg')
if result['success']:
    print(f"Scanner: {result['results']['scanner_brand']}")
    client.generate_report(result['results'])
```

### JavaScript/Node.js SDK

```javascript
class TraceFinderClient {
    constructor(baseURL = 'http://localhost:5000') {
        this.baseURL = baseURL;
    }
    
    async healthCheck() {
        const response = await fetch(`${this.baseURL}/health`);
        return await response.json();
    }
    
    async analyzeDocument(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${this.baseURL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        return await response.json();
    }
    
    async generateReport(results) {
        const response = await fetch(`${this.baseURL}/generate_report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ results })
        });
        
        return await response.blob();
    }
}

// Usage
const client = new TraceFinderClient();
const result = await client.analyzeDocument(fileInput.files[0]);
if (result.success) {
    console.log('Scanner:', result.results.scanner_brand);
    const reportBlob = await client.generateReport(result.results);
    // Download or display report
}
```

---

## Webhooks

*Coming in future version*

Webhooks will allow you to receive notifications when analysis is complete for asynchronous processing.

---

## Support

For API questions or issues:
- GitHub Issues: [Project Issues](https://github.com/AI-TraceFinder/Rahul_Mahato-TraceFinder/issues)
- Email: [Contact Developer]

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for API version history and breaking changes.

---

**Version:** 1.0.0  
**Last Updated:** January 21, 2026
