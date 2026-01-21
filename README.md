# TraceFinder - Forensic Scanner Identification System

A professional forensic analysis tool that identifies and traces scanner devices through digital fingerprint analysis.

## 🎯 Overview

TraceFinder is an advanced forensic tool designed to identify scanner models by analyzing digital artifacts and unique fingerprints left in scanned documents. Using machine learning and image processing techniques, it can trace the origin scanner with high accuracy.

## ✨ Features

- **Scanner Fingerprint Analysis** - Detect unique patterns left by different scanner models
- **Multi-Format Support** - Analyze JPG, PNG, TIFF, and PDF documents
- **Machine Learning Detection** - AI-powered scanner identification
- **Noise Pattern Recognition** - Identify scanner-specific noise signatures
- **Metadata Extraction** - Extract and analyze EXIF and embedded metadata
- **Detailed Reports** - Generate comprehensive forensic analysis reports
- **Modern Web Interface** - User-friendly dashboard for analysis
- **Batch Processing** - Analyze multiple documents simultaneously

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum (8GB recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AI-TraceFinder/Rahul_Mahato-TraceFinder.git
cd Rahul_Mahato-TraceFinder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## 💡 Usage

1. **Upload Document**: Click "Choose File" and select a scanned document
2. **Analyze**: Click "Analyze Document" to start the forensic analysis
3. **View Results**: Review the detailed scanner identification report
4. **Export Report**: Download the analysis report in PDF or JSON format

## 🏗️ Project Structure

```
TraceFinder/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── config.py                       # Configuration settings
├── models/                         # ML models and weights
│   ├── scanner_classifier.pkl
│   └── feature_extractor.pkl
├── modules/                        # Core analysis modules
│   ├── __init__.py
│   ├── image_processor.py         # Image processing utilities
│   ├── scanner_detector.py        # Scanner identification logic
│   ├── feature_extractor.py       # Feature extraction algorithms
│   ├── noise_analyzer.py          # Noise pattern analysis
│   └── report_generator.py        # Report generation
├── static/                         # Static files
│   ├── css/
│   │   └── style.css              # Custom styles
│   ├── js/
│   │   └── main.js                # Frontend logic
│   └── uploads/                   # Temporary upload directory
└── templates/                      # HTML templates
    ├── index.html                 # Main interface
    ├── results.html               # Results page
    └── about.html                 # About page
```

## 🔬 Technical Details

### Scanner Detection Methods

1. **PRNU (Photo Response Non-Uniformity) Analysis**
   - Extracts sensor noise patterns unique to each scanner
   - Uses wavelet transforms for noise separation

2. **Frequency Domain Analysis**
   - Analyzes periodic patterns in the frequency spectrum
   - Identifies scanner-specific artifacts

3. **Metadata Forensics**
   - Extracts EXIF data
   - Analyzes software signatures

4. **Texture Analysis**
   - Examines micro-texture patterns
   - Uses GLCM (Gray Level Co-occurrence Matrix)

## 📊 Supported Scanners

- Canon CanoScan Series
- Epson Perfection Series
- HP ScanJet Series
- Brother Scanner Series
- Fujitsu Scanner Series
- And many more...

## 🔒 Security & Privacy

- All uploads are processed locally
- No data is stored permanently
- Automatic cleanup after analysis
- Secure file handling

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Image Processing**: OpenCV, Pillow, scikit-image
- **Machine Learning**: TensorFlow, scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Analysis**: NumPy, SciPy

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Rahul Mahato**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This tool is for educational and legitimate forensic purposes only. Always ensure you have proper authorization before analyzing documents.
