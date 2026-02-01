"""
Test script to verify all supported image formats work correctly
"""
import os
import sys
from modules.scanner_detector import ScannerDetector
from config import Config
import cv2
import numpy as np

def test_image_formats():
    print("=" * 60)
    print("Testing Image Format Support")
    print("=" * 60)
    
    # Show configured allowed extensions
    print(f"\nConfigured Allowed Extensions:")
    print(f"   {', '.join(sorted(Config.ALLOWED_EXTENSIONS))}")
    
    # Find test images in data folder
    test_images = []
    if os.path.exists('data'):
        for file in os.listdir('data'):
            ext = file.split('.')[-1].lower()
            if ext in Config.ALLOWED_EXTENSIONS:
                test_images.append(os.path.join('data', file))
    
    # Also check static/uploads
    if os.path.exists('static/uploads'):
        for file in os.listdir('static/uploads'):
            ext = file.split('.')[-1].lower()
            if ext in Config.ALLOWED_EXTENSIONS and file != '.gitkeep':
                test_images.append(os.path.join('static/uploads', file))
    
    if not test_images:
        print("\n❌ No test images found in data/ or static/uploads/")
        print("Please add test images to test different formats.")
        return False
    
    print(f"\nFound {len(test_images)} test image(s):")
    for img in test_images:
        ext = img.split('.')[-1].lower()
        size = os.path.getsize(img)
        print(f"   • {os.path.basename(img)} ({ext.upper()}, {size:,} bytes)")
    
    # Initialize detector
    detector = ScannerDetector()
    print(f"\nModel Mode: {'Trained ML Model' if detector.use_trained_model else 'Signature-based Fallback'}")
    
    # Test each image format
    print("\n" + "=" * 60)
    print("Testing Each Image Format:")
    print("=" * 60)
    
    results_summary = []
    
    for test_image in test_images:
        ext = test_image.split('.')[-1].upper()
        basename = os.path.basename(test_image)
        
        print(f"\n{ext} Format Test: {basename}")
        print("-" * 60)
        
        try:
            # Test if OpenCV can read it
            img = cv2.imread(test_image)
            if img is None:
                print(f"   ❌ OpenCV cannot read {ext} file")
                results_summary.append({
                    'format': ext,
                    'file': basename,
                    'opencv_read': False,
                    'analysis': False,
                    'error': 'OpenCV failed to read'
                })
                continue
            
            print(f"   ✓ OpenCV can read {ext} format")
            print(f"   Image dimensions: {img.shape[1]}x{img.shape[0]} pixels")
            
            # Test analysis
            results = detector.analyze(test_image)
            
            if results['success']:
                print(f"   ✓ Analysis completed successfully")
                print(f"   Scanner: {results['scanner_brand']} {results['scanner_model']}")
                print(f"   Confidence: {results['confidence']*100:.2f}%")
                
                # Check if detailed analysis is present
                has_details = 'detailed_analysis' in results
                has_anomalies = has_details and 'anomalies' in results['detailed_analysis']
                
                print(f"   Detailed Analysis: {'✓' if has_details else '❌'}")
                print(f"   Anomalies Detection: {'✓' if has_anomalies else '❌'}")
                
                results_summary.append({
                    'format': ext,
                    'file': basename,
                    'opencv_read': True,
                    'analysis': True,
                    'scanner': f"{results['scanner_brand']} {results['scanner_model']}",
                    'confidence': f"{results['confidence']*100:.1f}%",
                    'has_details': has_details,
                    'has_anomalies': has_anomalies
                })
            else:
                print(f"   ❌ Analysis failed: {results.get('error', 'Unknown error')}")
                results_summary.append({
                    'format': ext,
                    'file': basename,
                    'opencv_read': True,
                    'analysis': False,
                    'error': results.get('error', 'Unknown error')
                })
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
            results_summary.append({
                'format': ext,
                'file': basename,
                'opencv_read': False,
                'analysis': False,
                'error': str(e)
            })
    
    # Summary table
    print("\n" + "=" * 60)
    print("SUMMARY TABLE")
    print("=" * 60)
    print(f"{'Format':<8} {'OpenCV':<8} {'Analysis':<10} {'Details':<8} {'Anomalies':<10}")
    print("-" * 60)
    
    all_passed = True
    for result in results_summary:
        opencv_status = '✓' if result.get('opencv_read') else '❌'
        analysis_status = '✓' if result.get('analysis') else '❌'
        details_status = '✓' if result.get('has_details') else '❌'
        anomalies_status = '✓' if result.get('has_anomalies') else '❌'
        
        print(f"{result['format']:<8} {opencv_status:<8} {analysis_status:<10} {details_status:<8} {anomalies_status:<10}")
        
        if not (result.get('opencv_read') and result.get('analysis') and 
                result.get('has_details') and result.get('has_anomalies')):
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("✓ ALL FORMAT TESTS PASSED")
        print("All supported formats work correctly with full analysis!")
    else:
        print("⚠ SOME TESTS FAILED")
        print("Check the detailed results above for specific issues.")
    
    print("=" * 60)
    return all_passed

if __name__ == '__main__':
    success = test_image_formats()
    sys.exit(0 if success else 1)
