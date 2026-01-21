import numpy as np
import pandas as pd
import cv2
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import json
from modules.feature_extractor import FeatureExtractor
from modules.image_processor import ImageProcessor

class ModelTrainer:
    """Train scanner identification model from CSV dataset"""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.image_processor = ImageProcessor()
        self.model = None
        self.label_encoder = None
        self.feature_names = []
        self.training_history = {}
        
    def load_csv_dataset(self, csv_path, image_column='image_path', label_column='scanner_model'):
        """
        Load dataset from CSV file
        
        CSV format expected:
        image_path,scanner_brand,scanner_model
        path/to/image1.jpg,Canon,LiDE 300
        path/to/image2.jpg,Epson,V600
        
        Args:
            csv_path: Path to CSV file
            image_column: Column name containing image paths
            label_column: Column name containing scanner labels
        """
        print(f"Loading dataset from {csv_path}...")
        
        try:
            df = pd.read_csv(csv_path)
            print(f"Found {len(df)} entries in dataset")
            
            # Auto-detect image path column
            if 'absolute_path' in df.columns and image_column == 'image_path' and image_column not in df.columns:
                image_column = 'absolute_path'
                print(f"Using 'absolute_path' column for image paths")
            elif 'file_path' in df.columns and image_column == 'image_path' and image_column not in df.columns:
                image_column = 'file_path'
                print(f"Using 'file_path' column for image paths")
            
            # Validate columns
            if image_column not in df.columns:
                raise ValueError(f"Column '{image_column}' not found in CSV. Available columns: {list(df.columns)}")
            if label_column not in df.columns:
                raise ValueError(f"Column '{label_column}' not found in CSV. Available columns: {list(df.columns)}")
            
            return df, image_column
            
        except Exception as e:
            print(f"Error loading CSV: {str(e)}")
            raise
    
    def extract_features_from_dataset(self, df, image_column='image_path', label_column='scanner_model', base_path=''):
        """
        Extract features from all images in dataset
        
        Args:
            df: DataFrame with image paths and labels
            image_column: Column name for image paths
            label_column: Column name for labels
            base_path: Base directory to prepend to image paths
        """
        features_list = []
        labels_list = []
        valid_indices = []
        
        print("Extracting features from images...")
        
        for idx, row in df.iterrows():
            try:
                # Build full image path
                img_path = row[image_column]
                if base_path:
                    img_path = os.path.join(base_path, img_path)
                
                # Check if file exists
                if not os.path.exists(img_path):
                    print(f"Warning: Image not found: {img_path}")
                    continue
                
                # Load and process image
                img = self.image_processor.load_and_preprocess(img_path)
                
                if img is None:
                    print(f"Warning: Failed to load image: {img_path}")
                    continue
                
                # Extract features
                features = self.feature_extractor.extract_all_features(img)
                
                # Flatten features into vector
                feature_vector = self._flatten_features(features)
                
                features_list.append(feature_vector)
                labels_list.append(row[label_column])
                valid_indices.append(idx)
                
                if (idx + 1) % 10 == 0:
                    print(f"Processed {idx + 1}/{len(df)} images...")
                    
            except Exception as e:
                print(f"Error processing image {row[image_column]}: {str(e)}")
                continue
        
        print(f"\nSuccessfully extracted features from {len(features_list)} images")
        
        return np.array(features_list), np.array(labels_list), valid_indices
    
    def _flatten_features(self, features):
        """Flatten feature dictionary into a single vector"""
        vector = []
        
        # PRNU features
        prnu = features.get('prnu_pattern', {})
        vector.extend([
            prnu.get('mean', 0),
            prnu.get('std', 0),
            prnu.get('energy', 0),
            prnu.get('entropy', 0)
        ])
        
        # Texture features
        texture = features.get('texture_features', {})
        vector.extend([
            texture.get('contrast', 0),
            texture.get('correlation', 0),
            texture.get('energy', 0),
            texture.get('homogeneity', 0)
        ])
        
        # Frequency features
        frequency = features.get('frequency_features', {})
        vector.extend([
            frequency.get('dominant_frequency', 0),
            frequency.get('frequency_spread', 0),
            frequency.get('high_freq_ratio', 0)
        ])
        
        # Wavelet features
        wavelet = features.get('wavelet_features', {})
        for component in ['cA', 'cH', 'cV', 'cD']:
            comp_data = wavelet.get(component, {})
            vector.extend([
                comp_data.get('mean', 0),
                comp_data.get('std', 0),
                comp_data.get('energy', 0)
            ])
        
        return np.array(vector)
    
    def train_model(self, X, y, test_size=0.2, random_state=42):
        """
        Train Random Forest classifier
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Labels array (n_samples,)
            test_size: Proportion of test set
            random_state: Random seed
        """
        print("\nTraining model...")
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
        )
        
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Number of classes: {len(self.label_encoder.classes_)}")
        print(f"Classes: {list(self.label_encoder.classes_)}")
        
        # Train Random Forest
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
            verbose=1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        train_accuracy = accuracy_score(y_train, y_pred_train)
        test_accuracy = accuracy_score(y_test, y_pred_test)
        
        print(f"\nTraining accuracy: {train_accuracy * 100:.2f}%")
        print(f"Test accuracy: {test_accuracy * 100:.2f}%")
        
        # Detailed report
        print("\nClassification Report (Test Set):")
        print(classification_report(y_test, y_pred_test, target_names=self.label_encoder.classes_))
        
        # Store training history
        self.training_history = {
            'train_accuracy': float(train_accuracy),
            'test_accuracy': float(test_accuracy),
            'n_samples': int(len(X)),
            'n_features': int(X.shape[1]),
            'n_classes': int(len(self.label_encoder.classes_)),
            'classes': list(self.label_encoder.classes_),
            'confusion_matrix': confusion_matrix(y_test, y_pred_test).tolist()
        }
        
        return train_accuracy, test_accuracy
    
    def save_model(self, model_dir='models'):
        """Save trained model, encoder, and metadata"""
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(model_dir, 'scanner_classifier.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {model_path}")
        
        # Save label encoder
        encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        print(f"Label encoder saved to {encoder_path}")
        
        # Save training history
        history_path = os.path.join(model_dir, 'training_history.json')
        with open(history_path, 'w') as f:
            json.dump(self.training_history, f, indent=4)
        print(f"Training history saved to {history_path}")
        
        print(f"\nModel training complete!")
        print(f"Test accuracy: {self.training_history['test_accuracy'] * 100:.2f}%")
    
    def load_model(self, model_dir='models'):
        """Load trained model from disk"""
        try:
            model_path = os.path.join(model_dir, 'scanner_classifier.pkl')
            encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
            
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            print(f"Model loaded successfully from {model_dir}")
            return True
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def predict(self, image_path):
        """Predict scanner for a single image"""
        if self.model is None or self.label_encoder is None:
            raise ValueError("Model not trained or loaded")
        
        # Load and process image
        img = self.image_processor.load_and_preprocess(image_path)
        if img is None:
            raise ValueError("Failed to load image")
        
        # Extract features
        features = self.feature_extractor.extract_all_features(img)
        feature_vector = self._flatten_features(features)
        
        # Predict
        X = feature_vector.reshape(1, -1)
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        # Get scanner name
        scanner = self.label_encoder.inverse_transform([prediction])[0]
        confidence = float(probabilities[prediction])
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_predictions = [
            {
                'scanner': self.label_encoder.inverse_transform([idx])[0],
                'confidence': float(probabilities[idx])
            }
            for idx in top_indices
        ]
        
        return {
            'scanner': scanner,
            'confidence': confidence,
            'top_predictions': top_predictions
        }


def train_from_csv(csv_path, image_base_path='', output_dir='models'):
    """
    Main training function - call this to train from CSV
    
    Args:
        csv_path: Path to CSV file with dataset
        image_base_path: Base directory for image paths in CSV
        output_dir: Directory to save trained model
    """
    trainer = ModelTrainer()
    
    # Load CSV
    df, image_column = trainer.load_csv_dataset(csv_path)
    
    # Extract features
    X, y, valid_indices = trainer.extract_features_from_dataset(
        df, 
        image_column=image_column,
        label_column='scanner_model',
        base_path=image_base_path
    )
    
    if len(X) == 0:
        print("Error: No valid samples extracted from dataset")
        return None
    
    # Train model
    train_acc, test_acc = trainer.train_model(X, y)
    
    # Save model
    trainer.save_model(output_dir)
    
    return trainer


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python model_trainer.py <csv_path> [image_base_path]")
        print("\nExample:")
        print("  python model_trainer.py dataset.csv")
        print("  python model_trainer.py dataset.csv C:/TraceFinder/dataset")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    image_base_path = sys.argv[2] if len(sys.argv) > 2 else ''
    
    train_from_csv(csv_path, image_base_path)
