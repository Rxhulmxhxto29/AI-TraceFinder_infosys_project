# TraceFinder - Frequently Asked Questions (FAQ)

## General Questions

### Q1: What is TraceFinder?
**A:** TraceFinder is a forensic analysis tool that identifies which scanner device was used to create a scanned document. It analyzes digital fingerprints and unique patterns left by scanner sensors.

### Q2: How accurate is TraceFinder?
**A:** TraceFinder aims for >75% confidence in scanner identification. Accuracy depends on image quality, scanner database completeness, and whether the image has been heavily processed or compressed.

### Q3: Is this for legal/forensic use?
**A:** TraceFinder is designed for educational and legitimate forensic purposes. Always ensure you have proper authorization before analyzing documents. Results should be used as part of comprehensive investigations, not as sole evidence.

### Q4: What file formats are supported?
**A:** JPG, JPEG, PNG, TIFF, TIF, and PDF (scanned documents). Maximum file size is 16 MB.

---

## Technical Questions

### Q5: What is PRNU analysis?
**A:** PRNU (Photo Response Non-Uniformity) is the unique noise pattern created by image sensors. Each sensor has microscopic manufacturing imperfections that create a consistent pattern, like a fingerprint. TraceFinder extracts and analyzes these patterns.

### Q6: How does texture analysis work?
**A:** TraceFinder uses GLCM (Gray Level Co-occurrence Matrix) to analyze texture patterns. Different scanners produce different micro-texture characteristics in scanned images.

### Q7: What is frequency domain analysis?
**A:** Using FFT (Fast Fourier Transform), TraceFinder converts images to frequency domain to detect periodic artifacts and patterns specific to scanner models.

### Q8: Why use wavelet analysis?
**A:** Wavelets decompose images into multiple resolution levels, helping identify scanner-specific characteristics at different scales.

### Q9: How is confidence calculated?
**A:** Confidence is calculated by:
1. Matching extracted features against scanner signatures
2. Assessing feature quality
3. Verifying metadata consistency
4. Combining scores with weighted average

---

## Installation & Setup

### Q10: What are the system requirements?
**A:**
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- Windows, Linux, or macOS
- 500MB free disk space

### Q11: Installation fails - what should I do?
**A:** Try these steps:
1. Update pip: `pip install --upgrade pip`
2. Install dependencies one by one
3. Use CPU-only TensorFlow: `pip install tensorflow-cpu`
4. Check Python version: `python --version`

### Q12: Port 5000 is already in use?
**A:** Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Q13: OpenCV won't install on Windows?
**A:** Install Visual C++ Redistributable or try:
```bash
pip install opencv-python-headless
```

---

## Usage Questions

### Q14: How do I upload a file?
**A:**
1. Open http://localhost:5000
2. Click "Choose File"
3. Select your scanned document
4. Click "Analyze Document"

### Q15: How long does analysis take?
**A:** Typically 5-10 seconds depending on image size and computer performance.

### Q16: Can I analyze multiple files at once?
**A:** Currently, TraceFinder processes one file at a time. Batch processing is planned for future versions.

### Q17: How do I generate a report?
**A:** After analysis completes, click "Generate PDF Report" button. The PDF will download automatically.

### Q18: Can I export results as JSON?
**A:** Yes! Click "Export JSON" after analysis to download results in JSON format.

### Q19: Why does analysis fail on my image?
**A:** Common reasons:
- File too large (>16MB)
- Unsupported format
- Corrupted file
- Heavily compressed/edited image
- Not a scanned document

---

## Scanner Database

### Q20: Which scanners are supported?
**A:** Currently supports:
- Canon CanoScan series
- Epson Perfection and WorkForce series
- HP ScanJet series
- Brother ADS and MFC series
- Fujitsu ScanSnap and fi series

### Q21: Can I add more scanners to the database?
**A:** Yes! Edit `config.py` and add to `SCANNER_DATABASE`:
```python
SCANNER_DATABASE = {
    'YourBrand': ['Model1', 'Model2']
}
```

### Q22: My scanner isn't in the database - will it work?
**A:** The system will try to match to the closest known scanner. Accuracy may be lower. You can add your scanner to the database for better results.

---

## Results & Interpretation

### Q23: What do the confidence levels mean?
**A:**
- **Very High (>90%)**: Very reliable identification
- **High (75-90%)**: Reliable identification
- **Medium (60-75%)**: Moderate confidence
- **Low (40-60%)**: Low confidence
- **Very Low (<40%)**: Unreliable

### Q24: What are "Primary Indicators"?
**A:** Main forensic features that match the identified scanner (PRNU patterns, texture characteristics, frequency signatures).

### Q25: What are "Secondary Indicators"?
**A:** Supporting evidence like noise profiles, wavelet characteristics, and metadata.

### Q26: What does "Anomalies Detected" mean?
**A:** Unusual patterns that might indicate:
- Image manipulation
- Heavy compression
- Degradation
- Unusual scanning conditions

### Q27: Can I trust low confidence results?
**A:** No. Results below 60% confidence should be considered unreliable. Try with higher quality images or collect more samples.

---

## Troubleshooting

### Q28: Application won't start?
**A:** Check:
1. Virtual environment activated
2. All dependencies installed
3. No errors in terminal
4. Port not already in use

### Q29: "Module not found" error?
**A:** Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Q30: Out of memory errors?
**A:** Reduce image size or use images under 2000x2000 pixels.

### Q31: Analysis takes too long?
**A:** 
- Reduce image resolution
- Use JPEG instead of TIFF
- Check system resources
- Close other applications

### Q32: Can't generate PDF report?
**A:** Ensure ReportLab is installed:
```bash
pip install reportlab
```

---

## Development & Customization

### Q33: Can I customize the confidence threshold?
**A:** Yes! Edit `config.py`:
```python
CONFIDENCE_THRESHOLD = 0.80  # Increase to 80%
```

### Q34: How do I change the maximum file size?
**A:** Edit `config.py`:
```python
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
```

### Q35: Can I add my own analysis algorithms?
**A:** Yes! Create a new method in `scanner_detector.py` and call it in the analysis pipeline.

### Q36: How do I customize the UI?
**A:** Edit `static/css/style.css` for styling and `templates/index.html` for structure.

### Q37: Can I create an API-only version?
**A:** Yes! Remove template routes and keep only API endpoints in `app.py`.

---

## Performance & Optimization

### Q38: How can I make it faster?
**A:**
1. Use smaller images
2. Reduce `IMAGE_SIZE` in config
3. Decrease `WAVELET_LEVEL`
4. Use GPU acceleration (future feature)

### Q39: Does it support GPU?
**A:** Not currently. GPU support for TensorFlow is planned for future versions.

### Q40: Can I run it on a server?
**A:** Yes! Use Gunicorn or uWSGI:
```bash
gunicorn -w 4 app:app
```

---

## Security & Privacy

### Q41: Is my data stored?
**A:** No. All uploads are processed locally and deleted immediately after analysis.

### Q42: Is it safe to analyze confidential documents?
**A:** Yes, as long as you run it locally. No data is sent externally. However, always follow your organization's security policies.

### Q43: Should I use HTTPS?
**A:** For production deployment, yes. Use a reverse proxy like Nginx with SSL certificates.

### Q44: Can I add user authentication?
**A:** Not included by default, but you can add Flask-Login or similar authentication systems.

---

## Advanced Features

### Q45: Can I train my own ML models?
**A:** Yes! Collect training data and use scikit-learn to train custom classifiers. Save them in the `models/` directory.

### Q46: How do I add metadata analysis?
**A:** The system already extracts EXIF data. You can enhance it in `scanner_detector.py`.

### Q47: Can I detect image tampering?
**A:** Basic tampering detection is included. Advanced techniques can be added to the forensic analysis pipeline.

### Q48: Is batch processing possible?
**A:** Not in current version, but you can modify `app.py` to accept multiple files.

---

## Contributing & Support

### Q49: Can I contribute to the project?
**A:** Yes! Follow standard GitHub contribution practices:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Q50: Where do I report bugs?
**A:** Open an issue on the GitHub repository with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- System information
- Error logs

### Q51: How do I request features?
**A:** Open a feature request on GitHub with:
- Feature description
- Use case
- Expected behavior
- Why it's needed

### Q52: Is there a community forum?
**A:** Currently, use GitHub Discussions or Issues for community support.

---

## Future Development

### Q53: What features are planned?
**A:** See `CHANGELOG.md` for the roadmap:
- Batch processing
- More scanner models
- Deep learning models
- GPU acceleration
- Mobile app
- API improvements

### Q54: Will there be a commercial version?
**A:** TraceFinder is open-source under MIT license. You can use it commercially with proper attribution.

### Q55: Can I use this in my research?
**A:** Absolutely! Please cite the project appropriately in your research papers.

---

## Licensing & Usage

### Q56: What license is this under?
**A:** MIT License. Free to use, modify, and distribute with attribution.

### Q57: Can I use this commercially?
**A:** Yes, under MIT license terms. Provide attribution to the original project.

### Q58: Can I modify the code?
**A:** Yes! That's encouraged. Follow the MIT license requirements.

### Q59: Do I need to credit the author?
**A:** Yes, maintain the copyright notice and attribution as per MIT license.

### Q60: Can I sell this software?
**A:** Yes, but you must include the MIT license and copyright notice.

---

## Education & Learning

### Q61: Is this suitable for learning?
**A:** Absolutely! The project demonstrates:
- Image processing
- Machine learning
- Web development
- Forensic techniques
- Software architecture

### Q62: Can I use this for my thesis?
**A:** Yes! It covers multiple computer science topics suitable for academic work.

### Q63: Where can I learn more about forensics?
**A:** Study:
- Digital image forensics textbooks
- Academic papers on PRNU
- OpenCV documentation
- Machine learning courses

### Q64: Are there tutorials for this?
**A:** The documentation provides comprehensive guides. Create your own tutorials based on the code!

### Q65: Can students use this for projects?
**A:** Yes! It's an excellent learning resource for computer science students.

---

## Miscellaneous

### Q66: Why is it called "TraceFinder"?
**A:** It "traces" and "finds" the source (scanner) of digital documents through forensic analysis.

### Q67: How is this different from existing tools?
**A:** TraceFinder combines multiple forensic techniques in a user-friendly web interface specifically for scanner identification.

### Q68: Can it work offline?
**A:** Yes! No internet connection required after installation.

### Q69: What's the future of this project?
**A:** Continuous improvement with more features, better accuracy, and community contributions.

### Q70: How can I stay updated?
**A:** Watch the GitHub repository for updates, releases, and announcements.

---

## Still Have Questions?

If your question isn't answered here:
1. Check the documentation files
2. Review the code comments
3. Open an issue on GitHub
4. Contact the developer

---

**Last Updated**: January 21, 2026  
**Version**: 1.0.0  
**Author**: Rahul Mahato
