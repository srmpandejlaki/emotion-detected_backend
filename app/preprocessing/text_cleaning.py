import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Pastikan resource NLTK sudah tersedia
nltk.download('punkt')
nltk.download('stopwords')

# Inisialisasi stemmer dan stopwords
stemmer = StemmerFactory().create_stemmer()
stop_words = set(stopwords.words('indonesian'))

def preprocess_text(text: str) -> str:
    """
    Melakukan preprocessing teks:
    - Lowercase
    - Hapus angka dan tanda baca
    - Tokenisasi
    - Hapus stopwords
    - Stemming
    """
    try:
        # Lowercase
        text = text.lower()

        # Hapus angka dan tanda baca
        text = re.sub(r'\d+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Tokenisasi
        tokens = word_tokenize(text)

        # Hapus stopword
        tokens = [word for word in tokens if word not in stop_words and word.isalnum()]

        # Stemming
        stemmed_tokens = [stemmer.stem(word) for word in tokens]

        return ' '.join(stemmed_tokens)

    except Exception as e:
        raise ValueError(f"Gagal melakukan preprocessing: {e}")
