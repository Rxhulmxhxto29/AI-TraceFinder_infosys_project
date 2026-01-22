import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from modules.model_trainer import train_from_csv

print("Starting training...")
trainer = train_from_csv(
    csv_path=os.path.join(current_dir, 'multi_scanner_dataset.csv'),
    image_base_path='',
    output_dir=os.path.join(current_dir, 'models')
)
print("Training complete!")
