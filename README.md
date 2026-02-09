## 🎥 Demo Video

Watch the full demonstration on LinkedIn: [TraceFinder Demo Video](https://www.linkedin.com/posts/rahul-mahato-0b1534254_infosysspringboard-tracefinder-ai-activity-7424065147620724737-7-sC?utm_source=share&utm_medium=member_desktop)

# TraceFinder - Forensic Scanner Identification System

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

🔍 **Advanced forensic analysis system for identifying scanners from scanned documents using machine learning and digital forensics techniques.**

## 🌐 Live Demo

### 🚀 Deploy on Vercel (Recommended - 1-Click Deploy)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/AI-TraceFinder/Rahul_Mahato-TraceFinder)

**Quick Deployment Steps:**
1. Click the "Deploy with Vercel" button above
2. Sign in with GitHub (100% free, no credit card needed)
3. Your app will be live in 2-3 minutes at `https://your-app-name.vercel.app`

✅ **Instant Deployment** | ✅ **Global CDN** | ✅ **Auto HTTPS** | ✅ **Free Forever**

---

### Alternative: Deploy on Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/AI-TraceFinder/Rahul_Mahato-TraceFinder)

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

## 🌐 Deploy Your Own Instance

### Recommended: Render.com (Free Forever)

**Why Render?**
- ✅ 100% Free tier with no credit card required
- ✅ Automatic deployment from GitHub
- ✅ HTTPS included
- ✅ Always-on service (doesn't sleep)
- ✅ Easy to use dashboard

**Deploy Now:**
1. Click the "Deploy to Render" button at the top
2. Authorize Render to access your GitHub
3. Click "Deploy" - Done! 🎉

Your app will be live at: `https://tracefinder-XXXX.onrender.com`

### Alternative: Run Locally
```bash
# Clone and run locally
git clone https://github.com/AI-TraceFinder/Rahul_Mahato-TraceFinder.git
cd Rahul_Mahato-TraceFinder
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000
```

## 🎓 Documentation

- **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
- **[Training Guide](TRAINING_GUIDE.md)** - How to train with your dataset
- **[API Documentation](API_DOCUMENTATION.md)** - REST API reference
- **[Features](FEATURES.md)** - Complete feature list
- **[FAQ](FAQ.md)** - Frequently asked questions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Rahul Mahato**
- GitHub: [@AI-TraceFinder](https://github.com/AI-TraceFinder)
- Project: [TraceFinder](https://github.com/AI-TraceFinder/Rahul_Mahato-TraceFinder)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support:
- 🐛 [Open an Issue](https://github.com/AI-TraceFinder/Rahul_Mahato-TraceFinder/issues)
- 💬 Discussions on GitHub
- 📖 Check [Documentation](DOCUMENTATION_INDEX.md)

## ⭐ Show Your Support

Give a ⭐ if this project helped you!

---

**Note**: This tool is for educational and legitimate forensic purposes only. Always ensure you have proper authorization before analyzing documents.

**Made with ❤️ by Rahul Mahato | TraceFinder © 2026**
