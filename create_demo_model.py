"""
Create a working demonstration model for TraceFinder
This creates a simple but functional model for demo purposes
"""
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

def create_demo_model():
    print("Creating demonstration model...")
    
    # Create synthetic training data that represents Canon and HP scanners
    np.random.seed(42)
    
    # Number of features (must match the feature extraction)
    n_features = 23
    n_samples_per_class = 50
    
    # Canon features (pattern 1)
    canon_features = np.random.randn(n_samples_per_class, n_features)
    canon_features[:, 0] += 0.5  # Shift some features
    canon_features[:, 5] += 1.0
    canon_features[:, 10] -= 0.5
    
    # HP features (pattern 2)
    hp_features = np.random.randn(n_samples_per_class, n_features)
    hp_features[:, 0] -= 0.5  # Different shift
    hp_features[:, 5] -= 1.0
    hp_features[:, 10] += 0.5
    
    # Combine features
    X = np.vstack([canon_features, hp_features])
    y = np.array(['Canon'] * n_samples_per_class + ['HP'] * n_samples_per_class)
    
    # Create and train model
    print("Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X, y)
    
    # Create scaler
    scaler = StandardScaler()
    scaler.fit(X)
    
    # Create label encoder
    label_encoder = LabelEncoder()
    label_encoder.fit(y)
    
    # Save model components
    print("Saving model files...")
    
    with open('models/scanner_classifier.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('models/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    with open('models/feature_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Test the model
    print("\nTesting model...")
    test_canon = np.random.randn(1, n_features)
    test_canon[:, 0] += 0.5
    test_canon[:, 5] += 1.0
    
    test_hp = np.random.randn(1, n_features)
    test_hp[:, 0] -= 0.5
    test_hp[:, 5] -= 1.0
    
    test_canon_scaled = scaler.transform(test_canon)
    test_hp_scaled = scaler.transform(test_hp)
    
    canon_pred = model.predict(test_canon_scaled)[0]
    canon_prob = model.predict_proba(test_canon_scaled)[0]
    
    hp_pred = model.predict(test_hp_scaled)[0]
    hp_prob = model.predict_proba(test_hp_scaled)[0]
    
    print(f"\nTest 1 (Canon-like): Predicted={canon_pred}, Confidence={max(canon_prob)*100:.1f}%")
    print(f"Test 2 (HP-like): Predicted={hp_pred}, Confidence={max(hp_prob)*100:.1f}%")
    
    print("\n✓ Model created successfully!")
    print("\nClasses:", label_encoder.classes_)
    print("Feature vector size:", n_features)
    print("Model accuracy on training data:", model.score(X, y) * 100, "%")
    
    return model, scaler, label_encoder

if __name__ == "__main__":
    print("="*70)
    print("TraceFinder - Create Demo Model")
    print("="*70)
    print("\nThis creates a working demonstration model that can distinguish")
    print("between different scanner patterns based on image features.")
    print()
    
    create_demo_model()
    
    print("\n" + "="*70)
    print("Model files saved to models/ directory")
    print("Restart the server to use the new model")
    print("="*70)
