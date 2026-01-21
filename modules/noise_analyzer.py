import numpy as np
import cv2
from scipy import stats
import pywt

class NoiseAnalyzer:
    """Advanced noise analysis for scanner fingerprinting"""
    
    def __init__(self):
        self.noise_models = {
            'gaussian': self._gaussian_noise_model,
            'poisson': self._poisson_noise_model,
            'salt_pepper': self._salt_pepper_model
        }
    
    def analyze_noise_profile(self, image):
        """Comprehensive noise profile analysis"""
        # Ensure image is float32
        if image.dtype != np.float32:
            image = image.astype(np.float32) / 255.0
        
        # Extract noise using multiple methods
        noise_estimates = {
            'median_absolute_deviation': self._estimate_noise_mad(image),
            'wavelet_based': self._estimate_noise_wavelet(image),
            'local_variance': self._estimate_noise_local_variance(image),
            'gradient_based': self._estimate_noise_gradient(image)
        }
        
        # Analyze noise characteristics
        noise_characteristics = {
            'distribution_type': self._identify_noise_distribution(image),
            'spatial_correlation': self._compute_spatial_correlation(image),
            'frequency_characteristics': self._analyze_noise_frequency(image),
            'homogeneity': self._compute_noise_homogeneity(image),
            'estimates': noise_estimates
        }
        
        return noise_characteristics
    
    def _estimate_noise_mad(self, image):
        """Estimate noise using Median Absolute Deviation"""
        # Compute gradient
        gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(gx**2 + gy**2)
        
        # Use MAD on gradient
        median = np.median(gradient_magnitude)
        mad = np.median(np.abs(gradient_magnitude - median))
        sigma = 1.4826 * mad
        
        return float(sigma)
    
    def _estimate_noise_wavelet(self, image):
        """Estimate noise using wavelet decomposition"""
        # Use DWT to separate noise
        coeffs = pywt.dwt2(image, 'db4')
        _, (cH, cV, cD) = coeffs
        
        # Estimate noise from high-frequency components
        sigma = np.median(np.abs(cD)) / 0.6745
        
        return float(sigma)
    
    def _estimate_noise_local_variance(self, image):
        """Estimate noise using local variance method"""
        # Divide image into blocks
        block_size = 8
        h, w = image.shape
        
        variances = []
        for i in range(0, h - block_size, block_size):
            for j in range(0, w - block_size, block_size):
                block = image[i:i+block_size, j:j+block_size]
                variances.append(np.var(block))
        
        # Use minimum variance as noise estimate
        if variances:
            noise_variance = np.percentile(variances, 5)
            return float(np.sqrt(noise_variance))
        return 0.0
    
    def _estimate_noise_gradient(self, image):
        """Estimate noise using gradient-based method"""
        # Laplacian for edge detection
        laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=3)
        
        # Noise in smooth regions
        threshold = np.percentile(np.abs(laplacian), 25)
        smooth_regions = np.abs(laplacian) < threshold
        
        if np.sum(smooth_regions) > 0:
            noise_std = np.std(laplacian[smooth_regions])
            return float(noise_std)
        return 0.0
    
    def _identify_noise_distribution(self, image):
        """Identify the type of noise distribution"""
        # Extract noise
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        noise = image - blurred
        
        # Flatten and sample
        noise_flat = noise.flatten()
        sample = np.random.choice(noise_flat, min(10000, len(noise_flat)), replace=False)
        
        # Test different distributions
        distributions = {}
        
        # Gaussian test
        _, p_gaussian = stats.normaltest(sample)
        distributions['gaussian'] = float(p_gaussian)
        
        # Laplacian test
        _, p_laplace = stats.kstest(sample, 'laplace')
        distributions['laplacian'] = float(p_laplace)
        
        # Return best fit
        best_dist = max(distributions, key=distributions.get)
        return {
            'type': best_dist,
            'confidence': distributions[best_dist],
            'all_scores': distributions
        }
    
    def _compute_spatial_correlation(self, image):
        """Compute spatial correlation of noise"""
        # Extract noise
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        noise = image - blurred
        
        # Compute autocorrelation
        correlations = []
        for offset in [1, 2, 3, 5]:
            shifted = np.roll(noise, offset, axis=0)
            corr = np.corrcoef(noise.flatten(), shifted.flatten())[0, 1]
            correlations.append(abs(corr))
        
        return {
            'mean_correlation': float(np.mean(correlations)),
            'max_correlation': float(np.max(correlations)),
            'correlations': [float(c) for c in correlations]
        }
    
    def _analyze_noise_frequency(self, image):
        """Analyze noise in frequency domain"""
        # Extract noise
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        noise = image - blurred
        
        # FFT
        fft = np.fft.fft2(noise)
        fft_shift = np.fft.fftshift(fft)
        magnitude = np.abs(fft_shift)
        
        # Analyze frequency bands
        h, w = magnitude.shape
        center_y, center_x = h // 2, w // 2
        
        # Low, mid, high frequency energy
        radius_low = min(h, w) // 8
        radius_mid = min(h, w) // 4
        
        y, x = np.ogrid[:h, :w]
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        low_freq_mask = distance < radius_low
        mid_freq_mask = (distance >= radius_low) & (distance < radius_mid)
        high_freq_mask = distance >= radius_mid
        
        return {
            'low_freq_energy': float(np.mean(magnitude[low_freq_mask])),
            'mid_freq_energy': float(np.mean(magnitude[mid_freq_mask])),
            'high_freq_energy': float(np.mean(magnitude[high_freq_mask])),
            'spectral_flatness': float(self._compute_spectral_flatness(magnitude))
        }
    
    def _compute_noise_homogeneity(self, image):
        """Compute homogeneity of noise across image"""
        # Extract noise
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        noise = image - blurred
        
        # Divide into regions
        h, w = noise.shape
        region_size = min(h, w) // 4
        
        region_stds = []
        for i in range(0, h - region_size, region_size):
            for j in range(0, w - region_size, region_size):
                region = noise[i:i+region_size, j:j+region_size]
                region_stds.append(np.std(region))
        
        # Compute homogeneity as inverse of std variance
        if len(region_stds) > 1:
            homogeneity = 1.0 / (1.0 + np.std(region_stds))
        else:
            homogeneity = 1.0
        
        return {
            'homogeneity_score': float(homogeneity),
            'region_std_variance': float(np.var(region_stds)) if region_stds else 0.0,
            'num_regions': len(region_stds)
        }
    
    def _compute_spectral_flatness(self, spectrum):
        """Compute spectral flatness measure"""
        # Avoid log(0)
        spectrum = spectrum + 1e-10
        
        geometric_mean = np.exp(np.mean(np.log(spectrum)))
        arithmetic_mean = np.mean(spectrum)
        
        flatness = geometric_mean / arithmetic_mean
        return flatness
    
    def _gaussian_noise_model(self, noise):
        """Model noise as Gaussian"""
        return {
            'mean': float(np.mean(noise)),
            'std': float(np.std(noise))
        }
    
    def _poisson_noise_model(self, noise):
        """Model noise as Poisson"""
        # Poisson parameter estimation
        mean = np.mean(noise)
        return {
            'lambda': float(mean)
        }
    
    def _salt_pepper_model(self, noise):
        """Model salt and pepper noise"""
        # Count extremes
        threshold_high = np.percentile(noise, 99)
        threshold_low = np.percentile(noise, 1)
        
        salt = np.sum(noise > threshold_high)
        pepper = np.sum(noise < threshold_low)
        total = noise.size
        
        return {
            'salt_ratio': float(salt / total),
            'pepper_ratio': float(pepper / total)
        }
    
    def compare_noise_patterns(self, noise1, noise2):
        """Compare two noise patterns for similarity"""
        # Ensure same size
        min_size = min(noise1.shape[0], noise2.shape[0], noise1.shape[1], noise2.shape[1])
        n1 = noise1[:min_size, :min_size]
        n2 = noise2[:min_size, :min_size]
        
        # Correlation
        correlation = np.corrcoef(n1.flatten(), n2.flatten())[0, 1]
        
        # Structural similarity
        from skimage.metrics import structural_similarity as ssim
        similarity = ssim(n1, n2, data_range=n1.max() - n1.min())
        
        return {
            'correlation': float(correlation),
            'structural_similarity': float(similarity),
            'match_score': float((correlation + similarity) / 2)
        }
