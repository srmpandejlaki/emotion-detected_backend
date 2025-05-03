# app/api/routes/__init__.py
from app.api.routes import processing_router

all_routers = [
    processing_router.router,
    # tambahkan yang lain nanti di sini
]

