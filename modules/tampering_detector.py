import numpy as np
import cv2
from PIL import Image
import io

class TamperingDetector:
    """Detect image manipulation and tampering"""
    
    def __init__(self):
        pass
    
    def detect_tampering(self, image_path):
        """Detect various types of image tampering"""
        try:
            results = {
                'success': True,
                'tampering_detected': False,
                'confidence': 0.0,
                'indicators': [],
                'techniques': {}
            }
            
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                return {'success': False, 'error': 'Failed to load image'}
            
            # Run various tampering detection techniques
            ela_result = self._error_level_analysis(image_path)
            noise_result = self._noise_consistency_analysis(img)
            jpeg_result = self._jpeg_ghost_analysis(image_path)
            metadata_result = self._metadata_analysis(image_path)
            
            # Combine results
            results['techniques'] = {
                'error_level_analysis': ela_result,
                'noise_consistency': noise_result,
                'jpeg_artifacts': jpeg_result,
                'metadata_check': metadata_result
            }
            
            # Calculate overall tampering confidence
            indicators_count = 0
            if ela_result['suspicious']: 
                indicators_count += 1
                results['indicators'].append('Inconsistent compression levels detected')
            
            if noise_result['suspicious']:
                indicators_count += 1
                results['indicators'].append('Noise pattern inconsistencies found')
            
            if jpeg_result['suspicious']:
                indicators_count += 1
                results['indicators'].append('JPEG ghost artifacts present')
            
            if metadata_result['suspicious']:
                indicators_count += 1
                results['indicators'].append('Metadata anomalies detected')
            
            # Determine tampering status
            results['confidence'] = float((indicators_count / 4.0) * 100)
            results['tampering_detected'] = bool(indicators_count >= 2)
            
            if results['tampering_detected']:
                results['verdict'] = 'Tampering Likely'
                results['risk_level'] = 'High' if indicators_count >= 3 else 'Medium'
            else:
                results['verdict'] = 'No Tampering Detected' if indicators_count == 0 else 'Uncertain'
                results['risk_level'] = 'Low'
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Tampering detection failed: {str(e)}'
            }
    
    def _error_level_analysis(self, image_path):
        """Error Level Analysis (ELA) - detects different compression levels"""
        try:
            # Load original image
            original = Image.open(image_path)
            
            # Resave at known quality
            temp_buffer = io.BytesIO()
            original.save(temp_buffer, 'JPEG', quality=90)
            temp_buffer.seek(0)
            
            # Load resaved image
            resaved = Image.open(temp_buffer)
            
            # Convert to numpy arrays
            orig_arr = np.array(original.convert('RGB'))
            resaved_arr = np.array(resaved.convert('RGB'))
            
            # Calculate difference
            diff = cv2.absdiff(orig_arr, resaved_arr)
            
            # Calculate statistics
            mean_diff = np.mean(diff)
            std_diff = np.std(diff)
            max_diff = np.max(diff)
            
            # Detect suspicious regions (areas with unusually high/low error)
            suspicious = std_diff > 15 or (max_diff > 100 and mean_diff < 10)
            
            return {
                'suspicious': bool(suspicious),
                'mean_error': float(mean_diff),
                'std_error': float(std_diff),
                'max_error': float(max_diff),
                'analysis': 'Inconsistent error levels suggest potential editing' if suspicious else 'Normal error distribution'
            }
            
        except Exception as e:
            return {'suspicious': False, 'error': str(e)}
    
    def _noise_consistency_analysis(self, img):
        """Analyze noise pattern consistency across image"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
            
            # Divide image into regions
            h, w = gray.shape
            regions = []
            region_size = 64
            
            for i in range(0, h - region_size, region_size):
                for j in range(0, w - region_size, region_size):
                    region = gray[i:i+region_size, j:j+region_size]
                    
                    # Apply high-pass filter to isolate noise
                    blurred = cv2.GaussianBlur(region, (5, 5), 0)
                    noise = cv2.absdiff(region, blurred)
                    
                    # Calculate noise statistics
                    noise_std = np.std(noise)
                    regions.append(noise_std)
            
            # Check for consistency
            if len(regions) > 0:
                mean_noise = np.mean(regions)
                std_noise = np.std(regions)
                
                # Suspicious if noise varies significantly across regions
                variation_coefficient = std_noise / mean_noise if mean_noise > 0 else 0
                suspicious = variation_coefficient > 0.4
                
                return {
                    'suspicious': bool(suspicious),
                    'variation_coefficient': float(variation_coefficient),
                    'mean_noise_level': float(mean_noise),
                    'analysis': 'Inconsistent noise patterns across image' if suspicious else 'Consistent noise distribution'
                }
            
            return {'suspicious': False, 'analysis': 'Unable to analyze noise patterns'}
            
        except Exception as e:
            return {'suspicious': False, 'error': str(e)}
    
    def _jpeg_ghost_analysis(self, image_path):
        """Detect JPEG ghosts indicating re-compression"""
        try:
            img = Image.open(image_path)
            
            # Save at different quality levels and compare
            qualities = [95, 90, 85, 80, 75]
            ghost_scores = []
            
            for quality in qualities:
                temp_buffer = io.BytesIO()
                img.save(temp_buffer, 'JPEG', quality=quality)
                temp_buffer.seek(0)
                
                compressed = Image.open(temp_buffer)
                
                # Calculate difference
                orig_arr = np.array(img.convert('RGB'))
                comp_arr = np.array(compressed.convert('RGB'))
                diff = cv2.absdiff(orig_arr, comp_arr)
                
                ghost_scores.append(np.mean(diff))
            
            # Look for plateau in ghost scores (indicates previous compression at that level)
            ghost_scores_arr = np.array(ghost_scores)
            diffs = np.diff(ghost_scores_arr)
            
            # Suspicious if there's a significant plateau
            suspicious = np.min(diffs) < 0.5 and np.max(diffs) > 2.0
            
            return {
                'suspicious': bool(suspicious),
                'ghost_scores': [float(x) for x in ghost_scores],
                'analysis': 'JPEG ghost detected - image likely re-compressed' if suspicious else 'No significant JPEG ghosts'
            }
            
        except Exception as e:
            return {'suspicious': False, 'error': str(e)}
    
    def _metadata_analysis(self, image_path):
        """Check metadata for inconsistencies"""
        try:
            from PIL.ExifTags import TAGS
            
            img = Image.open(image_path)
            exif = img._getexif()
            
            if not exif:
                return {
                    'suspicious': False,
                    'analysis': 'No EXIF metadata found'
                }
            
            suspicious_indicators = []
            
            # Check for common editing software signatures
            software_tags = []
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag in ['Software', 'ProcessingSoftware']:
                    software_tags.append(str(value).lower())
            
            editing_software = ['photoshop', 'gimp', 'paint.net', 'pixlr', 'affinity']
            for sw in software_tags:
                if any(edit_sw in sw for edit_sw in editing_software):
                    suspicious_indicators.append(f'Edited with: {sw}')
            
            # Check for metadata manipulation
            if 'DateTime' in [TAGS.get(tag_id) for tag_id in exif.keys()]:
                suspicious_indicators.append('Date/time metadata present but may be modified')
            
            suspicious = len(suspicious_indicators) > 0
            
            return {
                'suspicious': bool(suspicious),
                'indicators': suspicious_indicators,
                'analysis': '; '.join(suspicious_indicators) if suspicious else 'No metadata anomalies'
            }
            
        except Exception as e:
            return {'suspicious': False, 'error': str(e)}
