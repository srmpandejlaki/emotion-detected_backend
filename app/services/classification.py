import pickle
from .preprocess import preprocess_text

# Load model Naïve Bayes (pastikan model sudah dilatih)
with open("model_nb.pkl", "rb") as file:
    model = pickle.load(file)

# Load vectorizer TF-IDF
with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

def classify_text(text: str) -> dict:
    """Mengklasifikasikan teks ke dalam kategori emosi."""
    processed_text = preprocess_text(text)
    text_vector = vectorizer.transform([processed_text])
    prediction = model.predict(text_vector)[0]

    return {"original_text": text, "processed_text": processed_text, "predicted_emotion": prediction}
