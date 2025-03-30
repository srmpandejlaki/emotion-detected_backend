import pandas as pd
from fastapi import UploadFile
from io import StringIO

def process_csv(file: UploadFile):
    contents = file.file.read().decode("utf-8")
    df = pd.read_csv(StringIO(contents))
    
    # Pastikan hanya kolom "text" yang dikirim ke frontend
    return df.to_dict(orient="records")
