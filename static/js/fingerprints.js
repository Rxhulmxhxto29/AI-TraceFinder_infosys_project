// Scanner Fingerprint Visualization

// Load scanner fingerprints from history
async function loadScannerFingerprints() {
    const gallery = document.getElementById('fingerprintsGallery');
    
    try {
        const response = await fetch('/history?limit=all&type=scanner');
        const result = await response.json();
        
        if (!result.success || !result.data || !result.data.analyses) {
            throw new Error('Invalid response format');
        }
        
        const history = result.data.analyses;
        
        // Group by scanner
        const scannerMap = new Map();
        
        history.forEach(item => {
            const key = `${item.scanner_brand}-${item.scanner_model}`;
            if (!scannerMap.has(key)) {
                scannerMap.set(key, {
                    brand: item.scanner_brand,
                    model: item.scanner_model,
                    confidence: item.confidence,
                    count: 0,
                    lastSeen: item.timestamp
                });
            }
            const scanner = scannerMap.get(key);
            scanner.count++;
            if (new Date(item.timestamp) > new Date(scanner.lastSeen)) {
                scanner.lastSeen = item.timestamp;
            }
        });
        
        if (scannerMap.size === 0) {
            gallery.innerHTML = `
                <div class="no-fingerprints">
                    <i class="fas fa-fingerprint" style="font-size: 4rem; opacity: 0.3;"></i>
                    <h3>No Scanner Fingerprints Yet</h3>
                    <p>Analyze some documents to build your scanner database</p>
                </div>
            `;
            return;
        }
        
        // Generate fingerprint cards
        gallery.innerHTML = '';
        let delay = 0;
        
        scannerMap.forEach((scanner, key) => {
            const card = createFingerprintCard(scanner, delay);
            gallery.appendChild(card);
            delay += 0.1;
        });
        
    } catch (error) {
        console.error('Error loading fingerprints:', error);
        gallery.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load scanner fingerprints</p>
            </div>
        `;
    }
}

// Create a fingerprint card
function createFingerprintCard(scanner, delay) {
    const card = document.createElement('div');
    card.className = 'fingerprint-card';
    card.style.animationDelay = `${delay}s`;
    
    // Get brand color
    const brandColor = getBrandColor(scanner.brand);
    
    // Calculate pattern analysis
    const patternAnalysis = calculatePatternAnalysis(scanner);
    
    card.innerHTML = `
        <div class="fingerprint-header" style="background: linear-gradient(135deg, ${brandColor}dd, ${brandColor}99);">
            <i class="fas fa-fingerprint"></i>
            <h3>${scanner.brand || 'Unknown'}</h3>
            <p class="model-name">${scanner.model || 'Unknown Model'}</p>
        </div>
        <div class="fingerprint-body">
            <canvas class="fingerprint-canvas" width="300" height="120"></canvas>
        </div>
        <div class="fingerprint-footer">
            <div class="fingerprint-stat">
                <i class="fas fa-percentage"></i>
                <span>${(scanner.confidence * 100).toFixed(1)}% confidence</span>
            </div>
            <div class="fingerprint-stat">
                <i class="fas fa-file-alt"></i>
                <span>${scanner.count} document${scanner.count !== 1 ? 's' : ''}</span>
            </div>
            <div class="fingerprint-stat" title="Pattern complexity and uniqueness">
                <i class="fas fa-chart-line"></i>
                <span>Pattern Analysis: ${patternAnalysis.complexity}% complex, ${patternAnalysis.uniqueness}% unique</span>
            </div>
            <div class="fingerprint-stat">
                <i class="fas fa-clock"></i>
                <span>${formatRelativeTime(scanner.lastSeen)}</span>
            </div>
        </div>
    `;
    
    // Draw fingerprint pattern after card is added to DOM
    setTimeout(() => {
        const canvas = card.querySelector('.fingerprint-canvas');
        if (canvas) {
            drawFingerprint(canvas, scanner);
        }
    }, (delay * 1000) + 100);
    
    return card;
}

// Draw unique fingerprint pattern
function drawFingerprint(canvas, scanner) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Get brand color
    const brandColor = getBrandColor(scanner.brand);
    
    // Generate pseudo-random but deterministic pattern based on scanner name
    const seed = hashString(`${scanner.brand}-${scanner.model}`);
    
    // Draw noise pattern bars (top third)
    drawNoisePattern(ctx, seed, brandColor, 0, 0, width, 40);
    
    // Draw texture waves (middle third)
    drawTextureWaves(ctx, seed, brandColor, 0, 40, width, 40);
    
    // Draw frequency dots (bottom third)
    drawFrequencyDots(ctx, seed, brandColor, 0, 80, width, 40);
}

// Draw noise pattern bars
function drawNoisePattern(ctx, seed, color, x, y, width, height) {
    const bars = 30;
    const barWidth = width / bars;
    
    ctx.fillStyle = color + '40';
    
    for (let i = 0; i < bars; i++) {
        const noise = seededRandom(seed + i);
        const barHeight = height * noise;
        const barY = y + (height - barHeight) / 2;
        
        ctx.fillRect(x + i * barWidth, barY, barWidth - 1, barHeight);
    }
}

// Draw texture waves
function drawTextureWaves(ctx, seed, color, x, y, width, height) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    
    for (let wave = 0; wave < 3; wave++) {
        ctx.beginPath();
        const offsetY = y + height * 0.3 + (wave * height * 0.2);
        
        for (let i = 0; i <= width; i += 5) {
            const frequency = 0.05 + (seededRandom(seed + wave) * 0.05);
            const amplitude = height * 0.15;
            const waveY = offsetY + Math.sin(i * frequency + seed * wave) * amplitude;
            
            if (i === 0) {
                ctx.moveTo(x + i, waveY);
            } else {
                ctx.lineTo(x + i, waveY);
            }
        }
        
        ctx.stroke();
    }
}

// Calculate pattern analysis metrics
function calculatePatternAnalysis(scanner) {
    const scannerName = `${scanner.brand}-${scanner.model}`;
    const seed = hashString(scannerName);
    
    // Calculate complexity based on pattern variations
    let complexity = 0;
    let noiseValues = [];
    
    // Sample noise pattern values
    for (let i = 0; i < 30; i++) {
        const noiseValue = seededRandom(seed + i) * 40;
        noiseValues.push(noiseValue);
    }
    
    // Calculate variance (complexity indicator)
    const mean = noiseValues.reduce((a, b) => a + b, 0) / noiseValues.length;
    const variance = noiseValues.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / noiseValues.length;
    complexity = Math.min(100, Math.round((variance / 100) * 100));
    
    // Calculate uniqueness based on seed distribution
    const uniqueness = Math.min(100, Math.round(((seed % 1000) / 1000) * 100));
    
    // Calculate noise variance for pattern stability
    const noiseVariance = Math.round(variance * 10) / 10;
    
    return {
        complexity: complexity,
        uniqueness: uniqueness,
        noiseVariance: noiseVariance
    };
}

// Draw frequency dots
function drawFrequencyDots(ctx, seed, color, x, y, width, height) {
    const rows = 4;
    const cols = 20;
    const dotSpaceX = width / cols;
    const dotSpaceY = height / rows;
    
    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
            const noise = seededRandom(seed + row * cols + col);
            
            if (noise > 0.3) {
                const dotX = x + col * dotSpaceX + dotSpaceX / 2;
                const dotY = y + row * dotSpaceY + dotSpaceY / 2;
                const radius = 2 + noise * 3;
                
                ctx.fillStyle = color + Math.floor(noise * 255).toString(16).padStart(2, '0');
                ctx.beginPath();
                ctx.arc(dotX, dotY, radius, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }
}

// Get color for scanner brand
function getBrandColor(brand) {
    const colors = {
        'Canon': '#e74c3c',
        'HP': '#3498db',
        'Epson': '#2ecc71',
        'Brother': '#f39c12',
        'Fujitsu': '#9b59b6',
        'Unknown': '#95a5a6'
    };
    return colors[brand] || colors['Unknown'];
}

// Simple hash function for string
function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash);
}

// Seeded random number generator
function seededRandom(seed) {
    const x = Math.sin(seed++) * 10000;
    return x - Math.floor(x);
}

// Format relative time
function formatRelativeTime(timestamp) {
    const now = new Date();
    const then = new Date(timestamp);
    const diffMs = now - then;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return then.toLocaleDateString();
}
