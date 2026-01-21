import numpy as np
import cv2
from modules.feature_extractor import FeatureExtractor
from modules.image_processor import ImageProcessor

class ImageComparator:
    """Compare two images to determine if they're from the same scanner"""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.image_processor = ImageProcessor()
    
    def compare_images(self, image_path1, image_path2):
        """Compare two images and calculate similarity score"""
        try:
            # Load both images
            img1 = self.image_processor.load_and_preprocess(image_path1)
            img2 = self.image_processor.load_and_preprocess(image_path2)
            
            if img1 is None or img2 is None:
                return {
                    'success': False,
                    'error': 'Failed to load one or both images'
                }
            
            # Extract features from both images
            features1 = self.feature_extractor.extract_all_features(img1)
            features2 = self.feature_extractor.extract_all_features(img2)
            
            # Calculate similarity scores
            prnu_similarity = self._compare_prnu(features1['prnu'], features2['prnu'])
            texture_similarity = self._compare_texture(features1['texture'], features2['texture'])
            frequency_similarity = self._compare_frequency(features1['frequency'], features2['frequency'])
            wavelet_similarity = self._compare_wavelet(features1['wavelet'], features2['wavelet'])
            
            # Calculate overall similarity
            weights = {
                'prnu': 0.35,
                'texture': 0.25,
                'frequency': 0.25,
                'wavelet': 0.15
            }
            
            overall_similarity = (
                prnu_similarity * weights['prnu'] +
                texture_similarity * weights['texture'] +
                frequency_similarity * weights['frequency'] +
                wavelet_similarity * weights['wavelet']
            )
            
            # Determine match status
            if overall_similarity >= 0.85:
                match_status = 'High Probability - Same Scanner'
                match_confidence = 'Very High'
            elif overall_similarity >= 0.70:
                match_status = 'Likely - Same Scanner'
                match_confidence = 'High'
            elif overall_similarity >= 0.50:
                match_status = 'Possible - Similar Scanner Type'
                match_confidence = 'Medium'
            else:
                match_status = 'Unlikely - Different Scanners'
                match_confidence = 'Low'
            
            return {
                'success': True,
                'overall_similarity': round(overall_similarity * 100, 2),
                'match_status': match_status,
                'match_confidence': match_confidence,
                'detailed_scores': {
                    'prnu_similarity': round(prnu_similarity * 100, 2),
                    'texture_similarity': round(texture_similarity * 100, 2),
                    'frequency_similarity': round(frequency_similarity * 100, 2),
                    'wavelet_similarity': round(wavelet_similarity * 100, 2)
                },
                'analysis': self._generate_comparison_analysis(
                    overall_similarity, 
                    prnu_similarity,
                    texture_similarity,
                    frequency_similarity,
                    wavelet_similarity
                )
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Comparison failed: {str(e)}'
            }
    
    def _compare_prnu(self, prnu1, prnu2):
        """Compare PRNU patterns using correlation"""
        try:
            # Calculate correlation between PRNU patterns
            correlation = np.corrcoef(prnu1['pattern'].flatten(), prnu2['pattern'].flatten())[0, 1]
            
            # Compare statistics
            mean_diff = abs(prnu1['mean'] - prnu2['mean'])
            std_diff = abs(prnu1['std'] - prnu2['std'])
            
            # Normalize differences
            mean_similarity = 1.0 - min(mean_diff / 0.1, 1.0)
            std_similarity = 1.0 - min(std_diff / 0.02, 1.0)
            
            # Combine scores
            similarity = (abs(correlation) * 0.6 + mean_similarity * 0.2 + std_similarity * 0.2)
            return max(0.0, min(1.0, similarity))
            
        except:
            return 0.0
    
    def _compare_texture(self, tex1, tex2):
        """Compare texture features"""
        try:
            # Compare GLCM properties
            properties = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation']
            similarities = []
            
            for prop in properties:
                if prop in tex1 and prop in tex2:
                    val1 = tex1[prop]
                    val2 = tex2[prop]
                    max_val = max(abs(val1), abs(val2), 0.001)
                    diff = abs(val1 - val2) / max_val
                    similarity = 1.0 - min(diff, 1.0)
                    similarities.append(similarity)
            
            return np.mean(similarities) if similarities else 0.0
            
        except:
            return 0.0
    
    def _compare_frequency(self, freq1, freq2):
        """Compare frequency domain features"""
        try:
            # Compare frequency ratios
            ratio_diff = abs(freq1['low_high_ratio'] - freq2['low_high_ratio'])
            ratio_similarity = 1.0 - min(ratio_diff / 5.0, 1.0)
            
            # Compare dominant frequencies
            dom_freq_diff = abs(freq1['dominant_frequency'] - freq2['dominant_frequency'])
            freq_similarity = 1.0 - min(dom_freq_diff / 100.0, 1.0)
            
            return (ratio_similarity * 0.6 + freq_similarity * 0.4)
            
        except:
            return 0.0
    
    def _compare_wavelet(self, wav1, wav2):
        """Compare wavelet features"""
        try:
            similarities = []
            
            for level in ['cA', 'cH', 'cV', 'cD']:
                if level in wav1 and level in wav2:
                    energy_diff = abs(wav1[level]['energy'] - wav2[level]['energy'])
                    energy_similarity = 1.0 - min(energy_diff / 1000.0, 1.0)
                    similarities.append(energy_similarity)
            
            return np.mean(similarities) if similarities else 0.0
            
        except:
            return 0.0
    
    def _generate_comparison_analysis(self, overall, prnu, texture, frequency, wavelet):
        """Generate detailed analysis text"""
        analysis = []
        
        if prnu >= 0.8:
            analysis.append("Strong PRNU pattern match indicates same sensor")
        elif prnu >= 0.6:
            analysis.append("Moderate PRNU similarity suggests similar scanner type")
        else:
            analysis.append("Low PRNU correlation indicates different scanners")
        
        if texture >= 0.7:
            analysis.append("Consistent texture characteristics across both scans")
        
        if frequency >= 0.7:
            analysis.append("Matching frequency signatures detected")
        
        if overall >= 0.85:
            analysis.append("Multiple indicators strongly support same scanner origin")
        elif overall < 0.5:
            analysis.append("Significant differences suggest different scanner devices")
        
        return analysis
