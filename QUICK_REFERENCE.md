# TraceFinder - Quick Reference Card

## 🚀 Quick Commands

### Start Application
```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# Or manually
python app.py
```

### Access Application
```
http://localhost:5000
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main application entry point |
| `config.py` | Configuration settings |
| `requirements.txt` | Python dependencies |
| `README.md` | Main documentation |
| `PROJECT_SUMMARY.md` | Complete project overview |

---

## 🔧 Core Modules

| Module | Function |
|--------|----------|
| `image_processor.py` | Image loading and preprocessing |
| `feature_extractor.py` | Extract forensic features |
| `scanner_detector.py` | Main detection engine |
| `noise_analyzer.py` | Advanced noise analysis |
| `report_generator.py` | Generate PDF reports |

---

## 🎯 Main Features

✅ Scanner brand identification  
✅ Scanner model detection  
✅ Confidence scoring  
✅ PRNU analysis  
✅ Texture analysis (GLCM)  
✅ Frequency domain analysis  
✅ Wavelet decomposition  
✅ Noise pattern analysis  
✅ Metadata extraction  
✅ PDF report generation  
✅ JSON export  
✅ Modern web interface  

---

## 📊 Supported Formats

- JPG / JPEG
- PNG
- TIFF / TIF
- PDF (scanned)

**Max file size:** 16 MB

---

## 🔬 Analysis Pipeline

```
Upload → Preprocess → Extract Features → Match Signatures → 
Calculate Confidence → Generate Results → Create Report
```

---

## 🎨 Key Algorithms

1. **PRNU** - Photo Response Non-Uniformity
2. **GLCM** - Gray Level Co-occurrence Matrix
3. **FFT** - Fast Fourier Transform
4. **DWT** - Discrete Wavelet Transform
5. **MAD** - Median Absolute Deviation

---

## 🌐 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main page |
| `/about` | GET | About page |
| `/upload` | POST | Upload and analyze |
| `/analyze` | POST | Detailed analysis |
| `/generate_report` | POST | Generate PDF |
| `/health` | GET | Health check |

---

## 📝 Important Directories

```
TraceFinder/
├── modules/          # Core Python modules
├── templates/        # HTML templates
├── static/          # CSS, JS, uploads
│   ├── css/
│   ├── js/
│   └── uploads/
└── models/          # ML models
```

---

## 🔑 Key Configuration

In `config.py`:
- `UPLOAD_FOLDER` - Upload directory
- `MAX_CONTENT_LENGTH` - Max file size (16MB)
- `CONFIDENCE_THRESHOLD` - Min confidence (0.75)
- `SCANNER_DATABASE` - Supported scanners

---

## 🐛 Troubleshooting

### Port Already in Use
```python
# In app.py, change:
app.run(port=8000)  # Instead of 5000
```

### Module Not Found
```bash
pip install -r requirements.txt --upgrade
```

### Permission Denied
```bash
# Run as administrator or use sudo
```

---

## 📚 Documentation Files

- `README.md` - Overview and features
- `INSTALLATION.md` - Setup guide
- `API_DOCUMENTATION.md` - API reference
- `TESTING.md` - Testing guide
- `CHANGELOG.md` - Version history
- `PROJECT_SUMMARY.md` - Complete summary

---

## 🎓 Key Concepts

**PRNU**: Unique noise pattern from image sensors  
**GLCM**: Texture analysis matrix  
**FFT**: Frequency domain transformation  
**Wavelet**: Multi-resolution decomposition  
**Confidence Score**: 0.0 (low) to 1.0 (high)  

---

## 🔒 Security Features

- Secure file uploads
- Local processing
- No permanent storage
- Automatic cleanup
- File type validation
- Size limits

---

## 🎯 Supported Scanners

- **Canon**: CanoScan series
- **Epson**: Perfection, WorkForce
- **HP**: ScanJet series
- **Brother**: ADS, MFC series
- **Fujitsu**: ScanSnap, fi series

---

## 📈 Performance

- Analysis time: < 10 seconds
- Memory usage: < 500 MB
- File size limit: 16 MB
- Target accuracy: > 75%

---

## 🛠️ Tech Stack

**Backend**: Python, Flask, NumPy, OpenCV, scikit-learn  
**Frontend**: HTML5, CSS3, JavaScript  
**ML**: TensorFlow, scikit-learn  
**Reporting**: ReportLab  

---

## 📞 Getting Help

1. Check `PROJECT_SUMMARY.md`
2. Review `INSTALLATION.md`
3. Read specific documentation
4. Check error messages
5. Review logs

---

## ✅ Pre-Submission Checklist

- [ ] Application runs successfully
- [ ] Can upload and analyze images
- [ ] Results display correctly
- [ ] Can generate PDF reports
- [ ] Understand core algorithms
- [ ] Documentation is complete
- [ ] Can explain the project
- [ ] Code is clean and commented

---

## 🎉 Quick Test

```bash
# 1. Start application
python app.py

# 2. Open browser
# http://localhost:5000

# 3. Upload test image

# 4. View results

# 5. Generate report
```

---

**Version**: 1.0.0  
**Author**: Rahul Mahato  
**Date**: January 21, 2026  
**License**: MIT  

---

**Keep this reference card handy for quick access to common tasks!**
