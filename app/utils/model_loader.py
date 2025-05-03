import pickle

def load_latest_model():
    try:
        with open("saved_model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None
