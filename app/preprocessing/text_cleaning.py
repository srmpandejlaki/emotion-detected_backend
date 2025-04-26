import re
import json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# --- Setup Stemmer dan Stopwords ---
stemmer = StemmerFactory().create_stemmer()
stopword_factory = StopWordRemoverFactory()
default_stopwords = stopword_factory.get_stop_words()

# Kata penting yang dipertahankan
emotion_words = {"tidak", "gak", "ga", "bukan", "kurang", "belum"}

# Custom stopwords: hapus kata penting dari stopwords
custom_stopwords = set(default_stopwords) - emotion_words

# --- Load Slang Dictionary from JSON File ---
def load_slang_dict(filepath="app/utils/slang.json"):
    with open(filepath, 'r', encoding='utf-8') as f:
        slang_dict = json.load(f)
    return slang_dict

slang_replacements = load_slang_dict()

# --- Text Processing Functions ---
def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)             # Remove mentions
    text = re.sub(r"#\w+", "", text)             # Remove hashtags
    text = re.sub(r"[^\w\s]", " ", text)          # Remove punctuation
    text = re.sub(r"\d+", "", text)               # Remove numbers
    text = re.sub(r"\s+", " ", text).strip()       # Remove extra whitespace
    return text

def replace_slang(text):
    words = text.split()
    return ' '.join(slang_replacements.get(word, word) for word in words)

def remove_stopwords(text):
    words = text.split()
    return ' '.join(word for word in words if word not in custom_stopwords)

def preprocess_text(text):
    text = clean_text(text)
    text = replace_slang(text)
    text = stemmer.stem(text)
    text = remove_stopwords(text)
    return text
