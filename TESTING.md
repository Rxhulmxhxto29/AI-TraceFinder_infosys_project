# Testing Guide for TraceFinder

## Overview

This guide provides comprehensive testing instructions for the TraceFinder Forensic Scanner Identification System.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Unit Testing](#unit-testing)
3. [Integration Testing](#integration-testing)
4. [Manual Testing](#manual-testing)
5. [Performance Testing](#performance-testing)
6. [Test Data](#test-data)

## Prerequisites

Install testing dependencies:

```bash
pip install pytest pytest-cov pytest-flask selenium
```

## Unit Testing

### Testing Image Processor

```python
# tests/test_image_processor.py
import pytest
from modules.image_processor import ImageProcessor
import numpy as np

def test_image_loading():
    processor = ImageProcessor()
    # Test with sample image
    result = processor.load_and_preprocess('test_images/sample.jpg')
    assert result is not None
    assert 'original' in result
    assert 'grayscale' in result

def test_noise_filter():
    processor = ImageProcessor()
    test_image = np.random.rand(100, 100).astype(np.float32)
    noise = processor.apply_noise_filter(test_image)
    assert noise.shape == test_image.shape
```

### Testing Feature Extractor

```python
# tests/test_feature_extractor.py
from modules.feature_extractor import FeatureExtractor
import numpy as np

def test_feature_extraction():
    extractor = FeatureExtractor()
    test_data = {
        'normalized': np.random.rand(512, 512).astype(np.float32),
        'resized': (np.random.rand(512, 512) * 255).astype(np.uint8)
    }
    features = extractor.extract_all_features(test_data)
    
    assert 'prnu' in features
    assert 'texture' in features
    assert 'frequency' in features
    assert 'wavelet' in features
```

### Testing Scanner Detector

```python
# tests/test_scanner_detector.py
from modules.scanner_detector import ScannerDetector

def test_scanner_detection():
    detector = ScannerDetector()
    result = detector.analyze('test_images/sample_scan.jpg')
    
    assert 'success' in result
    if result['success']:
        assert 'scanner_brand' in result
        assert 'confidence' in result
        assert 0 <= result['confidence'] <= 1
```

## Integration Testing

### Testing Flask Application

```python
# tests/test_app.py
import pytest
from app import app
import io

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'TraceFinder' in response.data

def test_file_upload(client):
    data = {
        'file': (io.BytesIO(b'fake image data'), 'test.jpg')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code in [200, 400]

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'
```

## Manual Testing

### Test Cases

#### TC001: Upload Valid Image
**Steps:**
1. Navigate to http://localhost:5000
2. Click "Choose File"
3. Select a valid JPEG image
4. Click "Analyze Document"

**Expected Result:**
- Loading screen appears
- Analysis completes successfully
- Results display scanner brand, model, and confidence score

#### TC002: Upload Invalid File
**Steps:**
1. Navigate to http://localhost:5000
2. Try to upload a .txt or .doc file

**Expected Result:**
- Error message: "Invalid file type"
- Upload is rejected

#### TC003: Upload Oversized File
**Steps:**
1. Try to upload a file larger than 16MB

**Expected Result:**
- Error message about file size limit
- Upload is rejected

#### TC004: Generate PDF Report
**Steps:**
1. Complete a successful analysis
2. Click "Generate PDF Report"

**Expected Result:**
- PDF file downloads automatically
- PDF contains analysis results
- PDF is properly formatted

#### TC005: Export JSON
**Steps:**
1. Complete a successful analysis
2. Click "Export JSON"

**Expected Result:**
- JSON file downloads
- JSON contains all analysis data
- JSON is valid and parseable

#### TC006: Multiple File Formats
**Steps:**
1. Test with JPG image
2. Test with PNG image
3. Test with TIFF image

**Expected Result:**
- All formats process successfully
- Results are consistent

## Performance Testing

### Load Testing

```python
# tests/performance_test.py
import time
from modules.scanner_detector import ScannerDetector

def test_analysis_speed():
    detector = ScannerDetector()
    
    start_time = time.time()
    result = detector.analyze('test_images/sample.jpg')
    end_time = time.time()
    
    analysis_time = end_time - start_time
    print(f"Analysis time: {analysis_time:.2f} seconds")
    
    # Analysis should complete in reasonable time
    assert analysis_time < 10.0  # 10 seconds max
```

### Memory Testing

```python
import psutil
import os

def test_memory_usage():
    process = psutil.Process(os.getpid())
    
    # Measure memory before
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Run analysis
    detector = ScannerDetector()
    detector.analyze('test_images/sample.jpg')
    
    # Measure memory after
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    
    memory_increase = mem_after - mem_before
    print(f"Memory increase: {memory_increase:.2f} MB")
    
    # Should not leak excessive memory
    assert memory_increase < 500  # 500 MB max increase
```

## Test Data

### Creating Test Images

```python
# Create synthetic test images
import cv2
import numpy as np

# Generate test image with known characteristics
def create_test_image():
    # Create base image
    image = np.random.rand(1000, 1000, 3) * 255
    image = image.astype(np.uint8)
    
    # Add scanner-like artifacts
    # Add periodic pattern
    for i in range(0, 1000, 10):
        image[i, :] = image[i, :] * 0.98
    
    # Save
    cv2.imwrite('test_images/synthetic_scan.jpg', image)
```

### Test Image Requirements

For comprehensive testing, collect:
1. **Real scanner samples** from different brands
   - Canon scans (3-5 samples)
   - Epson scans (3-5 samples)
   - HP scans (3-5 samples)
   - Brother scans (3-5 samples)
   - Fujitsu scans (3-5 samples)

2. **Different resolutions**
   - Low: 300 DPI
   - Medium: 600 DPI
   - High: 1200 DPI

3. **Different content types**
   - Text documents
   - Photos
   - Mixed content
   - Color and grayscale

4. **Edge cases**
   - Very dark images
   - Very bright images
   - Low contrast images
   - Compressed images

## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run with coverage:
```bash
pytest --cov=modules tests/
```

### Run specific test file:
```bash
pytest tests/test_image_processor.py
```

### Run with verbose output:
```bash
pytest -v tests/
```

## Continuous Integration

For CI/CD integration (GitHub Actions example):

```yaml
# .github/workflows/test.yml
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
      run: pytest --cov=modules tests/
```

## Troubleshooting Tests

### Common Issues

1. **Import errors**: Ensure virtual environment is activated
2. **Missing test images**: Create test_images directory with samples
3. **Memory errors**: Reduce test image sizes
4. **Timeout errors**: Increase timeout limits for slow systems

## Test Metrics

Target metrics:
- **Code Coverage**: > 80%
- **Test Pass Rate**: 100%
- **Analysis Speed**: < 10 seconds per image
- **Memory Usage**: < 500 MB increase per analysis
- **Accuracy**: > 75% confidence on known samples

## Reporting Issues

When reporting test failures, include:
1. Test case identifier
2. Steps to reproduce
3. Expected vs actual results
4. System information
5. Log files
6. Sample data (if not sensitive)

---

**Happy Testing! 🧪**
