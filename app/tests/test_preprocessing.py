import pytest
from app.services.preprocessing_service import preprocess_text
from fastapi import HTTPException

# Contoh fungsi untuk preprocessing yang akan di-test
def test_preprocess_text_valid_input():
    # Input valid
    text = "I am very happy today!"
    processed_text = preprocess_text(text)
    
    # Asumsi fungsi preprocessing mengembalikan hasil dalam bentuk string
    assert isinstance(processed_text, str)
    assert processed_text != text  # Teks seharusnya sudah diproses, misalnya diubah menjadi lowercase

def test_preprocess_text_invalid_input():
    # Input invalid (misalnya kosong)
    text = ""
    
    # Mengecek apakah fungsi mengeluarkan exception jika input invalid
    with pytest.raises(HTTPException):
        preprocess_text(text)
