import os
import joblib

MODEL_PATH = "app/models/naive_bayes_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

def save_model(model):
    joblib.dump(model, MODEL_PATH)
