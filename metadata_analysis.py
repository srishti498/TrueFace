import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

class MetadataModel:
    def __init__(self, model_path="models/metadata_model.pkl"):
        self.model = joblib.load(model_path)
    
    def predict(self, metadata):
        # Feature Engineering
        metadata["follower_ratio"] = metadata["followers"] / (metadata["following"] + 1)
        metadata["username_digits"] = sum(c.isdigit() for c in str(metadata["username"]))
        
        # Predict
        proba = self.model.predict_proba([[
            metadata["followers"],
            metadata["following"],
            metadata["posts"],
            metadata["follower_ratio"],
            metadata["username_digits"],
        ]])[0][1]  # Fake probability
        
        return {"fake_probability": proba}

# Load model globally
model = MetadataModel()

def analyze_metadata(metadata):
    return model.predict(metadata)