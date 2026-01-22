import numpy as np
import pandas as pd
import cv2
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
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
        self.scaler = StandardScaler()
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
    
    def _balance_dataset(self, X, y):
        """Balance dataset by oversampling minority class with slight variations"""
        unique, counts = np.unique(y, return_counts=True)
        max_count = np.max(counts)
        
        X_balanced = []
        y_balanced = []
        
        for class_label in unique:
            # Get samples for this class
            class_indices = np.where(y == class_label)[0]
            class_samples = X[class_indices]
            
            # Add original samples
            X_balanced.append(class_samples)
            y_balanced.extend([class_label] * len(class_samples))
            
            # If minority class, oversample
            if len(class_samples) < max_count:
                n_to_add = max_count - len(class_samples)
                # Randomly sample with replacement and add small noise
                indices = np.random.choice(len(class_samples), size=n_to_add, replace=True)
                synthetic_samples = class_samples[indices].copy().astype(np.float64)
                # Add small random noise (0.1% of std)
                noise = np.random.normal(0, 0.001, synthetic_samples.shape)
                synthetic_samples = synthetic_samples + noise
                
                X_balanced.append(synthetic_samples)
                y_balanced.extend([class_label] * n_to_add)
        
        return np.vstack(X_balanced), np.array(y_balanced)
    
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
        
        # Check class distribution
        unique, counts = np.unique(y, return_counts=True)
        print("\nClass distribution:")
        for cls, cnt in zip(unique, counts):
            print(f"  {cls}: {cnt} samples")
        
        # Split dataset - use 85% training for small datasets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.15, random_state=random_state, stratify=y_encoded
        )
        
        # Balance training set using SMOTE-like duplication for minority class
        X_train_balanced, y_train_balanced = self._balance_dataset(X_train, y_train)
        
        # Scale features for better SVM performance
        X_train_scaled = self.scaler.fit_transform(X_train_balanced)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"\nOriginal training set: {len(X_train)} samples")
        print(f"Balanced training set: {len(X_train_balanced)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Number of classes: {len(self.label_encoder.classes_)}")
        print(f"Classes: {list(self.label_encoder.classes_)}")
        
        # Try SVM with RBF kernel - better for small datasets
        self.model = SVC(
            kernel='rbf',
            C=10.0,
            gamma='scale',
            class_weight='balanced',
            random_state=random_state,
            probability=True,  # Enable probability estimates
            verbose=True
        )
        
        self.model.fit(X_train_scaled, y_train_balanced)
        
        # Evaluate
        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_test = self.model.predict(X_test_scaled)
        
        train_accuracy = accuracy_score(y_train_balanced, y_pred_train)
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
        """Save trained model, encoder, scaler, and metadata"""
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(model_dir, 'scanner_classifier.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {model_path}")
        
        # Save scaler
        scaler_path = os.path.join(model_dir, 'feature_scaler.pkl')
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Feature scaler saved to {scaler_path}")
        
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
