import numpy as np
import cv2
from skimage.feature import graycomatrix, graycoprops
import pywt
from config import Config

class FeatureExtractor:
    """Extract forensic features from scanned images"""
    
    def __init__(self):
        self.glcm_distances = Config.GLCM_DISTANCES
        self.glcm_angles = np.array(Config.GLCM_ANGLES) * np.pi / 180
        self.wavelet_type = Config.WAVELET_TYPE
        self.wavelet_level = Config.WAVELET_LEVEL
    
    def extract_all_features(self, image_data):
        """Extract comprehensive feature set"""
        features = {}
        
        # Get processed images
        normalized = image_data['normalized']
        gray = image_data['resized']
        
        # PRNU features
        features['prnu'] = self.extract_prnu_features(normalized)
        
        # Texture features (GLCM)
        features['texture'] = self.extract_texture_features(gray)
        
        # Frequency features
        features['frequency'] = self.extract_frequency_features(normalized)
        
        # Wavelet features
        features['wavelet'] = self.extract_wavelet_features(normalized)
        
        # Statistical features
        features['statistical'] = self.extract_statistical_features(gray)
        
        # Noise characteristics
        features['noise'] = self.extract_noise_features(normalized)
        
        return features
    
    def extract_prnu_features(self, image):
        """Extract Photo Response Non-Uniformity features"""
        # This is a simplified PRNU extraction
        # Real PRNU extraction is more complex
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(
            (image * 255).astype(np.uint8),
            None, 10, 7, 21
        ).astype(np.float32) / 255.0
        
        # Extract noise residual (PRNU pattern)
        prnu = image - denoised
        
        # Calculate PRNU statistics
        prnu_mean = np.mean(prnu)
        prnu_std = np.std(prnu)
        prnu_skew = self._calculate_skewness(prnu)
        prnu_kurt = self._calculate_kurtosis(prnu)
        
        # Energy in different frequency bands
        fft_prnu = np.fft.fft2(prnu)
        fft_magnitude = np.abs(fft_prnu)
        
        return {
            'mean': float(prnu_mean),
            'std': float(prnu_std),
            'skewness': float(prnu_skew),
            'kurtosis': float(prnu_kurt),
            'fft_energy': float(np.mean(fft_magnitude)),
            'pattern_strength': float(prnu_std / (prnu_mean + 1e-10))
        }
    
    def extract_texture_features(self, image):
        """Extract texture features using GLCM"""
        # Normalize to 0-255 range and convert to uint8
        img_uint8 = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
        
        # Calculate GLCM
        glcm = graycomatrix(
            img_uint8,
            distances=self.glcm_distances,
            angles=self.glcm_angles,
            levels=256,
            symmetric=True,
            normed=True
        )
        
        # Extract properties
        contrast = graycoprops(glcm, 'contrast')
        dissimilarity = graycoprops(glcm, 'dissimilarity')
        homogeneity = graycoprops(glcm, 'homogeneity')
        energy = graycoprops(glcm, 'energy')
        correlation = graycoprops(glcm, 'correlation')
        
        return {
            'contrast': float(np.mean(contrast)),
            'dissimilarity': float(np.mean(dissimilarity)),
            'homogeneity': float(np.mean(homogeneity)),
            'energy': float(np.mean(energy)),
            'correlation': float(np.mean(correlation)),
            'contrast_std': float(np.std(contrast))
        }
    
    def extract_frequency_features(self, image):
        """Extract frequency domain features"""
        # FFT
        fft = np.fft.fft2(image)
        fft_shift = np.fft.fftshift(fft)
        magnitude = np.abs(fft_shift)
        
        # Divide into frequency bands
        h, w = magnitude.shape
        center_y, center_x = h // 2, w // 2
        
        # Low frequency (center)
        low_freq = magnitude[
            center_y - h//8:center_y + h//8,
            center_x - w//8:center_x + w//8
        ]
        
        # High frequency (edges)
        mask = np.ones_like(magnitude)
        mask[center_y - h//8:center_y + h//8, center_x - w//8:center_x + w//8] = 0
        high_freq = magnitude * mask
        
        # Calculate statistics
        return {
            'low_freq_energy': float(np.mean(low_freq)),
            'high_freq_energy': float(np.mean(high_freq[high_freq > 0])),
            'freq_ratio': float(np.mean(low_freq) / (np.mean(high_freq[high_freq > 0]) + 1e-10)),
            'spectral_flatness': float(self._spectral_flatness(magnitude)),
            'spectral_centroid': float(self._spectral_centroid(magnitude))
        }
    
    def extract_wavelet_features(self, image):
        """Extract wavelet-based features"""
        # Multilevel 2D wavelet decomposition
        coeffs = pywt.wavedec2(image, self.wavelet_type, level=self.wavelet_level)
        
        # Extract statistics from each level
        features = {}
        
        # Approximation coefficients
        approx = coeffs[0]
        features['approx_energy'] = float(np.mean(np.abs(approx)))
        features['approx_std'] = float(np.std(approx))
        
        # Detail coefficients
        detail_energies = []
        for i, (cH, cV, cD) in enumerate(coeffs[1:]):
            energy = np.mean(np.abs(cH)) + np.mean(np.abs(cV)) + np.mean(np.abs(cD))
            detail_energies.append(energy)
            features[f'detail_energy_level_{i+1}'] = float(energy)
        
        features['total_detail_energy'] = float(np.sum(detail_energies))
        
        return features
    
    def extract_statistical_features(self, image):
        """Extract statistical features"""
        return {
            'mean': float(np.mean(image)),
            'std': float(np.std(image)),
            'variance': float(np.var(image)),
            'skewness': float(self._calculate_skewness(image)),
            'kurtosis': float(self._calculate_kurtosis(image)),
            'min': float(np.min(image)),
            'max': float(np.max(image)),
            'range': float(np.ptp(image)),
            'entropy': float(self._calculate_entropy(image))
        }
    
    def extract_noise_features(self, image):
        """Extract noise characteristics"""
        # Apply different noise filters
        gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)
        noise = image - gaussian_blur
        
        # Noise statistics
        return {
            'noise_mean': float(np.mean(np.abs(noise))),
            'noise_std': float(np.std(noise)),
            'noise_power': float(np.mean(noise ** 2)),
            'snr': float(self._calculate_snr(image, noise)),
            'noise_variance': float(np.var(noise))
        }
    
    def _calculate_skewness(self, data):
        """Calculate skewness"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0
        return np.mean(((data - mean) / std) ** 3)
    
    def _calculate_kurtosis(self, data):
        """Calculate kurtosis"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0
        return np.mean(((data - mean) / std) ** 4) - 3
    
    def _calculate_entropy(self, image):
        """Calculate Shannon entropy"""
        hist, _ = np.histogram(image.flatten(), bins=256, range=(0, 256))
        hist = hist / hist.sum()
        hist = hist[hist > 0]
        return -np.sum(hist * np.log2(hist))
    
    def _spectral_flatness(self, spectrum):
        """Calculate spectral flatness"""
        geometric_mean = np.exp(np.mean(np.log(spectrum + 1e-10)))
        arithmetic_mean = np.mean(spectrum)
        return geometric_mean / (arithmetic_mean + 1e-10)
    
    def _spectral_centroid(self, spectrum):
        """Calculate spectral centroid"""
        freqs = np.arange(spectrum.shape[0])
        return np.sum(freqs * spectrum.sum(axis=1)) / (np.sum(spectrum) + 1e-10)
    
    def _calculate_snr(self, signal, noise):
        """Calculate Signal-to-Noise Ratio"""
        signal_power = np.mean(signal ** 2)
        noise_power = np.mean(noise ** 2)
        if noise_power == 0:
            return float('inf')
        return 10 * np.log10(signal_power / noise_power)
