# app/services/preprocessing_service.py
from app.models import Dataset

def get_preprocessing_dataset():
    dataset = Dataset.query.filter(Dataset.label.is_(None)).all()
    return [{"id": item.id, "text": item.text} for item in dataset]

# app/services/preprocessing_service.py
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Pastikan untuk mengunduh stopwords dan punkt
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_data():
    stop_words = set(stopwords.words('indonesian'))
    stemmer = PorterStemmer()
    
    dataset = Dataset.query.filter(Dataset.label.is_(None)).all()
    processed_data = []
    
    for item in dataset:
        tokens = word_tokenize(item.text.lower())  # Tokenisasi
        filtered_tokens = [word for word in tokens if word not in stop_words]  # Hapus stopwords
        stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]  # Stemming
        processed_text = " ".join(stemmed_tokens)
        
        processed_data.append({"id": item.id, "processed_text": processed_text, "label": item.label})
    
    return processed_data

# app/services/preprocessing_service.py
def get_processed_results():
    dataset = Dataset.query.filter(Dataset.label.is_(None)).all()
    return [{"id": item.id, "processed_text": item.text, "label": item.label} for item in dataset]

# app/services/preprocessing_service.py
def update_label(label_data):
    item = Dataset.query.get(label_data.id)
    if item:
        item.label = label_data.label
        item.save()  # Asumsikan ada fungsi save untuk menyimpan perubahan

# app/services/preprocessing_service.py
def save_preprocessed_data():
    # Dataset sudah memiliki label, jadi kita bisa simpan ke database
    dataset = Dataset.query.filter(Dataset.label.is_(None)).all()
    for item in dataset:
        item.save()  # Menyimpan data setelah preprocessing
