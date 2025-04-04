from fastapi import HTTPException

def validate_csv_columns(df, required_columns={"text"}):
    if not required_columns.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail=f"CSV harus memiliki kolom {required_columns}")
