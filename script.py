# run_preprocessing.py

from app.preprocessing.text_cleaning import preprocess_batch_texts_from_csv

# Path ke file CSV yang ingin diproses
csv_path = "./app/dataCollection/kaget.csv"  # Ganti dengan path CSV yang sesuai

# Jalankan preprocessing untuk batch text dari file CSV
result = preprocess_batch_texts_from_csv(csv_path)

# Jika kamu ingin melihat hasilnya di terminal
print(result)
