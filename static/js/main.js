// TraceFinder - Main JavaScript File

let currentResults = null;

// File input handler
document.getElementById('fileInput').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Choose File';
    document.getElementById('fileName').textContent = fileName;
});

// Form submission handler
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        showNotification('Please select a file', 'error');
        return;
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
            currentResults = data.results;
            setTimeout(() => displayResults(data.results), 1500);
        } else {
            showNotification(data.error || 'Analysis failed', 'error');
            resetAnalysis();
        }
    } catch (error) {
        showNotification('Network error: ' + error.message, 'error');
        resetAnalysis();
    }
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
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
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
        
        const response = await fetch('/generate_report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ results: currentResults })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'tracefinder_report.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('Report generated successfully!', 'success');
        } else {
            showNotification('Failed to generate report', 'error');
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
    } else if (tabName === 'compare') {
        document.getElementById('compareTab').style.display = 'block';
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('compareResults').style.display = document.getElementById('compareContent').innerHTML ? 'block' : 'none';
        document.getElementById('tamperingResults').style.display = 'none';
    } else if (tabName === 'tampering') {
        document.getElementById('tamperingTab').style.display = 'block';
        document.querySelectorAll('.tab-btn')[2].classList.add('active');
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('compareResults').style.display = 'none';
        document.getElementById('tamperingResults').style.display = document.getElementById('tamperingContent').innerHTML ? 'block' : 'none';
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
    const content = `
        <div class="comparison-score">
            <h3>${data.overall_similarity}%</h3>
            <p style="font-size: 1.2rem;">${data.match_status}</p>
            <p>Confidence: ${data.match_confidence}</p>
        </div>
        
        <div class="comparison-details">
            <div class="detail-item">
                <h4>PRNU Similarity</h4>
                <div class="score">${data.detailed_scores.prnu_similarity}%</div>
            </div>
            <div class="detail-item">
                <h4>Texture Similarity</h4>
                <div class="score">${data.detailed_scores.texture_similarity}%</div>
            </div>
            <div class="detail-item">
                <h4>Frequency Similarity</h4>
                <div class="score">${data.detailed_scores.frequency_similarity}%</div>
            </div>
            <div class="detail-item">
                <h4>Wavelet Similarity</h4>
                <div class="score">${data.detailed_scores.wavelet_similarity}%</div>
            </div>
        </div>
        
        <div class="indicators-list">
            <h3>Analysis</h3>
            <ul>
                ${data.analysis.map(item => `<li><i class="fas fa-info-circle"></i> ${item}</li>`).join('')}
            </ul>
        </div>
        
        <button class="btn btn-primary" onclick="resetComparison()" style="margin-top: 2rem;">
            <i class="fas fa-redo"></i> Compare Another Pair
        </button>
    `;
    
    document.getElementById('compareContent').innerHTML = content;
    document.getElementById('compareResults').style.display = 'block';
    showNotification('Comparison complete!', 'success');
}

// Display tampering results
function displayTamperingResults(data) {
    const verdictClass = data.tampering_detected ? 
        (data.risk_level === 'High' ? 'danger' : 'suspicious') : 'safe';
    
    const indicatorsHTML = data.indicators.length > 0 ? `
        <div class="indicators-list">
            <h3><i class="fas fa-exclamation-triangle"></i> Suspicious Indicators</h3>
            <ul>
                ${data.indicators.map(item => `<li><i class="fas fa-exclamation-circle"></i> ${item}</li>`).join('')}
            </ul>
        </div>
    ` : '<p style="text-align: center; color: var(--success-color); font-size: 1.2rem;"><i class="fas fa-check-circle"></i> No tampering indicators detected</p>';
    
    const content = `
        <div class="tampering-verdict ${verdictClass}">
            <h3>${data.verdict}</h3>
            <p>Confidence: ${data.confidence.toFixed(1)}%</p>
            <p>Risk Level: ${data.risk_level}</p>
        </div>
        
        ${indicatorsHTML}
        
        <div class="details-section" style="margin-top: 2rem;">
            <h3>Technical Analysis</h3>
            <div class="forensic-details">
                <div class="detail-card">
                    <h4>Error Level Analysis</h4>
                    <p>${data.techniques.error_level_analysis.analysis}</p>
                </div>
                <div class="detail-card">
                    <h4>Noise Consistency</h4>
                    <p>${data.techniques.noise_consistency.analysis}</p>
                </div>
                <div class="detail-card">
                    <h4>JPEG Artifacts</h4>
                    <p>${data.techniques.jpeg_artifacts.analysis}</p>
                </div>
                <div class="detail-card">
                    <h4>Metadata Analysis</h4>
                    <p>${data.techniques.metadata_check.analysis}</p>
                </div>
            </div>
        </div>
        
        <button class="btn btn-primary" onclick="resetTampering()" style="margin-top: 2rem;">
            <i class="fas fa-redo"></i> Analyze Another Image
        </button>
    `;
    
    document.getElementById('tamperingContent').innerHTML = content;
    document.getElementById('tamperingResults').style.display = 'block';
    showNotification('Tampering detection complete!', 'success');
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('TraceFinder initialized with enhanced features');
});
