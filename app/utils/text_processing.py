import re

def preprocess_text(text: str) -> str:
    """
    Membersihkan teks dari karakter khusus dan mengubahnya menjadi huruf kecil.
    """
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Hapus karakter khusus
    text = re.sub(r'\s+', ' ', text).strip()  # Hapus spasi berlebih
    return text
