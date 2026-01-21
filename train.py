"""
Quick Start Training Script for TraceFinder

Run this after you've prepared your CSV dataset:
    python train.py
"""

from modules.model_trainer import train_from_csv
import os

def main():
    print("="*60)
    print("TraceFinder - Model Training")
    print("="*60)
    
    # Configuration
    csv_file = input("\nEnter path to your CSV file (e.g., dataset.csv): ").strip()
    
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found!")
        return
    
    base_path = input("Enter base path for images (press Enter if paths are absolute): ").strip()
    
    print("\nStarting training...")
    print("This may take several minutes depending on dataset size.\n")
    
    # Train model
    trainer = train_from_csv(
        csv_path=csv_file,
        image_base_path=base_path,
        output_dir='models'
    )
    
    if trainer:
        print("\n" + "="*60)
        print("✓ Training Complete!")
        print("="*60)
        print("\nTrained model saved to: models/")
        print("\nRestart the server to use the trained model:")
        print("  python app.py")
        print("\nThe system will automatically detect and use your trained model.")
        print("="*60)
    else:
        print("\n✗ Training failed. Check error messages above.")

if __name__ == "__main__":
    main()
