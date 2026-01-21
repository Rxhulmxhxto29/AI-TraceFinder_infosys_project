import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from modules.feature_extractor import FeatureExtractor
from modules.image_processor import ImageProcessor
import io
import base64

class FingerprintVisualizer:
    """Generate visual representations of scanner fingerprints"""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.image_processor = ImageProcessor()
    
    def generate_visualizations(self, image_path):
        """Generate all visualizations for scanner fingerprint"""
        try:
            # Load image
            img = self.image_processor.load_and_preprocess(image_path)
            if img is None:
                return {'success': False, 'error': 'Failed to load image'}
            
            # Extract features
            features = self.feature_extractor.extract_all_features(img)
            
            # Generate visualizations
            prnu_viz = self._visualize_prnu(features['prnu'])
            fft_viz = self._visualize_frequency(features['frequency'], img)
            noise_viz = self._visualize_noise(img)
            wavelet_viz = self._visualize_wavelet(features['wavelet'])
            
            return {
                'success': True,
                'visualizations': {
                    'prnu': prnu_viz,
                    'frequency': fft_viz,
                    'noise': noise_viz,
                    'wavelet': wavelet_viz
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _visualize_prnu(self, prnu_features):
        """Visualize PRNU pattern"""
        try:
            plt.figure(figsize=(10, 4))
            
            # PRNU pattern
            plt.subplot(1, 2, 1)
            pattern = prnu_features['pattern']
            plt.imshow(pattern, cmap='jet', interpolation='nearest')
            plt.title('PRNU Pattern')
            plt.colorbar(label='Intensity')
            plt.axis('off')
            
            # PRNU histogram
            plt.subplot(1, 2, 2)
            plt.hist(pattern.flatten(), bins=50, color='steelblue', edgecolor='black')
            plt.title('PRNU Distribution')
            plt.xlabel('Intensity')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return f'data:image/png;base64,{image_base64}'
            
        except Exception as e:
            print(f"PRNU visualization error: {e}")
            return None
    
    def _visualize_frequency(self, freq_features, img):
        """Visualize frequency domain analysis"""
        try:
            # Convert to grayscale if needed
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            # Compute FFT
            f_transform = np.fft.fft2(gray)
            f_shift = np.fft.fftshift(f_transform)
            magnitude_spectrum = np.log(np.abs(f_shift) + 1)
            
            plt.figure(figsize=(12, 4))
            
            # Original image
            plt.subplot(1, 3, 1)
            plt.imshow(gray, cmap='gray')
            plt.title('Original Image')
            plt.axis('off')
            
            # Frequency spectrum
            plt.subplot(1, 3, 2)
            plt.imshow(magnitude_spectrum, cmap='hot')
            plt.title('Frequency Spectrum')
            plt.colorbar(label='Magnitude')
            plt.axis('off')
            
            # Radial frequency profile
            plt.subplot(1, 3, 3)
            h, w = magnitude_spectrum.shape
            center_y, center_x = h // 2, w // 2
            
            # Calculate radial profile
            y, x = np.ogrid[:h, :w]
            r = np.sqrt((x - center_x)**2 + (y - center_y)**2).astype(int)
            
            radial_profile = []
            for radius in range(0, min(h, w) // 2, 5):
                mask = (r >= radius) & (r < radius + 5)
                if np.any(mask):
                    radial_profile.append(np.mean(magnitude_spectrum[mask]))
            
            plt.plot(range(0, len(radial_profile) * 5, 5), radial_profile, 
                    color='steelblue', linewidth=2)
            plt.title('Radial Frequency Profile')
            plt.xlabel('Frequency (pixels)')
            plt.ylabel('Magnitude')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return f'data:image/png;base64,{image_base64}'
            
        except Exception as e:
            print(f"Frequency visualization error: {e}")
            return None
    
    def _visualize_noise(self, img):
        """Visualize noise patterns"""
        try:
            # Convert to grayscale
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            # Extract noise using Gaussian filter
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            noise = cv2.absdiff(gray, blurred)
            
            plt.figure(figsize=(12, 4))
            
            # Original
            plt.subplot(1, 3, 1)
            plt.imshow(gray, cmap='gray')
            plt.title('Original Image')
            plt.axis('off')
            
            # Noise pattern
            plt.subplot(1, 3, 2)
            plt.imshow(noise, cmap='viridis')
            plt.title('Noise Pattern')
            plt.colorbar(label='Intensity')
            plt.axis('off')
            
            # Noise histogram
            plt.subplot(1, 3, 3)
            plt.hist(noise.flatten(), bins=50, color='green', edgecolor='black', alpha=0.7)
            plt.title('Noise Distribution')
            plt.xlabel('Noise Level')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return f'data:image/png;base64,{image_base64}'
            
        except Exception as e:
            print(f"Noise visualization error: {e}")
            return None
    
    def _visualize_wavelet(self, wavelet_features):
        """Visualize wavelet decomposition"""
        try:
            import pywt
            
            plt.figure(figsize=(10, 8))
            
            # Create sample decomposition for visualization
            titles = ['Approximation (cA)', 'Horizontal (cH)', 
                     'Vertical (cV)', 'Diagonal (cD)']
            
            coeffs_data = []
            for level in ['cA', 'cH', 'cV', 'cD']:
                if level in wavelet_features:
                    # Create a small sample matrix for visualization
                    energy = wavelet_features[level]['energy']
                    size = 64
                    sample = np.random.randn(size, size) * np.sqrt(energy)
                    coeffs_data.append(sample)
            
            for i, (coeff, title) in enumerate(zip(coeffs_data, titles)):
                plt.subplot(2, 2, i + 1)
                plt.imshow(coeff, cmap='RdBu_r', interpolation='nearest')
                plt.title(title)
                plt.colorbar()
                plt.axis('off')
            
            plt.suptitle('Wavelet Decomposition', fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            
            return f'data:image/png;base64,{image_base64}'
            
        except Exception as e:
            print(f"Wavelet visualization error: {e}")
            return None
