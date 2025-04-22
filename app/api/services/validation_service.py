import os
import joblib
import pandas as pd
from typing import List
from sqlalchemy.orm import Session
from app.models import PreprocessedData
from app.utils import preprocess_text
from app.constants import EMOTION_LABELS

MODEL_PATH = "app/models_ml/naive_bayes_model.pkl"


def predict_single_text(text: str, db: Session) -> str:
    if not os.path.exists(MODEL_PATH):
        return "Model belum tersedia."

    model, vectorizer = joblib.load(MODEL_PATH)
    clean_text = preprocess_text(text)
    vec = vectorizer.transform([clean_text])
    pred = model.predict(vec)[0]

    # Simpan sebagai data latih baru
    new_data = PreprocessedData(cleaned_text=clean_text, label=pred)
    db.add(new_data)
    db.commit()

    return EMOTION_LABELS.get(pred, "tidak diketahui")


def predict_batch_texts(df: pd.DataFrame, db: Session) -> List[dict]:
    if not os.path.exists(MODEL_PATH):
        return []

    model, vectorizer = joblib.load(MODEL_PATH)
    texts = df["text"].tolist()
    clean_texts = [preprocess_text(t) for t in texts]
    vecs = vectorizer.transform(clean_texts)
    preds = model.predict(vecs)

    # Simpan semua ke database
    for text, label in zip(clean_texts, preds):
        db.add(PreprocessedData(cleaned_text=text, label=label))
    db.commit()

    return [
        {"text": orig, "predicted_emotion": EMOTION_LABELS.get(label, "tidak diketahui")}
        for orig, label in zip(texts, preds)
    ]

def naive_bayes_predict(model: dict, test_data: List[str], threshold=0.05):
    """
    Predict the label of the test data using the trained Naive Bayes model.

    Args:
        model (dict): Trained Naive Bayes model containing prior probabilities and likelihoods.
        test_data (List[str]): List of test data for prediction.
        threshold (float): The threshold to consider if two probabilities are almost equal.

    Returns:
        List[str]: Predicted labels for the test data.
    """
    predicted_labels = []
    
    for doc in test_data:
        # Tokenize the document
        words = doc.split()
        
        # Calculate the score for each class
        class_scores = {}
        for label in model['prior']:
            # Start with the prior probability of the class
            score = math.log(model['prior'][label])  # Log scale to prevent underflow
            
            # Add the likelihoods of the words in the document
            for word in words:
                word_likelihood = model['likelihood'][label].get(word, 1 / (sum(model['likelihood'][label].values()) + len(model['likelihood'])))  # Smoothing
                score += math.log(word_likelihood)
            
            class_scores[label] = score
        
        # Check if there's a tie (if two classes have almost the same score)
        sorted_scores = sorted(class_scores.items(), key=lambda item: item[1], reverse=True)
        if len(sorted_scores) > 1 and abs(sorted_scores[0][1] - sorted_scores[1][1]) < threshold:
            # If there's a tie, pass to another model (e.g., BERT + Lexikon)
            predicted_label = handle_tie_case(doc, sorted_scores)  # Example: function to handle tie using BERT or Lexikon
        else:
            predicted_label = sorted_scores[0][0]
        
        predicted_labels.append(predicted_label)

    return predicted_labels
