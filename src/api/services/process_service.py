# src/api/services/process_service.py
import os
import json
import joblib
import uuid
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from src.database.config import SessionLocal
from src.database.models import Model, PreprocessedDataset
from src.processing.trainer import EmotionTrainer
from sklearn.model_selection import train_test_split


class ProcessService:
    """Service for processing and training models"""
    db = SessionLocal()
    STORAGE_PATH = "src/storage/models/"

    def __init__(self):
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary storage directories"""
        directories = [
            "trained/",
            "probabilities/",
            "tfidf_details/",
            "bert_details/",
            "evaluation_metrics/",
            "predict_results/"
        ]
        for dir_name in directories:
            os.makedirs(os.path.join(
                self.STORAGE_PATH, dir_name), exist_ok=True)

    def split_dataset(self, test_size=0.2):
        """Split dataset into training and testing sets"""
        # Fetch all preprocessed data
        preprocessed_data = self.db.query(PreprocessedDataset).all()

        if not preprocessed_data:
            return {"error": "No preprocessed data available"}, 400

        x = [d.preprocessed_text for d in preprocessed_data]
        y = [d.emotion for d in preprocessed_data]

        # Split the dataset
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, stratify=y, random_state=42
        )

        return {
            "train_size": len(x_train),
            "test_size": len(x_test),
            "train_per_label": {
                emotion: y_train.count(emotion) for emotion in set(y)
            },
            "test_per_label": {
                emotion: y_test.count(emotion) for emotion in set(y)
            }

        }

    def _save_to_file(self, data, subdir, filename, format='csv'):
        """Helper method to save data to files"""
        path = os.path.join(self.STORAGE_PATH, subdir, filename)

        if format == 'csv':
            if isinstance(data, pd.DataFrame):
                data.to_csv(path, index=False)
            else:
                df = pd.DataFrame(data)
                df.to_csv(path, index=False)
        elif format == 'joblib':
            joblib.dump(data, path)
        elif format == 'json':
            with open(path, 'w') as f:
                json.dump(data, f)
        return path

    def train_model(self, test_size=0.2, nb_threshold=0):
        """Train a new model with file-based storage"""

        unpreprocessed_data = self.db.query(PreprocessedDataset).filter_by(
            is_preprocessed=False
        ).all()
        if unpreprocessed_data:
            return {"error": "Please preprocess data before training"}, 400
        # Get preprocessed data from database
        preprocessed_data = self.db.query(PreprocessedDataset).filter_by(
            is_preprocessed=True,
        ).all()

        if not preprocessed_data:
            return {"error": "No preprocessed data available for training"}, 400

        # Convert to DataFrame
        df = pd.DataFrame([{
            'preprocessed_result': d.preprocessed_text,
            'emotion': d.emotion
        } for d in preprocessed_data])

        # Save to temp CSV for EmotionTrainer
        temp_path = os.path.join(self.STORAGE_PATH, "temp_training_data.csv")
        df.to_csv(temp_path, index=False)

        # Train model
        trainer = EmotionTrainer(temp_path)
        results = trainer.train(test_size=test_size, nb_threshold=nb_threshold)

        # Generate unique ID for this model
        model_id = str(uuid.uuid4())

        # Save all components to files
        model_path = self._save_to_file(
            results['model'],
            "trained",
            f"{model_id}.joblib",
            format='joblib'
        )

        # Save all data components
        paths = {
            'prior_probabilities': self._save_to_file(
                results['prior_probabilities'],
                "probabilities",
                f"{model_id}_prior_probs.json",
                format='json'
            ),
            'word_probabilities': self._save_to_file(results['word_probabilities'],
                                                     "probabilities",
                                                     f"{model_id}_word_probs.csv"
                                                     ),
            'tfidf_details': self._save_to_file(
                results['tfidf_details'],
                "tfidf_details",
                f"{model_id}_tfidf.csv"
            ),
            'bert_lexicon_details': self._save_to_file(
                results['bert_lexicon_details'],
                "bert_details",
                f"{model_id}_bert.csv",
            ),
            'evaluation_metrics': self._save_to_file(
                {
                    'accuracy': results['evaluation']['accuracy'],
                    'confusion_matrix': results['evaluation']['confusion_matrix'],
                    'classification_report': results['evaluation']['classification_report']
                },
                "evaluation_metrics",
                f"{model_id}_metrics.json",
                format='json'
            ),
            'predict_results': self._save_to_file(
                results['predict_results'],
                "predict_results",
                f"{model_id}_predictions.csv"
            )
        }

        # Create database record
        model = Model(
            name=f"EmotionModel-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            model_path=model_path,
            total_data=len(df),
            test_size=test_size,
            accuracy=results['evaluation']['accuracy'],
            train_time=results['training_time'],
            prior_probabilities_path=paths['prior_probabilities'],
            word_probabilities_path=paths['word_probabilities'],
            tfidf_details_path=paths['tfidf_details'],
            bert_lexicon_details_path=paths['bert_lexicon_details'],
            evaluation_metrics_path=paths['evaluation_metrics'],
            predict_results_path=paths['predict_results']
        )

        self.db.add(model)
        self.db.commit()

        # Mark data as trained
        for data in preprocessed_data:
            data.is_trained = True
            data.updated_at = datetime.utcnow()
        self.db.commit()

        # Clean up temp file
        os.remove(temp_path)

        # Return model details json serialize
        model = self.db.query(Model).filter_by(
            created_at=model.created_at).first()
        if not model:
            return None

        return {
            "message": "Model trained successfully",
            "model_id": model.id,
            "accuracy": model.accuracy,
            "training_time": model.train_time
        }

    def get_model(self):
        """Retrieve model details with lazy loading of file data"""
        model = self.db.query(Model).order_by(Model.created_at.desc()).first()
        if not model:
            return None

        return {
            "id": model.id,
            "name": model.name,
            "accuracy": model.accuracy,
            "train_time": model.train_time,
            "created_at": model.created_at,
            "test_size": model.test_size,
            "total_data": model.total_data,
        }

    def get_models_list(self):
        """Get lightweight list of models without loading file data"""
        models = self.db.query(Model).all()
        return [{
            "id": m.id,
            "name": m.name,
            "accuracy": m.accuracy,
            "train_time": m.train_time,
            "created_at": m.created_at,
            "test_size": m.test_size,
            "total_data": m.total_data
        } for m in models]

    def delete_model(self, model_id):
        """Delete model and all associated files"""
        model = self.db.query(Model).filter_by(id=model_id).first()
        if not model:
            return False

        # Delete all associated files
        file_paths = [
            model.model_path,
            model.prior_probabilities_path,
            model.word_probabilities_path,
            model.tfidf_details_path,
            model.bert_lexicon_details_path,
            model.evaluation_metrics_path,
            model.predict_results_path
        ]

        for path in file_paths:
            if path and os.path.exists(path):
                os.remove(path)

        # Delete database record
        self.db.delete(model)
        self.db.commit()
        return True

    # Add these methods to the ProcessService class

    def get_prior_probabilities(self):
        """Get prior probabilities for a model"""
        model = self.db.query(Model).order_by(Model.created_at.desc()).first()
        if not model or not model.prior_probabilities_path:
            return None

        try:
            with open(model.prior_probabilities_path, 'r') as f:
                return json.load(f)
        except:
            return None

    def get_word_probabilities(self):
        """Get word probabilities for a model"""
        model = self.db.query(Model).order_by(Model.created_at.desc()).first()
        if not model or not model.word_probabilities_path:
            return None

        try:
            return pd.read_csv(model.word_probabilities_path).to_dict('records')
        except:
            return None

    def get_tfidf_details(self):
        """Get TF-IDF details for a model"""
        # ambil model paling terakhir
        model = self.db.query(Model).order_by(Model.created_at.desc()).first()
        if not model or not model.tfidf_details_path:
            return None

        try:
            return pd.read_csv(model.tfidf_details_path).to_dict('records')
        except:
            return None

    def get_bert_lexicon_details(self):
        """Get BERT lexicon details for a model and remove 'kata_terkait' column"""
        model = self.db.query(Model).order_by(Model.created_at.desc()).first()
        if not model or not model.bert_lexicon_details_path:
            return None

        try:
            df = pd.read_csv(model.bert_lexicon_details_path)
            # Hapus kolom 'kata_terkait' jika ada
            if 'kata_terkait' in df.columns:
                df = df.drop(columns=['kata_terkait'])
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading BERT lexicon details: {e}")
            return None

    def get_evaluation_metrics(self):
        """Get evaluation metrics for a model"""
        model = self.db.query(Model).order_by(Model.created_at.desc()).first()
        if not model or not model.evaluation_metrics_path:
            return None

        try:
            with open(model.evaluation_metrics_path, 'r') as f:
                return json.load(f)
        except:
            return None

    def get_predict_results(self, page=1, limit=10):
        """Get prediction results with pagination and filtering"""
        model = self.db.query(Model).order_by(Model.created_at.desc()).first()
        if not model or not model.predict_results_path:
            return None

        try:
            df = pd.read_csv(model.predict_results_path)

            # Apply pagination
            total_data = len(df)
            start = (page - 1) * limit
            end = start + limit
            paginated_data = df.iloc[start:end].to_dict('records')

            return {
                "data": paginated_data,
                "total_data": total_data,
                "total_pages": (total_data + limit - 1) // limit,
                "current_page": page,
                "limit": limit,
            }
        except Exception as e:
            print(f"Error loading predict results: {e}")
            return None
