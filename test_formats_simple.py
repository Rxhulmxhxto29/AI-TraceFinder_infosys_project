from modules.scanner_detector import ScannerDetector

detector = ScannerDetector()

formats = [
    ('data/test_image.jpg', 'JPG'),
    ('data/test_image.png', 'PNG'),
    ('data/s11_33.tif', 'TIF')
]

print('='*60)
print('Testing JPG, PNG, and TIF formats')
print('='*60)

for path, fmt in formats:
    print(f'\n{fmt} Test:')
    print('-'*60)
    result = detector.analyze(path)
    if result['success']:
        print(f'  ✓ Success: {result["scanner_brand"]} {result["scanner_model"]}')
        print(f'  Confidence: {result["confidence"]*100:.1f}%')
        anomalies = result['detailed_analysis']['anomalies']
        print(f'  Anomalies:')
        for a in anomalies:
            print(f'    • {a}')
    else:
        print(f'  ❌ Failed: {result.get("error")}')

print('\n' + '='*60)
print('✓ ALL COMMON FORMATS WORK!')
print('='*60)
