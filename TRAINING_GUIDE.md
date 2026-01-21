# TraceFinder - Model Training Guide

## Training with Your Dataset

### Step 1: Prepare Your CSV Dataset

Your CSV file should have this format:

```csv
image_path,scanner_brand,scanner_model
dataset/canon1.jpg,Canon,LiDE 300
dataset/canon2.jpg,Canon,LiDE 300
dataset/epson1.jpg,Epson,V600
dataset/epson2.jpg,Epson,V600
dataset/hp1.jpg,HP,ScanJet Pro 2500
```

**Required columns:**
- `image_path`: Path to scanned image (relative or absolute)
- `scanner_model`: Scanner brand and model (e.g., "Canon LiDE 300")

**Optional column:**
- `scanner_brand`: Just the brand name (e.g., "Canon")

### Step 2: Organize Your Images

Place all your scanned images in a folder:
```
C:\TraceFinder\dataset\
├── canon1.jpg
├── canon2.jpg
├── epson1.jpg
├── hp1.jpg
└── ...
```

### Step 3: Run Training

**Option A: Using command line**
```bash
cd C:\TraceFinder
python modules\model_trainer.py dataset.csv dataset/
```

**Option B: Using Python script**
```python
from modules.model_trainer import train_from_csv

# Train model
trainer = train_from_csv(
    csv_path='dataset.csv',
    image_base_path='dataset/',  # Base path for images
    output_dir='models'
)
```

### Step 4: Training Output

The training will:
1. ✓ Load your CSV dataset
2. ✓ Extract forensic features from all images
3. ✓ Train Random Forest classifier
4. ✓ Evaluate accuracy on test set
5. ✓ Save trained model to `models/` directory

**Generated files:**
- `models/scanner_classifier.pkl` - Trained model
- `models/label_encoder.pkl` - Label encoder
- `models/training_history.json` - Training metrics

### Step 5: Use Trained Model

The system will automatically use your trained model! Just restart the server:
```bash
python app.py
```

## CSV Examples

### Example 1: Simple Format
```csv
image_path,scanner_model
images/scan1.jpg,Canon LiDE 300
images/scan2.jpg,Epson V600
images/scan3.jpg,HP ScanJet Pro 2500
```

### Example 2: With Brand Column
```csv
image_path,scanner_brand,scanner_model
data/001.png,Canon,Canon LiDE 300
data/002.png,Canon,Canon LiDE 400
data/003.png,Epson,Epson Perfection V600
data/004.png,HP,HP ScanJet Pro 2500
```

### Example 3: Absolute Paths
```csv
image_path,scanner_model
C:/Users/Data/Scans/canon_001.jpg,Canon LiDE 300
C:/Users/Data/Scans/epson_001.jpg,Epson V600
C:/Users/Data/Scans/hp_001.jpg,HP ScanJet Pro 2500
```

## Dataset Requirements

**Minimum requirements:**
- At least **50 images per scanner model**
- At least **3 different scanner models**
- High-quality scans (300+ DPI recommended)
- Unedited/uncompressed images preferred

**Optimal dataset:**
- 100-200 images per scanner model
- 5-10 different scanner models
- Mix of document types (text, images, mixed)
- Various scan settings (color, grayscale, B&W)

## Troubleshooting

**Error: "Column 'image_path' not found"**
- Check your CSV column names match exactly
- Use `image_path` and `scanner_model` as column names

**Error: "Image not found"**
- Verify image paths in CSV are correct
- Use `image_base_path` parameter to specify base directory

**Low accuracy (<70%)**
- Need more training data (add more images)
- Ensure images are from different scanners
- Check image quality

**Training is slow**
- Normal for large datasets (1000+ images)
- Can take 5-30 minutes depending on dataset size

## Expected Accuracy

- **50-100 images per class**: 70-85% accuracy
- **100-200 images per class**: 85-92% accuracy  
- **200+ images per class**: 90-95%+ accuracy

## Need Help?

Check:
1. CSV format matches examples above
2. All image files exist and are accessible
3. Images are valid scanner outputs (not camera photos)
4. At least 50 images per scanner model

---

**Ready to train? Place your CSV file and run:**
```bash
python modules\model_trainer.py your_dataset.csv path/to/images/
```
