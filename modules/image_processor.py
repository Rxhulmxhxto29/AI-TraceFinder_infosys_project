import cv2
import numpy as np
from PIL import Image
import os
from config import Config

class ImageProcessor:
    """Handles image loading, preprocessing, and conversion"""
    
    def __init__(self):
        self.target_size = Config.IMAGE_SIZE
    
    def load_and_preprocess(self, image_path):
        """Load and preprocess image for analysis"""
        try:
            # Load image
            if image_path.lower().endswith('.pdf'):
                image = self._process_pdf(image_path)
                if image is None:
                    return None
            else:
                # Read image with OpenCV
                image = cv2.imread(image_path)
                
                if image is None:
                    # Try with PIL
                    pil_image = Image.open(image_path)
                    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                
                if image is None:
                    return None
            
            # Preprocess
            processed = self._preprocess_image(image)
            
            return processed
        
        except Exception as e:
            print(f"Error loading image: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _preprocess_image(self, image):
        """Apply preprocessing steps"""
        try:
            # Convert to grayscale if needed for analysis
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # Resize for consistent analysis
            resized = cv2.resize(gray, self.target_size, interpolation=cv2.INTER_LANCZOS4)
            
            # Normalize - ensure resized is uint8 first
            if resized.dtype != np.uint8:
                resized = resized.astype(np.uint8)
            normalized = resized.astype(np.float32) / 255.0
            
            return {
                'original': image,
                'grayscale': gray,
                'resized': resized,
                'normalized': normalized,
                'dimensions': image.shape
            }
        except Exception as e:
            print(f"Error in _preprocess_image: {e}")
            return None
    
    def _process_pdf(self, pdf_path):
        """Extract first page from PDF and convert to image"""
        try:
            import fitz  # PyMuPDF
            
            # Open PDF and get first page
            print(f"Processing PDF: {pdf_path}")
            doc = fitz.open(pdf_path)
            
            if len(doc) == 0:
                print("PDF has no pages")
                doc.close()
                return None
            
            # Render first page at 200 DPI (matrix zoom factor = dpi/72)
            page = doc[0]
            zoom = 200 / 72  # 200 DPI
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix)
            
            # Convert to numpy array (RGB format)
            img_data = np.frombuffer(pix.samples, dtype=np.uint8)
            img_data = img_data.reshape(pix.height, pix.width, 3)
            
            # Convert RGB to BGR for OpenCV
            image = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
            
            doc.close()
            print(f"PDF converted successfully: {image.shape}")
            return image
            
        except ImportError as e:
            print(f"PDF processing requires pdf2image and poppler: {e}")
            return None
        except Exception as e:
            print(f"Error processing PDF: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def apply_noise_filter(self, image, sigma=2.0):
        """Apply noise filtering"""
        try:
            # Ensure image is float32 for subtraction
            if image.dtype != np.float32:
                image = image.astype(np.float32)
            filtered = cv2.GaussianBlur(image, (0, 0), sigma)
            noise = image - filtered
            return noise
        except Exception as e:
            print(f"Error in apply_noise_filter: {e}")
            return np.zeros_like(image, dtype=np.float32)
    
    def extract_frequency_domain(self, image):
        """Extract frequency domain representation"""
        # Apply FFT
        f_transform = np.fft.fft2(image)
        f_shift = np.fft.fftshift(f_transform)
        
        # Calculate magnitude spectrum
        magnitude = np.abs(f_shift)
        magnitude = np.log1p(magnitude)
        
        return {
            'fft': f_transform,
            'fft_shifted': f_shift,
            'magnitude': magnitude
        }
    
    def calculate_histogram(self, image):
        """Calculate image histogram"""
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist = hist.flatten()
        hist = hist / hist.sum()  # Normalize
        return hist
    
    def detect_edges(self, image):
        """Detect edges using Canny"""
        edges = cv2.Canny(image, 50, 150)
        return edges
    
    def extract_textures(self, image):
        """Extract texture patterns"""
        # Sobel operators
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        
        # Gradient magnitude
        gradient = np.sqrt(sobelx**2 + sobely**2)
        
        # Laplacian
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        
        return {
            'gradient_x': sobelx,
            'gradient_y': sobely,
            'gradient_magnitude': gradient,
            'laplacian': laplacian
        }
