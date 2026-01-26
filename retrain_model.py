"""
Retrain TraceFinder Model with Available Data
"""
import os
import sys
import pandas as pd
from modules.model_trainer import ModelTrainer
from glob import glob

def main():
    print("="*70)
    print("TraceFinder - Model Retraining")
    print("="*70)
    
    # Check what data is available
    data_dir = 'data'
    available_images = glob(os.path.join(data_dir, '*.tif')) + glob(os.path.join(data_dir, '*.jpg')) + glob(os.path.join(data_dir, '*.png'))
    
    print(f"\nFound {len(available_images)} images in data/ folder")
    
    if len(available_images) < 10:
        print("\n⚠ WARNING: Not enough training data!")
        print("   Need at least 10-20 images per scanner model for proper training")
        print("\nOptions:")
        print("1. Add more training images to data/ folder")
        print("2. Use existing CSV with correct paths")
        print("3. Continue with available data (may not work well)")
        
        choice = input("\nContinue anyway? (y/n): ").lower()
        if choice != 'y':
            print("Training cancelled.")
            return
    
    # Create a simple dataset from available images
    # Assuming all images in data/ are from scanner s11 (based on filenames)
    print("\nCreating dataset from available images...")
    
    data = []
    for img_path in available_images:
        filename = os.path.basename(img_path)
        # Try to determine scanner from filename
        if 's1_' in filename or 's11_' in filename:
            scanner = 'Canon'  # Assume Canon for s1/s11
        elif 's2_' in filename or 's22_' in filename:
            scanner = 'HP'  # Assume HP for s2/s22
        else:
            scanner = 'Canon'  # Default to Canon
        
        data.append({
            'image_path': img_path,
            'scanner_model': scanner
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Count samples per class
    print("\nDataset composition:")
    print(df['scanner_model'].value_counts())
    
    # Check if we have at least 2 classes
    if len(df['scanner_model'].unique()) < 2:
        print("\n⚠ ERROR: Need at least 2 different scanner models for training!")
        print("   Currently all images are labeled as the same scanner.")
        print("\nPlease:")
        print("1. Add images from different scanners to data/ folder")
        print("2. Or use a proper CSV with multiple scanner classes")
        return
    
    # Train model
    print("\n" + "="*70)
    print("Starting Training...")
    print("="*70)
    
    trainer = ModelTrainer()
    
    try:
        # Extract features
        features, labels = trainer.extract_features_from_dataset(df, 'image_path', 'scanner_model')
        
        if len(features) < 5:
            print("\n⚠ ERROR: Not enough valid images extracted!")
            print(f"   Only {len(features)} images were successfully processed")
            return
        
        # Train model
        trainer.train_model(features, labels, test_size=0.2)
        
        # Save model
        trainer.save_model('models')
        
        print("\n" + "="*70)
        print("✓ Training Complete!")
        print("="*70)
        print(f"\nModel saved to: models/")
        print(f"Training accuracy: {trainer.training_history.get('train_accuracy', 'N/A')}")
        print(f"Test accuracy: {trainer.training_history.get('test_accuracy', 'N/A')}")
        
        print("\nRestart the server to use the new model:")
        print("  taskkill /F /IM python.exe & python app.py")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Training failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
