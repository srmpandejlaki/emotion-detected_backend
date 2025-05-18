import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import time
from src.models.hybrid_model import EmotionHybridModel
from src.utilities.model_evaluations import evaluate_model
from itertools import product


class EmotionTrainer:
    """Trainer untuk model klasifikasi emosi dengan output lengkap"""

    def __init__(self, data_path, test_data_path=None):
        self.df = pd.read_csv(data_path, encoding='utf-8', sep=',')
        self.test_df = pd.read_csv(test_data_path) if test_data_path else None
        self.label_encoder = LabelEncoder()
        self.valid_emotions = list(np.unique(self.df['emotion']))

        self.label_encoder.fit(self.valid_emotions)

    def train(self, test_size=0.2, nb_threshold=0):
        """Train model dan return semua informasi yang diminta"""
        texts = self.df['preprocessed_result'].values

        y = self.df['emotion'].values
        y = self.label_encoder.fit_transform(y)\

        # Validasi label
        invalid_labels = set(self.df['emotion']) - set(self.valid_emotions)
        if invalid_labels:
            raise ValueError(
                f"Label tidak valid: {invalid_labels}. Hanya boleh: {self.valid_emotions}")
        # Validasi teks

        # Split data
        X_train, X_test, y_train, y_test, texts_train, texts_test = train_test_split(
            texts, y, texts, test_size=test_size, stratify=y, random_state=42)

        # Training
        start_time = time.time()
        model = EmotionHybridModel(nb_threshold=nb_threshold)
        model.fit(X_train, y_train, self.label_encoder)
        training_time = time.time() - start_time

        # Predictions
        y_pred, pred_sources = model.predict(X_test)
        y_pred_labels = y_pred

        y_test = self.label_encoder.inverse_transform(y_test)

        # 1. Prior Probabilities
        prior_probs = model.nb_model.get_prior_probabilities(X_test)

        # 2. Word Probabilities
        word_probs = model.nb_model.get_word_probabilities()

        # 3. TF-IDF Details
        tfidf_details = model.nb_model.get_tfidf_details(
            texts_test)

        # 4. BERT-Lexicon Details
        nb_preds_sample = model.nb_model.predict(X_test)
        bert_details = model.get_bert_lexicon_details(
            texts_test, nb_preds_sample)

        # 5. Evaluation Metrics
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(
            y_test, y_pred, target_names=self.label_encoder.classes_, output_dict=True)

        y_test_str = y_test
        y_pred_str = y_pred

        # Prediction Results
        predict_results = []
        for i in range(len(y_test_str)):
            result = {
                'text': texts_test[i],
                'true_label': y_test_str[i],
                'predicted_label': y_pred_str[i],
                'pred_source': pred_sources[i]
            }
            predict_results.append(result)

        # Return all results
        return {
            'model': model,
            'training_time': training_time,
            'prior_probabilities': prior_probs,
            'word_probabilities': word_probs,
            'tfidf_details': tfidf_details,
            'bert_lexicon_details': bert_details,
            'predict_results': predict_results,
            'evaluation': {
                'accuracy': accuracy,
                'confusion_matrix': cm.tolist(),
                'classification_report': report,
            }
        }

    def save_model(self, model, path):
        """Save model dan komponen pendukung"""
        joblib.dump(model, path)

    @staticmethod
    def load_model(path):
        """Load model yang telah disimpan"""
        return joblib.load(path)

    def grid_search(self, param_grid=None):
        """Perform grid search for hyperparameter tuning"""
        if param_grid is None:
            param_grid = {
                'test_size': [0.2, 0.25, 0.3, 0.35],
                'nb_threshold': [0, 0.5, 0.7, 0.9],
            }

        # Prepare data
        texts = self.df['preprocessed_result'].values
        y = self.df['emotion'].values
        y = self.label_encoder.fit_transform(y)

        best_score = 0
        best_params = None
        best_model = None
        results = []

        # Generate all parameter combinations
        for test_size, nb_threshold in product(param_grid['test_size'], param_grid['nb_threshold']):
            print(
                f"\nEvaluating: test_size={test_size}, nb_threshold={nb_threshold}")

            # Split data
            X_train, X_test, y_train, y_test, texts_train, texts_test = train_test_split(
                texts, y, texts, test_size=test_size, stratify=y, random_state=42
            )

            # Train model
            start_time = time.time()
            model = EmotionHybridModel(nb_threshold=nb_threshold)
            model.fit(X_train, y_train, label_encoder=self.label_encoder)
            train_time = time.time() - start_time

            # Evaluate
            y_test = self.label_encoder.inverse_transform(y_test)
            y_pred, _ = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)

            results.append({
                'params': {'test_size': test_size, 'nb_threshold': nb_threshold},
                'accuracy': accuracy,
                'training_time': train_time
            })

            print(
                f"Accuracy: {accuracy:.4f}, Training Time: {train_time:.2f}s")

            if accuracy > best_score:
                best_score = accuracy
                best_params = {'test_size': test_size,
                               'nb_threshold': nb_threshold}
                best_model = model

        # Sort results by accuracy
        results = sorted(results, key=lambda x: x['accuracy'], reverse=True)

        print("\nGrid Search Results:")
        print("Test Size\tNB Threshold\tAccuracy\tTraining Time")
        for result in results:
            print(f"{result['params']['test_size']}\t\t{result['params']['nb_threshold']}\t\t"
                  f"{result['accuracy']:.4f}\t\t{result['training_time']:.2f}s")

        return best_model, best_params, best_score


if __name__ == "__main__":
    # Initialize trainer
    trainer = EmotionTrainer(
        "src/storage/datasets/preprocessed/new_dataset_preprocessed_test.csv",)

    # Option 1: Simple training
    # results = trainer.train(test_size=0.25, nb_threshold=0)

    # print(f"\nTraining time: {results['training_time']:.2f}s")
    # print(f"\nPrior Probabilities:\n{results['prior_probabilities']}")
    # print(f"\nWord Probabilities:\n{results['word_probabilities']}")
    # print(f"\nTF-IDF Details:\n{results['tfidf_details']}")
    # print(f"\nBERT-Lexicon Details:\n{results['bert_lexicon_details']}")
    # print(f"\nPrediction Results:\n{results['predict_results']}")
    # print(f"\nConfusion Matrix:\n{results['evaluation']['confusion_matrix']}")
    # print(f"\nTest set evaluation:\n{results['test_evaluation']}")
    # print(f"\nAccuracy: {results['evaluation']['accuracy']}")
    # print(results['evaluation']['classification_report'])

    # Option 2: Grid search
    best_model, best_params, best_score = trainer.grid_search()
    print(f"\nBest params: {best_params}")
    print(f"Best accuracy: {best_score:.4f}")

    # # Save model
    trainer.save_model(best_model, "./src/storage/models/hybrid_model.joblib")
