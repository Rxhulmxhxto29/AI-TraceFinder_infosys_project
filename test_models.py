"""
Test script to verify both trained and untrained models work correctly
"""
import os
import sys
from modules.scanner_detector import ScannerDetector

def test_models():
    print("=" * 60)
    print("Testing Scanner Detection Models")
    print("=" * 60)
    
    # Test image path
    test_image = 'data/s11_33.tif'
    
    if not os.path.exists(test_image):
        print(f"❌ Test image not found: {test_image}")
        print("Looking for any available test images...")
        
        # Try to find any image in data folder
        if os.path.exists('data'):
            for file in os.listdir('data'):
                if file.lower().endswith(('.tif', '.jpg', '.jpeg', '.png')):
                    test_image = os.path.join('data', file)
                    print(f"✓ Found test image: {test_image}")
                    break
        
        if not os.path.exists(test_image):
            print("❌ No test images found. Please add an image to the data folder.")
            return False
    
    print(f"\nTest Image: {test_image}")
    print("-" * 60)
    
    # Initialize detector
    detector = ScannerDetector()
    
    # Check which mode is being used
    print(f"\n1. MODEL MODE CHECK:")
    print(f"   Trained Model Available: {detector.use_trained_model}")
    if detector.use_trained_model:
        print(f"   ✓ Using ML-based trained model")
        print(f"   Model Path: models/scanner_classifier.pkl")
        print(f"   Label Encoder: models/label_encoder.pkl")
        print(f"   Feature Scaler: {'models/feature_scaler.pkl' if hasattr(detector, 'feature_scaler') and detector.feature_scaler else 'Not found'}")
        print(f"   Number of Classes: {len(detector.label_encoder.classes_) if detector.label_encoder else 0}")
    else:
        print(f"   ✓ Using signature-based fallback method")
        print(f"   Available Signatures: {', '.join(detector.scanner_signatures.keys())}")
    
    # Perform analysis
    print(f"\n2. RUNNING ANALYSIS:")
    try:
        results = detector.analyze(test_image)
        
        if results['success']:
            print(f"   ✓ Analysis completed successfully")
            print(f"\n3. RESULTS:")
            print(f"   Scanner Brand: {results['scanner_brand']}")
            print(f"   Scanner Model: {results['scanner_model']}")
            print(f"   Confidence: {results['confidence']*100:.2f}%")
            print(f"   Confidence Level: {results['confidence_level']}")
            
            # Check detailed analysis
            if 'detailed_analysis' in results:
                details = results['detailed_analysis']
                print(f"\n4. DETAILED ANALYSIS:")
                
                # Primary indicators
                if 'primary_indicators' in details and details['primary_indicators']:
                    print(f"   Primary Indicators:")
                    for indicator in details['primary_indicators']:
                        print(f"      • {indicator}")
                else:
                    print(f"   ⚠ No primary indicators found")
                
                # Secondary indicators
                if 'secondary_indicators' in details and details['secondary_indicators']:
                    print(f"   Secondary Indicators:")
                    for indicator in details['secondary_indicators']:
                        print(f"      • {indicator}")
                else:
                    print(f"   ℹ No secondary indicators")
                
                # Anomalies
                if 'anomalies' in details and details['anomalies']:
                    print(f"   Anomalies:")
                    for anomaly in details['anomalies']:
                        print(f"      • {anomaly}")
                else:
                    print(f"   ⚠ No anomalies array found")
            else:
                print(f"   ⚠ No detailed_analysis found in results")
            
            # Features summary
            if 'features_summary' in results:
                print(f"\n5. FEATURES SUMMARY:")
                for feature, value in results['features_summary'].items():
                    print(f"   {feature}: {value}")
            
            print(f"\n" + "=" * 60)
            print("✓ ALL TESTS PASSED")
            print("=" * 60)
            return True
            
        else:
            print(f"   ❌ Analysis failed: {results.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_models()
    sys.exit(0 if success else 1)
