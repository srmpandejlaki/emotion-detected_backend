import re
import string
import json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords

# Inisialisasi stemming
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

# Load stopwords bahasa Indonesia
stop_words = set(stopwords.words('indonesian'))

# Load kamus lemmatization dari file JSON
def load_lemma_dictionary(filepath: str) -> dict:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

kamus_lemma = load_lemma_dictionary("kamus_lemma.json")

def clean_text(text: str) -> str:
    """Menghapus angka, tanda baca, dan mengubah ke huruf kecil."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    return text.strip()

def remove_stopwords(text: str) -> str:
    """Menghapus stopwords dari teks."""
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

def stemming_and_lemmatization(text: str) -> str:
    """Melakukan stemming dengan Sastrawi dan lemmatization dengan kamus JSON."""
    stemmed_text = stemmer.stem(text)
    words = stemmed_text.split()
    lemmatized_words = [kamus_lemma.get(word, word) for word in words]
    return ' '.join(lemmatized_words)

def preprocess_text(text: str) -> str:
    """Pipeline preprocessing: Cleaning → Stopwords Removal → Stemming & Lemmatization"""
    cleaned_text = clean_text(text)
    text_no_stopwords = remove_stopwords(cleaned_text)
    return stemming_and_lemmatization(text_no_stopwords)
