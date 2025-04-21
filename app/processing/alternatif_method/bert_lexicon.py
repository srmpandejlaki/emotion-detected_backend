from collections import defaultdict
from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import json

class BERTEmotionClassifier:
    def __init__(self, model_name: str = "indobenchmark/indobert-base-p1", 
                 label_file_path: str = "app/utils/labels.json", 
                 lexicon_file_path: str = "app/utils/emotion_lexicon.json"):
        # Load BERT model and tokenizer
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.eval()  # Set model to evaluation mode

        # Load label list and lexicon
        self.label_list = self.load_label_list(label_file_path)
        self.emotion_lexicon = self.load_lexicon(lexicon_file_path)

    def load_label_list(self, file_path: str) -> list:
        """Load the label list from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data.get("labels", [])
        except Exception as e:
            print(f"Error loading label list: {e}")
            return []

    def load_lexicon(self, file_path: str) -> dict:
        """Load the emotion lexicon from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading lexicon: {e}")
            return {}

    def predict_with_bert(self, text: str) -> List[float]:
        """Get BERT model probabilities for a given text."""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = F.softmax(outputs.logits, dim=1).squeeze().tolist()
        return probs  # Match the order with self.label_list

    def lexicon_score(self, text: str) -> List[float]:
        """Calculate lexicon-based emotion scores."""
        scores = defaultdict(int)
        words = text.lower().split()
        for word in words:
            if word in self.emotion_lexicon:
                for emotion in self.emotion_lexicon[word]:
                    scores[emotion] += 1

        total = sum(scores.values()) or 1  # Prevent division by 0
        normalized = {k: v / total for k, v in scores.items()}
        return [normalized.get(label, 0) for label in self.label_list]

    def combined_score(self, text: str) -> str:
        """Combine BERT and lexicon scores and return the label with the highest score."""
        bert_probs = self.predict_with_bert(text)
        lexicon_probs = self.lexicon_score(text)

        # Combine BERT and lexicon scores by averaging
        combined = [(b + l) / 2 for b, l in zip(bert_probs, lexicon_probs)]
        best_idx = combined.index(max(combined))  # Get index of the highest combined score
        return self.label_list[best_idx]
