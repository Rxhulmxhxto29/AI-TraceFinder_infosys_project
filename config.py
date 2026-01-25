import os

class Config:
    """Application configuration settings"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tracefinder-forensic-scanner-2026'
    DEBUG = True
    
    # Upload settings
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max total request size for batch uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff', 'tif', 'bmp', 'pdf'}
    
    # Model settings
    MODEL_FOLDER = 'models'
    CONFIDENCE_THRESHOLD = 0.75
    
    # Analysis settings
    IMAGE_SIZE = (512, 512)
    PRNU_BLOCK_SIZE = 64
    NOISE_SIGMA = 2.0
    
    # Scanner database
    SCANNER_DATABASE = {
        'Canon': ['CanoScan LiDE', 'CanoScan 9000F', 'imageFORMULA'],
        'Epson': ['Perfection V', 'WorkForce DS', 'Expression'],
        'HP': ['ScanJet Pro', 'ScanJet Enterprise', 'ScanJet G'],
        'Brother': ['ADS Series', 'MFC Series', 'DSmobile'],
        'Fujitsu': ['ScanSnap', 'fi Series', 'SP Series']
    }
    
    # Feature extraction settings
    GLCM_DISTANCES = [1, 3, 5]
    GLCM_ANGLES = [0, 45, 90, 135]
    WAVELET_LEVEL = 3
    WAVELET_TYPE = 'db4'
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.MODEL_FOLDER, exist_ok=True)
