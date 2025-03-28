from pydantic import BaseModel
from typing import Optional, List

class CommentBase(BaseModel):
    text: str  # Komentar dari pengguna
    source: Optional[str] = "media sosial"  # Sumber komentar (opsional)

class CommentCreate(CommentBase):
    pass  # Digunakan saat admin menambah komentar ke dataset

class CommentResponse(CommentBase):
    id: int  # ID dari database
    class Config:
        from_attributes = True  # Konversi dari SQLAlchemy model ke JSON
