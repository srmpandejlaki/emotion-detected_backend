import joblib
from src.preprocessing.extends.text_preprocessor import TextPreprocessor


class TweetClassifier:
    text_preprocessor = TextPreprocessor()
    valid_categories = {"joy", "trust",
                        "shock", "netral", "fear", "sadness", "anger"}  # Kategori yang valid

    def __init__(self, hybrid_model_path='./src/storage/models/hybrid_model.joblib'):
        """Inisialisasi model hybrid dan text preprocessor"""
        try:
            self.hybrid_model = joblib.load(hybrid_model_path)
        except Exception as e:
            print(f"❌ Gagal memuat Hybrid model: {e}")
            self.hybrid_model = None  # Hindari crash jika model tidak bisa dimuat

    def classify(self, sample_text):
        """ Mengklasifikasikan teks berita menggunakan model hybrid dan DeepSeek """
        processed_sample_text = self.text_preprocessor.preprocess(sample_text)
        print(f"Preprocessed Text: {processed_sample_text}")

        reasons = []

        # jika hasil preprocess ksosng
        if not processed_sample_text:
            return {
                "Preprocessed_Text": processed_sample_text,
                "Hybrid_C5_KNN": "Unknown",
                "Hybrid_Reason": "Unknown",
                "model_error": f"Failed to preprocess text: '{sample_text}'"
            }

        hybrid_error = ""
        try:
            hasil_model_hybrid, reasons = self.hybrid_model.predict(
                [processed_sample_text])
            hasil_model_hybrid = hasil_model_hybrid[0]
        except Exception as e:
            print(f"❌ Error pada model Hybrid: {e}")
            hasil_model_hybrid = "Unknown"
            hybrid_error = f"Hybrid Model Error: {e}"

        return {
            "Preprocessed_Text": processed_sample_text,
            "Hybrid_Result": hasil_model_hybrid,
            "Hybrid_Reason": reasons[0] if reasons else "Unknown",
            "model_error": f"{hybrid_error}"
        }
