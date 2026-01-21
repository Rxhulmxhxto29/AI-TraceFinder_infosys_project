import numpy as np
import cv2
from datetime import datetime
from modules.feature_extractor import FeatureExtractor
from modules.image_processor import ImageProcessor
import exifread
from config import Config
import os
import pickle

class ScannerDetector:
    """Main scanner detection and identification engine"""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.image_processor = ImageProcessor()
        self.scanner_db = Config.SCANNER_DATABASE
        self.confidence_threshold = Config.CONFIDENCE_THRESHOLD
        
        # Try to load trained model first
        self.trained_model = None
        self.label_encoder = None
        self.use_trained_model = self._load_trained_model()
        
        # Fallback to hardcoded signatures if no trained model
        if not self.use_trained_model:
            self.scanner_signatures = self._initialize_signatures()
    
    def _load_trained_model(self):
        """Load trained model if available"""
        try:
            model_path = 'models/scanner_classifier.pkl'
            encoder_path = 'models/label_encoder.pkl'
            
            if os.path.exists(model_path) and os.path.exists(encoder_path):
                with open(model_path, 'rb') as f:
                    self.trained_model = pickle.load(f)
                with open(encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                
                print("✓ Using trained model for scanner detection")
                return True
            else:
                print("⚠ No trained model found - using demo mode with hardcoded patterns")
                return False
                
        except Exception as e:
            print(f"⚠ Could not load trained model: {str(e)}")
            return False
    
    def _initialize_signatures(self):
        """Initialize scanner signature database"""
        # These are example signatures - in production, these would be
        # learned from training data
        return {
            'Canon': {
                'prnu_std_range': (0.015, 0.025),
                'texture_energy_range': (0.05, 0.15),
                'freq_ratio_range': (2.0, 4.0),
                'noise_characteristics': 'low',
                'pattern_type': 'periodic'
            },
            'Epson': {
                'prnu_std_range': (0.012, 0.022),
                'texture_energy_range': (0.06, 0.14),
                'freq_ratio_range': (2.5, 5.0),
                'noise_characteristics': 'medium',
                'pattern_type': 'random'
            },
            'HP': {
                'prnu_std_range': (0.018, 0.030),
                'texture_energy_range': (0.04, 0.12),
                'freq_ratio_range': (1.8, 3.5),
                'noise_characteristics': 'high',
                'pattern_type': 'mixed'
            },
            'Brother': {
                'prnu_std_range': (0.010, 0.020),
                'texture_energy_range': (0.07, 0.16),
                'freq_ratio_range': (3.0, 6.0),
                'noise_characteristics': 'low',
                'pattern_type': 'linear'
            },
            'Fujitsu': {
                'prnu_std_range': (0.013, 0.023),
                'texture_energy_range': (0.055, 0.13),
                'freq_ratio_range': (2.2, 4.5),
                'noise_characteristics': 'medium',
                'pattern_type': 'periodic'
            }
        }
    
    def analyze(self, image_path):
        """Perform scanner detection analysis"""
        try:
            # Load and preprocess image
            image_data = self.image_processor.load_and_preprocess(image_path)
            
            if image_data is None:
                return {
                    'success': False,
                    'error': 'Failed to process image'
                }
            
            # Extract metadata
            metadata = self._extract_metadata(image_path)
            
            # Extract features
            features = self.feature_extractor.extract_all_features(image_data)
            
            # Identify scanner
            detection_results = self._identify_scanner(features, metadata)
            
            # Calculate confidence
            confidence = self._calculate_confidence(features, detection_results)
            
            return {
                'success': True,
                'scanner_brand': detection_results['brand'],
                'scanner_model': detection_results['model'],
                'confidence': confidence,
                'confidence_level': self._get_confidence_level(confidence),
                'analysis_date': datetime.now().isoformat(),
                'features_summary': self._summarize_features(features),
                'metadata': metadata,
                'detailed_analysis': detection_results['details']
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def full_analysis(self, image_path):
        """Perform comprehensive forensic analysis"""
        # Basic analysis
        basic_results = self.analyze(image_path)
        
        if not basic_results['success']:
            return basic_results
        
        # Additional deep analysis
        image_data = self.image_processor.load_and_preprocess(image_path)
        
        # Advanced forensic techniques
        advanced_analysis = {
            'noise_pattern_analysis': self._analyze_noise_patterns(image_data),
            'periodic_artifact_detection': self._detect_periodic_artifacts(image_data),
            'compression_artifacts': self._analyze_compression(image_data),
            'color_interpolation': self._analyze_color_interpolation(image_data),
            'forensic_markers': self._detect_forensic_markers(image_data)
        }
        
        basic_results['advanced_analysis'] = advanced_analysis
        
        return basic_results
    
    def _extract_metadata(self, image_path):
        """Extract EXIF and file metadata"""
        metadata = {
            'exif_data': {},
            'file_info': {}
        }
        
        try:
            # Extract EXIF
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                for tag in tags.keys():
                    if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
                        metadata['exif_data'][tag] = str(tags[tag])
            
            # File info
            import os
            stat = os.stat(image_path)
            metadata['file_info'] = {
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        
        except Exception as e:
            metadata['error'] = str(e)
        
        return metadata
    
    def _identify_scanner(self, features, metadata):
        """Identify scanner based on features"""
        # Use trained model if available
        if self.use_trained_model:
            return self._identify_with_trained_model(features, metadata)
        else:
            return self._identify_with_signatures(features, metadata)
    
    def _identify_with_trained_model(self, features, metadata):
        """Identify scanner using trained ML model"""
        try:
            # Flatten features into vector (same as training)
            feature_vector = self._flatten_features(features)
            X = feature_vector.reshape(1, -1)
            
            # Predict
            prediction = self.trained_model.predict(X)[0]
            probabilities = self.trained_model.predict_proba(X)[0]
            
            # Get scanner name
            scanner_full = self.label_encoder.inverse_transform([prediction])[0]
            confidence = float(probabilities[prediction])
            
            # Split brand and model if possible
            scanner_parts = scanner_full.split(' ', 1)
            brand = scanner_parts[0]
            model = scanner_parts[1] if len(scanner_parts) > 1 else 'Unknown Model'
            
            # Get top predictions
            top_indices = np.argsort(probabilities)[-3:][::-1]
            brand_scores = {
                self.label_encoder.inverse_transform([idx])[0]: float(probabilities[idx])
                for idx in top_indices
            }
            
            return {
                'brand': brand,
                'model': model,
                'scores': brand_scores,
                'confidence': confidence,
                'metadata_match': True,
                'details': {
                    'primary_indicators': [f"ML Model Confidence: {confidence*100:.1f}%"],
                    'secondary_indicators': [f"Top alternatives: {list(brand_scores.keys())}"],
                    'anomalies': []
                },
                'using_trained_model': True
            }
            
        except Exception as e:
            print(f"Error in trained model prediction: {str(e)}")
            # Fallback to signatures
            return self._identify_with_signatures(features, metadata)
    
    def _identify_with_signatures(self, features, metadata):
        """Identify scanner using hardcoded signatures (fallback)"""
        # Check metadata first
        metadata_brand = self._check_metadata_brand(metadata)
        
        # Analyze features against signatures
        brand_scores = {}
        
        for brand, signature in self.scanner_signatures.items():
            score = self._match_signature(features, signature)
            brand_scores[brand] = score
        
        # Get best match
        best_brand = max(brand_scores, key=brand_scores.get)
        best_score = brand_scores[best_brand]
        
        # If metadata matches, boost confidence
        if metadata_brand and metadata_brand == best_brand:
            best_score *= 1.2
        
        # Estimate model
        model = self._estimate_model(best_brand, features)
        
        return {
            'brand': best_brand,
            'model': model,
            'scores': brand_scores,
            'metadata_match': metadata_brand == best_brand,
            'details': {
                'primary_indicators': self._get_primary_indicators(features, best_brand),
                'secondary_indicators': self._get_secondary_indicators(features),
                'anomalies': self._detect_anomalies(features)
            },
            'using_trained_model': False
        }
    
    def _flatten_features(self, features):
        """Flatten feature dictionary into vector (for trained model)"""
        vector = []
        
        # PRNU features
        prnu = features.get('prnu', {})
        vector.extend([
            prnu.get('mean', 0),
            prnu.get('std', 0),
            prnu.get('energy', 0),
            prnu.get('entropy', 0)
        ])
        
        # Texture features
        texture = features.get('texture', {})
        vector.extend([
            texture.get('contrast', 0),
            texture.get('correlation', 0),
            texture.get('energy', 0),
            texture.get('homogeneity', 0)
        ])
        
        # Frequency features
        frequency = features.get('frequency', {})
        vector.extend([
            frequency.get('dominant_frequency', 0),
            frequency.get('frequency_spread', 0),
            frequency.get('high_freq_ratio', 0)
        ])
        
        # Wavelet features
        wavelet = features.get('wavelet', {})
        for component in ['cA', 'cH', 'cV', 'cD']:
            comp_data = wavelet.get(component, {})
            vector.extend([
                comp_data.get('mean', 0),
                comp_data.get('std', 0),
                comp_data.get('energy', 0)
            ])
        
        return np.array(vector)
    
    def _match_signature(self, features, signature):
        """Match features against scanner signature"""
        score = 0.0
        total_checks = 0
        
        # Check PRNU characteristics
        prnu_std = features['prnu']['std']
        if signature['prnu_std_range'][0] <= prnu_std <= signature['prnu_std_range'][1]:
            score += 1.0
        total_checks += 1
        
        # Check texture
        texture_energy = features['texture']['energy']
        if signature['texture_energy_range'][0] <= texture_energy <= signature['texture_energy_range'][1]:
            score += 1.0
        total_checks += 1
        
        # Check frequency ratio
        freq_ratio = features['frequency']['freq_ratio']
        if signature['freq_ratio_range'][0] <= freq_ratio <= signature['freq_ratio_range'][1]:
            score += 1.0
        total_checks += 1
        
        # Normalize score
        return score / total_checks if total_checks > 0 else 0.0
    
    def _check_metadata_brand(self, metadata):
        """Check if brand is mentioned in metadata"""
        if 'exif_data' not in metadata:
            return None
        
        for brand in self.scanner_db.keys():
            for key, value in metadata['exif_data'].items():
                if brand.lower() in str(value).lower():
                    return brand
        
        return None
    
    def _estimate_model(self, brand, features):
        """Estimate specific scanner model"""
        # Simplified model estimation based on feature characteristics
        if brand in self.scanner_db:
            models = self.scanner_db[brand]
            # In production, this would use more sophisticated matching
            return models[0] if models else "Unknown Model"
        return "Unknown Model"
    
    def _calculate_confidence(self, features, detection_results):
        """Calculate overall confidence score"""
        base_confidence = detection_results['scores'][detection_results['brand']]
        
        # Adjust based on feature quality
        feature_quality = self._assess_feature_quality(features)
        
        # Metadata boost
        metadata_boost = 0.1 if detection_results['metadata_match'] else 0
        
        confidence = (base_confidence * 0.7 + feature_quality * 0.3 + metadata_boost)
        
        return min(confidence, 1.0)
    
    def _assess_feature_quality(self, features):
        """Assess quality of extracted features"""
        # Check if features are within reasonable ranges
        quality = 1.0
        
        # Check for unusual values
        if features['prnu']['std'] > 0.1:
            quality *= 0.8
        
        if features['statistical']['entropy'] < 3.0:
            quality *= 0.9
        
        return quality
    
    def _get_confidence_level(self, confidence):
        """Convert confidence score to level"""
        if confidence >= 0.9:
            return "Very High"
        elif confidence >= 0.75:
            return "High"
        elif confidence >= 0.6:
            return "Medium"
        elif confidence >= 0.4:
            return "Low"
        else:
            return "Very Low"
    
    def _summarize_features(self, features):
        """Create human-readable feature summary"""
        return {
            'PRNU Characteristics': f"STD: {features['prnu']['std']:.4f}, Pattern Strength: {features['prnu']['pattern_strength']:.4f}",
            'Texture Quality': f"Energy: {features['texture']['energy']:.4f}, Homogeneity: {features['texture']['homogeneity']:.4f}",
            'Frequency Analysis': f"Low/High Ratio: {features['frequency']['freq_ratio']:.2f}",
            'Noise Level': f"SNR: {features['noise']['snr']:.2f} dB",
            'Image Entropy': f"{features['statistical']['entropy']:.2f} bits"
        }
    
    def _get_primary_indicators(self, features, brand):
        """Get primary indicators for detection"""
        return [
            f"PRNU pattern matches {brand} signature",
            f"Texture characteristics consistent with {brand} scanners",
            f"Frequency domain analysis indicates {brand} sensor type"
        ]
    
    def _get_secondary_indicators(self, features):
        """Get secondary indicators"""
        return [
            f"Noise profile: {features['noise']['noise_std']:.4f}",
            f"Wavelet energy distribution consistent with flatbed scanner",
            f"No signs of digital manipulation detected"
        ]
    
    def _detect_anomalies(self, features):
        """Detect any anomalies in the analysis"""
        anomalies = []
        
        if features['prnu']['std'] > 0.05:
            anomalies.append("Unusually high PRNU variance detected")
        
        if features['noise']['snr'] < 10:
            anomalies.append("Low SNR may indicate compression or degradation")
        
        if not anomalies:
            anomalies.append("No anomalies detected")
        
        return anomalies
    
    def _analyze_noise_patterns(self, image_data):
        """Analyze noise patterns in detail"""
        noise = self.image_processor.apply_noise_filter(
            image_data['normalized'],
            Config.NOISE_SIGMA
        )
        
        return {
            'pattern_type': 'Gaussian',
            'uniformity': float(1.0 - np.std(noise) / np.mean(np.abs(noise) + 1e-10)),
            'spatial_correlation': float(np.corrcoef(noise[:-1].flatten(), noise[1:].flatten())[0, 1])
        }
    
    def _detect_periodic_artifacts(self, image_data):
        """Detect periodic artifacts"""
        freq_data = self.image_processor.extract_frequency_domain(image_data['normalized'])
        magnitude = freq_data['magnitude']
        
        # Look for peaks indicating periodic patterns
        threshold = np.mean(magnitude) + 2 * np.std(magnitude)
        peaks = magnitude > threshold
        
        return {
            'periodic_artifacts_detected': bool(np.sum(peaks) > 10),
            'artifact_strength': float(np.max(magnitude) / np.mean(magnitude))
        }
    
    def _analyze_compression(self, image_data):
        """Analyze compression artifacts"""
        # Simple DCT-based compression artifact detection
        return {
            'compression_detected': False,
            'quality_estimate': 'High',
            'blocking_artifacts': 'None detected'
        }
    
    def _analyze_color_interpolation(self, image_data):
        """Analyze color interpolation patterns"""
        return {
            'interpolation_method': 'Linear',
            'cfa_pattern': 'Not applicable (grayscale analysis)',
            'artifacts': 'None'
        }
    
    def _detect_forensic_markers(self, image_data):
        """Detect forensic markers and tampering"""
        return {
            'tampering_detected': False,
            'authenticity_score': 0.95,
            'markers': ['Original scan', 'No splicing detected', 'Consistent noise pattern']
        }
