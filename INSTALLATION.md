# Installation Guide

## Prerequisites

Before installing TraceFinder, ensure you have:
- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning)

## Step-by-Step Installation

### 1. Clone or Download the Repository

**Option A: Using Git**
```bash
git clone https://github.com/AI-TraceFinder/Rahul_Mahato-TraceFinder.git
cd Rahul_Mahato-TraceFinder
```

**Option B: Download ZIP**
- Download the ZIP file from GitHub
- Extract it to your desired location
- Open terminal/command prompt in that directory

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Flask (Web framework)
- OpenCV (Image processing)
- NumPy, SciPy (Numerical computing)
- scikit-learn, TensorFlow (Machine learning)
- Pillow (Image handling)
- And other dependencies

### 4. Create Required Directories

The application will create these automatically, but you can do it manually:

```bash
mkdir -p static/uploads
mkdir -p models
```

### 5. Run the Application

```bash
python app.py
```

You should see:
```
============================================================
TraceFinder - Forensic Scanner Identification System
============================================================
Starting server on http://localhost:5000
Press CTRL+C to quit
============================================================
```

### 6. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Make sure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Port 5000 already in use

**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

### Issue: OpenCV import errors on Windows

**Solution:** Install Visual C++ Redistributable:
- Download from Microsoft's official website
- Or try: `pip install opencv-python-headless`

### Issue: TensorFlow installation problems

**Solution:** 
- For CPU-only version: `pip install tensorflow-cpu`
- Or skip TensorFlow if not needed: Comment out in requirements.txt

### Issue: Permission denied when creating directories

**Solution:** Run with appropriate permissions or create directories manually

## Configuration

Edit `config.py` to customize:
- Upload folder location
- Maximum file size
- Confidence threshold
- Scanner database

## Development Mode

To run in development mode with auto-reload:
```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
python app.py
```

## Production Deployment

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Updating

To update to the latest version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstallation

To uninstall:
1. Deactivate virtual environment: `deactivate`
2. Delete the project folder
3. Remove virtual environment folder if created separately

## Support

For issues or questions:
- Check the README.md for documentation
- Review common issues above
- Open an issue on GitHub
- Contact the developer

---

**Happy Analyzing! 🔍**
