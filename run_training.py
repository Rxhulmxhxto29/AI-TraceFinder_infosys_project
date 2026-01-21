import sys
sys.path.insert(0, 'C:\\TraceFinder')

from modules.model_trainer import train_from_csv

print("Starting training...")
trainer = train_from_csv(
    csv_path='C:\\TraceFinder\\dataset_corrected.csv',
    image_base_path='',
    output_dir='C:\\TraceFinder\\models'
)
print("Training complete!")
