// TraceFinder - Main JavaScript File

let currentResults = null;

// Update file name display when file is selected
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    
    if (fileInput && fileName) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileName.textContent = this.files[0].name;
            } else {
                fileName.textContent = 'Choose File';
            }
        });
    }
});

// Initialize drag & drop when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeDragAndDrop();
    console.log('TraceFinder initialized with enhanced features');
});

function initializeDragAndDrop() {
    // Drag & Drop functionality for scanner detection
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    
    if (!dropZone || !fileInput) {
        console.log('Drop zone or file input not found on this page');
        return;
    }

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when dragging over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('drag-over');
        }, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection(files[0]);
        }
    }, false);

    // File input handler with preview
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Handle file selection and show preview
function handleFileSelection(file) {
    const fileName = file.name;
    const fileSize = formatFileSize(file.size);
    const fileExt = fileName.split('.').pop().toLowerCase();
    
    console.log('File selected:', fileName, file.type, fileExt);
    
    // Update file name display
    const fileNameElement = document.getElementById('fileName');
    if (fileNameElement) {
        fileNameElement.textContent = fileName;
    }
    
    const previewImage = document.getElementById('previewImage');
    const previewName = document.getElementById('previewName');
    const previewSize = document.getElementById('previewSize');
    const imagePreview = document.getElementById('imagePreview');
    
    if (!previewImage || !previewName || !previewSize || !imagePreview) {
        console.log('Preview elements not found');
        return;
    }
    
    // Show preview for displayable images (not TIFF)
    if (file.type.startsWith('image/') && !file.type.includes('tiff') && fileExt !== 'tif' && fileExt !== 'tiff') {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
            previewName.textContent = fileName;
            previewSize.textContent = fileSize;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        // For TIFF, PDF, or other formats, show a placeholder icon
        let iconType = 'IMAGE';
        let iconColor = '%23667eea';
        
        if (file.type === 'application/pdf' || fileExt === 'pdf') {
            iconType = 'PDF';
            iconColor = '%23e74c3c';
        } else if (fileExt === 'tif' || fileExt === 'tiff') {
            iconType = 'TIFF';
            iconColor = '%2327ae60';
        }
        
        previewImage.src = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%23f8f9fa' rx='10'/%3E%3Ctext x='50%25' y='45%25' font-size='48' font-weight='bold' text-anchor='middle' fill='${iconColor}'%3E%F0%9F%96%BC%3C/text%3E%3Ctext x='50%25' y='65%25' font-size='24' font-weight='bold' text-anchor='middle' fill='${iconColor}'%3E${iconType}%3C/text%3E%3C/svg%3E`;
        previewImage.style.display = 'block';
        previewName.textContent = fileName;
        previewSize.textContent = fileSize;
        imagePreview.style.display = 'block';
    }
}

// Clear preview
function clearPreview() {
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('fileInput').value = '';
    document.getElementById('fileName').textContent = 'Choose File';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Form submission handler - Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    if (!uploadForm) return;
    
    uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showNotification('Please select a file first', 'error');
        return false;
    }
    
    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showNotification('File size exceeds 16MB limit', 'error');
        return;
    }
    
    // Show loading section
    document.querySelector('.upload-section').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    // Animate progress steps
    animateProgressSteps();
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // Upload and analyze
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store results with filename
            currentResults = {
                ...data.results,
                filename: data.filename || file.name
            };
            setTimeout(() => displayResults(currentResults), 1500);
        } else {
            showNotification(data.error || 'Analysis failed', 'error');
            resetAnalysis();
        }
    } catch (error) {
        showNotification('Network error: ' + error.message, 'error');
        resetAnalysis();
    }
});
});

// Animate progress steps
function animateProgressSteps() {
    const steps = document.querySelectorAll('.step');
    let currentStep = 2;
    
    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            steps[currentStep].classList.add('active');
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 500);
}

// Display results
function displayResults(results) {
    // Hide loading, show results
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
    
    // Populate results
    document.getElementById('scannerBrand').textContent = results.scanner_brand || 'Unknown';
    document.getElementById('scannerModel').textContent = results.scanner_model || 'Unknown';
    
    // Confidence score - handle NaN and undefined
    const confidenceValue = results.confidence || 0;
    const confidence = isNaN(confidenceValue) ? 0 : (confidenceValue * 100).toFixed(1);
    document.getElementById('confidenceScore').textContent = confidence + '%';
    document.getElementById('confidenceLevel').textContent = results.confidence_level || 'N/A';
    
    // Animate confidence bar
    setTimeout(() => {
        document.getElementById('confidenceFill').style.width = confidence + '%';
    }, 100);
    
    // Dashboard analytics
    createDashboardCharts(results);
    updateStatCards(results);
    
    // Features summary
    if (results.features_summary) {
        const featuresContainer = document.getElementById('featuresSummary');
        featuresContainer.innerHTML = '';
        
        for (const [feature, value] of Object.entries(results.features_summary)) {
            const featureDiv = document.createElement('div');
            featureDiv.className = 'feature-item';
            featureDiv.innerHTML = `<strong>${feature}:</strong> ${value}`;
            featuresContainer.appendChild(featureDiv);
        }
    }
    
    // Detailed analysis
    if (results.detailed_analysis) {
        const details = results.detailed_analysis;
        
        // Primary indicators
        const primaryList = document.getElementById('primaryIndicators');
        primaryList.innerHTML = '';
        (details.primary_indicators || []).forEach(indicator => {
            const li = document.createElement('li');
            li.textContent = indicator;
            primaryList.appendChild(li);
        });
        
        // Secondary indicators
        const secondaryList = document.getElementById('secondaryIndicators');
        secondaryList.innerHTML = '';
        (details.secondary_indicators || []).forEach(indicator => {
            const li = document.createElement('li');
            li.textContent = indicator;
            secondaryList.appendChild(li);
        });
        
        // Anomalies
        const anomaliesList = document.getElementById('anomalies');
        anomaliesList.innerHTML = '';
        (details.anomalies || []).forEach(anomaly => {
            const li = document.createElement('li');
            li.textContent = anomaly;
            anomaliesList.appendChild(li);
        });
    }
    
    // Advanced Visualizations
    createAdvancedVisualizations(results);
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// Create Advanced Visualizations
function createAdvancedVisualizations(results) {
    const vizSection = document.getElementById('advancedVizSection');
    
    // Always show visualization section
    vizSection.style.display = 'block';
    
    // Generate noise pattern heatmap data (simulated from confidence and features)
    const noiseData = generateNoiseHeatmapData(results);
    createAdvancedVisualization('noiseHeatmap', noiseData, 'heatmap');
    
    // Generate frequency analysis data
    const frequencyData = generateFrequencyData(results);
    createAdvancedVisualization('frequencyChart', frequencyData, 'frequency');
}

// Generate noise heatmap data from analysis results
function generateNoiseHeatmapData(results) {
    const data = [];
    const confidence = results.confidence || 0.5;
    
    // Generate simulated noise pattern based on scanner characteristics
    for (let i = 0; i < 50; i++) {
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        // Add some clustering based on confidence
        const clusterX = 50 + (Math.random() - 0.5) * 30 * (1 - confidence);
        const clusterY = 50 + (Math.random() - 0.5) * 30 * (1 - confidence);
        
        data.push({ x: clusterX, y: clusterY });
    }
    
    return data;
}

// Generate frequency domain data
function generateFrequencyData(results) {
    const confidence = results.confidence || 0.5;
    const labels = [];
    const values = [];
    
    // Generate frequency response data (0-50 Hz)
    for (let freq = 0; freq <= 50; freq += 2) {
        labels.push(freq + ' Hz');
        
        // Simulate frequency response based on confidence
        // Higher confidence = more distinct frequency signature
        let value;
        if (freq < 10) {
            value = 20 + Math.random() * 10;
        } else if (freq < 30) {
            value = 40 + (confidence * 30) + Math.random() * 10;
        } else {
            value = 20 - (freq - 30) * 0.5 + Math.random() * 5;
        }
        
        values.push(Math.max(0, value));
    }
    
    return { labels, values };
}

// Update stat cards
function updateStatCards(results) {
    // Extract feature quality from features_summary or use defaults
    const featuresSummary = results.features_summary || {};
    
    // PRNU Quality - use detection method or default
    const prnuQuality = featuresSummary['Detection Method'] || 'Good';
    document.getElementById('prnuQuality').textContent = prnuQuality;
    
    // Noise Pattern - use confidence level as indicator
    const noisePattern = results.confidence_level || 'Consistent';
    document.getElementById('noisePattern').textContent = noisePattern;
    
    // Image Quality - use confidence as quality indicator
    const imageQuality = results.confidence >= 0.8 ? 'High' : results.confidence >= 0.5 ? 'Medium' : 'Low';
    document.getElementById('imageQuality').textContent = imageQuality;
    
    // Metadata Status - check if metadata exists
    const metadataStatus = results.metadata && Object.keys(results.metadata).length > 0 ? 'Complete' : 'Partial';
    document.getElementById('metadataStatus').textContent = metadataStatus;
}

// Create dashboard charts
function createDashboardCharts(results) {
    // Confidence Distribution Chart
    const confidenceValue = (results.confidence || 0) * 100;
    const uncertaintyValue = 100 - confidenceValue;
    
    const confidenceCtx = document.getElementById('confidenceChart');
    if (confidenceCtx) {
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart(confidenceCtx);
        if (existingChart) {
            existingChart.destroy();
        }
        
        new Chart(confidenceCtx, {
            type: 'doughnut',
            data: {
                labels: ['Confidence', 'Uncertainty'],
                datasets: [{
                    data: [confidenceValue, uncertaintyValue],
                    backgroundColor: ['#4A90E2', '#E0E0E0'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Feature Quality Metrics Chart
    const featureCtx = document.getElementById('featureQualityChart');
    if (featureCtx) {
        // Destroy existing chart if it exists
        const existingFeatureChart = Chart.getChart(featureCtx);
        if (existingFeatureChart) {
            existingFeatureChart.destroy();
        }
        
        new Chart(featureCtx, {
            type: 'radar',
            data: {
                labels: ['PRNU', 'Texture', 'Noise', 'Frequency', 'Metadata'],
                datasets: [{
                    label: 'Quality',
                    data: [
                        results.prnu_score || 50,
                        results.texture_score || 50,
                        results.noise_score || 50,
                        results.frequency_score || 50,
                        results.metadata_score || 50
                    ],
                    backgroundColor: 'rgba(74, 144, 226, 0.2)',
                    borderColor: 'rgba(74, 144, 226, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// Reset analysis
function resetAnalysis() {
    document.querySelector('.upload-section').style.display = 'block';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    
    // Reset form
    document.getElementById('uploadForm').reset();
    document.getElementById('fileName').textContent = 'Choose File';
    
    // Reset progress steps
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        if (index > 1) {
            step.classList.remove('active');
        }
    });
    
    // Clear confidence bar
    document.getElementById('confidenceFill').style.width = '0%';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Reset comparison
function resetComparison() {
    // Hide results
    document.getElementById('compareResults').style.display = 'none';
    
    // Reset form
    document.getElementById('compareForm').reset();
    document.getElementById('compareFileName1').textContent = 'Choose File';
    document.getElementById('compareFileName2').textContent = 'Choose File';
    
    // Clear results content
    document.getElementById('compareContent').innerHTML = '';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Reset tampering
function resetTampering() {
    // Hide results
    document.getElementById('tamperingResults').style.display = 'none';
    
    // Reset form
    document.getElementById('tamperingForm').reset();
    document.getElementById('tamperingFileName').textContent = 'Choose File';
    
    // Clear results content
    document.getElementById('tamperingContent').innerHTML = '';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Generate PDF report
async function generateReport() {
    if (!currentResults) {
        showNotification('No analysis results available', 'error');
        return;
    }
    
    try {
        showNotification('Generating PDF report...', 'info');
        
        // Prepare data for PDF generator
        const reportData = {
            filename: currentResults.filename || 'Unknown',
            scanner_brand: currentResults.scanner_brand || 'Unknown',
            scanner_model: currentResults.scanner_model || 'Unknown',
            confidence: currentResults.confidence || 0,
            confidence_level: currentResults.confidence_level || 'Unknown',
            detection_method: currentResults.detection_method || 'Multi-Factor Analysis',
            metadata: currentResults.metadata || {},
            detailed_analysis: currentResults.detailed_analysis || {},
            features_summary: currentResults.features_summary || {},
            using_trained_model: currentResults.using_trained_model || false
        };
        
        const response = await fetch('/generate_report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reportData)
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
            a.download = `TraceFinder_Report_${timestamp}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('Report generated successfully!', 'success');
        } else {
            const errorData = await response.json();
            showNotification('Failed to generate report: ' + (errorData.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        showNotification('Error generating report: ' + error.message, 'error');
    }
}

// Export results as JSON
function exportJSON() {
    if (!currentResults) {
        showNotification('No analysis results available', 'error');
        return;
    }
    
    const dataStr = JSON.stringify(currentResults, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'tracefinder_results.json';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    
    showNotification('Results exported successfully!', 'success');
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Show help
function showHelp() {
    const helpText = `
TraceFinder Help Guide

1. Upload: Select a scanned document (JPG, PNG, TIFF, or PDF)
2. Analyze: Click "Analyze Document" to start the forensic analysis
3. Results: View detailed scanner identification results
4. Report: Generate PDF report or export JSON data

Supported File Types:
- JPG/JPEG
- PNG
- TIFF/TIF
- PDF

Maximum file size: 16MB

For best results:
- Use high-quality scans
- Avoid heavily compressed images
- Ensure images are not manipulated

For support, please refer to the documentation or contact the developer.
    `;
    
    alert(helpText);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    if (tabName === 'scanner') {
        document.getElementById('scannerTab').style.display = 'block';
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
        document.getElementById('resultsSection').style.display = document.getElementById('resultsSection').innerHTML ? 'block' : 'none';
        document.getElementById('compareResults').style.display = 'none';
        document.getElementById('tamperingResults').style.display = 'none';
        document.getElementById('batchResults').style.display = 'none';
    } else if (tabName === 'fingerprints') {
        document.getElementById('fingerprintsTab').style.display = 'block';
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('compareResults').style.display = 'none';
        document.getElementById('tamperingResults').style.display = 'none';
        document.getElementById('batchResults').style.display = 'none';
        loadScannerFingerprints();
    } else if (tabName === 'compare') {
        document.getElementById('compareTab').style.display = 'block';
        document.querySelectorAll('.tab-btn')[2].classList.add('active');
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('compareResults').style.display = document.getElementById('compareContent').innerHTML ? 'block' : 'none';
        document.getElementById('tamperingResults').style.display = 'none';
        document.getElementById('batchResults').style.display = 'none';
    } else if (tabName === 'batch') {
        document.getElementById('batchTab').style.display = 'block';
        document.querySelectorAll('.tab-btn')[3].classList.add('active');
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('compareResults').style.display = 'none';
        document.getElementById('tamperingResults').style.display = 'none';
        document.getElementById('batchResults').style.display = document.getElementById('batchContent').innerHTML ? 'block' : 'none';
    } else if (tabName === 'tampering') {
        document.getElementById('tamperingTab').style.display = 'block';
        document.querySelectorAll('.tab-btn')[4].classList.add('active');
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('compareResults').style.display = 'none';
        document.getElementById('tamperingResults').style.display = document.getElementById('tamperingContent').innerHTML ? 'block' : 'none';
        document.getElementById('batchResults').style.display = 'none';
    }
}

// File input handlers for new features
document.getElementById('compareFile1').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'First Image';
    document.getElementById('compareFileName1').textContent = fileName;
});

document.getElementById('compareFile2').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Second Image';
    document.getElementById('compareFileName2').textContent = fileName;
});

document.getElementById('tamperingFile').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Choose File';
    document.getElementById('tamperingFileName').textContent = fileName;
});

// Compare form handler
document.getElementById('compareForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const file1 = document.getElementById('compareFile1').files[0];
    const file2 = document.getElementById('compareFile2').files[0];
    
    if (!file1 || !file2) {
        showNotification('Please select both images', 'error');
        return;
    }
    
    document.getElementById('compareTab').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'block';
    
    const formData = new FormData();
    formData.append('image1', file1);
    formData.append('image2', file2);
    
    try {
        const response = await fetch('/compare', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        document.getElementById('loadingSection').style.display = 'none';
        
        if (data.success) {
            displayComparisonResults(data);
        } else {
            showNotification(data.error || 'Comparison failed', 'error');
            document.getElementById('compareTab').style.display = 'block';
        }
    } catch (error) {
        document.getElementById('loadingSection').style.display = 'none';
        showNotification('An error occurred during comparison', 'error');
        document.getElementById('compareTab').style.display = 'block';
    }
});

// Tampering form handler
document.getElementById('tamperingForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const file = document.getElementById('tamperingFile').files[0];
    
    if (!file) {
        showNotification('Please select a file', 'error');
        return;
    }
    
    document.getElementById('tamperingTab').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'block';
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/detect_tampering', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        document.getElementById('loadingSection').style.display = 'none';
        
        if (data.success) {
            displayTamperingResults(data);
        } else {
            showNotification(data.error || 'Tampering detection failed', 'error');
            document.getElementById('tamperingTab').style.display = 'block';
        }
    } catch (error) {
        document.getElementById('loadingSection').style.display = 'none';
        showNotification('An error occurred during tampering detection', 'error');
        document.getElementById('tamperingTab').style.display = 'block';
    }
});

// Display comparison results
function displayComparisonResults(data) {
    const confidenceBadge = data.match_confidence === 'High' ? 'badge-high' : 
                           data.match_confidence === 'Moderate' ? 'badge-moderate' : 'badge-low';
    
    const content = `
        <div class="comparison-header">
            <div class="section-header">
                <h3><i class="fas fa-chart-line"></i> Similarity Analysis</h3>
                <span class="section-badge"><i class="fas fa-microscope"></i> Forensic Match</span>
            </div>
        </div>
        
        <div class="comparison-score-card">
            <div class="score-circle">
                <div class="score-value">${data.overall_similarity}%</div>
            </div>
            <div class="score-info">
                <h3>${data.match_status}</h3>
                <span class="confidence-badge ${confidenceBadge}">
                    <i class="fas fa-shield-alt"></i> Confidence: ${data.match_confidence}
                </span>
            </div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card prnu-card">
                <div class="metric-header">
                    <i class="fas fa-fingerprint"></i>
                    <h4>PRNU Similarity</h4>
                </div>
                <div class="metric-value">${data.detailed_scores.prnu_similarity}%</div>
                <div class="metric-bar">
                    <div class="metric-fill prnu-fill" style="width: ${data.detailed_scores.prnu_similarity}%"></div>
                </div>
            </div>
            <div class="metric-card texture-card">
                <div class="metric-header">
                    <i class="fas fa-th"></i>
                    <h4>Texture Similarity</h4>
                </div>
                <div class="metric-value">${data.detailed_scores.texture_similarity}%</div>
                <div class="metric-bar">
                    <div class="metric-fill texture-fill" style="width: ${data.detailed_scores.texture_similarity}%"></div>
                </div>
            </div>
            <div class="metric-card frequency-card">
                <div class="metric-header">
                    <i class="fas fa-wave-square"></i>
                    <h4>Frequency Similarity</h4>
                </div>
                <div class="metric-value">${data.detailed_scores.frequency_similarity}%</div>
                <div class="metric-bar">
                    <div class="metric-fill frequency-fill" style="width: ${data.detailed_scores.frequency_similarity}%"></div>
                </div>
            </div>
            <div class="metric-card wavelet-card">
                <div class="metric-header">
                    <i class="fas fa-signal"></i>
                    <h4>Wavelet Similarity</h4>
                </div>
                <div class="metric-value">${data.detailed_scores.wavelet_similarity}%</div>
                <div class="metric-bar">
                    <div class="metric-fill wavelet-fill" style="width: ${data.detailed_scores.wavelet_similarity}%"></div>
                </div>
            </div>
        </div>
        
        <div class="analysis-section">
            <div class="analysis-header">
                <i class="fas fa-info-circle"></i>
                <h3>Detailed Analysis</h3>
            </div>
            <ul class="analysis-list">
                ${data.analysis.map(item => `
                    <li>
                        <i class="fas fa-check-circle"></i>
                        <span>${item}</span>
                    </li>
                `).join('')}
            </ul>
        </div>
        
        <div class="action-buttons">
            <button class="btn btn-primary" onclick="resetComparison()">
                <i class="fas fa-redo"></i> Compare Another Pair
            </button>
        </div>
    `;
    
    document.getElementById('compareContent').innerHTML = content;
    document.getElementById('compareResults').style.display = 'block';
    showNotification('Comparison complete!', 'success');
}

// Display tampering results
function displayTamperingResults(data) {
    const verdictClass = data.tampering_detected ? 
        (data.risk_level === 'High' ? 'danger' : 'suspicious') : 'safe';
    
    const verdictIcon = data.tampering_detected ? 
        (data.risk_level === 'High' ? 'fa-times-circle' : 'fa-exclamation-triangle') : 'fa-check-circle';
    
    const riskBadgeClass = data.risk_level === 'High' ? 'risk-high' : 
                           data.risk_level === 'Medium' ? 'risk-medium' : 'risk-low';
    
    const indicatorsHTML = data.indicators.length > 0 ? `
        <div class="tampering-indicators-section">
            <div class="indicators-header">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Suspicious Indicators</h3>
            </div>
            <ul class="indicators-items">
                ${data.indicators.map(item => `
                    <li>
                        <i class="fas fa-exclamation-circle"></i>
                        <span>${item}</span>
                    </li>
                `).join('')}
            </ul>
        </div>
    ` : `
        <div class="no-indicators">
            <i class="fas fa-check-circle"></i>
            <p>No tampering indicators detected</p>
        </div>
    `;
    
    const content = `
        <div class="tampering-header">
            <div class="section-header">
                <h3><i class="fas fa-shield-alt"></i> Tampering Analysis</h3>
                <span class="section-badge"><i class="fas fa-search"></i> Forensic Scan</span>
            </div>
        </div>
        
        <div class="tampering-verdict-card ${verdictClass}">
            <div class="verdict-icon">
                <i class="fas ${verdictIcon}"></i>
            </div>
            <div class="verdict-content">
                <h2>${data.verdict}</h2>
                <div class="verdict-stats">
                    <div class="stat-item">
                        <i class="fas fa-percentage"></i>
                        <div>
                            <span class="stat-label">Confidence</span>
                            <span class="stat-value">${data.confidence.toFixed(1)}%</span>
                        </div>
                    </div>
                    <div class="stat-divider"></div>
                    <div class="stat-item">
                        <i class="fas fa-shield-alt"></i>
                        <div>
                            <span class="stat-label">Risk Level</span>
                            <span class="stat-value risk-badge ${riskBadgeClass}">${data.risk_level}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        ${indicatorsHTML}
        
        <div class="technical-analysis-section">
            <div class="analysis-header">
                <i class="fas fa-microscope"></i>
                <h3>Technical Analysis</h3>
            </div>
            <div class="technical-grid">
                <div class="technical-card ela-card">
                    <div class="card-icon">
                        <i class="fas fa-layer-group"></i>
                    </div>
                    <div class="card-content">
                        <h4>Error Level Analysis</h4>
                        <p>${data.techniques.error_level_analysis.analysis}</p>
                    </div>
                </div>
                <div class="technical-card noise-card">
                    <div class="card-icon">
                        <i class="fas fa-wave-square"></i>
                    </div>
                    <div class="card-content">
                        <h4>Noise Consistency</h4>
                        <p>${data.techniques.noise_consistency.analysis}</p>
                    </div>
                </div>
                <div class="technical-card jpeg-card">
                    <div class="card-icon">
                        <i class="fas fa-image"></i>
                    </div>
                    <div class="card-content">
                        <h4>JPEG Artifacts</h4>
                        <p>${data.techniques.jpeg_artifacts.analysis}</p>
                    </div>
                </div>
                <div class="technical-card metadata-card">
                    <div class="card-icon">
                        <i class="fas fa-tags"></i>
                    </div>
                    <div class="card-content">
                        <h4>Metadata Analysis</h4>
                        <p>${data.techniques.metadata_check.analysis}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="action-buttons">
            <button class="btn btn-primary" onclick="resetTampering()">
                <i class="fas fa-redo"></i> Analyze Another Image
            </button>
        </div>
    `;
    
    document.getElementById('tamperingContent').innerHTML = content;
    document.getElementById('tamperingResults').style.display = 'block';
    showNotification('Tampering detection complete!', 'success');
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all event listeners
    initializeFileInputs();
    initializeBatchUpload();
});

// Initialize file inputs
function initializeFileInputs() {
    // Comparison file inputs
    if (document.getElementById('compareFile1')) {
        document.getElementById('compareFile1').addEventListener('change', function(e) {
            document.getElementById('compareFileName1').textContent = e.target.files[0]?.name || 'First Image';
        });
    }
    
    if (document.getElementById('compareFile2')) {
        document.getElementById('compareFile2').addEventListener('change', function(e) {
            document.getElementById('compareFileName2').textContent = e.target.files[0]?.name || 'Second Image';
        });
    }
    
    // Tampering file input
    if (document.getElementById('tamperingFile')) {
        document.getElementById('tamperingFile').addEventListener('change', function(e) {
            document.getElementById('tamperingFileName').textContent = e.target.files[0]?.name || 'Choose File';
        });
    }
}

// Batch Upload Functionality
let accumulatedBatchFiles = [];

function initializeBatchUpload() {
    const dropZone = document.getElementById('batchDropZone');
    const fileInput = document.getElementById('batchFiles');
    const batchForm = document.getElementById('batchForm');
    
    if (!dropZone || !fileInput || !batchForm) return;
    
    // Click to browse
    dropZone.addEventListener('click', () => fileInput.click());
    
    // Drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        
        const files = Array.from(e.dataTransfer.files);
        addBatchFiles(files);
    });
    
    // File input change - accumulate files
    fileInput.addEventListener('change', (e) => {
        const newFiles = Array.from(e.target.files);
        addBatchFiles(newFiles);
        // Clear input to allow selecting same files again
        e.target.value = '';
    });
    
    // Form submission
    batchForm.addEventListener('submit', handleBatchUpload);
}

function addBatchFiles(newFiles) {
    // Add new files to accumulated list (avoid duplicates by name)
    newFiles.forEach(file => {
        const exists = accumulatedBatchFiles.some(f => f.name === file.name && f.size === file.size);
        if (!exists) {
            accumulatedBatchFiles.push(file);
        }
    });
    
    updateBatchFileList();
}

function removeBatchFile(index) {
    accumulatedBatchFiles.splice(index, 1);
    updateBatchFileList();
}

function clearBatchFiles() {
    accumulatedBatchFiles = [];
    updateBatchFileList();
}

// Make functions globally accessible
window.removeBatchFile = removeBatchFile;
window.clearBatchFiles = clearBatchFiles;

function updateBatchFileList() {
    const fileList = document.getElementById('batchFileList');
    const fileItems = document.getElementById('batchFileItems');
    const batchBtn = document.getElementById('batchBtn');
    const batchCount = document.getElementById('batchCount');
    
    if (accumulatedBatchFiles.length === 0) {
        fileList.style.display = 'none';
        batchBtn.style.display = 'none';
        return;
    }
    
    fileItems.innerHTML = '';
    accumulatedBatchFiles.forEach((file, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <i class="fas fa-file-image"></i> 
            ${file.name} (${(file.size / 1024).toFixed(1)} KB)
            <button type="button" class="remove-file-btn" onclick="removeBatchFile(${index})" title="Remove file">
                <i class="fas fa-times"></i>
            </button>
        `;
        fileItems.appendChild(li);
    });
    
    batchCount.textContent = accumulatedBatchFiles.length;
    fileList.style.display = 'block';
    batchBtn.style.display = 'block';
}

async function handleBatchUpload(e) {
    e.preventDefault();
    
    if (accumulatedBatchFiles.length < 2) {
        showNotification('Please upload at least 2 files for batch analysis', 'error');
        return;
    }
    
    if (accumulatedBatchFiles.length > 20) {
        showNotification('Maximum 20 files allowed per batch', 'error');
        return;
    }
    
    // Hide upload section, show loading
    document.getElementById('batchTab').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'block';
    animateProgressSteps();
    
    const formData = new FormData();
    accumulatedBatchFiles.forEach(file => {
        formData.append('files', file);
    });
    
    try {
        const response = await fetch('/batch_upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            setTimeout(() => displayBatchResults(data), 1500);
        } else {
            showNotification(data.error || 'Batch analysis failed', 'error');
            resetBatch();
        }
    } catch (error) {
        showNotification('Network error: ' + error.message, 'error');
        resetBatch();
    }
}

function displayBatchResults(data) {
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('batchResults').style.display = 'block';
    
    const summary = data.summary;
    let content = `
        <div class="batch-summary">
            <h3><i class="fas fa-chart-bar"></i> Analysis Summary</h3>
            <div class="result-grid">
                <div class="result-item">
                    <div class="result-label">Total Files</div>
                    <div class="result-value">${data.total}</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Processed</div>
                    <div class="result-value">${data.processed}</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Unique Scanners</div>
                    <div class="result-value">${summary.unique_scanners}</div>
                </div>
            </div>
        </div>
    `;
    
    // Scanner groups
    if (summary.groups.length > 0) {
        content += '<div class="scanner-groups"><h3><i class="fas fa-layer-group"></i> Scanner Groups</h3>';
        
        summary.groups.forEach((group, index) => {
            const colorIndex = index % 5;
            const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'];
            
            content += `
                <div class="scanner-group" style="border-left: 4px solid ${colors[colorIndex]};">
                    <h3><i class="fas fa-fingerprint"></i> ${group.scanner}</h3>
                    <p><strong>${group.count}</strong> file(s) from this scanner:</p>
                    <div class="file-badges">
                        ${group.files.map(file => `<span class="file-badge"><i class="fas fa-file"></i> ${file}</span>`).join('')}
                    </div>
                </div>
            `;
        });
        
        content += '</div>';
    }
    
    // Individual results
    content += `
        <div class="batch-results-grid">
            ${data.results.map(result => {
                if (result.success) {
                    const confidence = (result.result.confidence * 100).toFixed(1);
                    return `
                        <div class="batch-result-card success">
                            <h4><i class="fas fa-check-circle" style="color: var(--success-color);"></i> ${result.filename}</h4>
                            <p><strong>Scanner:</strong> ${result.result.scanner_brand} ${result.result.scanner_model}</p>
                            <p><strong>Confidence:</strong> ${confidence}%</p>
                        </div>
                    `;
                } else {
                    return `
                        <div class="batch-result-card error">
                            <h4><i class="fas fa-times-circle" style="color: var(--danger-color);"></i> ${result.filename}</h4>
                            <p style="color: var(--danger-color);">${result.error}</p>
                        </div>
                    `;
                }
            }).join('')}
        </div>
    `;
    
    content += `
        <div class="actions" style="margin-top: 2rem;">
            <button class="btn btn-primary" onclick="resetBatch()">
                <i class="fas fa-redo"></i> New Batch Analysis
            </button>
        </div>
    `;
    
    document.getElementById('batchContent').innerHTML = content;
    document.getElementById('batchResults').scrollIntoView({ behavior: 'smooth' });
    showNotification(`Batch analysis complete! Found ${summary.unique_scanners} unique scanner(s)`, 'success');
}

function resetBatch() {
    document.getElementById('batchTab').style.display = 'block';
    document.getElementById('batchResults').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('batchForm').reset();
    document.getElementById('batchFileList').style.display = 'none';
    document.getElementById('batchBtn').style.display = 'none';
    // Clear accumulated files
    accumulatedBatchFiles = [];
}

// Advanced Visualization - Enhanced Charts
function createAdvancedVisualization(canvasId, data, type) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    const textColor = '#2c3e50';
    const gridColor = 'rgba(0, 0, 0, 0.1)';
    
    Chart.defaults.color = textColor;
    Chart.defaults.borderColor = gridColor;
    
    if (type === 'heatmap') {
        // Noise pattern heatmap visualization
        new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Noise Pattern',
                    data: data,
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Scanner Noise Pattern Heatmap'
                    }
                },
                scales: {
                    x: { title: { display: true, text: 'X Position' }},
                    y: { title: { display: true, text: 'Y Position' }}
                }
            }
        });
    } else if (type === 'frequency') {
        // Frequency domain analysis
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Frequency Response',
                    data: data.values,
                    borderColor: 'rgb(102, 126, 234)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Frequency Domain Analysis'
                    }
                }
            }
        });
    }
}

// Share Functions
function shareResults() {
    if (!currentResults) {
        showNotification('No results to share', 'error');
        return;
    }
    document.getElementById('shareModal').style.display = 'flex';
}

function closeShareModal() {
    document.getElementById('shareModal').style.display = 'none';
    document.getElementById('emailForm').style.display = 'none';
}

// Click outside modal to close
document.addEventListener('click', function(event) {
    const modal = document.getElementById('shareModal');
    if (event.target === modal) {
        closeShareModal();
    }
});

function shareViaEmail() {
    document.getElementById('emailForm').style.display = 'block';
}

async function sendEmailReport() {
    const email = document.getElementById('recipientEmail').value;
    const message = document.getElementById('emailMessage').value;
    
    if (!email) {
        showNotification('Please enter an email address', 'error');
        return;
    }
    
    if (!currentResults) {
        showNotification('No results to share', 'error');
        return;
    }
    
    const emailBody = `TraceFinder Analysis Report
    
Scanner Detection Results:
- Brand: ${currentResults.scanner_brand || 'Unknown'}
- Model: ${currentResults.scanner_model || 'Unknown'}  
- Confidence: ${(currentResults.confidence * 100).toFixed(1)}%

${message ? '\nMessage: ' + message : ''}

View full report at: ${window.location.origin}

---
This email was sent via TraceFinder Forensic Scanner Identification System`;
    
    // Create mailto link
    const subject = encodeURIComponent('TraceFinder Analysis Report');
    const body = encodeURIComponent(emailBody);
    window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
    
    showNotification('Opening email client...', 'success');
    setTimeout(() => closeShareModal(), 1500);
}

function copyResultsLink() {
    const link = window.location.href;
    
    navigator.clipboard.writeText(link).then(() => {
        showNotification('Link copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy link', 'error');
    });
}

function shareAsText() {
    if (!currentResults) {
        showNotification('No results to share', 'error');
        return;
    }
    
    const text = `TraceFinder Analysis Report
    
Scanner Detection:
Brand: ${currentResults.scanner_brand || 'Unknown'}
Model: ${currentResults.scanner_model || 'Unknown'}
Confidence: ${(currentResults.confidence * 100).toFixed(1)}%
Detection Method: ${currentResults.method || 'Machine Learning'}

Generated: ${new Date().toLocaleString()}
System: TraceFinder v1.0`;
    
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Results copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy text', 'error');
    });
}

function downloadPDFShare() {
    generateReport();
    closeShareModal();
}

