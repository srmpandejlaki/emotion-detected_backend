import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Pastikan stopwords bahasa Indonesia sudah diunduh
nltk.download("stopwords")
nltk.download("punkt")

stop_words = set(stopwords.words("indonesian"))

def preprocess_text(text: str) -> str:
    """
    Membersihkan teks dari karakter khusus, menghapus stopwords, dan mengubah ke huruf kecil.
    :param text: Kalimat asli
    :return: Kalimat yang sudah dibersihkan
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Hapus karakter khusus
    text = re.sub(r'\s+', ' ', text).strip()    # Hapus spasi berlebih

    words = word_tokenize(text)
    words = [word for word in words if word.isalnum()]  # Hapus tanda baca
    words = [word for word in words if word not in stop_words]

    return " ".join(words)
