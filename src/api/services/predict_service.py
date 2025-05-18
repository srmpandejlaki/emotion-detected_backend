from src.features.classifier import TweetClassifier


class PredictService:

    def predict(self, text, model_path='./src/storage/models/trained/27fe3a44-e850-477e-b9d8-1947af990a72.joblib'):
        """ Mengklasifikasikan teks berita menggunakan model hybrid dan DeepSeek """
        classifier = TweetClassifier(model_path)
        result = classifier.classify(text)
        return result
