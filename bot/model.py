import pickle
import os

MODEL_PATH = "models/degen_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        print("⚠️ No trained model found. Run training first.")
        return None
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def predict_trade(model, coin_features):
    if model is None:
        return False
    prediction = model.predict([coin_features])[0]
    return prediction == 1