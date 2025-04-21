import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_and_save_model(csv_path="data/profiles.csv"):
    df = pd.read_csv(csv_path)
    
    # Feature Engineering
    df["follower_ratio"] = df["followers"] / (df["following"] + 1)
    df["username_digits"] = df["username"].apply(lambda x: sum(c.isdigit() for c in str(x)))
    
    # Train Model
    X = df[["followers", "following", "posts", "follower_ratio", "username_digits"]]
    y = df["is_fake"]
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    
    # Save Model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/metadata_model.pkl")
    print("Model trained & saved!")

if __name__ == "__main__":
    train_and_save_model()