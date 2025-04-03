# app/services/data_service.py
from typing import List, Dict

def process_uploaded_csv(df) -> List[Dict[str, str]]:
    preview = []
    for index, row in df.iterrows():
        # Preview hanya text dan label kosong
        preview.append({
            "id": index + 1,
            "text": row['text'],  # Pastikan kolom 'text' ada di CSV
            "label": None
        })
    return preview

# app/services/data_service.py
from app.models import Dataset

def add_manual_data(data) -> Dict:
    # Menambahkan data manual ke database
    new_entry = Dataset(text=data.text, label=data.label)
    new_entry.save()  # Asumsikan kamu memiliki fungsi save()
    return {"id": new_entry.id, "text": new_entry.text, "label": new_entry.label}

# app/services/data_service.py
from app.models import Dataset

def save_dataset(dataset):
    for data in dataset:
        new_entry = Dataset(text=data.text, label=data.label)
        new_entry.save()

# app/services/data_service.py
from app.models import Dataset

def get_paginated_dataset(page: int, limit: int):
    offset = (page - 1) * limit
    data = Dataset.query.offset(offset).limit(limit).all()
    total_items = Dataset.query.count()
    total_pages = (total_items + limit - 1) // limit

    return {
        "page": page,
        "total_pages": total_pages,
        "data": [{"id": item.id, "text": item.text, "label": item.label} for item in data]
    }
